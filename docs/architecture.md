# Arquitetura — IBC Gestão

**Situação:** proposta inicial (Sprint 0). Nada aqui foi implementado ainda.
Revisar depois que as respostas de `DECISOES_PENDENTES.md` chegarem.

## 1. Visão geral

Monólito Django único, renderizado no servidor (Django Templates + HTMX),
com PostgreSQL próprio. Sem SPA, sem filas, sem microserviços (CLAUDE.md §2).

```
Navegador ──HTTPS──> proxy reverso ──> gunicorn ──> Django ──> PostgreSQL (exclusivo do IBC)
                                                    │
                                                    └── arquivos enviados (logotipo, favicon)
```

## 2. Estrutura de pastas prevista

```
ibc-gestao/
├── CLAUDE.md
├── README.md
├── manage.py
├── pyproject.toml / requirements*.txt
├── .env.example                 # só nomes das variáveis, sem valores reais
├── config/                      # settings (base, dev, prod), urls, wsgi
├── apps/
│   ├── accounts/                # usuário customizado, login, perfis
│   ├── people/                  # pessoa, vínculos familiares
│   ├── membership/              # situação e eventos da membresia (histórico)
│   ├── reregistration/          # recadastramento e fila da secretaria
│   ├── audit/                   # registro de ações relevantes
│   └── institution/             # configurações institucionais e preferências
├── templates/
│   ├── base.html
│   └── partials/                # sidebar, messages, form_field
├── static/ibc/
│   ├── css/design-tokens.css
│   └── img/ibc-logo-oficial.png
├── docs/
└── tests/ (ou tests/ dentro de cada app)
```

Código em inglês, interface em português (CLAUDE.md §4).

## 3. Camadas

- **Modelos:** dados e restrições de integridade (constraints e índices no
  banco, além da validação no formulário).
- **Serviços (`services.py` em cada app):** regras de negócio e transações.
  Ex.: `approve_reregistration()`, `register_membership_event()`. Views e
  comandos só chamam serviços.
- **Formulários:** validação de entrada (Django Forms).
- **Views:** autenticação + autorização + chamar serviço + renderizar.
- **Templates:** só apresentação; nada de regra de negócio.

## 4. Autorização

- Usuário customizado (`accounts.User`) criado **antes da primeira
  migration**.
- Perfis como `Group` do Django com permissões explícitas
  (`people.view_person`, `membership.add_event`, ...), criados por migration
  de dados para ficarem iguais em todos os ambientes.
- Toda view protegida verifica permissão no servidor (mixin/decorator) **e**
  o escopo do registro (um membro só vê o próprio cadastro). Teste para cada
  perfil, permitido e negado, incluindo tentativa de trocar o ID na URL.
- Administrador gerencia usuários e configurações, mas **não** recebe por
  padrão a permissão de registros pastorais sensíveis.
- Usuário desativado (`is_active=False`) perde acesso na hora.

## 5. Dados e histórico

- Pessoa (`Person`) separada de usuário (`User`): nem toda pessoa tem login.
- Histórico da membresia é uma lista de eventos (`MembershipEvent`) que não
  se apaga; correção vira novo registro com motivo.
- A situação atual da pessoa é derivada do último evento válido (ou guardada
  e recalculada pelo serviço na mesma transação).
- Recadastramento (`ReregistrationRequest`) guarda o que a pessoa enviou;
  só altera `Person` quando a secretaria aprova.
- Auditoria registra quem, quando, o quê e quais campos mudaram, sem copiar
  valores sensíveis.

## 6. Configuração e segredos

- Variáveis de ambiente (`.env` fora do git): `SECRET_KEY`, `DATABASE_URL`,
  `ALLOWED_HOSTS`, e-mail, etc. O repositório só terá `.env.example`.
- Fuso: `TIME_ZONE = "America/Campo_Grande"`, `USE_TZ = True` (banco em UTC,
  exibição no horário local).
- Produção: `DEBUG=False`, cookies seguros, HSTS, CSRF, cabeçalhos de
  segurança.

## 7. Ambientes

- **Desenvolvimento:** local / ambiente isolado, PostgreSQL local, dados
  fictícios.
- **Produção:** a definir (ver `DECISOES_PENDENTES.md` §9). Nenhuma alteração
  na VPS atual sem autorização explícita.

## 8. Testes

- `django.test` / `pytest-django`.
- Para cada funcionalidade: permissões positivas e negativas dos perfis,
  entradas inválidas, duplicidades, transições de estado.
- Teste que detecta migration esquecida (`makemigrations --check`).
- Somente dados fictícios.
