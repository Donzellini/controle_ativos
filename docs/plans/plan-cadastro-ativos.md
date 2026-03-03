# 📐 Plano de Implementação: Cadastro de Ativos

## Fase 1: Backend (Database + API)

### 1.1 - Preparar estrutura do banco de dados
- [ ] Criar `backend/models.py` com classe `Ativo`
- [ ] Implementar tabela `ativos` com SQLite
- [ ] Campos: id, descricao, tipo, numero_serie, mac_address, valor, data_aquisicao, status, localizacao, created_at, updated_at

### 1.2 - Criar endpoints da API
- [ ] POST `/api/ativos` - Criar novo ativo
  - Entrada: JSON com dados do ativo
  - Validação: número_serie único
  - Saída: {success: true, id: 123, message: "Ativo cadastrado"}
  
- [ ] GET `/api/ativos` - Listar todos os ativos
  - Saída: JSON array com todos os ativos

- [ ] GET `/api/ativos/<id>` - Obter ativo específico
  - Saída: JSON com dados do ativo

### 1.3 - Tratamento de erros
- [ ] Validar campos obrigatórios
- [ ] Verificar duplicação de número de série
- [ ] Retornar erro 400 com mensagem clara para cliente

## Fase 2: Frontend (Interface)

### 2.1 - Estrutura HTML
- [ ] Criar `frontend/cadastro-ativos.html`
- [ ] Formulário com campos: descrição, tipo, série, MAC, valor, data, localização
- [ ] Bootstrap 5 para responsividade
- [ ] Buttons para Salvar e Limpar

### 2.2 - Interatividade JavaScript
- [ ] Criar `frontend/js/cadastro-ativos.js`
- [ ] Listener para envio do formulário
- [ ] Fetch API para POST ao backend
- [ ] Exibir mensagem de sucesso/erro
- [ ] Limpar formulário após sucesso
- [ ] Validação client-side antes de enviar

### 2.3 - Lista de ativos (visualização)
- [ ] Criar `frontend/lista-ativos.html`
- [ ] Fetch GET `/api/ativos`
- [ ] Exibir em tabela com DataType ou cards
- [ ] Badges de status (Disponível=verde, Emprestado=amarelo, Danificado=vermelho)

## Ordem de Execução
1. Começar pelo **Backend** (modelos + banco de dados)
2. Criar **Endpoints básicos** (CRUD)
3. Testar endpoints com curl ou Postman
4. Construir **Frontend** consumindo API
5. Integrar e testar fluxo completo

## Próximos Passos
1. ✅ Especificação criada
2. ⏳ Implementar Fase 1 (Backend)
3. ⏳ Implementar Fase 2 (Frontend)
4. ⏳ Testes integrados
