# PRD — IBC Gestão
**Versão:** 1.0  
**Status:** Especificação inicial para validação  
**Produto:** Sistema de gestão da membresia oficial da Igreja Batista Central (IBC)  
**Localidade institucional:** Campo Grande/MS  
**Stack prevista:** Python 3.12, Django, PostgreSQL, Django Templates, HTMX e CSS responsivo  
**Agente de desenvolvimento:** Claude Code

---

## 1. Resumo executivo

O IBC Gestão será uma aplicação web para administrar a membresia oficial da Igreja Batista Central (IBC). A primeira versão criará uma nova base de dados, sem importar registros antigos, e oferecerá cadastro, recadastramento, histórico eclesiástico, autenticação, controle de acesso e ferramentas administrativas básicas.

O sistema deverá ser seguro, responsivo, simples de manter e preparado para receber novos módulos em versões futuras. A infraestrutura atual também hospeda Morumbi Festas e Morumbi 3D; qualquer plano de hospedagem deverá preservar integralmente a disponibilidade desses sistemas.

## 2. Problema e oportunidade

A igreja precisa de uma base organizada e atualizada dos membros, com processos claros para coleta, validação, consulta e correção de informações. Uma aplicação centralizada pode reduzir duplicidades, formulários dispersos, inconsistências e acesso indevido a dados.

## 3. Objetivos do produto

1. Criar uma base oficial nova de pessoas e membresia.
2. Permitir que usuários autorizados cadastrem e mantenham registros.
3. Implementar recadastramento com revisão pela secretaria.
4. Registrar eventos e alterações relevantes do histórico eclesiástico.
5. Restringir dados conforme função e necessidade de acesso.
6. Aplicar identidade visual oficial da IBC, com personalização administrativa controlada.
7. Estabelecer segurança, privacidade, auditoria e recuperação de dados desde o início.
8. Entregar uma base técnica que possa evoluir para módulos de pequenos grupos, ministérios, eventos e comunicação.

## 4. Não objetivos do MVP

Não fazem parte da primeira versão:
- Importação de planilhas ou bancos antigos.
- Gestão financeira ou contabilidade.
- Aplicativo móvel nativo.
- Integração automática com WhatsApp.
- Gestão completa de visitantes, evangelismo ou discipulado.
- EAD ou LMS.
- Inteligência artificial para avaliar membros.
- Gestão de escalas, eventos ou ministérios, além do necessário para estruturar futuras extensões.
- Publicação na VPS antes da análise técnica e autorização explícita.

Esses itens poderão entrar em versões posteriores após validação do MVP.

## 5. Usuários e perfis

O MVP terá quatro perfis funcionais:

### 5.1 Administrador
- Gerenciar contas e ativação de usuários.
- Atribuir perfis e permissões conforme política aprovada.
- Administrar configurações institucionais.
- Acessar cadastros e relatórios somente conforme permissões e finalidade autorizadas.
- Consultar auditoria administrativa.

### 5.2 Pastor
- Consultar e administrar informações necessárias às suas atribuições autorizadas.
- Consultar informações de membresia e relatórios conforme permissões definidas.
- Não recebe automaticamente acesso irrestrito a conteúdos pastorais sensíveis.

### 5.3 Líder
- Acessar apenas dados necessários ao seu grupo ou escopo formalmente autorizado.
- Não pode consultar a base completa por padrão.
- Não pode alterar perfis, permissões globais ou configurações institucionais.

### 5.4 Membro
- Consultar informações próprias disponibilizadas pelo sistema.
- Solicitar ou enviar atualização dos próprios dados pelo fluxo aprovado.
- Não pode consultar dados privados de outros membros.
- Não pode modificar o próprio perfil de autorização.

**Requisito transversal:** autorização deve ser verificada no servidor para cada operação. Ocultar botões na interface não constitui controle de acesso suficiente.

## 6. Escopo funcional do MVP

### RF-01 — Autenticação
O sistema deve permitir login individual e logout seguro. Deve oferecer recuperação de senha por mecanismo seguro, se houver serviço de e-mail configurado. Contas iniciais devem ser provisionadas por procedimento administrativo, sem cadastro público com privilégios automáticos.

**Critérios de aceitação**
- Páginas protegidas exigem autenticação.
- Erros de autenticação não revelam se uma conta específica existe.
- Sessões e cookies usam configuração segura em produção.
- Contas desativadas não podem iniciar novas sessões e devem ter o acesso existente revogado conforme o mecanismo adotado.

### RF-02 — Gestão de usuários e perfis
O administrador autorizado pode criar, ativar, desativar e atribuir perfis a usuários. Mudanças de perfil devem ser registradas.

**Critérios de aceitação**
- Membro, por requisição direta, não consegue elevar o próprio privilégio.
- Operações administrativas são verificadas no backend.
- Mudanças de acesso ficam auditadas.

### RF-03 — Cadastro de pessoas
O sistema deve permitir cadastrar pessoas com identificador interno único, nome completo e campos adicionais aprovados pela igreja.

Campos potenciais, sujeitos à revisão de necessidade:
- Nome completo.
- Data de nascimento, quando necessária.
- Telefone e e-mail.
- Endereço, quando necessário.
- Contato de emergência, se houver finalidade definida.
- Informações eclesiásticas pertinentes.
- Situação cadastral.
- Data da última atualização.

**Critérios de aceitação**
- Campos obrigatórios e opcionais são definidos e documentados.
- Validações ocorrem no servidor.
- O sistema sinaliza possíveis duplicidades, sem excluir registros automaticamente.
- Busca e listagem respeitam as permissões do usuário.
- Campos desnecessários não são coletados por padrão.

### RF-04 — Ficha individual
Cada pessoa deve ter uma ficha que apresente os dados permitidos ao usuário autenticado e autorizado.

**Critérios de aceitação**
- Acesso à ficha de outra pessoa é negado quando não autorizado, inclusive se o ID for alterado na URL.
- Dados sensíveis não aparecem em listas ou resumos sem necessidade.
- Alterações relevantes são registradas na auditoria.

### RF-05 — Histórico de membresia
O sistema deve registrar eventos eclesiásticos definidos pela IBC, como recepção, batismo, transferência, desligamento e falecimento, quando aplicável e formalmente registrado.

Cada evento deve guardar, conforme aplicável:
- Pessoa relacionada.
- Tipo de evento.
- Data do evento e data do registro.
- Responsável pelo lançamento.
- Observação administrativa estritamente necessária.
- Referência documental, quando pertinente.

**Critérios de aceitação**
- O histórico mantém rastreabilidade.
- Correções preservam evidência da alteração.
- Eventos não alteram automaticamente a situação da pessoa sem regra institucional definida.
- A visualização respeita permissões.

### RF-06 — Recadastramento
O sistema deve permitir a submissão de uma solicitação de atualização e sua revisão pela secretaria ou pessoa designada.

Estados iniciais:
- Não iniciada.
- Enviada.
- Em análise.
- Pendente de correção.
- Aprovada.
- Cancelada, quando aplicável.

**Critérios de aceitação**
- Enviar formulário não concede acesso à base geral.
- Uma solicitação não altera automaticamente o cadastro oficial sem a validação prevista.
- A vinculação da solicitação à pessoa é segura; nome e data de nascimento isoladamente não são prova suficiente de identidade.
- A secretaria pode aprovar, rejeitar ou pedir correção conforme fluxo aprovado.
- Reenvios acidentais são tratados sem duplicar solicitações.
- Data, responsável e resultado da revisão ficam registrados.

### RF-07 — Painel administrativo
O painel deve apresentar indicadores úteis, por exemplo:
- Total de membros segundo definição institucional aprovada.
- Solicitações pendentes.
- Recadastramentos aprovados.
- Cadastros incompletos.
- Atualizações recentes.

**Critérios de aceitação**
- Indicadores são derivados dos registros reais.
- Definições e filtros são claros.
- Os indicadores não inferem condição espiritual nem fazem julgamento pastoral.
- Cada usuário visualiza somente os dados agregados permitidos ao seu perfil.

### RF-08 — Pesquisa e filtros
O sistema deve permitir pesquisar pessoas e filtrar registros conforme permissões, com paginação para listas extensas.

**Critérios de aceitação**
- Resultados não revelam dados além do necessário.
- Filtros são validados no servidor.
- Paginação e ordenação não permitem contornar autorização.

### RF-09 — Configurações institucionais e personalização
O administrador autorizado pode configurar itens permitidos:
- Nome exibido da igreja.
- Logotipo e favicon, com validação de arquivo.
- Cor primária institucional e opções visuais previamente definidas.
- Dados de contato institucionais.
- Preferências regionais aprovadas.
- Ativação de campos opcionais previamente definidos.
- Modelos de documentos e versões de avisos.

**Critérios de aceitação**
- Configurações inválidas são rejeitadas.
- Alterações relevantes são auditadas.
- Configurações não permitem inserir código arbitrário.
- Personalização não desativa validações, controles de acesso ou requisitos de segurança.
- O logotipo oficial fornecido é preservado sem distorção.

### RF-10 — Auditoria
O sistema deve registrar ações relevantes, como criação e edição de pessoas, alterações de situação eclesiástica, mudanças de perfil, aprovações de recadastramento e exportações.

**Critérios de aceitação**
- Registros de auditoria incluem autor, ação, data/hora e referência ao objeto, conforme aplicável.
- Não são registrados senhas, tokens ou conteúdo excessivo de dados sensíveis.
- Usuários comuns não podem modificar ou excluir registros de auditoria.
- A política de retenção da auditoria será definida pela igreja.

### RF-11 — Relatórios e exportações básicas
Permitir relatórios administrativos estritamente necessários, com exportação apenas para perfis autorizados.

**Critérios de aceitação**
- Exportação exige autorização explícita.
- O sistema exporta somente os campos necessários ao relatório.
- Ações de exportação são auditadas.
- Não há exportação pública nem links permanentes desprotegidos.

### RF-12 — Aviso de privacidade e direitos dos titulares
O sistema deve exibir aviso de privacidade claro, explicar finalidades e canais de contato e apoiar o tratamento de pedidos de correção e demais direitos aplicáveis.

**Critérios de aceitação**
- O aviso corresponde aos tratamentos realmente implementados.
- Consentimentos específicos, como uso de imagem, são separados quando aplicáveis.
- Não se presume que consentimento genérico autorize todo tratamento.
- A instituição documenta as bases legais e os períodos de retenção com assessoria adequada quando necessário.

## 7. Requisitos não funcionais

### RNF-01 — Segurança
- HTTPS obrigatório em produção.
- Proteção CSRF, XSS e contra injeção por meio das práticas e ferramentas adequadas do Django.
- Hash de senhas com os mecanismos nativos do Django.
- Segredos apenas em variáveis de ambiente ou mecanismo apropriado.
- Nenhum segredo em Git, logs ou documentação.
- Dependências revisadas e atualizadas.
- Mensagens de erro não expõem stack traces em produção.

### RNF-02 — Privacidade
- Minimização de dados.
- Acesso baseado em função e escopo.
- Dados que revelem filiação religiosa tratados como sensíveis.
- Política documentada de conservação, correção e descarte.
- Dados de menores exigem avaliação específica antes de serem coletados.

### RNF-03 — Usabilidade e acessibilidade
- Interface responsiva em celular, tablet e desktop.
- Labels visíveis, mensagens de erro compreensíveis e foco de teclado.
- Contraste e componentes revisados com meta WCAG 2.2 AA.
- A cor não deve ser o único meio de indicar status.

### RNF-04 — Manutenibilidade
- Código modular Django.
- Migrations versionadas.
- Testes automatizados.
- Documentação técnica atualizada.
- Dependências justificadas e limitadas.
- Git com alterações pequenas e revisáveis.

### RNF-05 — Desempenho e recursos
- Paginação em listagens.
- Índices definidos com base em consultas reais.
- Evitar tarefas pesadas desnecessárias no MVP.
- Medir consumo antes de implantar na VPS existente.

### RNF-06 — Backup e recuperação
- Definir frequência, retenção, local e responsáveis.
- Manter cópias protegidas e separadas do ambiente principal.
- Testar restauração antes da entrada em produção.
- Documentar RPO/RTO com a liderança conforme criticidade e recursos disponíveis.

### RNF-07 — Compatibilidade operacional
- Desenvolver em ambiente local ou isolado.
- Não depender de alterar os sistemas Morumbi Festas ou Morumbi 3D.
- Hospedagem final será definida após o diagnóstico técnico.
- Nenhuma alteração na VPS de produção sem autorização explícita.

## 8. Modelo conceitual inicial de dados

As entidades abaixo são uma proposta inicial, a validar durante a Sprint 0:
- `User`: autenticação e credenciais.
- `Profile`: dados de perfil e relação com pessoa.
- `Person`: dados cadastrais.
- `MembershipEvent`: eventos do histórico eclesiástico.
- `RecadastroRequest`: solicitações de atualização e estados de revisão.
- `Family` e `FamilyMembership`: vínculos familiares, se aprovados.
- `InstitutionSettings`: configurações institucionais permitidas.
- `ConsentRecord`: consentimentos específicos, quando aplicáveis.
- `AuditEvent`: trilha de ações relevantes.

Uma pessoa pode existir sem possuir conta de acesso. Os registros eclesiásticos devem ser separados dos dados de autenticação. Conteúdos pastorais sensíveis não fazem parte da ficha cadastral comum do MVP.

## 9. Regras de negócio iniciais

1. A base começa vazia, sem importação de registros antigos.
2. Cada pessoa recebe um identificador interno único.
3. A situação de membresia e o estado do recadastramento são conceitos distintos.
4. Enviar recadastramento não significa que a atualização foi aprovada.
5. Duplicidades são sinalizadas para revisão, não removidas automaticamente.
6. Alterações eclesiásticas preservam rastreabilidade.
7. O perfil de acesso não substitui a validação do escopo da pessoa que consulta o dado.
8. Campos sensíveis não serão obrigatórios sem finalidade e aprovação definidas.
9. Uso de imagem deve ser tratado separadamente do cadastro de membresia, quando aplicável.
10. Regras eclesiásticas específicas devem ser aprovadas pela liderança da IBC antes da implementação.

## 10. Fora do escopo técnico e limites operacionais

- Não instalar pacotes ou serviços na VPS durante o desenvolvimento local.
- Não reiniciar ou parar containers, processos ou serviços.
- Não alterar Caddy, proxy reverso, DNS, firewall ou portas.
- Não alterar bancos, volumes, configurações ou arquivos de Morumbi Festas e Morumbi 3D.
- Não executar migrations em produção sem revisão, backup verificado, plano de rollback e autorização.
- Não publicar a aplicação sem autorização explícita.
- Não ler ou compartilhar arquivos `.env`, senhas, tokens ou chaves privadas.

## 11. Critérios de aceitação do MVP

O MVP poderá ser submetido à aprovação quando:
1. Os quatro perfis estiverem implementados e testados.
2. O cadastro e a edição de pessoas funcionarem.
3. A pesquisa e os filtros respeitarem permissões.
4. O histórico eclesiástico preservar rastreabilidade.
5. O recadastramento tiver fluxo de envio, revisão, correção e aprovação.
6. As duplicidades forem sinalizadas.
7. A auditoria registrar ações relevantes.
8. As configurações institucionais forem validadas e protegidas.
9. Os testes críticos de autorização forem aprovados.
10. O aviso de privacidade e procedimentos institucionais forem revisados.
11. O backup tiver restauração testada em ambiente de teste.
12. A implantação tiver plano de rollback e aprovação explícita.

## 12. Dependências e decisões pendentes

- Confirmar campos obrigatórios e opcionais com a secretaria.
- Definir regras formais da membresia e quais eventos serão registrados.
- Definir como a identidade do membro será confirmada no recadastramento.
- Definir quem pode revisar e aprovar solicitações.
- Definir o escopo de acesso dos líderes.
- Definir política de retenção e processo de atendimento aos titulares.
- Confirmar cores e variantes oficiais do logotipo com a IBC.
- Concluir inventário e avaliação da VPS antes da decisão de hospedagem.
- Definir serviço de e-mail, se recuperação de senha e notificações forem necessárias.

## 13. Relação com o roadmap

O trabalho deve seguir `docs/ROADMAP.md`:
- Sprint 0: validar requisitos, arquitetura, campos e regras.
- Sprint 1: fundação, autenticação e permissões.
- Sprint 2: Design System e interface.
- Sprint 3: cadastro e histórico da membresia.
- Sprint 4: recadastramento.
- Sprint 5: painel, relatórios e auditoria.
- Sprint 6: homologação, segurança, backups e publicação controlada.

## 14. Definition of Done

Uma funcionalidade só está concluída quando:
- Atende aos critérios de aceitação.
- Tem testes relevantes aprovados.
- As permissões são aplicadas no backend.
- Não utiliza dados reais em testes.
- A documentação está atualizada.
- Não expõe segredos nem dados pessoais indevidos.
- Não causou alterações não autorizadas na VPS ou nos sistemas existentes.

---

**Nota:** este PRD é a especificação inicial do produto. As decisões de base legal, retenção, consentimentos e processos institucionais devem ser validadas pela IBC e por assessoria jurídica adequada antes da entrada em produção.
