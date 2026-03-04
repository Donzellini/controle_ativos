# 📜 Constituição do Projeto: Gerenciador de TI (Almoxarifado)

## 🎯 Objetivo e Visão
Este projeto visa o controle rigoroso de ativos de TI (notebooks, mouses, projetores) e a gestão de seus empréstimos dentro de uma instituição. 

## 🏗️ Pilares da Arquitetura
- **Metodologia**: Spec-driven Development (SDD) utilizando o **Spec Kit**.
- **Workflow**: Toda nova funcionalidade deve começar por uma especificação em `docs/specs/` antes de qualquer implementação.
- **Context-Driven**: O código gerado deve respeitar o estilo e a simplicidade do projeto de "Cadastro de Voluntariado" anterior.

## 💻 Stack Tecnológica
### Backend (Diretório `/backend`)
- **Linguagem**: Python 3.x.
- **Framework**: FastAPI (seguindo o padrão RESTful).
- **Banco de Dados**: SQLite (persistência simples em arquivo `.db`).
- **Padrão de Resposta**: JSON para todos os endpoints da API.

### Frontend (Diretório `/frontend`)
- **Base**: HTML5, CSS3 e **Bootstrap 5**.
- **UI/UX**: Design limpo, uso de ícones do **Bootstrap Icons** e badges coloridos para status (ex: Sucesso = Disponível, Perigo = Emprestado/Danificado).
- **Comunicação**: JavaScript nativo (Fetch API) consumindo o backend Python.

## 🛠️ Regras de Desenvolvimento (Ground Rules)
1. **Consistência de Dados**: Ativos nunca são excluídos permanentemente se houver histórico de empréstimo; em vez disso, são marcados como "Inativo" ou "Danificado".
2. **Modularidade**: Manter a lógica de rotas no `app.py` clara e funções de manipulação de banco de dados isoladas.
3. **Interface Amigável**: Seguir o modelo de "Cards" e "DataTables" utilizado no projeto de voluntariado para exibição de listas.
4. **Tratamento de Erros**: Tanto o backend quanto o frontend devem informar claramente ao usuário se uma operação (como emprestar um item já ocupado) falhou.

## 📂 Organização de Arquivos
- `/docs/specs/`: Arquivos `.md` definindo as funcionalidades.
- `/docs/plans/`: Planos de implementação gerados pela IA.
- `/backend/`: Servidor FastAPI e banco de dados.
- `/frontend/`: Arquivos estáticos (HTML/JS/CSS).