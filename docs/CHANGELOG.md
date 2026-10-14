# Changelog

## [Não publicado]

### Sprint 1 — Fundação, autenticação e permissões

- Projeto Django 5.2 (LTS) com PostgreSQL, configuração por `.env`
  (`.env.example` sem segredos reais), fuso `America/Campo_Grande`.
- Usuário customizado com login por e-mail (sem diferença de maiúsculas).
- Entrar, sair, trocar senha e recuperar senha por e-mail.
- Os quatro perfis (Administrador, Pastor, Líder, Membro) definidos em código
  e sincronizados a cada `migrate`.
- Login exigido em todas as páginas por padrão.
- Gestão de usuários pelo Administrador: listar, criar, editar, ativar e
  desativar, atribuir perfis, definir senha provisória.
- Senha provisória obriga a troca no próximo acesso.
- Auditoria básica de criação, alteração, perfis, ativação e senha definida
  pelo administrador.
- Comando `criar_usuario` para criar o primeiro administrador.
- Estilos mínimos com os tokens do Design System (botão e borda dos campos
  com contraste AA).
- 39 testes automatizados.

### Sprint 0 — Preparação

- Estrutura inicial do repositório.
- Adicionados `CLAUDE.md`, `docs/ROADMAP.md` e o Design System
  (`docs/DESIGN_SYSTEM_IBC.md`, `static/ibc/css/design-tokens.css`,
  `static/ibc/img/ibc-logo-oficial.png`), como recebidos.
- Adicionada a lista de decisões pendentes (`docs/DECISOES_PENDENTES.md`),
  incluindo a revisão de contraste dos tokens.
- Adicionada a proposta de arquitetura (`docs/architecture.md`).
- Adicionada a PRD v1.0 (`docs/PRD_IBC_GESTAO.md`), como recebida (só o
  caminho do roadmap foi corrigido). Arquitetura e decisões pendentes
  alinhadas a ela.
