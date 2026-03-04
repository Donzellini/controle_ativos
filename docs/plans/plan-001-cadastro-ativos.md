# Plano de Implementação: Cadastro de Ativos

**Branch**: `001-cadastro-ativos` | **Data**: 2026-03-03 | **Spec**: [feature-cadastro-ativos.md](../specs/feature-cadastro-ativos.md)

## Resumo

Sistema web para cadastro e gerenciamento de ativos de TI (notebooks, mouses, projetores, etc.) em uma instituição. Administradores podem registrar ativos com informações essenciais, o sistema valida unicidade de série e persiste em SQLite, permitindo rastreamento de inventário.

## Contexto Técnico

**Linguagem/Versão**: Python 3.11+  
**Principais Dependências**: FastAPI (backend), Bootstrap 5 (frontend), SQLite (database)  
**Armazenamento**: SQLite 3 com tabelas para ativos e tipos  
**Testes**: pytest (unitários e integração)  
**Plataforma Alvo**: Aplicação web (navegador + servidor Python)  
**Tipo de Projeto**: web-service (full-stack)  
**Metas de Performance**: <200ms para requisições I/O, suportar 100+ ativos simultâneos  
**Restrições**: Sem autenticação inicial (acesso admin livre), dados persistem em arquivo `.db`  
**Escopo/Scale**: MVP com 3 tipos principais (Notebook, Mouse, Projetor), ~10 campos por ativo

## Verificação de Constituição

✅ **Simples e escalável**: Estrutura com backend/frontend separados  
✅ **Banco de dados apropriado**: SQLite para persistência local  
✅ **Sem over-engineering**: Sem padrões Repository/DDD inicialmente  
✅ **Alinhado com constituição**: FastAPI + Bootstrap 5 conforme especificado

## Estrutura do Projeto

### Documentação

```text
docs/
├── specs/
│   ├── constitution.md              # Constituição do projeto
│   └── feature-cadastro-ativos.md   # Especificação desta feature
└── plans/
    └── plan-001-cadastro-ativos.md  # Este arquivo
```

### Código-fonte

```text
backend/
├── main.py              # Aplicação FastAPI principal
├── models.py            # Modelos de dados (Ativo, Tipo, Enum Status)
├── database.py          # Inicialização SQLite e schemas
├── routes/
│   └── ativos.py        # Endpoints para ativos (/api/ativos)
├── requirements.txt     # Dependências Python
└── tests/
    ├── test_models.py
    ├── test_database.py
    └── test_routes.py

frontend/
├── index.html           # Página principal com lista de ativos
├── cadastro.html        # Formulário de cadastro/edição
├── css/
│   └── style.css        # Estilos Bootstrap customizado
├── js/
│   ├── cadastro.js      # Lógica do formulário (validação, POST)
│   └── lista.js         # Lógica da listagem (busca, filtros, detalhes)
└── assets/
    └── ícones.html      # Bootstrap Icons SVG inline

data.db                 # SQLite (será criado na primeira execução)
```

**Decisão de Estrutura**: Arquitetura monolítica simples com FastAPI backend servindo HTML/JS estático. Uma única instância SQLite compartilhada para MVP. Sem Docker inicial.

## Fases de Implementação

### Fase 1: Database & Backend API (MVP Core - P1)

**Objetivos**: 
- Modelos de dados funcionais
- Endpoints básicos CRUD para ativos
- Validações de negócio

**Tasks**:
- [ ] Criar `backend/models.py` com models Ativo, TipoAtivo, StatusAtivo
- [ ] Implementar `backend/database.py` com SQLite setup e schemas
- [ ] Criar `backend/main.py` com configuração FastAPI
- [ ] Implementar `backend/routes/ativos.py`:
  - [ ] POST `/api/ativos` - Criar ativo (validar série única, data válida)
  - [ ] GET `/api/ativos` - Listar com paginação
  - [ ] GET `/api/ativos/<id>` - Detalhes de um ativo
  - [ ] PUT `/api/ativos/<id>` - Atualizar ativo (P3)
  - [ ] DELETE `/api/ativos/<id>` - Soft delete (status = Inativo)
- [ ] Testes unitários para models (`tests/test_models.py`)
- [ ] Testes integração para API (`tests/test_routes.py`)
- [ ] `requirements.txt` com FastAPI, SQLAlchemy, pytest
- [ ] Documentação Swagger automática (FastAPI padrão)

**Critérios de Aceitação**:
- POST /api/ativos com série única retorna 201 e ID
- POST /api/ativos com série duplicada retorna 400
- GET /api/ativos retorna lista paginada
- Testes passam com >80% cobertura

### Fase 2: Frontend Interface (MVP UI - P1)

**Objetivos**:
- Interface responsiva com Bootstrap 5
- Integração com API
- Feedback claro ao usuário

**Tasks**:
- [ ] Criar `frontend/index.html` - Página lista de ativos
  - [ ] Tabela com colunas: descrição, tipo, série, status, localização
  - [ ] Filtros por tipo e status (dropdowns)
  - [ ] Busca por série/descrição
  - [ ] Badges coloridas para status
  - [ ] Botão "Novo Ativo" + "Detalhes"
- [ ] Criar `frontend/cadastro.html` - Formulário de cadastro
  - [ ] Form com campos: descrição, tipo, série, MAC, valor, data, localização
  - [ ] Validação client-side (série obrigatória, data não-futura)
  - [ ] Submit com feedback (loading, erro, sucesso)
  - [ ] Botão de voltar/cancelar
- [ ] Criar `frontend/js/cadastro.js`
  - [ ] Listener submit do form
  - [ ] Fetch POST para /api/ativos
  - [ ] Exibir mensagens de sucesso/erro com toast/alert
  - [ ] Redirecionar para lista após sucesso
- [ ] Criar `frontend/js/lista.js`
  - [ ] Fetch GET /api/ativos na carga da página
  - [ ] Renderizar tabela dinamicamente
  - [ ] Filtros e busca (client-side ou server-side)
  - [ ] Modal/card de detalhes ao clicar em item
- [ ] `frontend/css/style.css`
  - [ ] Customizações Bootstrap (cores, espaços)
  - [ ] Responsividade mobile (tabela scrollável em mobile)
  - [ ] Tema consistente com badges de status

**Critérios de Aceitação**:
- Página lista carrega com 10+ ativos em <1s
- Formulário cadastro funciona end-to-end
- Validações exibem mensagens em português
- Responsivo em mobile (viewport <600px)

### Fase 3: Polish & Testes Completos (Nice-to-have - P2/P3)

**Tasks**:
- [ ] Testes E2E com Selenium ou Playwright
- [ ] Tratamento de edge cases (caracteres especiais em série, valores muito grandes)
- [ ] Performance: lazy-load em listas grandes
- [ ] Edição de ativos (form edit) - P3
- [ ] Confirmação antes de soft-delete - P2
- [ ] Ícones com Bootstrap Icons
- [ ] Dark mode (opcional com CSS variables)
- [ ] Logs e auditoria básica
- [ ] Documentação de API no Swagger

## Dependências Externas

```
[FastAPI]
fastapi==0.109.2
uvicorn==0.27.0
sqlalchemy==2.0.27
pydantic==2.6.3

[Testing]
pytest==7.4.4
pytest-cov==4.1.0
httpx==0.26.0

[Database]
# SQLite vem com Python

[Frontend]
# Apenas HTML/CSS/JS vanilla + Bootstrap CDN
```

## Sequência de Desenvolvimento Recomendada

1. Setup rápido: modelos + database
2. Endpoints básicos GET/POST
3. Testes para validar (TDD)
4. Frontend lista (GET)
5. Frontend cadastro (POST)
6. Integração end-to-end
7. Polish e refinamento

## Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Série duplicada em race condition | Médio | Validar no banco (unique constraint) |
| Usuário perde formulário ao erro | Alto | Salvar em localStorage antes de submit |
| Banco cresce muito (1000+ ativos) | Baixo (MVP) | Implementar índices e paginação |
| Validação client diferente de server | Médio | Compartilhar lógica ou duplicar redundantemente |

## Métricas de Sucesso

- ✅ MVP completo em <2 semanas (Fase 1+2)
- ✅ Cobertura de testes >70%
- ✅ Tempo resposta <200ms para 100 ativos
- ✅ Admin consegue cadastrar ativo em <2 min
- ✅ Zero regressões após refactor
