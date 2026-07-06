# CasaStock Premium (SaaS)

O **CasaStock Premium** é um sistema moderno de Gestão de Estoque e Compras em formato SaaS (Software as a Service) Multi-Tenant. 
Ele foi projetado inicialmente para uso doméstico, mas escalou para uma arquitetura onde você pode adicionar e gerenciar **múltiplos clientes**, sendo que cada cliente tem acesso apenas ao seu próprio estoque isoladamente, sem vazamento de dados.

## 🚀 Principais Funcionalidades

- **Isolamento de Dados (Multi-Tenant):** Uma arquitetura segura onde o estoque e as compras do Cliente A são invisíveis para o Cliente B.
- **Painel de Administração (Super Admin):** Usuários com papel de `superadmin` têm uma aba exclusiva para gerenciar clientes, resetar senhas e acompanhar cadastros.
- **Gestão de Estoque:** Controle inteligente de produtos com alertas de estoque baixo e falta de itens.
- **Gestão de Compras (Lista Inteligente):** Produtos com estoque abaixo do mínimo exibem um botão ágil para irem direto à lista de compras.
- **Histórico de Gastos:** Registre compras e acompanhe o total de gastos do mês no painel principal.
- **Theme Adaptável:** O sistema tem um visual moderno "Flat" (similar ao Claude/Notion) que se adapta perfeitamente aos modos Claro e Escuro.
- **Agnóstico a Banco de Dados:** O sistema roda com SQLite para testes locais rápidos, mas está equipado com `psycopg2` para se conectar a bancos PostgreSQL (como Supabase/Neon) em produção, evitando perda de dados em serviços serverless (como Render).

## 🛠 Tecnologias Utilizadas

- **Frontend & Backend (Híbrido):** [Flet](https://flet.dev/) (Framework Python focado em UI inspirada no Flutter).
- **Linguagem:** Python 3.10+
- **Banco de Dados:** SQLite (Desenvolvimento) / PostgreSQL (Produção via URL).
- **Hospedagem de Produção recomendada:** [Render.com](https://render.com/) (Web Service) + [Supabase](https://supabase.com/) (Banco de Dados).

---

## 💻 Como rodar o projeto localmente

1. **Clone o repositório:**
```bash
git clone https://github.com/mayconsuel1155-rgb/CasaStock.git
cd CasaStock
```

2. **Crie um ambiente virtual e ative-o (Opcional, mas recomendado):**
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Mac/Linux:
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Inicie o servidor local:**
```bash
python app.py
```
*O sistema abrirá automaticamente no seu navegador padrão ou fornecerá uma URL local (ex: `http://127.0.0.1:8080`).*

> **Nota sobre o primeiro acesso:** Na primeira vez que o sistema rodar, ele criará o banco de dados e inserirá um super-usuário padrão.
> **Usuário:** `admin` | **Senha:** `admin`

---

## ☁️ Como Configurar na Nuvem (PostgreSQL)

Se você hospedar o projeto no **Render** (ou plataformas similares), lembre-se que eles apagam discos locais a cada atualização, destruindo o seu `casastock.db`. Para transformar o CasaStock num SaaS eterno e protegido:

1. Crie um banco PostgreSQL no [Supabase](https://supabase.com) ou [Neon](https://neon.tech).
2. Pegue a **Connection String** (`postgresql://...`).
3. No painel da sua hospedagem (Render), vá em **Environment Variables**.
4. Adicione uma variável com:
   - **Key:** `DATABASE_URL`
   - **Value:** `[SUA CONNECTION STRING]`
5. O sistema detectará o link, abandonará o SQLite local, e criará toda a estrutura Multi-Tenant direto no Supabase.

---
*Desenvolvido em Python com muito ❤️.*
