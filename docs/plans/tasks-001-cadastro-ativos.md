# Tasks: Cadastro de Ativos

**Input**: Design documents from planos e specs  
**Pré-requisitos**: [plan-001-cadastro-ativos.md](plan-001-cadastro-ativos.md) ✅, [feature-cadastro-ativos.md](../specs/feature-cadastro-ativos.md) ✅

**Testes**: Inclusos por story (pytest - unit + integration)

**Organização**: Tasks agrupadas por User Story (US1, US2, US3) para permitir implementação e testes independentes

---

## Formato: `[ID] [P] [Story] Descrição`

- **[P]**: Pode rodar em paralelo (arquivos diferentes, sem dependências)
- **[Story]**: Qual user story (US1=Cadastro, US2=Listagem, US3=Edição)
- Caminhos exatos: `backend/` e `frontend/` conforme plano

---

## Fase 1: Setup (Infraestrutura Compartilhada)

**Objetivo**: Inicialização do projeto e estrutura básica

- [ ] T001 Criar estrutura de diretórios: `backend/`, `frontend/`, conforme plano
- [ ] T002 Criar `backend/requirements.txt` com FastAPI, SQLAlchemy, Pydantic, pytest
- [ ] T003 [P] Criar `backend/.env.example` com variáveis (DB_PATH, LOG_LEVEL, etc)
- [ ] T004 [P] Criar `frontend/index.html` (template vazio com Bootstrap 5 CDN)
- [ ] T005 [P] Criar `backend/main.py` com FastAPI app base
- [ ] T006 Configurar `.gitignore` com `*.db`, `__pycache__/`, `.venv/`, `.env`

---

## Fase 2: Foundational (Pré-requisito Crítico)

**Objetivo**: Infraestrutura core que DEVE estar pronta antes de qualquer User Story

⚠️ **CRÍTICO**: Nenhuma story pode começar até esta fase estar 100% completa

- [ ] T007 Criar `backend/database.py` com SQLite init + session factory
- [ ] T008 [P] Criar `backend/models.py` com:
  - [ ] T008.1 Model `Ativo` (id, descricao, tipo, numero_serie, mac_address, valor_estimado, data_aquisicao, status, localizacao, criado_em, atualizado_em)
  - [ ] T008.2 Model `TipoAtivo` (id, nome, descricao)
  - [ ] T008.3 Enum `StatusAtivo` (Disponível, Emprestado, Danificado, Inativo)
  - [ ] T008.4 Relacionamento: Ativo → TipoAtivo (FK)
- [ ] T009 [P] Criar `backend/schemas.py` com Pydantic schemas:
  - [ ] T009.1 `AtivoCreate` (descricao, tipo_id, numero_serie, mac_address, valor_estimado, data_aquisicao, localizacao)
  - [ ] T009.2 `AtivoResponse` (id, descricao, tipo, numero_serie, status, localizacao, criado_em)
  - [ ] T009.3 `AtivoUpdate` (descricao, localizacao, status) [para P3]
- [ ] T010 Implementar `backend/main.py` com:
  - [ ] T010.1 Criar database na primeira execução
  - [ ] T010.2 Registrar routers
  - [ ] T010.3 Configurar CORS para frontend
  - [ ] T010.4 Definir /docs (Swagger automático)
- [ ] T011 [P] Implementar `backend/routes/__init__.py` (arquivo vazio)

**Checkpoint**: Fundação pronta - User Stories podem implementar em paralelo

---

## Fase 3: User Story 1 - Admin cadastra novo ativo (Priority: P1) 🎯 MVP

**Goal**: Administrador consegue submeter formulário e sistema valida + persiste novo ativo

**Independent Test**: POST /api/ativos com dados válidos retorna 201 + ID. POST com série duplicada retorna 400 com mensagem clara.

### Testes para User Story 1 (TDD - Write FIRST, see them FAIL)

- [ ] T012 [P] [US1] Unit test para modelo `Ativo` em `backend/tests/test_models.py`
  - Validar que Ativo com mesma série não pode ser criado (unique constraint)
  - Validar que data_aquisicao não pode ser no futuro
  - Validar campos obrigatórios
- [ ] T013 [P] [US1] Integration test para POST /api/ativos em `backend/tests/test_ativos_create.py`
  - POST com dados válidos → 201, retorna id gerado
  - POST sem numero_serie → 400 com mensagem "Número de série é obrigatório"
  - POST com numero_serie duplicado → 400 com mensagem clara
  - POST com data no futuro → 400 com mensagem "Data não pode ser no futuro"
  - POST com valor negativo → 400 com mensagem "Valor deve ser positivo"

### Implementação para User Story 1

- [ ] T014 [US1] Criar `backend/routes/ativos.py` com endpoint POST /api/ativos
- [ ] T015 [US1] Implementar validação em `backend/routes/ativos.py`:
  - [ ] T015.1 Verificar numero_serie único (query DB antes de inserir)
  - [ ] T015.2 Verificar data_aquisicao ≤ hoje
  - [ ] T015.3 Verificar valor_estimado ≥ 0
  - [ ] T015.4 Retornar erros formatados em português: `{"error": "mensagem", "field": "campo"}`
- [ ] T016 [US1] Implementar resposta JSON sucesso: `{"success": true, "id": 123, "message": "Ativo cadastrado com sucesso"}`
- [ ] T017 [US1] Adicionar logging com timestamp para POST /api/ativos em `backend/main.py`
- [ ] T018 [US1] Criar `frontend/cadastro.html` com formulário Bootstrap 5:
  - Campos: descrição, tipo (select/dropdown), série, MAC, valor, data, localização
  - Validação HTML5 (required, type="number", type="date", etc)
  - Botão Salvar + Limpar
- [ ] T019 [US1] Criar `frontend/js/cadastro.js`:
  - [ ] T019.1 Event listener no submit do form
  - [ ] T019.2 Validação client-side (série obrigatória, valor positivo)
  - [ ] T019.3 Fetch POST para http://localhost:8000/api/ativos
  - [ ] T019.4 Exibir alert/toast de sucesso (vermelho/verde)
  - [ ] T019.5 Redirecionar para index.html após sucesso
  - [ ] T019.6 Exibir mensagem de erro se POST falhar (stderr em português)
- [ ] T020 [US1] Criar link "Novo Ativo" em `frontend/index.html` apontando para cadastro.html

**Checkpoint**: User Story 1 funcional ponta-a-ponta. Admin consegue cadastrar ativo.

---

## Fase 4: User Story 2 - Admin visualiza lista de ativos (Priority: P2)

**Goal**: Admin consegue ver todos os ativos em tabela com filtros e busca

**Independent Test**: GET /api/ativos retorna lista. Tabela renderiza 10+ ativos em <1s. Filtro por tipo funciona.

### Testes para User Story 2

- [ ] T021 [P] [US2] Integration test para GET /api/ativos em `backend/tests/test_ativos_list.py`
  - GET /api/ativos com 0 ativos → 200, retorna lista vazia `[]`
  - GET /api/ativos com 10 ativos → 200, retorna 10 items
  - GET /api/ativos?tipo=Notebook → 200, filtra por tipo_id
  - GET /api/ativos?search=SN-123 → 200, busca em numero_serie e descricao
  - GET /api/ativos?skip=0&limit=5 → 200, retorna 5 items (paginação)
- [ ] T022 [P] [US2] Performance test: 100 ativos carregam em <1s

### Implementação para User Story 2

- [ ] T023 [US2] Implementar GET /api/ativos em `backend/routes/ativos.py`:
  - [ ] T023.1 Query all ativos com paginação (skip, limit)
  - [ ] T023.2 Filtro por tipo_id opcional
  - [ ] T023.3 Busca por numero_serie ou descricao (LIKE)
  - [ ] T023.4 Retornar lista de `AtivoResponse` (sem campos sensíveis)
  - [ ] T023.5 Incluir total count na resposta: `{"items": [...], "total": 25, "skip": 0, "limit": 10}`
- [ ] T024 [P] [US2] Implementar GET /api/tipos em `backend/routes/ativos.py` (lista de tipos para dropdown)
  - Retornar: `[{id: 1, nome: "Notebook"}, ...]`
- [ ] T025 [US2] Criar `frontend/js/lista.js`:
  - [ ] T025.1 Fetch GET /api/ativos na carga da página
  - [ ] T025.2 Renderizar tabela HTML dinamicamente com:
    - Colunas: Descrição, Tipo, Série, Status, Localização, Ações
    - Badge colorida para status (verde=Disponível, amarelo=Emprestado, vermelho=Danificado, cinza=Inativo)
  - [ ] T025.3 Implementar filtro por tipo (dropdown → GET com ?tipo=X)
  - [ ] T025.4 Implementar busca (input text → GET com ?search=X)
  - [ ] T025.5 Paginação com botões Anterior/Próxima
- [ ] T026 [US2] Criar modal/card de detalhes ao clicar em ativo:
  - Se clica em linha → mostra modal com todos os campos
  - Botão fechar modal
- [ ] T027 [US2] Criar `frontend/index.html` definitivo:
  - Navbar com title "Inventário de Ativos"
  - Botão "Novo Ativo" → cadastro.html
  - Tabela com filtros (tipo dropdown, busca input)
  - Loader enquanto fetcha dados
- [ ] T028 [P] [US2] Criar `frontend/css/style.css`:
  - Customizar cores Bootstrap (primária, badges)
  - Responsividade mobile (tabela scrollável em <600px)
  - Cores badges: #28a745 (verde), #ffc107 (amarelo), #dc3545 (vermelho), #6c757d (cinza)

**Checkpoint**: User Story 2 funcional. Admin consegue listar e buscar ativos.

---

## Fase 5: User Story 3 - Admin atualiza ativo existente (Priority: P3)

**Goal**: Admin consegue editar localizacao/status de ativo após cadastro

**Independent Test**: PUT /api/ativos/<id> com dados novos persiste. Interface permite edit.

### Testes para User Story 3

- [ ] T029 [P] [US3] Integration test para PUT /api/ativos/<id> em `backend/tests/test_ativos_update.py`
  - PUT /api/ativos/1 com novo status → 200, atualiza
  - PUT /api/ativos/999 → 404 "Ativo não encontrado"
  - PUT sem permissão (depois de autenticação) → 403

### Implementação para User Story 3

- [ ] T030 [US3] Implementar GET /api/ativos/<id> em `backend/routes/ativos.py`:
  - Retorna 200 com ativo completo, ou 404 se não existe
- [ ] T031 [US3] Implementar PUT /api/ativos/<id> em `backend/routes/ativos.py`:
  - [ ] T031.1 Aceita esquema `AtivoUpdate` (descricao, localizacao, status)
  - [ ] T031.2 Valida status é um dos valores do Enum
  - [ ] T031.3 Retorna ativo atualizado em 200
- [ ] T032 [P] [US3] Criar form de edição em `frontend/cadastro.html`:
  - Se URL tem ?id=123 → preenche form com dados atuais
  - Modo "edit" vs "create"
- [ ] T033 [US3] Adicionar botão "Editar" em cada linha da tabela (lista.js):
  - Clica → redireciona para cadastro.html?id=123
- [ ] T034 [US3] Adicionar botão "Soft Delete" (marca como Inativo):
  - Clica → call PUT /api/ativos/<id> com status=Inativo
  - Pede confirmação antes

**Checkpoint**: User Story 3 funcional. Admin consegue editar e marcar como inativo.

---

## Fase 6: Polish & Quality

- [ ] T035 [P] Verificar cobertura de testes: `pytest --cov=backend tests/`
  - Alvo: >70% cobertura
- [ ] T036 [P] Verificar linting: `ruff check backend/ frontend/`
- [ ] T037 Testes manuais E2E:
  - [ ] T037.1 Cadastrar 5 ativos com tipos diferentes
  - [ ] T037.2 Listar, buscar, filtrar
  - [ ] T037.3 Editar localização
  - [ ] T037.4 Marcar como inativo (não deleta)
- [ ] T038 Documentação:
  - [ ] T038.1 README.md com setup instructions
  - [ ] T038.2 Acessível em /docs (Swagger FastAPI)
  - [ ] T038.3 Comentários em código complexo

---

## Execução Recomendada

**Sequência crítica:**
1. Fase 1 (Setup) - sem parallelizar
2. Fase 2 (Foundation) - T007-T011
3. Fase 3 (US1) - T012-T020 (escreva testes PRIMEIRO)
4. Fase 4 (US2) - T021-T028 (parallelizável com US1)
5. Fase 5 (US3) - T029-T034 (baixa prioridade, pode ficar para depois)
6. Fase 6 (Polish)

**Tempo estimado:**
- Fase 1-2: 1-2 horas
- Fase 3: 3-4 horas (com testes)
- Fase 4: 3-4 horas  
- Fase 5: 1-2 horas
- Fase 6: 1 hora
- **Total: 9-13 horas para MVP completo**

---

## Status de Conclusão

- [ ] Fase 1: Setup
- [ ] Fase 2: Foundation
- [ ] Fase 3: US1 (Cadastro) ← **COMEÇAR AQUI**
- [ ] Fase 4: US2 (Listagem)
- [ ] Fase 5: US3 (Edição)
- [ ] Fase 6: Polish
