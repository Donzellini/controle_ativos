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


class StatusResponsabilidade(str, PyEnum):
    """Status enum for Chromebook responsibility"""
    PENDENTE = "Pendente"
    DEVOLVIDO = "Devolvido"
    COM_FALTA = "Com falta"
    NAO_REALIZADO = "Não realizado"


class ProfessorCreate(BaseModel):
    """Schema for creating a professor"""
    nome: str = Field(..., min_length=1, max_length=255)
    email: Optional[str] = Field(None, max_length=255)

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v):
        if not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v.strip()


class ProfessorResponse(BaseModel):
    """Schema for professor response"""
    id: int
    nome: str
    email: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True


class ResponsabilidadeCreate(BaseModel):
    """Schema for creating a Chromebook responsibility"""
    professor_id: int
    data: datetime
    periodo_turma: str = Field(..., min_length=1, max_length=10)
    quantidade_chromebooks: int = Field(..., ge=1)
    observacoes: Optional[str] = Field(None, max_length=500)

    @field_validator("quantidade_chromebooks")
    @classmethod
    def validate_quantidade(cls, v):
        if v <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        return v

    @field_validator("periodo_turma")
    @classmethod
    def validate_periodo(cls, v):
        periodos_validos = ["1ºA", "2ºA", "2ºB", "3ºA", "3ºB", "3ºC", "4ºA", "4ºB", "4ºC", "5ºA", "5ºB", "5ºC"]
        if v not in periodos_validos:
            # Apenas aviso, permite outros valores (MVP flexível)
            pass
        return v


class ResponsabilidadeUpdate(BaseModel):
    """Schema for updating a Chromebook responsibility (status and notes)"""
    status: Optional[StatusResponsabilidade] = None
    observacoes: Optional[str] = Field(None, max_length=500)

    class Config:
        from_attributes = True


class ResponsabilidadeResponse(BaseModel):
    """Schema for Chromebook responsibility response"""
    id: int
    professor_id: int
    data: datetime
    periodo_turma: str
    quantidade_chromebooks: int
    status: StatusResponsabilidade
    observacoes: Optional[str] = None
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
