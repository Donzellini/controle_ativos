"""Routes for handling assets (ativos)"""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import Ativo, TipoAtivo, StatusAtivo
from schemas import AtivoCreate, AtivoResponse, AtivoUpdate, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ativos", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_ativo(
    ativo_data: AtivoCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new asset
    
    Validations:
    - numero_serie must be unique
    - data_aquisicao cannot be in the future
    - valor_estimado must be positive
    - tipo_id must exist
    """
    logger.info(f"Creating new ativo: {ativo_data.numero_serie}")
    
    # Check if tipo exists
    tipo = db.query(TipoAtivo).filter(TipoAtivo.id == ativo_data.tipo_id).first()
    if not tipo:
        logger.warning(f"TipoAtivo {ativo_data.tipo_id} not found")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Tipo de ativo não encontrado",
                "field": "tipo_id"
            }
        )
    
    # Check if numero_serie already exists
    existing_ativo = db.query(Ativo).filter(
        Ativo.numero_serie == ativo_data.numero_serie
    ).first()
    
    if existing_ativo:
        logger.warning(f"Duplicate numero_serie: {ativo_data.numero_serie}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Número de série já cadastrado",
                "field": "numero_serie"
            }
        )
    
    # Validate data_aquisicao is not in the future
    if ativo_data.data_aquisicao > datetime.utcnow():
        logger.warning(f"data_aquisicao in the future: {ativo_data.data_aquisicao}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Data não pode ser no futuro",
                "field": "data_aquisicao"
            }
        )
    
    # Validate valor_estimado is positive
    if ativo_data.valor_estimado < 0:
        logger.warning(f"negative valor_estimado: {ativo_data.valor_estimado}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Valor deve ser positivo",
                "field": "valor_estimado"
            }
        )
    
    try:
        # Create new ativo
        novo_ativo = Ativo(
            descricao=ativo_data.descricao,
            tipo_id=ativo_data.tipo_id,
            numero_serie=ativo_data.numero_serie,
            mac_address=ativo_data.mac_address,
            valor_estimado=ativo_data.valor_estimado,
            data_aquisicao=ativo_data.data_aquisicao,
            status=StatusAtivo.DISPONIVEL,
            localizacao=ativo_data.localizacao
        )
        
        db.add(novo_ativo)
        db.commit()
        db.refresh(novo_ativo)
        
        logger.info(f"Ativo created successfully: id={novo_ativo.id}, serie={novo_ativo.numero_serie}")
        
        return {
            "success": True,
            "id": novo_ativo.id,
            "message": "Ativo cadastrado com sucesso"
        }
    
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error while creating ativo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Erro ao cadastrar ativo - dados duplicados ou inválidos",
                "field": None
            }
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating ativo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Erro ao cadastrar ativo",
                "field": None
            }
        )


@router.get("/ativos", response_model=list[AtivoResponse])
async def list_ativos(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    List all assets with pagination
    
    Parameters:
    - skip: number of records to skip (default: 0)
    - limit: number of records to return (default: 20)
    """
    logger.info(f"Listing ativos: skip={skip}, limit={limit}")
    
    ativos = db.query(Ativo).offset(skip).limit(limit).all()
    return ativos


@router.get("/ativos/{ativo_id}", response_model=AtivoResponse)
async def get_ativo(
    ativo_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific asset by ID"""
    logger.info(f"Getting ativo: id={ativo_id}")
    
    ativo = db.query(Ativo).filter(Ativo.id == ativo_id).first()
    if not ativo:
        logger.warning(f"Ativo not found: id={ativo_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ativo não encontrado"
        )
    
    return ativo


@router.put("/ativos/{ativo_id}", response_model=dict)
async def update_ativo(
    ativo_id: int,
    ativo_data: AtivoUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing asset"""
    logger.info(f"Updating ativo: id={ativo_id}")
    
    ativo = db.query(Ativo).filter(Ativo.id == ativo_id).first()
    if not ativo:
        logger.warning(f"Ativo not found: id={ativo_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ativo não encontrado"
        )
    
    try:
        # Update fields if provided
        if ativo_data.descricao is not None:
            ativo.descricao = ativo_data.descricao
        if ativo_data.localizacao is not None:
            ativo.localizacao = ativo_data.localizacao
        if ativo_data.status is not None:
            ativo.status = ativo_data.status
        
        db.commit()
        db.refresh(ativo)
        
        logger.info(f"Ativo updated successfully: id={ativo.id}")
        
        return {
            "success": True,
            "id": ativo.id,
            "message": "Ativo atualizado com sucesso"
        }
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating ativo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar ativo"
        )
