# Feature Specification: Cadastro de Ativos

**Feature Branch**: `001-cadastro-ativos`  
**Created**: 2026-03-03  
**Status**: Draft  
**Input**: User description: "Sistema para cadastro de ativos de TI com validações e controle de estoque"

## User Scenarios & Testing

### User Story 1 - Admin cadastra novo ativo no sistema (Priority: P1)

Um administrador do sistema precisa registrar um novo ativo de TI (notebook, mouse, projetor, etc.) no inventário. Ele acessa o formulário de cadastro, preenche as informações essenciais do ativo e o sistema persiste os dados, permitindo rastreamento posterior.

**Why this priority**: Este é o fluxo principal da feature. Sem a capacidade de cadastrar ativos, o sistema não tem valor. Todos os outros fluxos dependem desta funcionalidade.

**Independent Test**: Pode ser testado completamente integrando formulário + API + database. Admin consegue preencher formulário, submeter, receber confirmação e ver ativo listado.

**Acceptance Scenarios**:

1. **Given** Admin está na página de cadastro vazia, **When** preenche todos os campos obrigatórios (descrição, tipo, número de série, valor, data, localização), **Then** o sistema salva o ativo e exibe mensagem de sucesso com ID gerado

2. **Given** Admin tenta cadastrar ativo sem número de série, **When** clica em salvar, **Then** o sistema rejeita com mensagem clara "Número de série é obrigatório"

3. **Given** Já existe ativo com número de série "SN-12345" no banco, **When** Admin tenta cadastrar outro com mesmo número, **Then** o sistema rejeita com mensagem "Número de série já cadastrado"

4. **Given** Admin preenche data de aquisição inválida (data no futuro), **When** clica em salvar, **Then** o sistema rejeita com mensagem "Data não pode ser no futuro"

5. **Given** Admin submete formulário com sucesso, **When** a página é recarregada, **Then** o novo ativo aparece na lista de inventário com status "Disponível"

---

### User Story 2 - Admin visualiza lista de ativos cadastrados (Priority: P2)

Um administrador precisa visualizar todos os ativos cadastrados no sistema em uma lista organizada, com filtros por tipo e status para facilitar a busca.

**Why this priority**: Essencial para o admin monitorar inventário, mas secundária à capacidade de criar ativos. Pode ser MVP sem filtros avançados.

**Independent Test**: Implementar somente listagem básica funciona como MVP. Admin consegue ver tabela com todos os ativos após cadastrar.

**Acceptance Scenarios**:

1. **Given** Existem 3 ativos no banco de dados, **When** Admin acessa página de listagem, **Then** todos os 3 ativos aparecem em uma tabela com colunas: descrição, tipo, série, status, localização

2. **Given** Lista contém ativos com status diferente (Disponível, Emprestado, Danificado), **When** Admin visualiza, **Then** cada status é exibido com badge colorido (verde, amarelo, vermelho)

3. **Given** Admin clica em um ativo na lista, **When** a ação é completada, **Then** modal ou página de detalhe mostra todas as informações do ativo

---

### User Story 3 - Admin atualiza informações de ativo existente (Priority: P3)

Um administrador precisar corrigir ou atualizar informações de um ativo que já foi cadastrado (ex: mudança de localização, atualização de valor).

**Why this priority**: Importante para manutenção de dados, mas pode ser implementado após MVP básico. Baixa frequência de uso comparada a P1 e P2.

**Independent Test**: Requer apenas a página de edição + API PUT. Admin consegue fazer alterações e persistir.

**Acceptance Scenarios**:

1. **Given** Admin está visualizando detalhes de um ativo, **When** clica no botão editar, **Then** formulário é carregado com os dados atuais para edição

2. **Given** Admin altera localização do ativo de "Sala A" para "Sala B" e salva, **When** a edição é submetida, **Then** o sistema persiste a mudança e mostra mensagem de sucesso

3. **Given** Admin tenta alterar número de série para um que já existe, **When** clica em salvar, **Then** o sistema rejeita com mensagem de duplicação

---

## Edge Cases

- O que acontece quando o admin tenta cadastrar um ativo com valor negativo? → Sistema rejeita
- Como o sistema se comporta se o número de série contiver caracteres especiais? → Aceita (ex: "SN-12345-A")
- Qual é o tamanho máximo para descrição do ativo? → 255 caracteres
- Um ativo pode ter status "Danificado" e ser emprestado simultaneamente? → Não, status Danificado bloqueia empréstimos

## Requirements

### Functional Requirements

- **FR-001**: Sistema MUST permitir cadastro de ativo com campos: descrição, tipo, número de série, MAC address (opcional), valor estimado, data de aquisição, status inicial (padrão: "Disponível"), localização

- **FR-002**: Sistema MUST validar número de série como único no banco de dados

- **FR-003**: Sistema MUST validar que data de aquisição não é no futuro

- **FR-004**: Sistema MUST validar que todos os campos obrigatórios estão preenchidos antes de salvar

- **FR-005**: Sistema MUST retornar erro com mensagem clara em português quando validação falha

- **FR-006**: Sistema MUST gerar ID único para cada ativo cadastrado e retornar ao usuário

- **FR-007**: Sistema MUST permitir listagem de todos os ativos com paginação (mínimo 20 por página)

- **FR-008**: Sistema MUST exibir status do ativo com visual diferenciado (badges coloridas): Disponível (verde), Emprestado (amarelo), Danificado (vermelho), Inativo (cinza)

- **FR-009**: Sistema MUST oferecer busca por número de série e descrição na listagem

- **FR-010**: Sistema MUST permitir edição de informações de ativo após cadastro, mantendo data de criação

### Key Entities

- **Ativo**: Representa um item de TI no inventário
  - Attributes: id, descrição, tipo, número_serie (único), mac_address, valor_estimado, data_aquisicao, status, localização, criado_em, atualizado_em

- **Tipo**: Categoria do ativo
  - Values: Notebook, Mouse, Teclado, Monitor, Projetor, Webcam, Headset, Outro

- **Status**: Estado do ativo
  - Values: Disponível, Emprestado, Danificado, Inativo

## Success Criteria

### Measurable Outcomes

- **SC-001**: Admin consegue cadastrar um novo ativo completamente em menos de 2 minutos (incluindo validações)

- **SC-002**: Sistema rejeita 100% de ativos com número de série duplicado com mensagem clara

- **SC-003**: Lista de ativos carrega com até 20 itens em menos de 1 segundo

- **SC-004**: 95% das tentativas de cadastro válidas são bem-sucedidas na primeira submissão

- **SC-005**: Admin consegue encontrar qualquer ativo em lista de 1000 itens usando busca em menos de 5 segundos
