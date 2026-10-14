# IBC Gestão — Roadmap do MVP

**Versão:** 1.0  
**Status:** Planejamento inicial  
**Produto:** Sistema de gestão da membresia oficial da Igreja Batista Central (IBC), Campo Grande/MS  
**Responsável técnico pelo desenvolvimento:** Projeto implementado com auxílio do Claude Code

---

## 1. Visão do produto

O IBC Gestão será uma aplicação web para organizar a membresia oficial da IBC, começando por uma base nova de cadastro, recadastramento e histórico eclesiástico. O sistema evoluirá posteriormente para apoiar pequenos grupos, ministérios, eventos e comunicação institucional.

### Objetivos do MVP

1. Criar uma base nova de membros, sem importar dados antigos.
2. Disponibilizar cadastro e recadastramento com validação pela secretaria.
3. Implementar quatro perfis iniciais: Administrador, Pastor, Líder e Membro.
4. Registrar alterações relevantes e histórico da membresia.
5. Aplicar segurança e privacidade desde o início, considerando a LGPD e os dados religiosos sensíveis.
6. Utilizar a identidade visual oficial da IBC e permitir personalização institucional controlada.
7. Entregar uma aplicação testada, documentada e preparada para publicação segura.

## 2. Stack e arquitetura de referência

- **Agente de desenvolvimento:** Claude Code.
- **Linguagem:** Python 3.12.
- **Framework:** Django.
- **Banco:** PostgreSQL.
- **Interface:** Django Templates, HTMX e CSS responsivo.
- **Versionamento:** Git.
- **Testes:** testes automatizados do Django e testes manuais de homologação.
- **Design System:** `DESIGN_SYSTEM_IBC.md` e `design-tokens.css`.

A hospedagem definitiva deve ser confirmada após o diagnóstico técnico. A VPS atual possui Ubuntu 24.04 LTS, 2 vCPU, aproximadamente 1,9 GiB de RAM e já hospeda outros sistemas. Não instalar serviços adicionais nem publicar o IBC antes de avaliar recursos, isolamento, backups e riscos.

## 3. Perfis iniciais

| Perfil | Responsabilidade geral |
|---|---|
| Administrador | Gerenciar configurações, usuários e permissões autorizadas |
| Pastor | Consultar e administrar informações conforme suas atribuições |
| Líder | Acessar somente informações necessárias ao grupo ou escopo autorizado |
| Membro | Consultar e solicitar atualização dos próprios dados, conforme o fluxo aprovado |

As permissões devem ser aplicadas no backend em todas as operações, não apenas escondendo elementos da interface. O papel de administrador não concede automaticamente acesso irrestrito a registros pastorais sensíveis.

## 4. Roadmap resumido

| Etapa | Duração estimada | Resultado |
|---|---:|---|
| Sprint 0 — Preparação | 2–3 dias | Requisitos, arquitetura e ambiente definidos |
| Sprint 1 — Fundação | 1 semana | Projeto Django, banco, autenticação e permissões |
| Sprint 2 — Design System | 1 semana | Identidade visual e interface responsiva |
| Sprint 3 — Membresia | 1 semana | Cadastro e histórico eclesiástico |
| Sprint 4 — Recadastramento | 1 semana | Formulário e fluxo de validação |
| Sprint 5 — Gestão | 1 semana | Painel, relatórios e auditoria |
| Sprint 6 — Homologação | 3–5 dias, mais correções | Testes, backups, aprovação e publicação controlada |

As durações são estimativas iniciais, não compromissos de entrega. Ajustar conforme a complexidade, a disponibilidade e os resultados dos testes.

---

## 5. Planejamento detalhado das sprints

### Sprint 0 — Preparação e arquitetura

**Duração estimada:** 2–3 dias.

**Objetivo:** fechar as decisões necessárias antes de iniciar a implementação.

**Tarefas**
- [ ] Validar o escopo do MVP com a liderança da IBC.
- [ ] Definir os campos necessários do cadastro e os opcionais.
- [ ] Documentar as regras de membresia e os eventos eclesiásticos.
- [ ] Confirmar os perfis e as permissões.
- [ ] Validar o logotipo e o Design System.
- [ ] Criar o repositório Git e a estrutura inicial de documentação.
- [ ] Definir a arquitetura Django/PostgreSQL.
- [ ] Planejar testes, backups, ambientes e publicação.
- [ ] Documentar a infraestrutura atual sem alterá-la.

**Entregáveis**
- PRD validada.
- Arquitetura técnica inicial.
- Backlog priorizado.
- Repositório preparado.
- Plano de testes e implantação.

**Critérios de conclusão**
- Regras essenciais documentadas.
- Decisões pendentes registradas.
- Nenhuma alteração feita na VPS de produção.

### Sprint 1 — Fundação, autenticação e permissões

**Duração estimada:** 1 semana.

**Objetivo:** criar uma base executável e segura.

**Tarefas**
- [ ] Criar o projeto Django e a configuração de desenvolvimento.
- [ ] Configurar PostgreSQL e migrations.
- [ ] Definir o modelo de usuário personalizado antes da primeira migration.
- [ ] Implementar login, logout e recuperação de senha.
- [ ] Criar os quatro perfis iniciais.
- [ ] Implementar verificações de autorização no backend.
- [ ] Configurar variáveis de ambiente e `.env.example` sem segredos reais.
- [ ] Criar testes de acesso permitido e negado.
- [ ] Documentar instalação e execução local.

**Entregáveis**
- Aplicação executável localmente.
- Autenticação funcional.
- Modelo inicial de usuários e perfis.
- Testes de autorização.

**Critérios de conclusão**
- Usuários não autenticados não acessam páginas protegidas.
- Membros não alteram o próprio perfil de autorização.
- Usuários desativados perdem acesso.
- Testes de permissões passam.

### Sprint 2 — Design System e interface institucional

**Duração estimada:** 1 semana.

**Objetivo:** aplicar a identidade visual oficial da IBC.

**Tarefas**
- [ ] Integrar o logotipo oficial sem distorção.
- [ ] Implementar tokens CSS definidos no Design System.
- [ ] Criar template base, cabeçalho e navegação.
- [ ] Criar componentes de botões, formulários, tabelas, cartões e badges.
- [ ] Implementar mensagens de erro, sucesso e estado vazio.
- [ ] Adaptar telas para celular e desktop.
- [ ] Implementar foco visível e navegação por teclado.
- [ ] Criar configurações iniciais de identidade visual e dados institucionais.

**Entregáveis**
- Layout base Django.
- Biblioteca de componentes reutilizáveis.
- Interface responsiva.
- Configurações iniciais de identidade visual.

**Critérios de conclusão**
- Telas usam tokens centralizados.
- Layout funciona em telas pequenas e grandes.
- Formulários têm labels e erros compreensíveis.
- Configurações visuais não permitem inserir código arbitrário.

### Sprint 3 — Cadastro e gestão da membresia

**Duração estimada:** 1 semana.

**Objetivo:** entregar o cadastro oficial de pessoas e o histórico eclesiástico.

**Tarefas**
- [ ] Criar modelos de pessoas e registros de membresia.
- [ ] Criar formulários de cadastro e edição.
- [ ] Implementar pesquisa e filtros.
- [ ] Criar ficha individual do membro.
- [ ] Implementar vínculos familiares, se aprovados.
- [ ] Registrar recepção, batismo, transferência e desligamento, conforme aplicável.
- [ ] Implementar detecção de possíveis duplicidades.
- [ ] Registrar alterações relevantes em auditoria.
- [ ] Testar permissões de consulta e edição.

**Entregáveis**
- Cadastro funcional.
- Ficha individual.
- Histórico eclesiástico.
- Pesquisa e filtros.

**Critérios de conclusão**
- Secretaria consegue cadastrar, consultar e corrigir registros.
- Não há importação de bases antigas.
- Alterações relevantes são rastreáveis.
- Duplicidades são sinalizadas sem excluir automaticamente registros.

### Sprint 4 — Recadastramento e validação

**Duração estimada:** 1 semana.

**Objetivo:** permitir que membros enviem atualizações e que a secretaria valide os dados.

**Tarefas**
- [ ] Criar formulário responsivo de recadastramento.
- [ ] Validar campos e entradas.
- [ ] Criar estados da solicitação: enviada, em análise, pendente de correção, aprovada e cancelada, conforme aplicável.
- [ ] Criar fila de revisão da secretaria.
- [ ] Implementar aprovação e pedido de correção.
- [ ] Registrar data, responsável e resultado.
- [ ] Evitar reenvios acidentais e solicitações duplicadas.
- [ ] Incluir aviso de privacidade.
- [ ] Definir processo seguro de vinculação à pessoa correta.
- [ ] Testar o fluxo com dados fictícios.

**Entregáveis**
- Formulário de recadastramento.
- Fila de revisão.
- Fluxo de aprovação e correção.
- Registro das atualizações.

**Critérios de conclusão**
- Enviar formulário não cria acesso ao sistema.
- Enviar formulário não altera automaticamente o cadastro oficial sem a validação prevista.
- Um usuário não consegue atualizar o cadastro de outra pessoa apenas conhecendo nome e data de nascimento.
- A secretaria consegue revisar e concluir solicitações.

### Sprint 5 — Painel, relatórios e auditoria

**Duração estimada:** 1 semana.

**Objetivo:** apoiar a gestão administrativa com indicadores confiáveis.

**Tarefas**
- [ ] Criar painel administrativo.
- [ ] Exibir total de membros segundo critérios aprovados.
- [ ] Exibir recadastramentos pendentes.
- [ ] Exibir cadastros incompletos.
- [ ] Implementar filtros e relatórios básicos.
- [ ] Controlar exportações de dados.
- [ ] Registrar ações administrativas relevantes.
- [ ] Criar histórico consultável por usuários autorizados.
- [ ] Testar consistência dos indicadores.

**Entregáveis**
- Dashboard administrativo.
- Relatórios básicos.
- Auditoria consultável.

**Critérios de conclusão**
- Indicadores correspondem aos dados reais.
- Relatórios respeitam permissões.
- Exportações não expõem campos desnecessários.
- Auditoria não permite alteração por usuários comuns.

### Sprint 6 — Homologação, segurança e publicação

**Duração estimada:** 3–5 dias, além do tempo para corrigir falhas.

**Objetivo:** preparar o sistema para uso real.

**Tarefas**
- [ ] Executar todos os testes automatizados.
- [ ] Testar os quatro perfis e tentativas de acesso indevido.
- [ ] Revisar configurações de produção, HTTPS e sessões.
- [ ] Criar backup e testar restauração.
- [ ] Verificar logs para evitar exposição de dados pessoais.
- [ ] Revisar aviso de privacidade e procedimento para solicitações dos titulares.
- [ ] Homologar com usuários autorizados da secretaria.
- [ ] Documentar implantação e rollback.
- [ ] Publicar somente após aprovação explícita.

**Entregáveis**
- Versão candidata à produção.
- Relatório de testes.
- Manual operacional.
- Plano de recuperação e rollback.

**Critérios de conclusão**
- Testes críticos aprovados.
- Restauração de backup comprovada em ambiente de teste.
- Falhas críticas corrigidas.
- Plano de reversão documentado.
- Publicação autorizada pela pessoa responsável.

---

## 6. Backlog priorizado

### P0 — Obrigatório para o MVP
- Autenticação e permissões.
- Cadastro de membros.
- Histórico eclesiástico.
- Recadastramento e validação.
- Auditoria essencial.
- Privacidade e segurança.
- Backups e restauração testada.

### P1 — Importante, se couber no prazo
- Personalização avançada dos formulários.
- Relatórios adicionais.
- Preferências individuais.
- Modelos de documentos institucionais.

### P2 — Pós-MVP
- Pequenos grupos.
- Ministérios e escalas de voluntários.
- Eventos e inscrições.
- Integração com WhatsApp.
- Portal ampliado do membro.
- Assistente de IA.

## 7. Definition of Done

Uma tarefa só será considerada concluída quando:
- [ ] O código estiver versionado no Git.
- [ ] As regras de negócio estiverem documentadas.
- [ ] Os testes relevantes estiverem passando.
- [ ] As permissões tiverem sido testadas no backend.
- [ ] Não houver segredos ou dados reais de membros em testes e logs.
- [ ] A interface estiver validada em desktop e celular.
- [ ] As migrations estiverem versionadas e testadas.
- [ ] A documentação estiver atualizada.
- [ ] A revisão de código tiver sido concluída antes da integração.

## 8. Riscos e medidas preventivas

| Risco | Prevenção |
|---|---|
| Crescimento do escopo | Congelar o escopo do MVP e manter melhorias no backlog |
| Permissões incorretas | Testes automatizados por perfil e revisão de autorização |
| Exposição de dados religiosos | Minimização, acesso restrito e controles de segurança |
| Sobrecarga da VPS | Desenvolver localmente e medir consumo antes da implantação |
| Perda de dados | Backups independentes e testes de restauração |
| Erros do agente de programação | Commits pequenos, revisão de código e testes |
| Duplicidades no recadastramento | Identificação segura, validação e revisão pela secretaria |

## 9. Regras de execução e proteção da produção

1. Desenvolver em ambiente local ou isolado.
2. Utilizar branches e commits pequenos.
3. Não alterar a VPS de produção durante o desenvolvimento sem autorização.
4. Não interromper nem modificar os sistemas Morumbi Festas e Morumbi 3D.
5. Não instalar serviços, executar migrations em produção ou publicar sem autorização explícita.
6. Não compartilhar arquivos `.env`, senhas, tokens ou chaves privadas.
7. Testar mudanças e preparar rollback antes de qualquer implantação.

## 10. Documentos relacionados

- `PRD_IBC_GESTAO.md` — requisitos do produto.
- `DESIGN_SYSTEM_IBC.md` — identidade visual e componentes.
- `design-tokens.css` — tokens visuais.
- `ROADMAP.md` — este documento.
- `CHANGELOG.md` — histórico de alterações.
- `CLAUDE.md` — instruções permanentes para o Claude Code.

## 11. Próxima ação

Iniciar pela Sprint 0: revisar a PRD, confirmar as regras da membresia, validar o Design System e preparar o repositório local. A implementação funcional começa após a aprovação dessas decisões.
