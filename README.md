# Controle de Ativos de TI

Sistema web para gerenciamento de ativos de TI (notebooks, impressoras, etc.) com validação de dados e controle de inventário.

## Features

- ✅ Cadastro de ativos com validações
- ✅ Listagem com filtros e busca
- ✅ Edição de ativos
- ✅ Interface responsiva com Bootstrap 5
- ✅ API RESTful com FastAPI
- ✅ Banco de dados SQLite
- ✅ Testes automatizados

## Estrutura do Projeto

```
.
├── backend/                    # Backend FastAPI
│   ├── main.py                # App principal
│   ├── database.py            # Configuração do banco de dados
│   ├── models.py              # Modelos SQLAlchemy
│   ├── schemas.py             # Schemas Pydantic
│   ├── requirements.txt        # Dependências Python
│   ├── .env.example           # Variáveis de ambiente
│   ├── routes/
│   │   ├── __init__.py
│   │   └── ativos.py          # Endpoints de ativos
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py     # Testes de modelos
│       └── test_ativos_create.py  # Testes de API
├── frontend/                   # Frontend HTML/CSS/JS
│   ├── index.html             # Página inicial
│   ├── cadastro.html          # Formulário de cadastro
│   ├── listagem.html          # Listagem de ativos
│   ├── editar.html            # Edição de ativo (a implementar)
│   ├── css/
│   │   └── style.css          # Estilos customizados
│   └── js/
│       ├── cadastro.js        # Lógica de cadastro
│       └── listagem.js        # Lógica de listagem
└── docs/                       # Documentação
    ├── specs/
    └── plans/
```

## Instalação e Setup

### Backend

1. **Instale as dependências Python:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure as variáveis de ambiente:**

```bash
cp .env.example .env
```

3. **Execute o servidor:**

```bash
python main.py
```

O servidor estará disponível em: `http://localhost:8000`

**Documentação Swagger:** `http://localhost:8000/docs`

### Frontend

1. **Abra o navegador** e acesse:

```
http://localhost:5500/frontend/index.html
```

Ou use Live Server do VS Code ou outro servidor web:

```bash
cd frontend
# Com Python 3
python -m http.server 5500

# Ou com Node.js (http-server)
npx http-server -p 5500
```

## API Endpoints

### Ativos

- `POST /api/ativos` - Criar novo ativo
- `GET /api/ativos` - Listar ativos (com paginação)
- `GET /api/ativos/{id}` - Obter ativo específico
- `PUT /api/ativos/{id}` - Atualizar ativo

### Exemplo de Requisição

```bash
# Criar ativo
curl -X POST "http://localhost:8000/api/ativos" \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Notebook Dell XPS 13",
    "tipo_id": 1,
    "numero_serie": "SN-12345",
    "mac_address": "00:1A:2B:3C:4D:5E",
    "valor_estimado": 3000.00,
    "data_aquisicao": "2025-01-15T00:00:00",
    "localizacao": "Sala 101"
  }'
```

## Testes

### Executar testes:

```bash
cd backend
pytest tests/
```

### Executar testes com cobertura:

```bash
pytest tests/ --cov=. --cov-report=html
```

## Validações

### Cadastro de Ativo

✅ **Descrição**: Obrigatória, máximo 255 caracteres  
✅ **Tipo**: Deve existir no banco de dados  
✅ **Número de Série**: Obrigatório, único, máximo 100 caracteres  
✅ **MAC Address**: Opcional, máximo 17 caracteres  
✅ **Valor Estimado**: Obrigatório, deve ser ≥ 0  
✅ **Data de Aquisição**: Obrigatória, não pode ser no futuro  
✅ **Localização**: Obrigatória, máximo 255 caracteres  

### Respostas de Erro

Erros retornam JSON estruturado:

```json
{
  "detail": {
    "error": "Mensagem de erro em português",
    "field": "nome_do_campo"
  }
}
```

## Status do Ativo

- **Disponível** (Verde): Ativo disponível para uso
- **Emprestado** (Amarelo): Ativo emprestado
- **Danificado** (Vermelho): Ativo danificado e indisponível
- **Inativo** (Cinza): Ativo fora de uso

## Desenvolvimento

### Adicionar novo endpoint

1. Crie a rota em `backend/routes/novo.py`
2. Importe o router em `backend/main.py`
3. Adicione o router ao app: `app.include_router(router, prefix="/api", tags=["tag"])`

### Adicionar teste

Crie arquivo `backend/tests/test_novo.py` e use pytest.

## Troubleshooting

### Erro: `Módulo 'database' não encontrado`

Certifique-se que está no diretório `backend/` ao executar:
```bash
cd backend
python main.py
```

### Erro: CORS bloqueando requisições

O CORS está configurado para aceitar todas as origens. Se precisar restringir, edite `backend/main.py`.

### Banco de dados não criado

Execute novamente:
```bash
python main.py
```

O banco de dados será criado automaticamente no primeiro acesso.

## Próximas Features (P2, P3)

- [ ] User Story 2: Listagem avançada com filtros e paginação
- [ ] User Story 3: Edição de ativos
- [ ] Exportação para CSV/Excel
- [ ] Relatórios de inventário
- [ ] Histórico de movimentações
- [ ] Sistema de empréstimos

## Licença

Este projeto é parte do Almoxarifado TI - Sistema de Controle de Ativos.

---

**Versão**: 1.0.0  
**Data**: 2026-03-03  
**Status**: MVP - Fase 1 (Cadastro de Ativos) Completa
