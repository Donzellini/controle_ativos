"""SQLAlchemy models for the application"""
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class StatusAtivo(str, PyEnum):
    """Status enum for assets"""
    DISPONIVEL = "Disponível"
    EMPRESTADO = "Emprestado"
    DANIFICADO = "Danificado"
    INATIVO = "Inativo"


class TipoAtivo(Base):
    """Asset type model"""
    __tablename__ = "tipo_ativo"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False, index=True)
    descricao = Column(String(255), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    ativos = relationship("Ativo", back_populates="tipo")

    def __repr__(self):
        return f"<TipoAtivo(id={self.id}, nome='{self.nome}')>"


class Ativo(Base):
    """Asset model"""
    __tablename__ = "ativo"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(255), nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipo_ativo.id"), nullable=False)
    numero_serie = Column(String(100), unique=True, nullable=False, index=True)
    mac_address = Column(String(17), nullable=True)
    valor_estimado = Column(Float, nullable=False)
    data_aquisicao = Column(DateTime, nullable=False)
    status = Column(Enum(StatusAtivo), default=StatusAtivo.DISPONIVEL, nullable=False)
    localizacao = Column(String(255), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    tipo = relationship("TipoAtivo", back_populates="ativos")

    # Constraints
    __table_args__ = (
        UniqueConstraint("numero_serie", name="uq_numero_serie"),
    )

    def __repr__(self):
        return f"<Ativo(id={self.id}, descricao='{self.descricao}', serie='{self.numero_serie}')>"
