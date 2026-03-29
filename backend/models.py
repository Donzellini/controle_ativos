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


class StatusResponsabilidade(str, PyEnum):
    """Status enum for Chromebook responsibility"""
    PENDENTE = "Pendente"
    DEVOLVIDO = "Devolvido"
    COM_FALTA = "Com falta"
    NAO_REALIZADO = "Não realizado"


class Professor(Base):
    """Professor/Teacher model"""
    __tablename__ = "professor"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    responsabilidades = relationship("ResponsabilidadeChromebook", back_populates="professor")

    def __repr__(self):
        return f"<Professor(id={self.id}, nome='{self.nome}')>"


class ResponsabilidadeChromebook(Base):
    """Chromebook responsibility tracking model"""
    __tablename__ = "responsabilidade_chromebook"

    id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professor.id"), nullable=False, index=True)
    data = Column(DateTime, nullable=False)  # Date of responsibility
    periodo_turma = Column(String(10), nullable=False)  # Period/Class (e.g., "1ºA", "3ºC")
    quantidade_chromebooks = Column(Integer, nullable=False)  # Number of Chromebooks
    status = Column(Enum(StatusResponsabilidade), default=StatusResponsabilidade.PENDENTE, nullable=False)
    observacoes = Column(String(500), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    professor = relationship("Professor", back_populates="responsabilidades")

    # Constraints
    __table_args__ = (
        UniqueConstraint("professor_id", "data", "periodo_turma", name="uq_professor_data_periodo"),
    )

    def __repr__(self):
        return f"<ResponsabilidadeChromebook(id={self.id}, professor_id={self.professor_id}, data={self.data})>"
