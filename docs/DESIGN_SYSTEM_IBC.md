# Design System — IBC Gestão
**Versão:** 1.0  
**Produto:** Sistema de Gestão da Igreja Batista Central — Campo Grande/MS  
**Implementação prevista:** Python 3.12 + Django + Django Templates + HTMX + CSS

## 1. Objetivo
Estabelecer uma linguagem visual consistente, acessível e personalizável para o IBC Gestão. O sistema deve usar a identidade visual oficial da Igreja Batista Central e permitir que administradores autorizados alterem configurações institucionais permitidas sem modificar o código-fonte.

O arquivo `assets/ibc-logo-oficial.png` é o logotipo fornecido pela igreja. Preservar o arquivo original; não redesenhar, distorcer, recolorir nem aplicar efeitos ao logotipo.

## 2. Identidade visual

A cor principal foi estimada a partir dos pixels do logotipo enviado.

| Token | Valor inicial | Uso |
|---|---|---|
| `--ibc-primary` | `#038EA8` | Cor institucional, links, elementos de marca |
| `--ibc-primary-hover` | `#02758B` | Hover e estados ativos |
| `--ibc-primary-dark` | `#075B6B` | Texto/elementos fortes sobre fundos claros |
| `--ibc-primary-soft` | `#E6F5F8` | Fundo suave, destaque discreto |
| `--ibc-text` | `#18252B` | Texto principal |
| `--ibc-text-muted` | `#5B6B72` | Texto secundário |
| `--ibc-border` | `#D9E3E6` | Bordas e divisores |
| `--ibc-surface` | `#FFFFFF` | Superfícies |
| `--ibc-background` | `#F5F8F9` | Fundo geral |
| `--ibc-success` | `#217346` | Sucesso |
| `--ibc-warning` | `#8A5A00` | Atenção |
| `--ibc-danger` | `#B42318` | Erro e ações destrutivas |

A cor principal deve ser validada visualmente pela equipe de comunicação da IBC antes da publicação. Não usar a cor institucional como único indicador de estado.

## 3. Tipografia
- Fonte principal: `Inter`, com fallback para `system-ui`, `-apple-system`, `Segoe UI`, sans-serif.
- Corpo: 16px / line-height 1.5.
- Texto auxiliar: 14px / line-height 1.45.
- Título de página: 28–32px, peso 700.
- Título de seção: 20–24px, peso 650–700.
- Rótulos de formulário: 14–16px, peso 600.
- Evitar textos longos em caixa alta.

Se a fonte Inter for carregada externamente, garantir alternativa local e avaliar política de privacidade/rede. Preferir hospedar arquivos de fonte localmente em produção.

## 4. Espaçamento, raios e elevação
Escala de espaçamento baseada em múltiplos de 4px:
- `4px`: detalhe mínimo
- `8px`: elementos próximos
- `12px`: espaçamento compacto
- `16px`: espaçamento padrão
- `24px`: separação entre blocos
- `32px`: seções
- `48px`: áreas amplas

Raios:
- Controles: 8px
- Cards: 12px
- Modais e painéis principais: 16px
- Pílulas: 999px

Sombras discretas, apenas para menus, popovers e modais. Evitar sombras fortes em todas as superfícies.

## 5. Layout e responsividade
- Mobile-first; suportar telas a partir de 320px.
- Barra lateral recolhível em telas pequenas.
- Em celular, tabelas devem oferecer visualização adaptada ou rolagem horizontal claramente indicada.
- Formulários longos devem ser divididos em seções com progresso e salvamento seguro quando aplicável.
- Conteúdo principal com largura confortável, espaçamento consistente e foco visível.
- Não depender exclusivamente de hover para revelar ações.

## 6. Componentes

### Botões
- Primário: fundo `--ibc-primary`, texto branco; usar apenas para a ação principal.
- Secundário: fundo branco, borda `--ibc-border`, texto `--ibc-text`.
- Destrutivo: fundo/realce `--ibc-danger`, com confirmação explícita.
- Todos os botões devem apresentar estados hover, focus-visible, disabled e loading.

### Formulários
- Rótulos sempre visíveis; não usar placeholder como único rótulo.
- Mensagens de erro específicas, junto ao campo.
- Indicar campos obrigatórios.
- Preservar dados preenchidos quando a validação falhar.
- Campos sensíveis devem ter finalidade e acesso definidos.

### Cards e tabelas
- Cards com título, conteúdo e ação claramente identificados.
- Tabelas com cabeçalhos semânticos, paginação e estados vazio/carregando/erro.
- Evitar exibir dados pessoais além do necessário na listagem.

### Status
Usar texto e ícone, além de cor:
- Ativo
- Pendente
- Em análise
- Inativo
- Requer atenção

Não confundir situação de recadastramento com situação eclesiástica da pessoa.

### Navegação
Menu principal inicial:
- Painel
- Membros
- Recadastramento
- Histórico de membresia
- Usuários e permissões (restrito)
- Configurações (restrito)

Módulos de pequenos grupos, ministérios e eventos podem ser adicionados posteriormente.

## 7. Personalização administrável
Criar área de configurações para administradores autorizados com:
- Nome institucional exibido.
- Logotipo e favicon.
- Cor principal, validada por formato hexadecimal.
- Preferência de tema, se implementada.
- Dados de contato institucional.
- Preferências de exibição que não alterem regras de negócio.

Regras:
1. Valores padrão versionados no código e usados quando não houver configuração salva.
2. Configurações institucionais armazenadas no banco; preferências pessoais em registro separado.
3. Auditar quem alterou configurações globais, quando e quais campos foram modificados.
4. Validar tipo, tamanho e conteúdo de uploads; limitar extensões e dimensões.
5. Não permitir que configurações editáveis alterem permissões de segurança, SQL, código, credenciais ou configurações do servidor.
6. Restringir alterações a usuários autorizados no backend.
7. A mudança de tema não pode reduzir contraste abaixo dos níveis de acessibilidade.
8. Prever botão de restaurar valores padrão.

## 8. Acessibilidade
- Buscar conformidade WCAG 2.2 nível AA.
- Contraste mínimo de 4.5:1 para texto normal e 3:1 para texto grande e componentes gráficos relevantes.
- Navegação integral por teclado e foco claramente visível.
- Usar HTML semântico e rótulos associados aos campos.
- Erros anunciados de forma compreensível e não identificados apenas pela cor.
- Respeitar `prefers-reduced-motion`.
- Alvos de toque confortáveis, idealmente próximos de 44×44px.

## 9. Privacidade e segurança visual
- Não expor listas de membros em dashboards públicos.
- Não mostrar dados sensíveis em notificações, URLs ou logs desnecessários.
- Ocultar informações pessoais em tabelas quando não forem necessárias.
- Separar cadastro comum de registros pastorais sensíveis.
- O consentimento de imagem deve ser tratado separadamente do cadastro de membresia.
- Restringir exportações e registrar operações administrativas relevantes.

## 10. Diretrizes Django
- Organizar componentes em templates reutilizáveis: `base.html`, `partials/sidebar.html`, `partials/messages.html`, `partials/form_field.html`.
- Usar CSS com variáveis de design; evitar estilos inline duplicados.
- Guardar configurações institucionais em modelo explícito, por exemplo `InstitutionSettings`, com validação no servidor.
- Guardar preferências por usuário em modelo separado.
- Usar Django Forms/ModelForms para validação.
- Aplicar autorização em views e serviços; esconder links no template não é controle de acesso.
- Implementar testes para permissões, uploads, restauração de padrões e validação de configurações.
- Nunca colocar segredos no repositório; usar variáveis de ambiente.

## 11. Critérios de aceitação
- O logotipo oficial aparece sem distorção nas áreas previstas.
- As páginas usam tokens consistentes de cor, tipografia, espaçamento e componentes.
- A interface funciona em celular e desktop.
- Campos e botões são acessíveis por teclado.
- Administrador autorizado pode alterar a identidade visual permitida.
- Usuários sem permissão não conseguem alterar configurações por requisição direta.
- Configurações inválidas são rejeitadas.
- É possível restaurar valores padrão.
- Alterações globais ficam auditadas.
- Personalização não contorna regras de negócio, segurança ou LGPD.

## 12. Implementação sugerida
1. Adicionar o logotipo em `static/ibc/img/ibc-logo-oficial.png`.
2. Criar `static/ibc/css/design-tokens.css` a partir do arquivo incluído.
3. Criar layout base e componentes reutilizáveis.
4. Implementar a página de configurações após autenticação e permissões.
5. Validar contraste, responsividade e testes automatizados antes da publicação.
