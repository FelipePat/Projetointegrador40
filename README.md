Micro-SaaS Gestão Alimentar

Projeto Integrador: Desenvolvimento de Sistemas Orientado a Dispositivos Móveis e Baseados na Web

Centro Universitário Senac — Senac EAD (2026) | Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas — Grupo 40

📋 Sobre o Projeto

O Micro-SaaS Gestão Alimentar é uma aplicação web móvel (PWA) desenvolvida para simplificar a gestão operacional e financeira de microempreendimentos alimentícios (pequenas marmitarias, lanchonetes de bairro e food trucks).

No dia a dia de operação intensa, microempreendedores frequentemente dependem de cadernos de anotação, comandas de papel ou planilhas complexas, o que gera falhas no fechamento de caixa, desperdício de insumos perecíveis e desconhecimento da margem de lucro real.

🎯 Proposta de Valor

PDV Mobile Ultra-Ágil: Registro de vendas no balcão em poucos toques de tela, otimizado para smartphones.

Baixa Automática de Estoque: Cada produto possui uma Ficha Técnica vinculada aos seus ingredientes; ao confirmar uma venda, o sistema debita os insumos em tempo real.

Apuração de Lucro Líquido Real: Dedução automática do Custo de Mercadoria Vendida (CMV) e das taxas de maquininha/meios de pagamento (Pix, Crédito, Débito e Dinheiro) no fechamento diário.

🛠️ Arquitetura e Tecnologias

Frontend (Mobile Web App): React + Vite + Progressive Web App (PWA) com design mobile-first.

Backend (API RESTful): Python + FastAPI + Pydantic.

Banco de Dados: SQLite integrado via SQLAlchemy ORM (com transações atômicas ACID).

✨ Funcionalidades Principais (MVP)

[x] Autenticação e Taxas: Cadastro/Login (JWT) e configuração das taxas percentuais por meio de pagamento.

[x] Controle de Insumos: Cadastro de ingredientes com custo unitário, estoque atual, estoque mínimo e alertas visuais (Verde, Amarelo e Vermelho).

[x] Produtos e Ficha Técnica: Criação de itens do cardápio com cálculo automático do CMV unitário.

[x] PDV Rápido: Catálogo touch-friendly com seleção rápida de itens, escolha da forma de pagamento e confirmação instantânea.

[x] Fechamento de Caixa Diário: Consolidação de faturamento bruto, taxas descontadas, CMV acumulado e Lucro Líquido Real, além de lista sugerida de compras.

📁 Estrutura do Repositório

micro-saas-gestao-alimentar/
├── backend/                  # API RESTful (Python + FastAPI + SQLAlchemy)
│   ├── app/
│   │   ├── models/           # Modelos relacionais (SQLite)
│   │   ├── schemas/          # Validação de dados (Pydantic)
│   │   ├── routes/           # Endpoints (auth, insumos, produtos, vendas, financeiro)
│   │   ├── services/         # Regras de negócio (CMV, taxas e baixa de estoque)
│   │   └── main.py           # Entrypoint da API
│   └── requirements.txt
│
├── frontend/                 # Aplicação Mobile Web App (React + PWA)
│   ├── public/               # manifest.json, ícones e service worker
│   ├── src/
│   │   ├── components/       # Componentes reutilizáveis (PDV, Badges, BottomNav)
│   │   ├── pages/            # Telas (PDV, Estoque, Produtos, Fechamento)
│   │   ├── services/         # Comunicação com a API REST
│   │   └── App.jsx
│   └── package.json
│
└── docs/                     # Documentação do Projeto Integrador (Entregas e Diagramas)


🚀 Como Executar o Projeto Localmente

Pré-requisitos

Python 3.10+

Node.js 18+ e npm (ou yarn)

1. Executando o Backend (FastAPI)

# Acesse a pasta do backend
cd backend

# Crie e ative um ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor de desenvolvimento
uvicorn app.main:app --reload


A API estará disponível em http://localhost:8000 e a documentação interativa (Swagger UI) em http://localhost:8000/docs.

2. Executando o Frontend (React PWA)

# Em outro terminal, acesse a pasta do frontend
cd frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev


A aplicação estará acessível em http://localhost:5173. (Dica: utilize o modo de visualização responsiva do navegador — DevTools F12 — para simular a tela de um smartphone).

🔄 Fluxo de Contribuição (Git Flow Simplificado)

Para manter a organização entre os integrantes do grupo:

Crie uma branch a partir da main ou develop para sua tarefa:

git checkout -b feature/nome-da-funcionalidade


Realize commits claros e objetivos:

git commit -m "feat: adiciona endpoint de baixa automatica de estoque"


Envie sua branch e abra um Pull Request para revisão dos colegas:

git push origin feature/nome-da-funcionalidade


👥 Integrantes — Grupo 40

Felipe de Carvalho Reinaldo

Felipe Pamplona Antunes Tremea

Gabriel da Silva Santos

Guilherme Rocha Ribas

Hugo Dutra Gomes

Joao Victor Ferreira Oliveira

Laura Luciano Cabral

Marco Antonio Negromonte Guimarães

📄 Licença

Este projeto foi desenvolvido para fins acadêmicos no âmbito do Projeto Integrador do Centro Universitário Senac.
