# Arquitetura — IBC Gestão

**Situação:** Sprint 1 implementada (contas, perfis, auditoria básica). O
restante é proposta; revisar quando chegarem as respostas de
`DECISOES_PENDENTES.md`.

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
├── config/                      # settings (um arquivo, guiado pelo .env), urls, wsgi
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

## 4. Autorização (implementado na Sprint 1)

- Usuário customizado (`accounts.User`), com e-mail como login, criado antes
  da primeira migration. Conta (`User`) é separada de pessoa (`Person`,
  Sprint 3).
- **Toda página exige login por padrão** (`LoginRequiredMiddleware`). Só as
  telas de entrar e recuperar senha são públicas. Um teste percorre todas as
  rotas e falha se alguma nova nascer aberta.
- Perfis são grupos do Django. As permissões de cada perfil ficam em
  `apps/accounts/roles.py`; a cada `migrate` o banco é ajustado para ficar
  igual ao arquivo, removendo permissões acrescentadas à mão.
- Cada view protegida declara a permissão (`@permission_required(...,
  raise_exception=True)`) e os serviços verificam de novo. Sem permissão: 403.
- O Django Admin não está instalado e não existe superusuário: ambos
  ignorariam as regras de permissão e auditoria.
- Desativar uma conta derruba as sessões abertas no próximo clique.
- Senha criada pelo administrador é provisória: a pessoa só consegue trocar a
  senha ou sair até criar a própria.
- Um administrador não pode desativar a própria conta nem tirar o próprio
  perfil de Administrador (evita ficar sem ninguém para administrar).

Permissões atuais:

| Permissão | Administrador | Pastor | Líder | Membro |
|---|:-:|:-:|:-:|:-:|
| Ver a própria conta e trocar a própria senha | ✓ | ✓ | ✓ | ✓ |
| Ver usuários (`accounts.view_user`) | ✓ | | | |
| Criar usuários (`accounts.add_user`) | ✓ | | | |
| Editar, ativar e desativar usuários (`accounts.change_user`) | ✓ | | | |
| Atribuir perfis (`accounts.assign_roles`) | ✓ | | | |
| Consultar auditoria (`audit.view_auditevent`, tela na Sprint 5) | ✓ | | | |

Pastor, Líder e Membro ganham permissões quando os dados de membresia
existirem (Sprint 3 em diante). Ninguém tem permissão de apagar usuário:
conta se desativa, não se apaga.

## 5. Dados e histórico

Entidades da PRD (§8), por app:

| App | Entidades |
|---|---|
| `accounts` | `User`, `Profile` (liga o usuário à `Person`) |
| `people` | `Person`, `Family`, `FamilyMembership` (se aprovados) |
| `membership` | `MembershipEvent` |
| `reregistration` | `ReregistrationRequest` (a PRD chama de `RecadastroRequest`; em inglês para seguir o CLAUDE.md §4) |
| `institution` | `InstitutionSettings`, `ConsentRecord` |
| `audit` | `AuditEvent` |

- Pessoa (`Person`) separada de usuário (`User`): nem toda pessoa tem login.
- Histórico da membresia é uma lista de eventos (`MembershipEvent`) que não
  se apaga; correção vira novo registro com motivo.
- A situação atual da pessoa fica num campo próprio. Um evento só a altera
  quando houver regra institucional aprovada para isso (PRD RF-05); até lá,
  a secretaria muda a situação explicitamente, e a mudança é auditada.
- Recadastramento (`ReregistrationRequest`) guarda o que a pessoa enviou;
  só altera `Person` quando a secretaria aprova.
- Auditoria (`AuditEvent`, já na Sprint 1) registra quem, quando, o quê e
  quais campos mudaram, sem copiar valores sensíveis. Registro não se altera
  nem se apaga pelo sistema. Proteção também no banco (gatilho) fica para a
  Sprint 5.

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

- Testes do próprio Django (`manage.py test`), contra PostgreSQL.
- Para cada funcionalidade: permissões positivas e negativas dos perfis,
  entradas inválidas, duplicidades, transições de estado.
- Teste que detecta migration esquecida (`makemigrations --check`).
- Teste que percorre todas as rotas e exige login nas não públicas.
- Somente dados fictícios.
