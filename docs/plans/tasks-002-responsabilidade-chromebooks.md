# Tasks: Responsabilidade de Chromebooks

**Input**: Design documents from [plan-002-responsabilidade-chromebooks.md](plan-002-responsabilidade-chromebooks.md), [feature-responsabilidade-chromebooks.md](../specs/feature-responsabilidade-chromebooks.md)  
**Pré-requisitos**: Fase 2 (Foundational) do projeto já completa ✅

**Testes**: Inclusos por Story (pytest - unit + integration)

**Organização**: Tasks agrupadas por User Story (US1, US2, US3) + por Fase (Backend, Frontend, Testes)

---

## Formato: `[ID] [P] [Story] Descrição`

- **[P]**: Pode rodar em paralelo (arquivos diferentes, sem dependências)
- **[Story]**: Qual user story (US1=Cadastro, US2=Cronograma, US3=Devolução)
- Status: Checkbox para rastreamento

---

## Fase 1: Setup & Models (Infraestrutura Compartilhada)

**Objetivo**: Adição de modelos e estrutura para nova feature

- [ ] T101 Atualizar `backend/models.py` - Adicionar modelo `Professor`:
  - [ ] T101.1 Campos: `id` (PK), `nome` (String 255, unique), `email` (String 255, nullable), `criado_em` (DateTime)
  - [ ] T101.2 Validação: nome não pode ser vazio
  - [ ] T101.3 Método `__repr__` para debug

- [ ] T102 Atualizar `backend/models.py` - Adicionar modelo `ResponsabilidadeChromebook`:
  - [ ] T102.1 Campos: `id` (PK), `professor_id` (FK → Professor), `data` (Date), `periodo_turma` (String 10, ex: "1ºA"), `quantidade_chromebooks` (Integer > 0), `status` (Enum), `observacoes` (String 500, nullable), `criado_em`, `atualizado_em`
  - [ ] T102.2 Enum `StatusResponsabilidade`: "Pendente", "Devolvido", "Com falta", "Não realizado"
  - [ ] T102.3 Relacionamento: ResponsabilidadeChromebook → Professor (FK)
  - [ ] T102.4 Index em (professor_id, data) para queries rápidas
  - [ ] T102.5 Método `__repr__` para debug

- [ ] T103 [P] Atualizar `backend/schemas.py` - Adicionar Pydantic schemas:
  - [ ] T103.1 `ProfessorCreate` (nome, email: Optional)
  - [ ] T103.2 `ProfessorResponse` (id, nome, email, criado_em)
  - [ ] T103.3 `ResponsabilidadeCreate` (professor_id, data, periodo_turma, quantidade_chromebooks, observacoes: Optional)
  - [ ] T103.4 `ResponsabilidadeResponse` (id, professor_id, data, periodo_turma, quantidade_chromebooks, status, observacoes, criado_em, atualizado_em)
  - [ ] T103.5 `ResponsabilidadeUpdate` (status, observacoes) [para PUT]

- [ ] T104 Criar `backend/routes/responsabilidades.py` (arquivo vazio, será preenchido em T2)

**Checkpoint**: Modelos prontos, schemas validam, pronto para endpoints

---

## Fase 2: User Story 1 - Admin registra responsabilidade (Priority: P1) 🎯 MVP

**Goal**: Administrador consegue criar registro de responsabilidade com validações

**Independent Test**: POST /api/responsabilidades com dados válidos retorna 201. POST com quantidade 0 retorna 400.

### Testes para User Story 1 (Write tests FIRST)

- [ ] T105 [P] [US1] Unit test em `backend/tests/test_models.py`:
  - Modelo Professor pode ser criado e recuperado
  - Modelo ResponsabilidadeChromebook valida quantidade > 0
  - Status enum funciona
  - Data é persistida corretamente (formato date)

- [ ] T106 [P] [US1] Integration test em `backend/tests/test_responsabilidades.py`:
  - POST /api/responsabilidades com dados válidos → 201, retorna id + data
  - POST sem professor_id → 400 "Professor é obrigatório"
  - POST com quantidade 0 → 400 "Quantidade deve ser maior que zero"
  - POST com quantidade negativa → 400
  - POST com periodo_turma inválido (ex: "10ºA") → 400 OU warning
  - POST com professor_id inexistente → 404 OU 400
  - POST com data no futuro → aceita OU avisa (spec não proíbe)

### Implementação para User Story 1

- [ ] T107 [P] [US1] Backend - Criar endpoint POST /api/professores (pré-requisito):
  - Recebe: `ProfessorCreate` (nome, email)
  - Valida: nome não vazio, email formato válido (se preenchido)
  - Retorna: 201 `ProfessorResponse`
  - Erro: 400 bad request com mensagem clara

- [ ] T108 [P] [US1] Backend - Criar endpoint GET /api/professores:
  - Lista todos os professores
  - Retorna: 200 list[`ProfessorResponse`]
  - Sem paginação (MVP)

- [ ] T109 [US1] Backend - Criar endpoint POST /api/responsabilidades:
  - Recebe: `ResponsabilidadeCreate`
  - Valida:
    - [ ] T109.1 professor_id existe no banco
    - [ ] T109.2 quantidade > 0
    - [ ] T109.3 data é válida (formato YYYY-MM-DD)
    - [ ] T109.4 periodo_turma está em lista permitida (1ºA, 2ºA, 2ºB, 3ºA, 3ºB, 3ºC, 4ºA, 4ºB, 4ºC, 5ºA, 5ºB, 5ºC) OU permite qualquer string
    - [ ] T109.5 No mesmo dia/período, máximo 1 professor responsável (OU permite múltiplos - spec não define)
  - Retorna: 201 `ResponsabilidadeResponse` com id gerado
  - Erro: 400 com descrição do campo inválido

- [ ] T110 [P] [US1] Backend - Criar endpoint GET /api/responsabilidades (com filtros):
  - Parâmetros: `?professor_id=X&data_inicio=YYYY-MM-DD&data_fim=YYYY-MM-DD&periodo_turma=1ºA`
  - Retorna: 200 list[`ResponsabilidadeResponse`]
  - Sem paginação (MVP)

- [ ] T111 [P] [US1] Backend - Integrar rotas em `backend/main.py`:
  - Imports de `routes/responsabilidades`
  - incluir router com prefixo `/api`

- [ ] T112 Backend - Criar/populat dados iniciais em `backend/seed.py`:
  - [ ] T112.1 Função para carregar lista de professores padrão (ex: from cronograma)
  - [ ] T112.2 Função para popular alguns registros de exemplo
  - [ ] T112.3 Comando ou script para rodar seed (opcional: rodar automaticamente na primeira execução)

### Frontend para User Story 1 (MVCs are UI-last)

- [ ] T113 [P] [US1] Criar `frontend/responsabilidade-form.html`:
  - Form com campos: Professor (select), Data (input date), Período (select com turmas), Quantidade (input number), Observações (textarea)
  - Botão: Salvar, Limpar, Voltar
  - Integrar Bootstrap 5
  - Seguir padrão visual do projeto

- [ ] T114 [P] [US1] Criar `frontend/js/responsabilidade.js`:
  - [ ] T114.1 Ao carregar página: GET /api/professores e preencher select
  - [ ] T114.2 Validação cliente (antes de POST):
    - Professor selecionado ✓
    - Data preenchida e válida ✓
    - Período preenchido ✓
    - Quantidade > 0 ✓
  - [ ] T114.3 Ao enviar: POST /api/responsabilidades com dados do formulário
  - [ ] T114.4 Sucesso: toast/alert "Responsabilidade registrada com sucesso" → redirect cronograma.html
  - [ ] T114.5 Erro: exibir mensagem do servidor em alert/card vermelho
  - [ ] T114.6 Loader/disabled button enquanto aguarda resposta

- [ ] T115 [P] [US1] Atualizar `frontend/index.html`:
  - Adicionar link no menu: "Responsabilidades" com submenu "Nova Responsabilidade"
  - Link aponta para `responsabilidade-form.html`
  - Manter padrão visual existente

**Checkpoint**: Can create responsibilities, see them in API

---

## Fase 3: User Story 2 - Admin visualiza cronograma (Priority: P2)

**Goal**: Administrador consegue ver cronograma com responsabilidades em tabela/calendário

**Independent Test**: GET /api/responsabilidades retorna lista formatada. Frontend renderiza cronograma.

### Backend para User Story 2 (Estende US1)

- [ ] T116 [P] [US2] Backend - Criar endpoint GET /api/cronograma (otimizado para UI):
  - Parâmetro: `?mes=03&ano=2026` (busca por mês)
  - Retorna: Estrutura preparada para calendário/tabela:
    ```json
    {
      "mes": 3,
      "ano": 2026,
      "dias": [
        {
          "data": "2026-03-02",
          "dia_semana": "SEGUNDA",
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
  - Retorna: 200 com estrutura pronta para renderizar

- [ ] T117 [P] [US2] Backend - Criar endpoint GET /api/responsabilidades/por-data (agrupado):
  - Agrupa responsabilidades por data dentro de um período
  - Útil para gerar relatórios/tabelas

### Frontend para User Story 2

- [ ] T118 [US2] Criar `frontend/cronograma.html`:
  - Estrutura: Tabela ou Calendário com responsabilidades
  - Colunas: Data | Período | Professor | Quantidade | Status | Ações
  - Filtros: Select professor, Select mês/ano
  - Novo botão: "+ Nova Responsabilidade" → responsabilidade-form.html
  - Integrar Bootstrap 5, badges coloridas por status

- [ ] T119 [US2] Criar `frontend/js/cronograma.js`:
  - [ ] T119.1 Ao carregar: GET /api/cronograma?mes=ATUAL&ano=ATUAL
  - [ ] T119.2 GET /api/professores para popular filtro professor
  - [ ] T119.3 Renderizar tabela dinamicamente com dados do servidor
  - [ ] T119.4 Clique em linha → modal com detalhes + opção editar status
  - [ ] T119.5 Filtro professor: refaz GET com ?professor_id=X&mes=...
  - [ ] T119.6 Filtro mês: refaz GET com novo mês
  - [ ] T119.7 Badge colorida: Pendente=azul, Devolvido=verde, Com falta=vermelho, Não realizado=cinza

- [ ] T120 [P] [US2] Adicionar estilos em `frontend/css/style.css`:
  - [ ] T120.1 Badges por status (cores da spec)
  - [ ] T120.2 Tabela responsiva (mobile friendly)
  - [ ] T120.3 Highlight linha ao hover
  - [ ] T120.4 Layout modal para detalhes

- [ ] T121 [P] [US2] Atualizar `frontend/index.html`:
  - Adicionar link no menu: "Cronograma de Responsabilidades" → cronograma.html

**Checkpoint**: Can view responsibilities in calendar/table, filter by professor/month

---

## Fase 4: User Story 3 - Registrar devolução/falta (Priority: P3) ⭐ Optional MVP

**Goal**: Administrador marca responsabilidade como encerrada (devolvido/com falta)

**Independent Test**: PUT /api/responsabilidades/{id} atualiza status. Frontend modal permite editar.

### Backend para User Story 3

- [ ] T122 [US3] Backend - Criar endpoint PUT /api/responsabilidades/{id}:
  - Recebe: `ResponsabilidadeUpdate` (status, observacoes)
  - Valida: id existe, status é válido
  - Retorna: 200 `ResponsabilidadeResponse` atualizado
  - Erro: 404 se id inexistente, 400 se status inválido

- [ ] T123 [P] [US3] Backend - Criar endpoint GET /api/responsabilidades/{id}:
  - Retorna: 200 `ResponsabilidadeResponse` com detalhe completo

- [ ] T124 [P] [US3] Testes em `backend/tests/test_responsabilidades.py`:
  - PUT /api/responsabilidades/{id} com status válido → 200
  - PUT com status inválido → 400
  - PUT {id} inexistente → 404

### Frontend para User Story 3

- [ ] T125 [US3] Atualizar `frontend/js/cronograma.js`:
  - Modal ao clicar em responsabilidade mostra:
    - Detalhes: Professor, Data, Período, Quantidade
    - Dropdown de status (Pendente, Devolvido, Com falta, Não realizado)
    - Textarea para observações
    - Botão: Salvar mudanças
  - PUT /api/responsabilidades/{id} ao salvar
  - Sucesso: atualiza linha na tabela, fecha modal
  - Erro: exibe mensagem

- [ ] T126 [P] [US3] Atualizar `frontend/css/style.css`:
  - Estilos do modal de edição

**Checkpoint**: Can edit responsibility status after creation

---

## Fase 5: Validação & Testes Completos

- [ ] T127 Executar todos os testes:
  - `pytest backend/tests/ -v --cov`
  - Cobertura mínima 70%

- [ ] T128 [P] Simulated manual testing:
  - [ ] T128.1 Criar 3 professores via form
  - [ ] T128.2 Criar 5 responsabilidades em datas diferentes
  - [ ] T128.3 Visualizar cronograma
  - [ ] T128.4 Filtrar por professor
  - [ ] T128.5 Editar status de 1 responsabilidade
  - [ ] T128.6 Validar que erros são exibidos (qtd 0, professor inválido)
  - [ ] T128.7 Testar em mobile (responsivo)

- [ ] T129 [P] Validação com spec:
  - [ ] T129.1 Todos os acceptance scenarios da spec foram validados?
  - [ ] T129.2 Edge cases tratados?
  - [ ] T129.3 Mensagens em português?

**Checkpoint**: Feature de responsabilidade completa e testada ✅

---

## Fase 6: Documentação & Polish (Final)

- [ ] T130 [P] Atualizar `README.md`:
  - Adicionar seção sobre nova feature
  - Instruções para popular arquivo de professores
  - Screenshot ou GIF do cronograma

- [ ] T131 [P] Atualizar `backend/requirements.txt`:
  - Confirmar que todas as dependências estão listadas

- [ ] T132 Revisar código:
  - [ ] T132.1 Sem console.log desnecessários no JS
  - [ ] T132.2 Sem print() de debug no Python
  - [ ] T132.3 Boas práticas (nomes de variáveis, comentários úteis)

**Checkpoint**: Feature pronta para produção 🚀

---

## Resumo de Dependências

```
Fase 1 (Models)
    ↓
T105-T106 (Testes) & T107-T112 (Backend) [paralelo]
    ↓
T113-T115 (Frontend US1) [após backend pronto]
    ↓
T116-T121 (Frontend US2 cronograma) [paralelo]
    ↓
T122-T126 (US3 edição) [opcional]
    ↓
T127-T132 (Testes + Polish)
```

---

## Critérios de Aceitar (Done - Feature Completa)

- [ ] Todos os tests passam
- [ ] POST /api/responsabilidades funciona com validações
- [ ] GET /api/responsabilidades com filtros funciona
- [ ] Cronograma exibe responsabilidades corretamente
- [ ] Frontend valida formulário
- [ ] Sem erros JavaScript no console
- [ ] Sem erros Python no logs
- [ ] Mobile responsivo (testar em celular ou DevTools mobile)
- [ ] Mensagens de erro em português
- [ ] Readme atualizado
