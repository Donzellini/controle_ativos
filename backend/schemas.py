"""Pydantic schemas for API requests and responses"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum as PyEnum


class StatusAtivo(str, PyEnum):
    """Status enum for responses"""
    DISPONIVEL = "Disponível"
    EMPRESTADO = "Emprestado"
    DANIFICADO = "Danificado"
    INATIVO = "Inativo"


class TipoAtivoSchema(BaseModel):
    """Schema for asset type"""
    id: int
    nome: str
    descricao: Optional[str] = None

    class Config:
        from_attributes = True


class AtivoCreate(BaseModel):
    """Schema for creating a new asset"""
    descricao: str = Field(..., min_length=1, max_length=255)
    tipo_id: int
    numero_serie: str = Field(..., min_length=1, max_length=100)
    mac_address: Optional[str] = Field(None, max_length=17)
    valor_estimado: float = Field(..., ge=0)
    data_aquisicao: datetime
    localizacao: str = Field(..., min_length=1, max_length=255)

    @field_validator("valor_estimado")
    @classmethod
    def validate_valor(cls, v):
        if v < 0:
            raise ValueError("Valor deve ser positivo")
        return v

    @field_validator("data_aquisicao")
    @classmethod
    def validate_data(cls, v):
        if v > datetime.utcnow():
            raise ValueError("Data não pode ser no futuro")
        return v


class AtivoUpdate(BaseModel):
    """Schema for updating an asset"""
    descricao: Optional[str] = Field(None, min_length=1, max_length=255)
    localizacao: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[StatusAtivo] = None

    class Config:
        from_attributes = True


class AtivoResponse(BaseModel):
    """Schema for asset response"""
    id: int
    descricao: str
    tipo_id: int
    numero_serie: str
    mac_address: Optional[str] = None
    valor_estimado: float
    data_aquisicao: datetime
    status: StatusAtivo
    localizacao: str
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Schema for error response"""
    error: str
    field: Optional[str] = None
