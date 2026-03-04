# 🚀 Guia de Deploy: Fly.io (Backend) + Netlify (Frontend)

## ✅ Pré-requisitos

1. **Fly.io Account**: https://fly.io (grátis com créditos iniciais)
2. **Netlify Account**: https://netlify.com (grátis)
3. **Git instalado** e repositório remoto (GitHub, GitLab, etc)
4. **Fly CLI instalado**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

---

## 📦 BACKEND - Fly.io

### 1️⃣ Preparar o Backend Localmente

```bash
cd /media/lumier/DADOS/Projects/controle_ativos
```

### 2️⃣ Fazer Login no Fly.io

```bash
flyctl auth login
```

### 3️⃣ Criar a App no Fly.io

```bash
flyctl launch
```

**Quando perguntar:**
- Name: `controle-ativos` (ou um nome único)
- Postgres? → `No` (vamos usar SQLite)
- Redis? → `No`
- Deploy now? → `No` (faremos depois)

**Resultado:** Um arquivo `fly.toml` será criado (já incluído no projeto)

### 4️⃣ Configurar Variáveis de Ambiente

```bash
flyctl secrets set \
  DATABASE_URL=sqlite:///./ativos.db \
  ENVIRONMENT=production
```

### 5️⃣ Build e Deploy do Backend

```bash
flyctl deploy
```

**Output esperado:**
```
✓ Image: registry.fly.io/controle-ativos:deployment-xxxxx
✓ Image size: 150 MB
✓ Pushing to registry
✓ Deployment created with ID: xxx
✓ Machines have reached desired state
✓ App deployed successfully
```

### 6️⃣ Verificar o Deploy

```bash
# Ver logs
flyctl logs

# Abrir a app
flyctl open

# Status
flyctl status
```

**Sua API estará em:** `https://controle-ativos.fly.dev`

### 7️⃣ Verificar a API

```bash
curl https://controle-ativos.fly.dev/
# Deve retornar: {"status":"ok","message":"Controle de Ativos API is running"}
```

---

## 🎨 FRONTEND - Netlify

### 1️⃣ Preparar o Frontend

**Atualizar URL da API** em todos os arquivos JavaScript:

#### `frontend/js/cadastro.js`
```javascript
// Alterar
const API_URL = 'http://localhost:8000/api';
// Para
const API_URL = 'https://controle-ativos.fly.dev/api';
```

#### `frontend/js/listagem.js`
```javascript
// Alterar
const API_URL = 'http://localhost:8000/api';
// Para
const API_URL = 'https://controle-ativos.fly.dev/api';
```

#### `frontend/js/editar.js`
```javascript
// Se existir, alterar
const API_URL = 'http://localhost:8000/api';
// Para
const API_URL = 'https://controle-ativos.fly.dev/api';
```

### 2️⃣ Fazer Push para o Git

```bash
# Adicionar e commitar
git add .
git commit -m "Adiciona config para deploy (Fly.io + Netlify)"
git push origin main
```

### 3️⃣ Conectar com Netlify

**Opção A: Via CLI**
```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# Fazer login
netlify login

# Deploy
netlify deploy --prod --dir=frontend
```

**Opção B: Via Website (recomendado)**
1. Acesse https://app.netlify.com
2. Clique em **"New site from Git"**
3. Selecione seu repositório (GitHub, GitLab, etc)
4. Configure:
   - **Build command:** deixe em branco (é conteúdo estático)
   - **Publish directory:** `frontend`
5. Clique em **Deploy site**

### 4️⃣ Configurar Redirects (se necessário)

O arquivo `netlify.toml` já está configurado, ele redireciona routes para `index.html`.

### 5️⃣ Seu Frontend estará em

```
https://seu-site.netlify.app
```

---

## 🔗 Conectar Frontend + Backend

Se o CORS ainda tiver problemas, no `backend/main.py` adicione:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "https://seu-site.netlify.app"  # Seu frontend Netlify
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Depois redeploy:
```bash
flyctl deploy
```

---

## 📊 Estrutura Final

```
Backend:  https://controle-ativos.fly.dev
Frontend: https://seu-site.netlify.app
```

---

## 🐛 Troubleshooting

### Backend não inicia?
```bash
flyctl logs
```

### Frontend não conecta na API?
1. Verifique CORS no backend
2. Verifique URL da API no JavaScript
3. Teste com `curl https://controle-ativos.fly.dev/ativos`

### Erro de banco de dados?
- SQLite não persiste por padrão no Fly.io
- Considere usar PostgreSQL para produção:
```bash
flyctl postgres create
```

---

## 💡 Dicas de Otimização

1. **Compressão de Imagens**: Optimize os assets do frontend
2. **Cache**: Configure cache headers no Netlify
3. **Monitoramento**: Use `flyctl monitoring` para verificar recursos
4. **Scaling**: Se necessário, aumente `min_machines_running` em `fly.toml`

---

## 📝 Próximos Passos

- [ ] Adicionar GitHub Actions para CI/CD automático
- [ ] Configurar banco de dados PostgreSQL
- [ ] Adicionar variáveis de ambiente para diferentes ambientes
- [ ] Implementar logs centralizados
- [ ] Adicionar testes no pipeline de deploy

