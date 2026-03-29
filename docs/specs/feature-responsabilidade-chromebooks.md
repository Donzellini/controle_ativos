# Feature Specification: Responsabilidade de Chromebooks

**Feature Branch**: `002-responsabilidade-chromebooks`  
**Created**: 2026-03-29  
**Status**: Draft  
**Input**: Transcrição de requisito semiestruturado da professora

## Context - Por que esta feature existe

As professoras têm acesso à sala de informática e aos Chromebooks em um cronograma específico. Cada dia, uma professora é responsável pela quantidade total de Chromebooks disponíveis naquele período. A vice-direção controla a numeração/patrimônio individual dos aparelhos, mas a professora é responsável por **cuidar e devolver a quantidade X** em determinado dia.

## User Scenarios & Testing

### User Story 1 - Admin registra responsabilidade de Chromebooks (Priority: P1)

Um administrador precisa registrar qual professora é responsável por quantos Chromebooks em qual dia. O sistema deve permitir associar um professor ao cronograma da informática especificando a quantidade de Chromebooks sob sua responsabilidade.

**Why this priority**: Sem este registro, não há rastreamento de responsabilidade. É o fluxo principal.

**Independent Test**: Admin consegue criar registro de responsabilidade, informar professor, data, período e quantidade.

**Acceptance Scenarios**:

1. **Given** Admin está na página de registrar responsabilidade vazia, **When** seleciona professor (de lista existente), data (do cronograma), período e quantidade válida de Chromebooks (exemplo: 20), **Then** o sistema salva o registro e exibe confirmação com ID gerado

2. **Given** Já existe um registro de responsabilidade de Prof. Maria para 02/03/2026 (segunda), **When** Admin tenta criar outro para mesma professora na mesma data/período, **Then** o sistema permite (ou avisa que já existe) e oferece opção de atualizar ou criar novo

3. **Given** Admin tenta registrar quantidade de Chromebooks como 0, **When** clica em salvar, **Then** o sistema rejeita com mensagem "Quantidade deve ser maior que zero"

4. **Given** Admin registra responsabilidade com quantidade 20 Chromebooks, **When** o registro é salvo, **Then** o sistema persiste e permite futuro rastreamento de devolução/falta

---

### User Story 2 - Admin visualiza cronograma de responsabilidades (Priority: P2)

Um administrador precisa visualizar o cronograma de quem é responsável pelos Chromebooks em cada dia/período, facilitando acompanhamento da sala de informática.

**Why this priority**: Essencial para monitorar e validar responsabilidades, mas secundária à criação do registro.

**Independent Test**: Lista mostra professor, data, período, quantidade e status.

**Acceptance Scenarios**:

1. **Given** Existem 5 registros de responsabilidade no banco, **When** Admin acessa cronograma, **Then** todos aparecem em formato de tabela/calendário com colunas: data, professor, quantidade, período (turma)

2. **Given** Cronograma mostra responsabilidades para março/2026, **When** Admin visualiza, **Then** pode identificar facilmente qual professora é responsável em cada data

3. **Given** Admin clica em um registro no cronograma, **When** ação é completada, **Then** exibe detalhes: total de Chromebooks, professor responsável, possível histórico de falta/devolução

---

### User Story 3 - Registro de devolução/falta de Chromebooks (Priority: P3)

Um administrador registra que ao final do período, o professor devolveu todos os Chromebooks ou faltam alguns, criando histórico de responsabilidade.

**Why this priority**: Importante para auditoria, mas pode ser MVP sem este recurso inicialmente.

**Independent Test**: Admin consegue marcar responsabilidade como "fechada" com devoluções validadas.

**Acceptance Scenarios**:

1. **Given** Professor é responsável por 20 Chromebooks em 02/03, **When** ao final do dia Admin registra como "Devolvido com sucesso", **Then** responsabilidade é marcada como encerrada

2. **Given** Professor era responsável por 20 Chromebooks, **When** Admin marca como "Faltam 2", **Then** sistema registra histórico e alerta sobre falta

---

## Edge Cases

- E se a professora falta naquele dia? → Responsabilidade pode ficar pendente ou ser reassignada
- E se há dois períodos no mesmo dia? → Diferentes responsáveis podem ser atribuídos
- Pode haver zero Chromebooks em um dia? → Sim, se sala não está agendada (mas melhor não criar registro)

## Requirements

### Functional Requirements

- **FR-101**: Sistema MUST permitir registrar responsabilidade com campos: professor (referência a tabela de usuários/professores), data, período/turma (do cronograma), quantidade de Chromebooks

- **FR-102**: Sistema MUST validar que quantidade de Chromebooks é > 0

- **FR-103**: Sistema MUST validar que data não é no passado (opcional, permite data presente/futura)

- **FR-104**: Sistema MUST permitir listar responsabilidades com filtros: por professor, por data, por período

- **FR-105**: Sistema MUST exibir cronograma visual mostrando professor responsável para cada data/período

- **FR-106**: Sistema MUST gerar ID único para cada registro de responsabilidade

- **FR-107**: Opcional - Sistema PODE registrar devolução/falta como status: "Pendente", "Devolvido", "Com falta", "Não realizado"

### Key Entities

**ResponsabilidadeChromebook**:
- `id` (PK)
- `professor_id` (FK) - Professor/usuário responsável
- `data` - Data do cronograma
- `periodo_turma` - String identifying turma (ex: "1ºA", "3ºC")
- `quantidade_chromebooks` - Quantidade sob responsabilidade
- `status` - "Pendente", "Devolvido", "Com falta", etc. (Enum)
- `observacoes` - Texto livre opcional
- `criado_em` (Timestamp)
- `atualizado_em` (Timestamp)

### Data Dependencies

- Deve referenciar a tabela de Professores (criar se não existir)
- Cronograma vem do PDF anexado (dados estruturados: data → turma → responsável)

---

## Implementation Notes

- Design simples, sem complexidade desnecessária
- Integrar com interface existente (HTML/JS do projeto)
- Considerar criar tabela "Professor" se não existe
- Dados iniciais podem ser carregados a partir do cronograma estruturado
