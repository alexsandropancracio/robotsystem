# robotsystem

Software desktop desenvolvido para **ambiente corporativo**, com foco na **automação de tarefas operacionais repetitivas envolvendo arquivos e documentos**.

O projeto foi criado com o objetivo de reduzir tempo manual, minimizar erros humanos e aumentar a produtividade em rotinas administrativas.

---

# 🎯 Objetivo do Projeto

Empresas lidam diariamente com:

- Separação manual de documentos  
- Organização e padronização de arquivos  
- Renomeação baseada em dados como CPF/CNPJ  
- Processos repetitivos que consomem horas da equipe  

Este software foi desenvolvido para **automatizar esses fluxos**, trazendo:

- ⚡ Agilidade operacional  
- 🔒 Segurança  
- 📈 Escalabilidade  
- 🏢 Estrutura preparada para ambiente corporativo  

---

# ⚙️ Funcionalidades

## 📁 1. Separação de Documentos

Permite:

- Selecionar pasta de origem  
- Selecionar pasta de destino  
- Definir parâmetros de separação  
- Executar processamento com barra de progresso em tempo real  

Ideal para rotinas onde múltiplos documentos precisam ser organizados automaticamente.

---

## 🏷️ 2. Renomeação Inteligente de Arquivos

Sistema de renomeação com filtros:

- Nome  
- CPF  
- CNPJ  

Inclui:

- Confirmação antes da execução  
- Exibição da quantidade de arquivos processados  
- Barra de progresso dinâmica  

Voltado para padronização e organização automatizada de arquivos empresariais.

---

## 🔐 3. Estrutura Completa de Autenticação (Backend)

O sistema já possui backend estruturado com:

- Cadastro de usuários  
- Login  
- Logout  
- Estrutura de autenticação  
- Controle de segurança  
- Banco de dados configurado  

Os endpoints já estão implementados — faltando apenas a integração final com o frontend.

---

# 🧠 Arquitetura do Projeto

O projeto foi desenvolvido com separação clara entre frontend e backend, seguindo boas práticas de arquitetura.

---

## 🖥️ Frontend (Desktop Application)

- React  
- TypeScript  
- Vite  
- Interface moderna e componentizada  
- Modais customizados (UX profissional)  
- Comunicação com backend via PyWebView  

---

## 🐍 Backend (API Corporativa)

- Python  
- SQLAlchemy  
- Alembic (controle de migrations)  
- PostgreSQL  
- Estrutura pronta para autenticação e controle de usuários  

---

# 🐳 Ambiente Containerizado

O backend roda totalmente containerizado com:

- Docker  
- Docker Compose  
- Banco PostgreSQL isolado  
- Migrations versionadas  
- Ambiente preparado para deploy escalável  

---

# 🧪 Qualidade e Testes

O backend já possui:

- ✅ Testes Unitários  
- ✅ Testes End-to-End (E2E)  
- ✅ Estrutura preparada para manutenção e crescimento  

---

# 🚀 Status Atual

✔️ Funcionalidades principais implementadas  
✔️ Backend estruturado com autenticação  
✔️ Banco de dados configurado  
✔️ Ambiente Dockerizado  
✔️ Testes implementados  
🔄 Próxima etapa: integração completa entre Frontend e Backend  

---

# 🏗️ Stack Completa

## Frontend
- React  
- TypeScript  
- Vite  

## Desktop Bridge
- PyWebView  

## Backend
- Python  
- SQLAlchemy  
- Alembic  
- PostgreSQL  

## Infraestrutura
- Docker  
- Docker Compose  

## Testes
- Pytest  
- Testes E2E  

---

# 💡 Visão de Produto

Este projeto foi pensado como base para um software corporativo de automação, podendo evoluir para:

- Controle de permissões por usuário  
- Histórico de operações  
- Logs auditáveis  
- Dashboard administrativo  
- Sistema SaaS  
- Deploy em ambiente cloud  

---

# 📌 Conclusão

Este não é apenas um sistema de manipulação de arquivos.

É a base de um **software corporativo estruturado**, com:

- Separação clara de camadas  
- Backend robusto  
- Banco de dados relacional  
- Ambiente containerizado  
- Testes automatizados  
- Arquitetura pronta para escalar  

O projeto representa a construção de uma solução real para ambientes empresariais que demandam automação, segurança e organização.

