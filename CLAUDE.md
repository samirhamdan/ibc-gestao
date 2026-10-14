# CLAUDE.md — IBC Gestão

Este arquivo define as instruções permanentes para o Claude Code neste repositório. Leia-o antes de planejar ou alterar código.

## 1. Contexto do projeto

O IBC Gestão é um sistema web de gestão da membresia oficial da Igreja Batista Central (IBC), em Campo Grande/MS.

Objetivo inicial: criar uma base nova de membros, permitir cadastro e recadastramento, manter histórico eclesiástico e oferecer acesso conforme os perfis autorizados.

A base será criada do zero. **Não importar cadastros antigos nesta fase.**

## 2. Stack definida

- Python 3.12
- Django
- PostgreSQL
- Django Templates
- HTMX quando simplificar interações sem necessidade de uma SPA
- CSS responsivo e tokens do Design System
- Git para versionamento
- Testes automatizados com as ferramentas apropriadas do Django

Não introduza React, Node.js como backend, microserviços, filas ou serviços adicionais sem justificativa técnica documentada e aprovação.

## 3. Perfis iniciais

Os quatro perfis funcionais são:

1. **Administrador**
2. **Pastor**
3. **Líder**
4. **Membro**

Os nomes podem ser exibidos em português. Implemente permissões explícitas no servidor. Não confie apenas em esconder botões ou links na interface.

Princípios:
- Membros acessam somente seus próprios dados e funções autorizadas.
- Líderes acessam somente informações necessárias ao seu grupo ou escopo autorizado.
- Pastores acessam informações necessárias às atribuições autorizadas.
- Administradores gerenciam usuários e configurações, mas não recebem acesso automático e irrestrito a registros pastorais sensíveis.
- Alterações de perfil e permissões devem ser restritas e auditáveis.

## 4. Diretrizes de arquitetura e código

- Prefira um monólito Django modular e simples para o MVP.
- Antes de criar modelos, revise a PRD, o Roadmap e o Design System.
- Use um modelo de usuário customizado antes da primeira migration, se o projeto ainda não tiver sido migrado.
- Use migrations versionadas para todas as alterações de schema.
- Separe domínio, views, formulários, templates e serviços quando isso melhorar a clareza.
- Evite abstrações genéricas prematuras e dependências desnecessárias.
- Use nomes de código claros e consistentes, preferencialmente em inglês no código e português na interface.
- Trate datas e horários com configuração explícita para `America/Campo_Grande`, após validar a política de fuso horário do projeto.
- Valide toda entrada no servidor.
- Use transações para operações que precisam ser atômicas.
- Não coloque regras de negócio críticas exclusivamente em JavaScript ou templates.
- Não use dados reais de membros em testes; utilize dados fictícios.
- Não faça refatorações amplas fora do escopo da tarefa sem explicar o motivo e pedir aprovação quando houver risco.

## 5. Segurança e LGPD

Os dados de filiação religiosa são dados pessoais sensíveis. A privacidade deve ser considerada desde o desenho.

Obrigatório:
- Coletar somente dados necessários para finalidades definidas.
- Documentar finalidade e base legal para cada tratamento relevante.
- Não presumir que consentimento genérico autoriza todos os usos.
- Separar consentimentos específicos, como uso de imagem, quando aplicável.
- Aplicar autorização no backend a cada operação protegida.
- Proteger formulários contra CSRF e entradas maliciosas.
- Usar o sistema de sessões e autenticação do Django de forma segura.
- Não armazenar senhas em texto puro; utilizar os mecanismos nativos de hash do Django.
- Não registrar senhas, tokens, cookies, segredos ou conteúdo sensível em logs.
- Minimizar dados exibidos em listas, relatórios e notificações.
- Registrar alterações administrativas relevantes sem guardar cópias excessivas de dados sensíveis.
- Criar processo documentado para correção de dados, solicitações dos titulares, conservação e descarte.
- Avaliar riscos de crianças e adolescentes antes de incluir cadastro de menores.
- Validar uploads por tipo, tamanho e conteúdo; nunca confiar somente na extensão.
- Manter dependências atualizadas e revisar vulnerabilidades antes da publicação.

Não afirme conformidade legal completa apenas porque existem caixas de consentimento ou um aviso de privacidade. Os processos e as bases legais devem ser revisados pela instituição e, quando necessário, por assessoria jurídica.

## 6. Banco de dados e integridade

- Usar PostgreSQL como banco previsto para produção.
- Não compartilhar o banco de dados dos sistemas Morumbi Festas ou Morumbi 3D.
- Não reutilizar credenciais, chaves ou variáveis de ambiente de outros projetos.
- Criar restrições de integridade no banco quando apropriado, além de validações na aplicação.
- Criar índices para campos usados frequentemente em buscas, após avaliar o modelo.
- Preservar histórico e rastreabilidade de registros eclesiásticos.
- Evitar exclusão definitiva de registros que devam ser preservados; definir regras de retenção e correção.
- Nunca executar migrations destrutivas em produção sem revisão, backup verificado, plano de rollback e autorização explícita.

## 7. Interface e Design System

A interface deve seguir `docs/DESIGN_SYSTEM_IBC.md` e os tokens em `static/css/design-tokens.css`, ajustando os caminhos à estrutura real do repositório.

- Utilizar o logotipo oficial fornecido, preservando proporção e integridade.
- Não inventar uma marca substituta nem redesenhar o logotipo.
- Usar os tokens CSS como fonte central das cores, espaçamentos, bordas e foco.
- A cor institucional inicial é `#038EA8`, sujeita à validação institucional.
- Criar componentes consistentes para formulários, botões, tabelas, cartões, alertas e estados vazios.
- Garantir responsividade em celular e desktop.
- Manter labels visíveis, mensagens de erro claras e foco de teclado.
- Buscar conformidade com WCAG 2.2 AA e testar contraste.
- Não usar apenas cor para comunicar status.
- Não permitir que administradores insiram CSS, HTML ou JavaScript arbitrário por configurações.

## 8. Personalização do sistema

A aplicação poderá permitir que administradores autorizados configurem:
- Logotipo e identidade visual, respeitando validações.
- Nome e contatos institucionais.
- Preferências gerais aprovadas.
- Campos opcionais de formulários previamente definidos.
- Modelos de documentos e versões de avisos.

Configurações globais devem ser separadas de preferências individuais. Toda alteração relevante deve ser auditável. Configurações não podem desativar validações essenciais, controles de acesso ou proteções legais.

## 9. Testes e qualidade

Para cada funcionalidade:
- Criar ou atualizar testes unitários e de integração.
- Testar permissões positivas e negativas para os quatro perfis.
- Testar entradas inválidas, duplicidades e falhas esperadas.
- Testar formulários, transições de estado e integridade do banco.
- Executar a suíte de testes relevante antes de concluir.
- Não remover ou enfraquecer testes para fazer uma implementação passar.
- Corrigir a causa dos erros, não mascarar falhas.
- Informar claramente quais testes foram executados e quais não foram.

Para fluxos sensíveis, incluir testes que comprovem que um usuário não consegue acessar dados de outra pessoa alterando IDs ou URLs.

## 10. Git e processo de trabalho

Antes de alterar código:
1. Inspecione a estrutura do projeto e o estado do Git.
2. Leia os documentos relevantes.
3. Resuma o plano de implementação.
4. Identifique os arquivos que serão alterados.
5. Verifique se há mudanças locais do usuário e preserve-as.

Durante o trabalho:
- Faça alterações pequenas e coerentes.
- Evite sobrescrever mudanças existentes.
- Não execute comandos destrutivos sem autorização.
- Não faça commit, push ou deploy sem solicitação ou autorização explícita.
- Atualize a documentação quando as regras ou a arquitetura mudarem.

Ao concluir:
- Resuma as alterações.
- Liste os arquivos afetados.
- Informe os testes executados e resultados.
- Liste pendências, riscos e próximos passos.
- Não declare testes, backups ou deploys realizados se não foram executados.

## 11. Proteção da VPS e dos sistemas existentes

A VPS atual hospeda Morumbi Festas e Morumbi 3D. A continuidade desses sistemas é requisito obrigatório.

**Sem autorização explícita, não:**
- Instale pacotes ou serviços na VPS.
- Reinicie ou pare containers, processos ou serviços.
- Altere Caddy, proxy reverso, DNS, firewall ou portas.
- Altere bancos, volumes, configurações ou arquivos dos sistemas existentes.
- Execute migrations em produção.
- Publique o IBC Gestão ou altere rotas públicas.
- Remova arquivos, imagens, containers, volumes ou backups.

Desenvolva localmente ou em ambiente isolado sempre que possível. Antes de qualquer implantação autorizada, documente o impacto, confirme os backups, prepare rollback e defina como validar a saúde dos sistemas existentes.

Nunca leia, imprima ou compartilhe arquivos `.env` completos, senhas, tokens, chaves privadas ou dados de clientes.

## 12. Documentação de referência

Antes de tomar decisões de produto, consulte os arquivos que existirem no repositório:
- `docs/PRD_IBC_GESTAO.md`
- `docs/ROADMAP.md`
- `docs/DESIGN_SYSTEM_IBC.md`
- `docs/CHANGELOG.md`
- `docs/architecture.md`

Se os nomes ou caminhos forem diferentes, localize os documentos existentes. Não invente que um documento foi lido se ele não estiver disponível.

## 13. Definition of Done

Uma tarefa está concluída somente quando:
- A implementação atende aos critérios de aceitação.
- As permissões foram testadas no backend.
- Os testes relevantes passam.
- Não há segredos ou dados reais nos arquivos de teste.
- A interface segue o Design System.
- As migrations e a documentação estão atualizadas, quando aplicável.
- Os riscos e limitações são relatados.
- Nenhuma alteração não autorizada foi feita na VPS ou nos sistemas Morumbi.
