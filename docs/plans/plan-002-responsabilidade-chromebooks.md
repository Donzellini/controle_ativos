# Plano de Implementação: Responsabilidade de Chromebooks

**Branch**: `002-responsabilidade-chromebooks` | **Data**: 2026-03-29 | **Spec**: [feature-responsabilidade-chromebooks.md](../specs/feature-responsabilidade-chromebooks.md)

## Resumo

Sistema para registrar e acompanhar a responsabilidade de Chromebooks por professores em cronogramas de períodos. Administradores registram qual professora é responsável por quantos Chromebooks em qual data/período. O sistema permite visualizar cronograma, filtrar por professor e registrar devoluções/faltas.

## Contexto Técnico

**Linguagem/Versão**: Python 3.11+ (igual ao projeto existente)  
**Stack**: FastAPI + SQLite (integrado ao projeto existente)  
**Armazenamento**: Tabelas novas em SQLite: `professor`, `responsabilidade_chromebook`  
**Testes**: pytest (unitários e integração)  
**Plataforma Alvo**: Extensão da aplicação web existente  
**Tipo de Projeto**: web-service (adiciona funcionalidade ao full-stack existente)  
**Metas de Performance**: <200ms para requisições, suportar cronograma anual (~250 registros/ano)  
**Restrições**: Sem autenticação inicial  
**Escopo**: MVP com CRUD básico + cronograma visual

## Verificação de Constituição

✅ **Alinhado com arquitetura**: Estende modelos/rotas existentes  
✅ **Banco de dados**: Novas tabelas em SQLite existente  
✅ **Modularidade**: Rotas isoladas em novo arquivo `routes/responsabilidades.py`  
✅ **Interface**: Segue padrão existente (cards, bootstrap, favicon colorido)

## Estrutura de Mudanças

### Novo Backend

```text
backend/
├── models.py                    # ADIÇÃO: Modelos Professor e ResponsabilidadeChromebook
├── routes/
│   ├── ativos.py               # existente
│   └── responsabilidades.py    # NOVO: Endpoints para responsabilidade
├── tests/
│   ├── test_models.py          # ADIÇÃO: testes para Professor
│   └── test_responsabilidades.py # NOVO: testes endpoints responsabilidade
└── seed.py                      # ADIÇÃO: seed com dados do cronograma

data.db                         # ADIÇÃO: novas tabelas
```

### Novo Frontend

```text
frontend/
├── cronograma.html             # NOVO: calendário/tabela de responsabilidades
├── responsabilidade-form.html  # NOVO: formulário registrar responsabilidade
├── js/
│   ├── cronograma.js           # NOVO: lógica de visualização cronograma
│   └── responsabilidade.js     # NOVO: lógica do formulário
└── css/
    └── style.css               # ADIÇÃO: estilos para cronograma
```

## Fases de Implementação

### Fase 1: Database & Backend API (P1 - Core)

**Objetivos**: 
- Criar tabelas: `professor` e `responsabilidade_chromebook`
- Implementar modelos Pydantic/SQLAlchemy
- Endpoints CRUD para responsabilidades

**Tarefas**:

1. **Criar modelo Professor**
   - Campos: `id`, `nome`, `email` (opcional), `criado_em`
   - Sem relationship complexa (é simples lista de professores)

2. **Criar modelo ResponsabilidadeChromebook**
   - Campos: `id`, `professor_id` (FK), `data`, `periodo_turma`, `quantidade_chromebooks`, `status` (Enum), `observacoes`, `criado_em`, `atualizado_em`
   - Status Enum: "Pendente", "Devolvido", "Com falta", "Não realizado"

3. **Implementar endpoints em `routes/responsabilidades.py`**
   ```
   POST   /api/responsabilidades         # Criar novo registro
   GET    /api/responsabilidades         # Listar (com filtros: professor, data, período)
   GET    /api/responsabilidades/{id}   # Obter detalhe
   PUT    /api/responsabilidades/{id}   # Atualizar status/observações
   DELETE /api/responsabilidades/{id}   # Deletar (soft delete ou hard)
   GET    /api/cronograma/março          # Listagem por mês format. para calendário
   ```

4. **Validações de Negócio**
   - Quantidade > 0
   - Data válida
   - Professor existe
   - Período válido (1ºA, 2ºB, 3ºC, 4ºA, 4ºB, 4ºC, 5ºA, 5ºB, 5ºC - conforme cronograma PDF)

5. **Seed de dados iniciais**
   - Arquivo `seed.py` carrega professores do cronograma
   - Pode Popular alguns registros de exemplo baseado em cronograma

### Fase 2: Frontend - Formulário (P1 - User Interface)

**Objetivos**: 
- Interface para registrar responsabilidade
- Validação de entrada
- Feedback ao usuário

**Tarefas**:

1. **Criar `responsabilidade-form.html`**
   - Campo select: Professor (carregado via API GET `/api/professores`)
   - Campo date: Data
   - Campo select: Período (dropdown com turmas: 1ºA, 2ºB, etc.)
   - Campo number: Quantidade Chromebooks (validar > 0)
   - Campo textarea: Observações (opcional)
   - Botão: Salvar

2. **Criar `responsabilidade.js`**
   - Carregar lista de professores ao abrir página
   - Validar formulário cliente (quantidade > 0, data válida)
   - POST para `/api/responsabilidades`
   - Tratamento de erros com alert/toast
   - Redirect para cronograma após sucesso

3. **Integrar ao menu principal**
   - Link na navbar: "Responsabilidades → Nova Responsabilidade"

### Fase 3: Frontend - Visualização Cronograma (P2 - Gallery/List)

**Objetivos**: 
- Visualizar responsabilidades em formato calendário/tabela
- Filtros básicos
- Detalhes ao clicar

**Tarefas**:

1. **Criar `cronograma.html`**
   - Tabela com colunas: Data | Período | Professor | Quantidade | Status | Ações
   - Ou: Calendário tipo grid (data nas linhas, períodos em colunas, professor + qtd nas células)
   - Filtro simples: por Professor (select), por Mês (select ano/mês)

2. **Criar `cronograma.js`**
   - GET `/api/cronograma/março?professor=id` com filtros
   - Renderizar tabela/calendário dinamicamente
   - Clique na linha → modal com detalhes (editar observações, mudar status)
   - PUT para `/api/responsabilidades/{id}` ao enviar mudanças

3. **Estilos em `style.css`**
   - Colorir badges por status (Pendente=azul, Devolvido=verde, Com falta=vermelho, Não realizado=cinza)
   - Responsive para mobile

### Fase 4: Testes & Refinement (P3, após MVP)

**Objetivos**: 
- Cobertura de testes para novos endpoints
- Validações robustas
- Edge cases tratados

**Tarefas**:

1. **Testes unitários em `test_models.py`**
   - Validar criação de Professor
   - Validar criação de ResponsabilidadeChromebook
   - Validar enums Status

2. **Testes integração em `test_responsabilidades.py`**
   - CRUD endpoints
   - Validações (quantidade 0, data inválida, professor não existe)
   - Filtros (por professor, por data)
   - Soft delete se implementado

3. **Testes frontend**
   - Validação form no JS
   - Renderização de cronograma com dados mockados

## Dependências Entre Tarefas

```
Fase 1 (Database + API)
    ↓
Fase 2 (Formulário) & Fase 3 (Cronograma) [podem ser paralelas]
    ↓
Fase 4 (Testes & Refinamento)
```

## Arquivos a Criar/Modificar

### Criar

- ✅ `docs/specs/feature-responsabilidade-chromebooks.md` (FEITO)
- `backend/models.py` - adicionar `Professor` e `ResponsabilidadeChromebook`
- `backend/routes/responsabilidades.py` - nova, endpoints completos
- `backend/tests/test_responsabilidades.py` - nova, testes
- `frontend/responsabilidade-form.html` - nova
- `frontend/cronograma.html` - nova
- `frontend/js/responsabilidade.js` - nova
- `frontend/js/cronograma.js` - nova

### Modificar

- `backend/main.py` - adicionar rota `/api/responsabilidades`
- `backend/database.py` - criar tabelas novas se necessário
- `backend/seed.py` - popular professores e exemplos
- `frontend/index.html` - adicionar link para novas páginas no menu
- `frontend/css/style.css` - adicionar estilos para cronograma

## Critérios de Aceitar (Done)

- [x] Especificação escrita e aprovada
- [ ] Modelos adicionados e compilam
- [ ] Endpoints funcionam (testáveis via Postman/REST Client)
- [ ] Base de dados popula corretamente
- [ ] Formulário frontend valida e envia dados
- [ ] Cronograma exibe registros corretamente
- [ ] Filtros funcionam
- [ ] Testes passam (>80% cobertura)
- [ ] Sem erros console (browser + backend)
- [ ] Responsivo (mobile + desktop)

## Notas Técnicas

- Período/turma é string livre (1ºA, 3ºC) - considerar enum se necessário after MVP
- Status pode ser estendido depois (ex: "Parcial" se 1-2 faltando)
- Foto/evidência de devolução pode ser adicionado em v2
- Integrações futuras: notificação via email se falta registrada
