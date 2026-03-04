"""Tests for Ativo model"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, Ativo, TipoAtivo, StatusAtivo
from database import SessionLocal


# Use in-memory SQLite for testing
@pytest.fixture
def db():
    """Create a fresh database for each test"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    # Create initial data
    tipo = TipoAtivo(nome="Notebook", descricao="Computadores portáteis")
    db.add(tipo)
    db.commit()
    
    yield db
    db.close()


def test_create_ativo_valid(db):
    """Test creating a valid ativo"""
    tipo = db.query(TipoAtivo).first()
    
    ativo = Ativo(
        descricao="Notebook Dell XPS",
        tipo_id=tipo.id,
        numero_serie="SN-12345",
        mac_address="00:1A:2B:3C:4D:5E",
        valor_estimado=3000.00,
        data_aquisicao=datetime.utcnow() - timedelta(days=10),
        status=StatusAtivo.DISPONIVEL,
        localizacao="Sala 101"
    )
    
    db.add(ativo)
    db.commit()
    db.refresh(ativo)
    
    assert ativo.id is not None
    assert ativo.numero_serie == "SN-12345"
    assert ativo.status == StatusAtivo.DISPONIVEL


def test_ativo_numero_serie_unique(db):
    """Test that numero_serie must be unique"""
    tipo = db.query(TipoAtivo).first()
    
    ativo1 = Ativo(
        descricao="Notebook Dell XPS",
        tipo_id=tipo.id,
        numero_serie="SN-12345",
        valor_estimado=3000.00,
        data_aquisicao=datetime.utcnow() - timedelta(days=10),
        localizacao="Sala 101"
    )
    
    db.add(ativo1)
    db.commit()
    
    # Try to add another ativo with same numero_serie
    ativo2 = Ativo(
        descricao="Outro Notebook",
        tipo_id=tipo.id,
        numero_serie="SN-12345",  # Duplicate
        valor_estimado=2500.00,
        data_aquisicao=datetime.utcnow() - timedelta(days=5),
        localizacao="Sala 102"
    )
    
    db.add(ativo2)
    
    with pytest.raises(IntegrityError):
        db.commit()


def test_ativo_fields_required(db):
    """Test that required fields are set"""
    tipo = db.query(TipoAtivo).first()
    
    ativo = Ativo(
        descricao="Notebook",
        tipo_id=tipo.id,
        numero_serie="SN-999",
        valor_estimado=2000.00,
        data_aquisicao=datetime.utcnow() - timedelta(days=5),
        localizacao="Sala 01"
    )
    
    assert ativo.descricao == "Notebook"
    assert ativo.numero_serie == "SN-999"
    assert ativo.valor_estimado == 2000.00


def test_ativo_default_status(db):
    """Test that default status is DISPONIVEL"""
    tipo = db.query(TipoAtivo).first()
    
    ativo = Ativo(
        descricao="Notebook",
        tipo_id=tipo.id,
        numero_serie="SN-555",
        valor_estimado=2000.00,
        data_aquisicao=datetime.utcnow() - timedelta(days=5),
        localizacao="Sala 01"
    )
    
    db.add(ativo)
    db.commit()
    
    assert ativo.status == StatusAtivo.DISPONIVEL


def test_ativo_timestamps(db):
    """Test that criado_em and atualizado_em are set"""
    tipo = db.query(TipoAtivo).first()
    
    before = datetime.utcnow()
    ativo = Ativo(
        descricao="Notebook",
        tipo_id=tipo.id,
        numero_serie="SN-777",
        valor_estimado=2000.00,
        data_aquisicao=datetime.utcnow() - timedelta(days=5),
        localizacao="Sala 01"
    )
    db.add(ativo)
    db.commit()
    after = datetime.utcnow()
    
    assert before <= ativo.criado_em <= after
    assert before <= ativo.atualizado_em <= after
