"""Integration tests for POST /api/ativos endpoint"""
import pytest
import json
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db
from models import TipoAtivo


# Use in-memory SQLite for testing
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db for tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup():
    """Setup test database with initial data before each test"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Add initial data
    db = TestingSessionLocal()
    
    # Create default tipos
    tipos = [
        TipoAtivo(nome="Notebook", descricao="Computadores portáteis"),
        TipoAtivo(nome="Impressora", descricao="Dispositivos de impressão"),
        TipoAtivo(nome="Monitor", descricao="Monitores"),
    ]
    
    for tipo in tipos:
        db.add(tipo)
    
    db.commit()
    db.close()
    
    yield
    
    # Cleanup after test
    Base.metadata.drop_all(bind=engine)


def test_create_ativo_with_valid_data():
    """Test creating ativo with all valid data"""
    response = client.post("/api/ativos", json={
        "descricao": "Notebook Dell XPS 13",
        "tipo_id": 1,
        "numero_serie": "SN-12345",
        "mac_address": "00:1A:2B:3C:4D:5E",
        "valor_estimado": 3000.00,
        "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "localizacao": "Sala 101"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "id" in data
    assert data["message"] == "Ativo cadastrado com sucesso"


def test_create_ativo_without_numero_serie():
    """Test that numero_serie is required"""
    response = client.post("/api/ativos", json={
        "descricao": "Notebook Dell XPS 13",
        "tipo_id": 1,
        "numero_serie": "",  # Empty
        "valor_estimado": 3000.00,
        "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "localizacao": "Sala 101"
    })
    
    assert response.status_code == 422  # Validation error


def test_create_ativo_with_duplicate_numero_serie():
    """Test that duplicate numero_serie is rejected"""
    # First ativo
    client.post("/api/ativos", json={
        "descricao": "Notebook Dell XPS 13",
        "tipo_id": 1,
        "numero_serie": "SN-DUPLICATE",
        "valor_estimado": 3000.00,
        "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "localizacao": "Sala 101"
    })
    
    # Second ativo with same numero_serie
    response = client.post("/api/ativos", json={
        "descricao": "Outro Notebook",
        "tipo_id": 1,
        "numero_serie": "SN-DUPLICATE",
        "valor_estimado": 2500.00,
        "data_aquisicao": (datetime.utcnow() - timedelta(days=5)).isoformat(),
        "localizacao": "Sala 102"
    })
    
    assert response.status_code == 400
    data = response.json()["detail"]
    assert data["error"] == "Número de série já cadastrado"
    assert data["field"] == "numero_serie"


def test_create_ativo_with_future_date():
    """Test that data_aquisicao cannot be in the future"""
    response = client.post("/api/ativos", json={
        "descricao": "Notebook",
        "tipo_id": 1,
        "numero_serie": "SN-FUTURE",
        "valor_estimado": 3000.00,
        "data_aquisicao": (datetime.utcnow() + timedelta(days=10)).isoformat(),  # Future
        "localizacao": "Sala 101"
    })
    
    assert response.status_code == 400
    data = response.json()["detail"]
    assert data["error"] == "Data não pode ser no futuro"
    assert data["field"] == "data_aquisicao"


def test_create_ativo_with_negative_valor():
    """Test that valor_estimado cannot be negative"""
    response = client.post("/api/ativos", json={
        "descricao": "Notebook",
        "tipo_id": 1,
        "numero_serie": "SN-NEGATIVE",
        "valor_estimado": -1000.00,  # Negative
        "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "localizacao": "Sala 101"
    })
    
    assert response.status_code == 400
    data = response.json()["detail"]
    assert data["error"] == "Valor deve ser positivo"
    assert data["field"] == "valor_estimado"


def test_create_ativo_with_invalid_tipo_id():
    """Test that tipo_id must exist"""
    response = client.post("/api/ativos", json={
        "descricao": "Notebook",
        "tipo_id": 999,  # Non-existent
        "numero_serie": "SN-INVALID-TIPO",
        "valor_estimado": 3000.00,
        "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "localizacao": "Sala 101"
    })
    
    assert response.status_code == 400
    data = response.json()["detail"]
    assert data["error"] == "Tipo de ativo não encontrado"
    assert data["field"] == "tipo_id"


def test_list_ativos():
    """Test listing all ativos"""
    # Create some ativos
    for i in range(3):
        client.post("/api/ativos", json={
            "descricao": f"Notebook {i}",
            "tipo_id": 1,
            "numero_serie": f"SN-LIST-{i}",
            "valor_estimado": 3000.00,
            "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
            "localizacao": "Sala 101"
        })
    
    # List ativos
    response = client.get("/api/ativos")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_list_ativos_with_pagination():
    """Test listing ativos with pagination"""
    # Create 5 ativos
    for i in range(5):
        client.post("/api/ativos", json={
            "descricao": f"Notebook {i}",
            "tipo_id": 1,
            "numero_serie": f"SN-PAGE-{i}",
            "valor_estimado": 3000.00,
            "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
            "localizacao": "Sala 101"
        })
    
    # List with limit=2
    response = client.get("/api/ativos?skip=0&limit=2")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_ativo_by_id():
    """Test getting a specific ativo"""
    # Create an ativo
    create_response = client.post("/api/ativos", json={
        "descricao": "Notebook",
        "tipo_id": 1,
        "numero_serie": "SN-GET-ID",
        "valor_estimado": 3000.00,
        "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "localizacao": "Sala 101"
    })
    
    ativo_id = create_response.json()["id"]
    
    # Get specific ativo
    response = client.get(f"/api/ativos/{ativo_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ativo_id
    assert data["numero_serie"] == "SN-GET-ID"


def test_get_ativo_not_found():
    """Test getting non-existent ativo"""
    response = client.get("/api/ativos/999")
    
    assert response.status_code == 404


def test_update_ativo():
    """Test updating an ativo"""
    # Create an ativo
    create_response = client.post("/api/ativos", json={
        "descricao": "Notebook Original",
        "tipo_id": 1,
        "numero_serie": "SN-UPDATE",
        "valor_estimado": 3000.00,
        "data_aquisicao": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "localizacao": "Sala 101"
    })
    
    ativo_id = create_response.json()["id"]
    
    # Update ativo
    response = client.put(f"/api/ativos/{ativo_id}", json={
        "descricao": "Notebook Atualizado",
        "localizacao": "Sala 102"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Verify update
    get_response = client.get(f"/api/ativos/{ativo_id}")
    updated_ativo = get_response.json()
    assert updated_ativo["descricao"] == "Notebook Atualizado"
    assert updated_ativo["localizacao"] == "Sala 102"
