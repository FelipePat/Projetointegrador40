# Micro-SaaS Gestão Alimentar

Projeto Integrador: Desenvolvimento de Sistemas Orientado a Dispositivos Móveis e Baseados na Web

Centro Universitário Senac — Senac EAD (2026) | Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas — Grupo 40

## 📋 Sobre o Projeto

O Micro-SaaS Gestão Alimentar é uma aplicação web móvel (PWA) para simplificar a gestão operacional e financeira de microempreendimentos alimentícios (marmitarias, lanchonetes de bairro e food trucks).

O sistema substitui cadernos, comandas de papel e planilhas por um PDV mobile que registra vendas em poucos toques, debita automaticamente os insumos da ficha técnica e apura o lucro considerando as taxas dos meios de pagamento.

### 🎯 Proposta de valor

- **PDV Mobile Ultra-Ágil:** registro de vendas no balcão em poucos toques, otimizado para smartphones.
- **Baixa Automática de Estoque:** ao confirmar a venda, os insumos vinculados à ficha técnica de cada produto são debitados em uma transação atômica.
- **Apuração de Lucro Líquido Real:** dedução do CMV e das taxas de Pix, crédito, débito e dinheiro.

## 🛠️ Arquitetura e tecnologias

- **Frontend (Mobile Web App):** React + Vite + PWA, design mobile-first.
- **Backend (API RESTful):** Python + FastAPI + Pydantic.
- **Banco de dados:** SQLite via SQLAlchemy ORM.

## ✅ Escopo entregue na PoC (2ª etapa)

Conforme o documento da 2ª entrega, o recorte estratégico foi a **Jornada 1 (Carla Martins — registro ágil de venda no balcão e baixa automática de estoque)**.

- [x] **Seed do banco** (`app/seed.py`): cria tabelas e popula insumos, produtos e fichas técnicas.
- [x] **Catálogo e CMV:** `GET /produtos` calcula o custo de cada item pela ficha técnica.
- [x] **Insumos e alertas:** `GET /insumos` retorna status VERDE / AMARELO / VERMELHO.
- [x] **Taxas:** `GET /taxas` expõe os percentuais configurados no backend.
- [x] **Registro de venda:** `POST /vendas` valida os itens, verifica estoque, debita insumos, grava a venda e calcula bruto, taxa, líquido, CMV e lucro em uma única transação.
- [x] **PDV mobile:** catálogo touch, carrinho, contador, modal de pagamento (Pix, débito, crédito, dinheiro) e toast de confirmação.
- [x] **Tela de Estoque:** listagem com badges coloridos, atualizada automaticamente após cada venda.
- [x] **PWA:** manifest, ícones e service worker registrado.
- [x] **Testes automatizados:** cobertura de vendas, baixa de estoque, rollback e validações (pytest).

### Taxas padrão

| Meio de pagamento | Taxa |
|---|---|
| Pix | 0% |
| Dinheiro | 0% |
| Débito | 1% |
| Crédito | 3% |

Os percentuais estão centralizados em `Tarefa05/backend/app/services.py`.

## 🚧 Backlog (ainda não implementado)

Itens descritos na visão do produto/README anterior, mas **fora do recorte da PoC**:

- [ ] **Jornada 2 — Fechamento de caixa:** dashboard diário com totais por forma de pagamento, CMV, taxas, lucro líquido, sugestão de reposição e confirmação de fechamento.
- [ ] **Autenticação JWT** (cadastro/login) e telas administrativas de cadastro.
- [ ] **Configuração de taxas via interface** (hoje os percentuais são constantes no backend).
- [ ] **Cache offline no service worker** (hoje o app é instalável, mas não funciona sem rede).
- [ ] **Capturas de tela e link do vídeo** a serem inseridos nos itens 4.3 e 4.4 do documento da 2ª entrega.

## 📁 Estrutura do repositório

```text
.
├── Projeto_Integrador_2a_ Entrega_Grupo_40.docx   # Documento da 2ª entrega
├── TAREFA05.zip                                   # Entrega original (T05)
└── Tarefa05/
    ├── backend/
    │   ├── app/
    │   │   ├── __init__.py
    │   │   ├── database.py      # Engine SQLite e sessões
    │   │   ├── main.py          # Endpoints da API
    │   │   ├── models.py        # Insumo, Produto, FichaTecnica, Venda
    │   │   ├── schemas.py       # Validação Pydantic
    │   │   ├── seed.py          # Carga inicial do banco
    │   │   └── services.py      # Taxas, CMV e lucro
    │   ├── requirements.txt
    │   ├── requirements-dev.txt       # Dependências dos testes
    │   └── tests/test_vendas.py       # Testes das regras de negócio
    └── frontend/
        ├── public/              # manifest.json, ícones e service worker
        ├── src/
        │   ├── components/      # PDV e Estoque
        │   ├── api.js           # Chamadas à API
        │   ├── App.jsx          # Navegação e toast
        │   ├── main.jsx
        │   └── styles.css
        ├── index.html
        ├── package.json
        └── vite.config.js
```

## 🚀 Como executar localmente

Pré-requisitos: **Python 3.10+** e **Node.js 18+** com npm.

### 1. Backend (FastAPI)

```bash
cd Tarefa05/backend
python -m venv venv
# Windows: venv\Scripts\activate   |   Linux/macOS: source venv/bin/activate
pip install -r requirements.txt

# Cria/popula o banco (necessário antes de iniciar a API)
python -m app.seed
# Para apagar e recriar os dados: python -m app.seed --reset

uvicorn app.main:app --reload
```

API em `http://localhost:8000` e Swagger UI em `http://localhost:8000/docs`.

Para rodar os testes (usam um banco SQLite temporário, sem afetar o banco local):

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

### 2. Frontend (React PWA)

```bash
cd Tarefa05/frontend
npm install
npm run dev
```

Aplicação em `http://localhost:5173`. Use o modo responsivo do navegador (F12) para simular um smartphone.

Para apontar o front para outro host da API, defina `VITE_API_URL` (padrão: `http://localhost:8000`).

### Fluxo de uma venda

1. No PDV, toque nos produtos para montar o carrinho.
2. Toque em **Fechar Pedido**, escolha a forma de pagamento e confirme.
3. O backend debita os insumos da ficha técnica e grava a venda.
4. O toast **“Venda confirmada! Insumos debitados”** aparece e a aba Estoque é atualizada.

## 🔄 Fluxo de contribuição

```bash
git checkout -b feature/nome-da-funcionalidade
git commit -m "feat: adiciona endpoint de baixa automática de estoque"
git push origin feature/nome-da-funcionalidade
# Abrir Pull Request para revisão do grupo
```

## 👥 Integrantes — Grupo 40

Felipe de Carvalho Reinaldo · Felipe Pamplona Antunes Tremea · Gabriel da Silva Santos · Guilherme Rocha Ribas · Hugo Dutra Gomes · Joao Victor Ferreira Oliveira · Laura Luciano Cabral · Marco Antonio Negromonte Guimarães

## 📄 Licença

Projeto desenvolvido para fins acadêmicos no âmbito do Projeto Integrador do Centro Universitário Senac.
