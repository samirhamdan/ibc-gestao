# Decisões pendentes — Sprint 0

Lista do que precisa ser respondido pela liderança e pela secretaria da IBC
antes de começar a programar (Sprint 1). Cada resposta vira regra na PRD
(`docs/PRD_IBC_GESTAO.md`, ainda não escrita).

Marque `[x]` quando decidir e anote a resposta logo abaixo da pergunta.

---

## 1. Escopo do MVP

- [ ] O MVP é só membresia (cadastro, recadastramento, histórico, painel)?
      Pequenos grupos, ministérios, eventos e WhatsApp ficam para depois, como
      diz o roadmap?
- [ ] Quem, na liderança, aprova o escopo e assina a homologação final?
- [ ] Existe data-alvo (ex.: campanha de recadastramento) que define o prazo?

## 2. Cadastro da pessoa

Para cada campo, decidir: **obrigatório**, **opcional** ou **não coletar**, e
**para que serve** (a LGPD exige finalidade).

| Campo | Obrigatório? | Para que serve | Quem pode ver |
|---|---|---|---|
| Nome completo | | | |
| Nome social / como prefere ser chamado | | | |
| Data de nascimento | | | |
| Sexo | | | |
| Estado civil | | | |
| CPF | | | |
| RG | | | |
| Telefone / WhatsApp | | | |
| E-mail | | | |
| Endereço completo | | | |
| Bairro / região (para grupos no futuro) | | | |
| Profissão | | | |
| Escolaridade | | | |
| Foto | | | |
| Nome do cônjuge / filhos (vínculo familiar) | | | |
| Igreja de origem | | | |

- [ ] O CPF é realmente necessário? Se for só para evitar duplicidade, talvez
      dê para usar nome + data de nascimento + telefone e não guardar o CPF.
- [ ] Haverá foto? Se sim, o uso de imagem precisa de consentimento separado.
- [ ] Vínculos familiares entram no MVP?

## 3. Menores de idade

- [ ] Crianças e adolescentes serão cadastrados no MVP?
- [ ] Se sim: a partir de que idade, quem autoriza (responsável legal) e quem
      pode ver esses dados?

O CLAUDE.md exige avaliar esse risco antes de incluir menores. A sugestão é
**deixar menores fora do MVP** e tratar depois.

## 4. Regras da membresia

- [ ] Quais são as situações possíveis de uma pessoa? Sugestão inicial:
      *Membro ativo*, *Membro inativo*, *Congregado (frequenta, não é membro)*,
      *Transferido*, *Desligado*, *Falecido*.
- [ ] Quais eventos entram no histórico? Sugestão: *Recepção por batismo*,
      *Recepção por carta de transferência*, *Recepção por aclamação /
      profissão de fé*, *Batismo*, *Transferência para outra igreja*,
      *Desligamento*, *Falecimento*, *Reintegração*.
- [ ] Cada evento precisa de quê? (data, número da ata / assembleia, igreja de
      origem ou destino, observação)
- [ ] Quem pode registrar cada evento? Só a secretaria? O pastor aprova?
- [ ] Um evento registrado errado pode ser corrigido? Sugestão: nunca apagar;
      registrar a correção com motivo, quem fez e quando.
- [ ] O que conta como "total de membros" no painel?

## 5. Perfis e permissões

O roadmap prevê **Administrador, Pastor, Líder e Membro**. Faltam respostas:

- [ ] **Secretaria** é um perfil separado? Ela aparece em quase todo o fluxo
      (cadastra, revisa recadastramento, corrige), mas não está na lista de
      perfis. Sugestão: criar o perfil *Secretaria*, ou dizer qual dos quatro
      faz esse papel.
- [ ] O que é o "escopo" do **Líder** no MVP, se pequenos grupos e ministérios
      só vêm depois? Sugestão: no MVP o Líder não acessa a membresia, ou o
      perfil fica para quando os grupos existirem.
- [ ] O **Membro** terá login no MVP, ou só preenche o formulário de
      recadastramento? (O roadmap diz que enviar o formulário não cria acesso.)
- [ ] O que é "registro pastoral sensível"? Haverá anotações pastorais no MVP?
      Se sim, só Pastor vê, e o Administrador não.
- [ ] Uma pessoa pode ter mais de um perfil (ex.: Pastor e Administrador)?
- [ ] Quem cria usuários e quem muda o perfil de alguém?

## 6. Recadastramento

- [ ] Como garantir que quem preenche é mesmo aquela pessoa? Opções:
      a) link individual enviado pela secretaria (WhatsApp/e-mail), que vale
         uma vez e expira;
      b) formulário aberto, e a secretaria confere tudo antes de aceitar;
      c) só com login.
      Sugestão: **a**. O roadmap exige que ninguém consiga alterar o cadastro
      de outra pessoa só sabendo nome e data de nascimento.
- [ ] Pessoas que ainda não estão na base (é uma base nova) usam o mesmo
      formulário? Sugestão: sim, e a secretaria decide se vira cadastro novo
      ou se junta a um existente.
- [ ] Quais situações a solicitação pode ter? Sugestão: *Enviada*,
      *Em análise*, *Pendente de correção*, *Aprovada*, *Cancelada*.
- [ ] Quem avisa a pessoa quando falta corrigir algo, e por qual canal?

## 7. Privacidade (LGPD)

- [ ] Quem é o responsável pelos dados na IBC (encarregado / contato para
      pedidos dos titulares)?
- [ ] Qual o texto do aviso de privacidade? Precisa de revisão jurídica.
- [ ] Por quanto tempo guardar dados de quem saiu da igreja ou faleceu?
- [ ] Exportação de listas (planilha) é permitida? Para quem? Quais campos?

## 8. Identidade visual

- [ ] A equipe de comunicação aprova a cor `#038EA8` e o logotipo enviado?
- [ ] Ajustes de acessibilidade encontrados na revisão dos tokens (contraste
      medido pela regra WCAG 2.2 AA):

  | Combinação | Contraste | Mínimo | Situação |
  |---|---:|---:|---|
  | Texto branco sobre `#038EA8` (botão principal) | 3,86 | 4,5 | não passa |
  | Link `#038EA8` sobre fundo branco | 3,86 | 4,5 | não passa |
  | Texto branco sobre `#02758B` (hover) | 5,36 | 4,5 | passa |
  | Borda dos campos `#D9E3E6` sobre branco | 1,31 | 3,0 | não passa |
  | Tema escuro: texto branco sobre `#37B5CB` | 2,43 | 4,5 | não passa |
  | Tema escuro: texto `#101A1E` sobre `#37B5CB` | 7,26 | 4,5 | passa |

  Proposta (sem mudar a cor da marca): manter `#038EA8` no logotipo, na barra
  e nos detalhes; usar `#02758B` como fundo dos botões e cor dos links; usar
  `#7F9096` (contraste 3,3) na borda dos campos; no tema escuro, botão com
  texto escuro. **Aguardando aprovação**; os tokens ainda não foram alterados.
- [ ] Haverá tema escuro no MVP? Sugestão: não; só o claro.
- [ ] Fonte Inter: hospedar os arquivos no próprio sistema (recomendado pelo
      Design System) ou usar só a fonte do aparelho?

## 9. Infraestrutura (só documentar, sem mexer)

- [ ] Onde o sistema vai rodar? A VPS atual tem 1,9 GiB de RAM e já roda
      Morumbi Festas, Morumbi 3D e IAGO. Um PostgreSQL a mais pode não caber.
      Alternativas: VPS separada para a IBC (isola os dados da igreja dos
      outros sistemas) ou banco gerenciado.
- [ ] Domínio: qual endereço o sistema vai usar?
- [ ] Backups: para onde vão as cópias, quem tem acesso, de quanto em quanto
      tempo?
- [ ] Este repositório no GitHub está **público**. Como o código não terá
      dados de membros, isso não vaza informação, mas é recomendado deixá-lo
      **privado**, para não expor detalhes do sistema da igreja.
