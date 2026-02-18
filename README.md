# robotsystem

Sistema desktop web-integrado para **automação, organização e processamento inteligente de documentos PDF e XML**, desenvolvido com foco em produtividade, escalabilidade e integração fullstack.

---

## 📌 Sobre o Projeto

O **RobotSystem** surgiu a partir de uma necessidade real dentro de empresa, onde tarefas manuais de organização de documentos consumiam muito tempo e eram altamente repetitivas.

Atividades como:

- Separar documentos personalizados  
- Renomear arquivos por Nome, CPF ou CNPJ  
- Converter XML em planilhas  
- Organizar grandes volumes de PDFs  

Eram feitas manualmente.

A partir disso surgiu a ideia:

> “Se eu já automatizo tarefas com scripts, por que não desenvolver um software completo?”

O que começou como scripts em Python evoluiu para um **sistema fullstack robusto**, com interface moderna, back-end estruturado e integração inteligente com processamento de documentos.

---

## 🚀 Funcionalidades

### 📂 Separação de Documentos
- Processamento automatizado de PDFs  
- Organização baseada em critérios definidos  
- Barra de progresso em tempo real  

---

### 🏷️ Renomeação Inteligente de PDFs
- Extração automática de:
  - Nome  
  - CPF  
  - CNPJ  
- Leitura via:
  - Texto nativo do PDF  
  - OCR (fallback para PDFs escaneados)  
- Normalização e sanitização de nomes de arquivo  
- Substituição segura sem conflitos  

---

### 📊 Conversão de XML
- Conversão de XML para:
  - CSV  
  - Excel  
- Estrutura pronta para análise e relatórios  

---

### 🔄 Progresso em Tempo Real
- Comunicação entre front-end e back-end via eventos customizados  
- Atualização dinâmica da barra de progresso  

---

## 🏗️ Arquitetura do Projeto

### 🔹 Backend

Desenvolvido em **Python + FastAPI**, com separação clara de responsabilidades:

- routes
- schemas
- services
- repositories
- models
- core


Principais características:

- Arquitetura em camadas (Clean-ish)  
- Regras de negócio desacopladas da camada HTTP  
- ORM com SQLAlchemy  
- Validação com Pydantic  
- Tratamento robusto de erros  
- Processamento de arquivos com:
  - PyMuPDF  
  - Tesseract OCR  
  - Expressões Regulares avançadas  

---

### 🔹 Frontend

Inicialmente desenvolvido com **HTML5 + JavaScript Vanilla**.  
Posteriormente migrado para uma stack moderna:

- React  
- TypeScript  
- Vite  

Principais características:

- Componentização  
- Gerenciamento de estado com `useState`  
- Efeitos com `useEffect`  
- Integração com back-end via PyWebView  
- CSS organizado por escopo de componente  
- Interface responsiva com foco em UX  

---

## 🔐 Segurança

- Hashing de senhas com **Argon2 + PEPPER**  
- Criptografia **AES-256**  
- Sanitização de dados para evitar falhas no sistema de arquivos  

---

## 🛠️ Tecnologias Utilizadas

### 👨‍💻 Linguagens
- Python  
- JavaScript  
- TypeScript  

### ⚙️ Backend
- FastAPI  
- SQLAlchemy  
- Pydantic  
- PyWebView  

### 🎨 Frontend
- React  
- Vite  
- HTML5  
- CSS3  

### 🗄️ Banco de Dados
- PostgreSQL  
- SQLite  

### 📄 Processamento de Arquivos
- PyMuPDF  
- Tesseract OCR  
- Pillow  

### 🐳 Infraestrutura
- Docker  
- Docker Compose  
- Git  
- GitHub  

---

## 🧠 Processo de Evolução

O projeto passou por múltiplas reconstruções:

1. Primeira versão em JavaScript Vanilla  
2. Projeto corrompido → reconstrução completa  
3. Evolução do back-end para API estruturada  
4. Migração total do front-end para React + TypeScript  
5. Integração completa entre camadas  

Esse processo consolidou:

- Entendimento profundo de arquitetura  
- Leitura e organização de fluxo entre arquivos  
- Estruturação escalável  
- Resiliência técnica  

---

## 🎯 Objetivo

O RobotSystem foi desenvolvido para:

- Reduzir tempo operacional  
- Diminuir erros humanos  
- Automatizar tarefas repetitivas  
- Estruturar processos internos  
- Servir como base para futura evolução para SaaS  

# 🚀 Status Atual

✔️ Funcionalidades principais implementadas  
✔️ Backend estruturado com autenticação  
✔️ Banco de dados configurado  
✔️ Ambiente Dockerizado  
✔️ Testes implementados  
🔄 Próxima etapa: integração completa entre Frontend e Backend  

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

## 👨‍💻 Autor

**Alexsandro Pancracio**

Desenvolvedor focado em automação, IA, arquitetura de sistemas e integração fullstack.

Este projeto representa uma evolução prática intensa, construída com estudo, persistência e aplicação real.

