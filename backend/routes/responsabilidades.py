"""Routes for Chromebook responsibility management"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List

from database import get_db
from models import Professor, ResponsabilidadeChromebook, StatusResponsabilidade
from schemas import (
    ProfessorCreate,
    ProfessorResponse,
    ResponsabilidadeCreate,
    ResponsabilidadeResponse,
    ResponsabilidadeUpdate,
    ErrorResponse,
)

router = APIRouter(
    tags=["responsabilidades"],
)


# ============== Professor Endpoints ==============


@router.post("/professores", response_model=ProfessorResponse, status_code=201)
def criar_professor(
    professor: ProfessorCreate,
    db: Session = Depends(get_db),
):
    """Criar novo professor"""
    # Validar nome único
    professor_existente = db.query(Professor).filter(
        Professor.nome == professor.nome
    ).first()

    if professor_existente:
        raise HTTPException(
            status_code=400,
            detail="Professor com este nome já existe",
        )

    novo_professor = Professor(
        nome=professor.nome,
        email=professor.email,
    )
    db.add(novo_professor)
    db.commit()
    db.refresh(novo_professor)

    return novo_professor


@router.get("/professores", response_model=List[ProfessorResponse])
def listar_professores(
    db: Session = Depends(get_db),
):
    """Listar todos os professores"""
    professores = db.query(Professor).order_by(Professor.nome).all()
    return professores


@router.get("/professores/{professor_id}", response_model=ProfessorResponse)
def obter_professor(
    professor_id: int,
    db: Session = Depends(get_db),
):
    """Obter detalhes de um professor específico"""
    professor = db.query(Professor).filter(Professor.id == professor_id).first()

    if not professor:
        raise HTTPException(
            status_code=404,
            detail="Professor não encontrado",
        )

    return professor


# ============== Responsabilidade Endpoints ==============


@router.post("/responsabilidades", response_model=ResponsabilidadeResponse, status_code=201)
def criar_responsabilidade(
    responsabilidade: ResponsabilidadeCreate,
    db: Session = Depends(get_db),
):
    """Criar novo registro de responsabilidade"""
    # Validar se professor existe
    professor = db.query(Professor).filter(
        Professor.id == responsabilidade.professor_id
    ).first()

    if not professor:
        raise HTTPException(
            status_code=404,
            detail="Professor não encontrado",
        )

    # Validar se já existe responsabilidade para mesmo professor/data/período
    responsabilidade_existente = db.query(ResponsabilidadeChromebook).filter(
        and_(
            ResponsabilidadeChromebook.professor_id == responsabilidade.professor_id,
            ResponsabilidadeChromebook.data == responsabilidade.data,
            ResponsabilidadeChromebook.periodo_turma == responsabilidade.periodo_turma,
        )
    ).first()

    if responsabilidade_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe um registro de responsabilidade para este professor nesta data/período",
        )

    nova_responsabilidade = ResponsabilidadeChromebook(
        professor_id=responsabilidade.professor_id,
        data=responsabilidade.data,
        periodo_turma=responsabilidade.periodo_turma,
        quantidade_chromebooks=responsabilidade.quantidade_chromebooks,
        observacoes=responsabilidade.observacoes,
        status=StatusResponsabilidade.PENDENTE,
    )

    db.add(nova_responsabilidade)
    db.commit()
    db.refresh(nova_responsabilidade)

    return nova_responsabilidade


@router.get("/responsabilidades", response_model=List[ResponsabilidadeResponse])
def listar_responsabilidades(
    professor_id: int = Query(None),
    data_inicio: str = Query(None),
    data_fim: str = Query(None),
    periodo_turma: str = Query(None),
    db: Session = Depends(get_db),
):
    """
    Listar responsabilidades com filtros opcionais.
    
    Query params:
    - professor_id: Filtrar por ID do professor
    - data_inicio: Data inicial (YYYY-MM-DD)
    - data_fim: Data final (YYYY-MM-DD)
    - periodo_turma: Período/turma específico (ex: 1ºA)
    """
    query = db.query(ResponsabilidadeChromebook)

    if professor_id:
        query = query.filter(ResponsabilidadeChromebook.professor_id == professor_id)

    if data_inicio:
        try:
            data_inicio_obj = datetime.fromisoformat(data_inicio)
            query = query.filter(ResponsabilidadeChromebook.data >= data_inicio_obj)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="data_inicio deve estar no formato YYYY-MM-DD",
            )

    if data_fim:
        try:
            data_fim_obj = datetime.fromisoformat(data_fim)
            query = query.filter(ResponsabilidadeChromebook.data <= data_fim_obj)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="data_fim deve estar no formato YYYY-MM-DD",
            )

    if periodo_turma:
        query = query.filter(ResponsabilidadeChromebook.periodo_turma == periodo_turma)

    responsabilidades = query.order_by(ResponsabilidadeChromebook.data).all()
    return responsabilidades


@router.get("/responsabilidades/{responsabilidade_id}", response_model=ResponsabilidadeResponse)
def obter_responsabilidade(
    responsabilidade_id: int,
    db: Session = Depends(get_db),
):
    """Obter detalhes de uma responsabilidade específica"""
    responsabilidade = db.query(ResponsabilidadeChromebook).filter(
        ResponsabilidadeChromebook.id == responsabilidade_id
    ).first()

    if not responsabilidade:
        raise HTTPException(
            status_code=404,
            detail="Responsabilidade não encontrada",
        )

    return responsabilidade


@router.put("/responsabilidades/{responsabilidade_id}", response_model=ResponsabilidadeResponse)
def atualizar_responsabilidade(
    responsabilidade_id: int,
    responsabilidade_update: ResponsabilidadeUpdate,
    db: Session = Depends(get_db),
):
    """Atualizar status ou observações de uma responsabilidade"""
    responsabilidade = db.query(ResponsabilidadeChromebook).filter(
        ResponsabilidadeChromebook.id == responsabilidade_id
    ).first()

    if not responsabilidade:
        raise HTTPException(
            status_code=404,
            detail="Responsabilidade não encontrada",
        )

    if responsabilidade_update.status is not None:
        responsabilidade.status = responsabilidade_update.status

    if responsabilidade_update.observacoes is not None:
        responsabilidade.observacoes = responsabilidade_update.observacoes

    responsabilidade.atualizado_em = datetime.utcnow()

    db.add(responsabilidade)
    db.commit()
    db.refresh(responsabilidade)

    return responsabilidade


@router.delete("/responsabilidades/{responsabilidade_id}", status_code=204)
def deletar_responsabilidade(
    responsabilidade_id: int,
    db: Session = Depends(get_db),
):
    """Deletar um registro de responsabilidade"""
    responsabilidade = db.query(ResponsabilidadeChromebook).filter(
        ResponsabilidadeChromebook.id == responsabilidade_id
    ).first()

    if not responsabilidade:
        raise HTTPException(
            status_code=404,
            detail="Responsabilidade não encontrada",
        )

    db.delete(responsabilidade)
    db.commit()

    return None


@router.get("/cronograma", response_model=dict)
def obter_cronograma(
    mes: int = Query(None),
    ano: int = Query(None),
    db: Session = Depends(get_db),
):
    """
    Obter cronograma de responsabilidades agrupado por data.
    Se mes e ano não forem fornecidos, usa mês/ano atual.
    """
    # Se não fornecido, usar mês/ano atual
    if mes is None or ano is None:
        hoje = datetime.utcnow()
        mes = mes or hoje.month
        ano = ano or hoje.year

    # Validar mês
    if not 1 <= mes <= 12:
        raise HTTPException(
            status_code=400,
            detail="Mês deve estar entre 1 e 12",
        )

    # Query responsabilidades para o mês/ano
    responsabilidades = db.query(ResponsabilidadeChromebook).filter(
        ResponsabilidadeChromebook.data >= datetime(ano, mes, 1),
        ResponsabilidadeChromebook.data < datetime(ano, mes + 1, 1) if mes < 12 else datetime(ano + 1, 1, 1),
    ).all()

    # Agrupar por data
    cronograma_dict = {}
    for resp in responsabilidades:
        data_str = resp.data.strftime("%Y-%m-%d")
        if data_str not in cronograma_dict:
            cronograma_dict[data_str] = {
                "data": data_str,
                "dia_semana": resp.data.strftime("%A"),  # Dia da semana em inglês (ou locale)
                "responsabilidades": [],
            }

        cronograma_dict[data_str]["responsabilidades"].append({
            "id": resp.id,
            "professor": resp.professor.nome,
            "professor_id": resp.professor_id,
            "periodo_turma": resp.periodo_turma,
            "quantidade": resp.quantidade_chromebooks,
            "status": resp.status.value,
        })

    # Converter para lista ordenada
    cronograma = {
        "mes": mes,
        "ano": ano,
        "dias": sorted(cronograma_dict.values(), key=lambda x: x["data"]),
    }

    return cronograma
