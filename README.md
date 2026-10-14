# IBC Gestão

Sistema de gestão da membresia oficial da Igreja Batista Central (IBC),
Campo Grande/MS.

**Situação:** Sprint 1 (fundação): login, senha, os quatro perfis e a
gestão de usuários. Cadastro de membros vem na Sprint 3.

## Documentos

| Arquivo | Conteúdo |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Regras permanentes para o desenvolvimento |
| [`docs/PRD_IBC_GESTAO.md`](docs/PRD_IBC_GESTAO.md) | Requisitos do produto (o que o sistema deve fazer) |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Plano das sprints do MVP |
| [`docs/DECISOES_PENDENTES.md`](docs/DECISOES_PENDENTES.md) | Perguntas que a IBC precisa responder antes da Sprint 1 |
| [`docs/architecture.md`](docs/architecture.md) | Proposta de arquitetura técnica |
| [`docs/DESIGN_SYSTEM_IBC.md`](docs/DESIGN_SYSTEM_IBC.md) | Identidade visual e componentes |
| [`static/ibc/css/design-tokens.css`](static/ibc/css/design-tokens.css) | Cores, espaçamentos e fontes |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Histórico de alterações |

A PRD é a versão 1.0, para validação. As respostas de
`DECISOES_PENDENTES.md` completam o que ela deixa em aberto (seção 12).

## Stack

Python 3.12, Django 5.2 (LTS), PostgreSQL 16, Django Templates e CSS.
HTMX entra quando alguma tela precisar.

## Rodar no computador (desenvolvimento)

Precisa de Python 3.12 e PostgreSQL instalados. Os comandos abaixo são para
Linux/macOS.

```bash
# 1. Criar o banco (uma vez). Troque a senha.
sudo -u postgres psql -c "CREATE ROLE ibc_dev LOGIN CREATEDB PASSWORD 'troque-esta-senha';"
sudo -u postgres psql -c "CREATE DATABASE ibc_gestao OWNER ibc_dev;"

# 2. Preparar o projeto (uma vez)
python3.12 -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env
#    abra o .env e preencha DJANGO_SECRET_KEY e DB_PASSWORD

# 3. Criar as tabelas e os perfis
venv/bin/python manage.py migrate

# 4. Criar o primeiro administrador (a senha é pedida na tela)
venv/bin/python manage.py criar_usuario --email voce@exemplo.com --nome "Seu Nome" --perfil Administrador

# 5. Abrir o sistema em http://localhost:8000
venv/bin/python manage.py runserver
```

Sem e-mail configurado no `.env`, o link de "Esqueci minha senha" aparece
no terminal onde o `runserver` está rodando.

## Testes

```bash
venv/bin/python manage.py test
```

Os testes criam um banco temporário (por isso o usuário do banco precisa de
`CREATEDB`) e usam só dados fictícios.

## Perfis e permissões

Definidos em `apps/accounts/roles.py`. A cada `migrate`, os perfis do banco
são ajustados para ficar iguais ao arquivo. Detalhes em
`docs/architecture.md` §4.
