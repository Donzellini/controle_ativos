"""Seed data for initial setup"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, init_db
from models import TipoAtivo, Ativo, StatusAtivo

load_dotenv()


def seed_database():
    """Initialize database with seed data"""
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if already seeded
        existing_tipos = db.query(TipoAtivo).count()
        if existing_tipos > 0:
            print("Database already seeded")
            return
        
        # Create TipoAtivo records
        tipos = [
            TipoAtivo(nome="Notebook", descricao="Computadores portáteis"),
            TipoAtivo(nome="Desktop", descricao="Computadores de mesa"),
            TipoAtivo(nome="Impressora", descricao="Dispositivos de impressão"),
            TipoAtivo(nome="Monitor", descricao="Monitores"),
            TipoAtivo(nome="Teclado", descricao="Teclados"),
            TipoAtivo(nome="Mouse", descricao="Mouses e trackpads"),
            TipoAtivo(nome="Webcam", descricao="Câmeras web"),
            TipoAtivo(nome="Projetor", descricao="Projetores multimídia"),
            TipoAtivo(nome="Scanner", descricao="Scanners"),
            TipoAtivo(nome="Roteador", descricao="Dispositivos de rede"),
        ]
        
        for tipo in tipos:
            db.add(tipo)
        
        db.commit()
        print(f"✅ Created {len(tipos)} TipoAtivo records")
        
        # Get first tipo for sample data
        notebook_tipo = db.query(TipoAtivo).filter(TipoAtivo.nome == "Notebook").first()
        
        # Create sample Ativo records (optional - commented out)
        # sample_ativos = [
        #     Ativo(
        #         descricao="Notebook Dell XPS 13",
        #         tipo_id=notebook_tipo.id,
        #         numero_serie="DELL-XPS-001",
        #         mac_address="00:1A:2B:3C:4D:5E",
        #         valor_estimado=3500.00,
        #         data_aquisicao=datetime(2024, 1, 15),
        #         status=StatusAtivo.DISPONIVEL,
        #         localizacao="Sala 101"
        #     ),
        #     Ativo(
        #         descricao="Notebook Lenovo ThinkPad",
        #         tipo_id=notebook_tipo.id,
        #         numero_serie="LENOVO-TP-001",
        #         mac_address="00:AA:BB:CC:DD:EE",
        #         valor_estimado=2800.00,
        #         data_aquisicao=datetime(2024, 2, 20),
        #         status=StatusAtivo.DISPONIVEL,
        #         localizacao="Sala 102"
        #     ),
        # ]
        # 
        # for ativo in sample_ativos:
        #     db.add(ativo)
        # 
        # db.commit()
        # print(f"✅ Created {len(sample_ativos)} sample Ativo records")
        
        print("✅ Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    seed_database()
