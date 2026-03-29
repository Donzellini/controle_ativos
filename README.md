# Controle de Ativos de TI

Sistema web completo para gerenciamento de ativos de TI e responsabilidade de Chromebooks, desenvolvido com Spec-Driven Development.

**Status**: ✅ MVP Completo  
**Versão**: 2.0.0  
**Data**: 2026-03-29  

## Features

- ✅ **Cadastro de Ativos** - Sistema completo de gestão de TI (Notebook, Desktop, Impressora, Monitor, Teclado, Mouse, Webcam, Projetor, Scanner, Roteador)
- ✅ **Responsabilidade de Chromebooks** - Rastreamento de responsabilidades por professor/período com cronograma
- ✅ **Listagem com filtros e busca** - Tabelas paginadas e responsivas
- ✅ **Edição de registros** - Interface intuitiva para atualização de dados
- ✅ **Interface responsiva com Bootstrap 5** - Compatível com mobile e desktop
- ✅ **API RESTful com FastAPI** - 14 endpoints documentados com Swagger
- ✅ **Banco de dados SQLite** - Com autorelacionamentos e integridade referencial
- ✅ **Validações robustas** - Cliente-side (JS) e server-side (Pydantic)
- ✅ **Testes automatizados** - Com pytest e cobertura

## Estrutura do Projeto

```
controle_ativos/
├── backend/
│   ├── main.py                   # FastAPI app principal
│   ├── database.py               # SQLite SessionLocal, init_db()
│   ├── models.py                 # TipoAtivo, Ativo, Professor, ResponsabilidadeChromebook
│   ├── schemas.py                # Pydantic: AtivoCreate, ProfessorCreate, etc.
│   ├── seed.py                   # Popula tipos, professores iniciais
│   ├── ativos.db                 # Banco de dados SQLite
│   ├── requirements.txt           # FastAPI, SQLAlchemy, Pydantic, pytest
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── ativos.py             # POST/GET/PUT /api/ativos
│   │   └── responsabilidades.py  # POST/GET/PUT /api/responsabilidades, /api/professores, /api/cronograma
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py        # Unit tests modelos
│       ├── test_ativos_create.py # Integration tests ativos
│       └── test_responsabilidades.py # Integration tests responsabilidades
│
├── frontend/
│   ├── index.html                # Página inicial com atalhos
│   ├── cadastro.html             # Form novo ativo
│   ├── listagem.html             # Tabela ativos
│   ├── editar.html               # Form edição ativo
│   ├── responsabilidade-form.html # Form nova responsabilidade
│   ├── cronograma.html           # Tabela cronograma
│   ├── css/
│   │   └── style.css             # Bootstrap custom + dark navbar
│   └── js/
│       ├── cadastro.js           # Lógica cadastro ativo
│       ├── listagem.js           # Lógica listagem ativos
│       ├── editar.js             # Lógica edição ativo
│       ├── responsabilidade.js   # Lógica form responsabilidade
│       └── cronograma.js         # Lógica cronograma
│
└── docs/
    ├── specs/
    │   ├── feature-cadastro-ativos.md
    │   └── feature-responsabilidade-chromebooks.md
    └── plans/
        ├── plan-001-cadastro-ativos.md
        ├── plan-002-responsabilidade-chromebooks.md
        ├── tasks-001-cadastro-ativos.md
        └── tasks-002-responsabilidade-chromebooks.md
```

## Instalação e Setup

### Backend

#### 1. Instalar Dependências

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Criar Banco de Dados

```bash
python seed.py
```

Isso cria `ativos.db` com 10 tipos de ativos e 5 professores.

#### 3. Rodar Servidor

```bash
uvicorn main:app --reload --port 8000
```

**Servidor**: `http://localhost:8000`  
**Docs**: `http://localhost:8000/docs`

### Frontend

#### 1. Rodar Servidor Estático

```bash
cd frontend
python -m http.server 5500
```

Ou use Live Server VS Code.

#### 2. Acessar no Navegador

```
http://localhost:5500
```

---

## 📌 IMPLEMENTAÇÃO TÉCNICA DETALHADA

Documentação técnica completa das 2 features implementadas.

---

### Feature 001: Cadastro de Ativos

**Status**: ✅ Completo | **Prioridade**: P1 | **Data**: 2026-03-03

#### 1.1 Overview

Sistema de cadastro, listagem e edição de ativos de TI com validações robustas. Cada ativo tem tipo, número de série único, valor, localização e status de disponibilidade.

#### 1.2 Modelos de Dados

**Tabela: `tipo_ativo`**

```python
class TipoAtivo(Base):
    id: Integer (Primary Key)
    nome: String[100] (Unique, Required)
    descricao: String[255] (Optional)
    criado_em: DateTime (Auto)
```

**Tipos Pré-Cadastrados:**
```
1. Notebook    6. Mouse
2. Desktop     7. Webcam
3. Impressora  8. Projetor
4. Monitor     9. Scanner
5. Teclado    10. Roteador
```

**Tabela: `ativo`**

```python
class Ativo(Base):
    id: Integer (PK)
    descricao: String[255] (Required)
    tipo_id: Integer (FK → tipo_ativo)
    numero_serie: String[100] (Unique, Required)
    mac_address: String[17] (Optional)
    valor_estimado: Float (Required, >= 0)
    data_aquisicao: DateTime (Required, not future)
    status: Enum(StatusAtivo) (Default: DISPONIVEL)
    localizacao: String[255] (Required)
    criado_em: DateTime (Auto)
    atualizado_em: DateTime (Auto)
```

**Enum: `StatusAtivo`**

```python
DISPONÍVEL = "Disponível"        # Verde ✓
EMPRESTADO = "Emprestado"        # Amarelo ⚠
DANIFICADO = "Danificado"        # Vermelho ✗
INATIVO = "Inativo"              # Cinza −
```

#### 1.3 API Endpoints - Ativos

| Método | Endpoint | Status | Descrição |
|--------|----------|--------|-----------|
| `POST` | `/api/ativos` | 201 | Criar novo ativo |
| `GET` | `/api/ativos` | 200 | Listar ativos (paginado) |
| `GET` | `/api/ativos/{id}` | 200/404 | Obter ativo específico |
| `PUT` | `/api/ativos/{id}` | 200/404 | Atualizar ativo |

**POST /api/ativos - Criar Ativo**

```bash
curl -X POST "http://localhost:8000/api/ativos" \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Notebook Dell XPS 13",
    "tipo_id": 1,
    "numero_serie": "DELL-XPS-001",
    "mac_address": "00:1A:2B:3C:4D:5E",
    "valor_estimado": 3500.00,
    "data_aquisicao": "2025-01-15T00:00:00",
    "localizacao": "Sala 101"
  }'
```

**Validações**:
- ✅ descricao obrigatória (1-255)
- ✅ tipo_id deve existir
- ✅ numero_serie único
- ✅ valor_estimado >= 0
- ✅ data_aquisicao não no futuro
- ✅ localizacao obrigatória

**GET /api/ativos - Listar Ativos**

```bash
curl "http://localhost:8000/api/ativos?skip=0&limit=20"
```

**GET /api/ativos/{id} - Obter Ativo**

```bash
curl "http://localhost:8000/api/ativos/1"
```

**PUT /api/ativos/{id} - Atualizar Ativo**

```bash
curl -X PUT "http://localhost:8000/api/ativos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "localizacao": "Sala 102",
    "status": "Emprestado"
  }'
```

#### 1.4 Frontend - Ativos

**Páginas HTML**:
- `index.html` - Página inicial com atalhos para Ativos e Responsabilidades
- `cadastro.html` - Formulário de novo ativo com 8 campos
- `listagem.html` - Tabela com ativos, search, paginação e status badges
- `editar.html` - Formulário de edição pré-preenchido

**Scripts JavaScript**:
- `cadastro.js` - Carrega tipos de ativos, POST /api/ativos, validação cliente
- `listagem.js` - GET /api/ativos, renderiza tabela, search/filtros, paginação
- `editar.js` - Carrega ativo para edição, PUT /api/ativos/{id}

---

### Feature 002: Responsabilidade de Chromebooks

**Status**: ✅ Completo | **Prioridade**: P1 | **Data**: 2026-03-29

#### 2.1 Overview

Sistema de rastreamento de responsabilidade de Chromebooks que permite designar qual professor é responsável por uma quantidade X de Chromebooks em um período específico. Desenvolvido baseado em requisito em áudio da vice-diretora, seguindo Spec-Driven Development.

**Contexto**: Professores têm cronograma na sala de informática. Cada período, uma professora é responsável pela quantidade total de Chromebooks. A vice-direção controla os números individuais; a professora controla a quantidade.

#### 2.2 Modelos de Dados

**Tabela: `professor`**

```python
class Professor(Base):
    id: Integer (Primary Key)
    nome: String[255] (Unique, Required)
    email: String[255] (Optional)
    criado_em: DateTime (Auto)
```

**Professores Pré-Cadastrados:**
```
1. Maria Silva (maria@escola.edu.br)
2. Ana Santos (ana@escola.edu.br)
3. Carla Oliveira (carla@escola.edu.br)
4. Diane Costa (diane@escola.edu.br)
5. Elaine Martins (elaine@escola.edu.br)
```

**Tabela: `responsabilidade_chromebook`**

```python
class ResponsabilidadeChromebook(Base):
    id: Integer (PK)
    professor_id: Integer (FK → professor, Required)
    data: DateTime (Required)
    periodo_turma: String[10] (Required)
    quantidade_chromebooks: Integer (Required, > 0)
    status: Enum(StatusResponsabilidade) (Default: PENDENTE)
    observacoes: String[500] (Optional)
    criado_em: DateTime (Auto)
    atualizado_em: DateTime (Auto)
    
    Constraint: Unique(professor_id, data, periodo_turma)
```

**Períodos/Turmas Válidos:**
```
1ºA, 2ºA, 2ºB, 3ºA, 3ºB, 3ºC, 4ºA, 4ºB, 4ºC, 5ºA, 5ºB, 5ºC
```

**Enum: `StatusResponsabilidade`**

```python
PENDENTE = "Pendente"              # Azul → Aguardando conclusão
DEVOLVIDO = "Devolvido"            # Verde → Chromebooks retornados
COM_FALTA = "Com falta"            # Vermelho → Faltam aparelhos
NAO_REALIZADO = "Não realizado"    # Cinza → Período não ocorreu
```

#### 2.3 API Endpoints - Responsabilidades

| Método | Endpoint | Status | Descrição |
|--------|----------|--------|-----------|
| `POST` | `/api/professores` | 201 | Criar professor |
| `GET` | `/api/professores` | 200 | Listar professores |
| `GET` | `/api/professores/{id}` | 200/404 | Obter professor |
| `POST` | `/api/responsabilidades` | 201 | Criar responsabilidade |
| `GET` | `/api/responsabilidades` | 200 | Listar responsabilidades (com filtros) |
| `GET` | `/api/responsabilidades/{id}` | 200/404 | Obter responsabilidade |
| `PUT` | `/api/responsabilidades/{id}` | 200/404 | Atualizar status/obs |
| `DELETE` | `/api/responsabilidades/{id}` | 204 | Deletar responsabilidade |
| `GET` | `/api/cronograma` | 200 | Cronograma agrupado por data |

**POST /api/professores - Criar Professor**

```bash
curl -X POST "http://localhost:8000/api/professores" \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "email": "joao@escola.edu.br"}'
```

**GET /api/professores - Listar Professores**

```bash
curl "http://localhost:8000/api/professores"
```

**POST /api/responsabilidades - Criar Responsabilidade**

```bash
curl -X POST "http://localhost:8000/api/responsabilidades" \
  -H "Content-Type: application/json" \
  -d '{
    "professor_id": 1,
    "data": "2026-03-02T00:00:00",
    "periodo_turma": "1ºA",
    "quantidade_chromebooks": 20,
    "observacoes": "Sala de informática"
  }'
```

**Validações**:
- ✅ professor_id deve existir
- ✅ quantidade > 0
- ✅ periodo_turma válido (1ºA-5ºC)
- ✅ Único por (professor_id, data, periodo_turma)

**GET /api/responsabilidades - Listar com Filtros**

```bash
# Todas
curl "http://localhost:8000/api/responsabilidades"

# Por professor
curl "http://localhost:8000/api/responsabilidades?professor_id=1"

# Por período
curl "http://localhost:8000/api/responsabilidades?periodo_turma=1ºA"

# Por data range
curl "http://localhost:8000/api/responsabilidades?data_inicio=2026-03-01&data_fim=2026-03-31"
```

**GET /api/cronograma - Cronograma por Mês**

```bash
curl "http://localhost:8000/api/cronograma?mes=3&ano=2026"
```

Resposta agrupada por data:
```json
{
  "mes": 3,
  "ano": 2026,
  "dias": [
    {
      "data": "2026-03-02",
      "dia_semana": "Monday",
      "responsabilidades": [
        {
          "id": 1,
          "professor": "Maria Silva",
          "periodo_turma": "1ºA",
          "quantidade": 20,
          "status": "Pendente"
        }
      ]
    }
  ]
}
```

**PUT /api/responsabilidades/{id} - Atualizar Status**

```bash
curl -X PUT "http://localhost:8000/api/responsabilidades/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Devolvido",
    "observacoes": "Todos os 20 retornados"
  }'
```

**DELETE /api/responsabilidades/{id} - Deletar**

```bash
curl -X DELETE "http://localhost:8000/api/responsabilidades/1"
```

#### 2.4 Frontend - Responsabilidades

**Páginas HTML**:
- `responsabilidade-form.html` - Formulário de nova responsabilidade (professor, data, período, quantidade)
- `cronograma.html` - Tabela de cronograma com filtros e edição inline via modal

**Scripts JavaScript**:
- `responsabilidade.js` - GET /api/professores (dropdown dinâmico), POST /api/responsabilidades
- `cronograma.js` - GET /api/cronograma, renderiza tabela, filtros, modal de edição, PUT responsabilidades

#### 2.5 Como Usar

**Registrar Nova Responsabilidade:**
1. Navbar → Responsabilidades → Nova Responsabilidade
2. Preencha: Professor, Data, Período (1ºA-5ºC), Quantidade
3. Clique "Registrar Responsabilidade"
4. Sistema redireciona para cronograma

**Visualizar Cronograma:**
1. Navbar → Responsabilidades → Cronograma
2. Tabela mostra responsabilidades do mês atual
3. Use filtros (Professor, Mês, Ano) para buscar
4. Clique "Editar" para alterar status

**Editar Responsabilidade:**
1. Na tabela cronograma, clique "Editar" em uma responsabilidade
2. Modal abre com status e observações
3. Altere conforme necessário
4. Clique "Salvar Mudanças"
5. Tabela atualiza em real-time

---

## API Endpoints

## Validações

### Feature 001 - Cadastro de Ativo

✅ **Descrição**: Obrigatória, máximo 255 caracteres  
✅ **Tipo**: Deve existir no banco de dados  
✅ **Número de Série**: Obrigatório, único, máximo 100 caracteres  
✅ **MAC Address**: Opcional, máximo 17 caracteres (formato válido)  
✅ **Valor Estimado**: Obrigatório, deve ser ≥ 0  
✅ **Data de Aquisição**: Obrigatória, não pode ser no futuro  
✅ **Localização**: Obrigatória, máximo 255 caracteres  

### Feature 002 - Responsabilidade de Chromebook

✅ **Professor**: Deve existir no banco de dados  
✅ **Data**: Formato válido (YYYY-MM-DD)  
✅ **Período/Turma**: Lista pré-definida (1ºA, 2ºA, 2ºB, 3ºA, 3ºB, 3ºC, 4ºA, 4ºB, 4ºC, 5ºA, 5ºB, 5ºC)  
✅ **Quantidade**: Deve ser > 0  
✅ **Unicidade**: Máximo 1 responsabilidade por (professor, data, período)  

## Testes

### Executar Todos os Testes

```bash
cd backend
pytest tests/ -v
```

### Com Cobertura de Código

```bash
pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### Teste Específico

```bash
pytest tests/test_ativos_create.py::test_criar_ativo_valido -v
```

## Stack Tecnológico

| Componente | Tecnologia | Versão |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI | 0.100.0+ |
| **ORM** | SQLAlchemy | 2.0.19+ |
| **Validação** | Pydantic | 2.0.3+ |
| **Servidor** | Uvicorn | 0.22.0+ |
| **Database** | SQLite 3 | Latest |
| **Frontend Markup** | HTML5 | Latest |
| **Frontend Framework** | Bootstrap | 5.3.0 |
| **Icons** | Bootstrap Icons | 1.11.0 |
| **Frontend JS** | Vanilla JS (Fetch API) | ES6+ |
| **Frontend Styling** | CSS3 + Bootstrap | Latest |
| **Testing** | Pytest | 7.0+ |
| **Python** | Python | 3.11+ |

## Troubleshooting

### ❌ Erro: Módulo 'routes' não encontrado

**Solução**: Certifique-se de estar no diretório `backend/`
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### ❌ Erro: CORS bloqueando requisições

**Verificação**: CORS está habilitado para todas as origens em `main.py`
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos
)
```

### ❌ Erro: Porta 8000 em uso

**Solução**: Use porta diferente
```bash
uvicorn main:app --reload --port 8001
```

### ❌ Banco de dados vazio (sem dados)

**Solução**: Executar seed para popular dados iniciais
```bash
python seed.py
```

### ❌ Número de série inválido ao criar ativo

**Verificação**: Número de série deve ser único
```bash
# Ver todos os ativos e suas séries
curl "http://localhost:8000/api/ativos" | python -m json.tool | grep numero_serie
```

### ❌ Form de responsabilidade não carrega professores

**Verificação**: API `/api/professores` está retornando?
```bash
curl "http://localhost:8000/api/professores"
```

Se vazio, rodar seed novamente: `python seed.py`

### ❌ Data no futuro ao registrar responsabilidade

**Observação**: ResponsabilidadeChromebook não tem validação de data (aceita datas futuras para planejamento)

---

## Documentação Completa

Para detalhes em profundidade, consulte os documentos de especificação e plano:

### Feature 001 - Cadastro de Ativos
- [Especificação Técnica](docs/specs/feature-cadastro-ativos.md)
- [Plano de Implementação](docs/plans/plan-001-cadastro-ativos.md)
- [Lista de Tarefas Detalhada](docs/plans/tasks-001-cadastro-ativos.md)

### Feature 002 - Responsabilidade de Chromebooks
- [Especificação Técnica](docs/specs/feature-responsabilidade-chromebooks.md)
- [Plano de Implementação](docs/plans/plan-002-responsabilidade-chromebooks.md)
- [Lista de Tarefas Detalhada](docs/plans/tasks-002-responsabilidade-chromebooks.md)

---

## Informações do Projeto

**Sistema**: Controle de Ativos de TI  
**Instituição**: Escola de Informática  
**Metodologia**: Spec-Driven Development (SDD) + Context-Driven Development  
**Versão**: 2.0.0 (MVP Completo)  
**Data**: 2026-03-29  
**Status**: ✅ Produção

---

**Desenvolvido seguindo as melhores práticas de desenvolvimento web com Python/FastAPI e JavaScript.**
