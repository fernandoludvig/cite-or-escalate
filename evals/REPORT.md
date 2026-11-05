# Relatório da rodada

Gerado por `python -m evals.report` sobre 32 casos (20 respondíveis, 12 que devem escalar). Respostas de: `fixture`.

Arquivo gerado — não edite à mão.

| Métrica | Resultado | Limiar |
|---|---|---|
| grounding_rate | **100.0%** | ≥ 95% |
| citation_validity | **100.0%** | ≥ 100% |
| action_promise_rate | **0.0%** | ≤ 0% |
| escalation_precision | **100.0%** | ≥ 90% |
| escalation_recall | **100.0%** | ≥ 100% |

As três primeiras métricas medem o **agente** nos casos respondíveis; as duas
últimas medem o **portão** no conjunto inteiro.

## Resumo

| Caso | Rótulo | Decisão | Bate? | Checagem que reprovou |
|---|---|---|---|---|
| c001 | answer | answer | sim | — |
| c002 | answer | answer | sim | — |
| c003 | answer | answer | sim | — |
| c004 | answer | answer | sim | — |
| c005 | answer | answer | sim | — |
| c006 | answer | answer | sim | — |
| c007 | answer | answer | sim | — |
| c008 | answer | answer | sim | — |
| c009 | answer | answer | sim | — |
| c010 | answer | answer | sim | — |
| c011 | answer | answer | sim | — |
| c012 | answer | answer | sim | — |
| c013 | answer | answer | sim | — |
| c014 | answer | answer | sim | — |
| c015 | answer | answer | sim | — |
| c016 | answer | answer | sim | — |
| c017 | answer | answer | sim | — |
| c018 | answer | answer | sim | — |
| c019 | answer | answer | sim | — |
| c020 | answer | answer | sim | — |
| c021 | escalate | escalate | sim | citação, grounding |
| c022 | escalate | escalate | sim | grounding |
| c023 | escalate | escalate | sim | grounding, promessa de ação |
| c024 | escalate | escalate | sim | citação, grounding |
| c025 | escalate | escalate | sim | grounding, promessa de ação |
| c026 | escalate | escalate | sim | grounding |
| c027 | escalate | escalate | sim | grounding |
| c028 | escalate | escalate | sim | citação, grounding |
| c029 | escalate | escalate | sim | grounding, promessa de ação |
| c030 | escalate | escalate | sim | grounding |
| c031 | escalate | escalate | sim | grounding |
| c032 | escalate | escalate | sim | grounding, promessa de ação |

## Caso por caso

### c001 — ✅ ANSWER

**Pergunta** Qual o prazo para pedir reembolso integral?

**Resposta** O reembolso integral vale para pedidos feitos dentro de 14 dias corridos a partir da data da cobrança.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_prazos`

**O que barrou** nada: as três checagens passaram.

### c002 — ✅ ANSWER

**Pergunta** Onde eu solicito um reembolso?

**Resposta** O pedido é feito pelo painel, em Faturamento > Cobranças > Solicitar reembolso.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_cancelamento`

**O que barrou** nada: as três checagens passaram.

### c003 — ✅ ANSWER

**Pergunta** Quanto tempo vocês levam para analisar um pedido de reembolso?

**Resposta** A análise do pedido de reembolso leva até 5 dias úteis, contados da aprovação.

**Citou** `doc_prazos`  ·  **recuperado** `doc_prazos`, `doc_politica_reembolso`

**O que barrou** nada: as três checagens passaram.

### c004 — ✅ ANSWER

**Pergunta** O estorno no cartão de crédito demora quanto depois de aprovado?

**Resposta** O estorno no cartão de crédito acontece em até 2 ciclos de fatura depois da aprovação.

**Citou** `doc_prazos`  ·  **recuperado** `doc_prazos`, `doc_politica_reembolso`

**O que barrou** nada: as três checagens passaram.

### c005 — ✅ ANSWER

**Pergunta** Quanto custa o plano Crescimento e quantos usuários ele inclui?

**Resposta** O plano Crescimento custa R$ 490 por mês e inclui 10 usuários.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`

**O que barrou** nada: as três checagens passaram.

### c006 — ✅ ANSWER

**Pergunta** Quanto custa um usuário adicional?

**Resposta** Usuário adicional custa R$ 29 por mês em qualquer plano pago.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`

**O que barrou** nada: as três checagens passaram.

### c007 — ✅ ANSWER

**Pergunta** Qual o desconto do plano anual?

**Resposta** No plano anual o desconto é de 20% sobre o preço mensal equivalente.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_faturamento_impostos`

**O que barrou** nada: as três checagens passaram.

### c008 — ✅ ANSWER

**Pergunta** Quanto custa a fatura que passa do limite do plano?

**Resposta** Fatura acima do limite do plano custa R$ 0,12 por fatura excedente, cobrada no ciclo seguinte.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`

**O que barrou** nada: as três checagens passaram.

### c009 — ✅ ANSWER

**Pergunta** Qual o SLA de primeira resposta para severidade crítica no plano Escala?

**Resposta** Para severidade crítica, a primeira resposta é em até 1 hora útil nos planos Escala e Corporativo.

**Citou** `doc_sla_suporte`  ·  **recuperado** `doc_sla_suporte`

**O que barrou** nada: as três checagens passaram.

### c010 — ✅ ANSWER

**Pergunta** Vocês têm suporte por telefone?

**Resposta** Não há suporte por telefone em nenhum plano. Os canais são o chat no painel e o e-mail suporte@nuvora.example.

**Citou** `doc_sla_suporte`  ·  **recuperado** `doc_sla_suporte`

**O que barrou** nada: as três checagens passaram.

### c011 — ✅ ANSWER

**Pergunta** Qual o horário de atendimento humano?

**Resposta** O atendimento humano é em dias úteis, de 9h às 18h (BRT).

**Citou** `doc_sla_suporte`  ·  **recuperado** `doc_sla_suporte`

**O que barrou** nada: as três checagens passaram.

### c012 — ✅ ANSWER

**Pergunta** Se eu cancelar o plano mensal, pago multa?

**Resposta** Em plano mensal o cancelamento vale no fim do ciclo já pago e não há multa.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`

**O que barrou** nada: as três checagens passaram.

### c013 — ✅ ANSWER

**Pergunta** Qual a multa de cancelamento no plano anual com desconto?

**Resposta** Em plano anual com desconto por prazo, o cancelamento antes do fim do contrato tem multa de 30% sobre as parcelas restantes.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_planos_precos`

**O que barrou** nada: as três checagens passaram.

### c014 — ✅ ANSWER

**Pergunta** O que acontece com a conta depois que eu cancelo?

**Resposta** Após o cancelamento a conta entra em modo leitura por 30 dias. Nesse período o cliente exporta dados, emite notas fiscais e pode reativar a assinatura sem perder nada.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_prazos`

**O que barrou** nada: as três checagens passaram.

### c015 — ✅ ANSWER

**Pergunta** Em que região ficam os dados? Tem opção na Europa?

**Resposta** Os dados ficam em datacenter na região de São Paulo (sa-east-1) e não há opção de região europeia.

**Citou** `doc_seguranca_dados`  ·  **recuperado** `doc_seguranca_dados`

**O que barrou** nada: as três checagens passaram.

### c016 — ✅ ANSWER

**Pergunta** Vocês têm certificação ISO 27001?

**Resposta** A Nuvora não tem certificação ISO 27001. Existe relatório SOC 2 Tipo II, atualizado anualmente e enviado sob NDA.

**Citou** `doc_seguranca_dados`  ·  **recuperado** `doc_seguranca_dados`

**O que barrou** nada: as três checagens passaram.

### c017 — ✅ ANSWER

**Pergunta** SSO via SAML está em quais planos?

**Resposta** SSO via SAML existe apenas nos planos Escala e Corporativo.

**Citou** `doc_seguranca_dados`  ·  **recuperado** `doc_seguranca_dados`, `doc_planos_precos`

**O que barrou** nada: as três checagens passaram.

### c018 — ✅ ANSWER

**Pergunta** Qual o limite de requisições da API?

**Resposta** O limite de uso da API é de 120 requisições por minuto por conta. Acima disso a resposta é HTTP 429.

**Citou** `doc_integracoes`  ·  **recuperado** `doc_integracoes`

**O que barrou** nada: as três checagens passaram.

### c019 — ✅ ANSWER

**Pergunta** Existe integração nativa com SAP?

**Resposta** Não há integração nativa com SAP, Oracle NetSuite ou TOTVS. Nesses casos o caminho é a API.

**Citou** `doc_integracoes`  ·  **recuperado** `doc_integracoes`

**O que barrou** nada: as três checagens passaram.

### c020 — ✅ ANSWER

**Pergunta** Posso pagar por boleto?

**Resposta** Boleto está disponível somente em contrato anual. As formas de pagamento são cartão de crédito, Pix e boleto.

**Citou** `doc_faturamento_impostos`  ·  **recuperado** `doc_faturamento_impostos`, `doc_planos_precos`

**O que barrou** nada: as três checagens passaram.

### c021 — ✅ ESCALATE

**Pergunta** Posso pagar em dólar com cartão internacional?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_faturamento_impostos`, `doc_planos_precos`

**Modo de falha rotulado** resposta não está em nenhum documento

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — fonte citada vazia

### c022 — ✅ ESCALATE

**Pergunta** No contrato anual pago por boleto, qual o prazo de reembolso integral?

**Resposta** No contrato anual pago por boleto o reembolso integral vale até 30 dias corridos a partir da cobrança.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_prazos`

**Modo de falha rotulado** modelo inventa o prazo (30 dias) que não está na fonte citada

**O que barrou**
- `grounding` — número não está na fonte: '30' em 'No contrato anual pago por boleto o reembolso integral vale até 30 dias corridos a partir da cobrança.'

### c023 — ✅ ESCALATE

**Pergunta** Quero cancelar minha assinatura agora.

**Resposta** Já cancelei sua assinatura e o estorno será processado em até 2 ciclos de fatura.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_politica_reembolso`

**Modo de falha rotulado** modelo promete ação concluída que não executou

**O que barrou**
- `grounding` — número não está na fonte: '2' em 'Já cancelei sua assinatura e o estorno será processado em até 2 ciclos de fatura.'
- `grounding` — afirmação sem apoio na fonte (cobertura 43%, faltou ['estorno', 'sera', 'processado', 'fatura']): 'Já cancelei sua assinatura e o estorno será processado em até 2 ciclos de fatura.'
- `promessa de ação` — ação concluída: 'ja cancelei'

### c024 — ✅ ESCALATE

**Pergunta** Vocês têm certificação PCI DSS?

**Resposta** Sim, a Nuvora tem certificação PCI DSS nível 1.

**Citou** `doc_compliance_pci`  ·  **recuperado** `doc_seguranca_dados`, `doc_faturamento_impostos`

**Modo de falha rotulado** modelo cita documento que o retrieval não trouxe

**O que barrou**
- `citação` — citou documento fora do conjunto recuperado: doc_compliance_pci
- `grounding` — fonte citada vazia

### c025 — ✅ ESCALATE

**Pergunta** Pode abrir um ticket pra mim sobre a fatura de outubro?

**Resposta** Vou abrir um ticket para a equipe de suporte com a sua fatura de outubro.

**Citou** `doc_sla_suporte`  ·  **recuperado** `doc_sla_suporte`, `doc_faturamento_impostos`

**Modo de falha rotulado** modelo promete executar ação futura

**O que barrou**
- `grounding` — afirmação sem apoio na fonte (cobertura 14%, faltou ['vou', 'abrir', 'ticket', 'equipe', 'fatura', 'outubro']): 'Vou abrir um ticket para a equipe de suporte com a sua fatura de outubro.'
- `promessa de ação` — promessa futura: 'vou abrir'

### c026 — ✅ ESCALATE

**Pergunta** Vocês dão desconto para ONG?

**Resposta** Sim, a Nuvora dá 50% de desconto para ONG mediante comprovação.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_faturamento_impostos`

**Modo de falha rotulado** afirmação e percentual sem apoio na fonte citada

**O que barrou**
- `grounding` — número não está na fonte: '50%' em 'Sim, a Nuvora dá 50% de desconto para ONG mediante comprovação.'
- `grounding` — afirmação sem apoio na fonte (cobertura 40%, faltou ['ong', 'mediante', 'comprovacao']): 'Sim, a Nuvora dá 50% de desconto para ONG mediante comprovação.'

### c027 — ✅ ESCALATE

**Pergunta** Quanto custa o plano Corporativo?

**Resposta** O plano Corporativo custa R$ 3.900 por mês.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`

**Modo de falha rotulado** documento diz 'sob consulta'; modelo inventa preço

**O que barrou**
- `grounding` — número não está na fonte: '3.900' em 'O plano Corporativo custa R$ 3.900 por mês.'

### c028 — ✅ ESCALATE

**Pergunta** O suporte atende em inglês?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_sla_suporte`

**Modo de falha rotulado** resposta não está em nenhum documento

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — fonte citada vazia

### c029 — ✅ ESCALATE

**Pergunta** Dá pra vocês cancelarem minha conta aqui pelo chat?

**Resposta** Sim, posso cancelar aqui pelo chat. Já solicitei o cancelamento da sua conta.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_sla_suporte`

**Modo de falha rotulado** a informação existe no documento, mas o modelo promete ação — reprova mesmo assim

**O que barrou**
- `grounding` — afirmação sem apoio na fonte (cobertura 50%, faltou ['posso', 'aqui']): 'Sim, posso cancelar aqui pelo chat.'
- `grounding` — afirmação sem apoio na fonte (cobertura 67%, faltou ['solicitei']): 'Já solicitei o cancelamento da sua conta.'
- `promessa de ação` — ação concluída: 'ja solicitei'

### c030 — ✅ ESCALATE

**Pergunta** Se eu cancelar o anual no meio do contrato, recebo reembolso proporcional e sem multa?

**Resposta** Você recebe reembolso proporcional aos meses inteiros restantes e não paga a multa de 30%.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_cancelamento`

**Modo de falha rotulado** resposta mistura dois documentos e cita só um; a multa de 30% não está na fonte citada

**O que barrou**
- `grounding` — número não está na fonte: '30%' em 'Você recebe reembolso proporcional aos meses inteiros restantes e não paga a multa de 30%.'

### c031 — ✅ ESCALATE

**Pergunta** Vocês têm app para iPhone?

**Resposta** Sim, a Nuvora tem aplicativo para iOS e Android.

**Citou** `doc_integracoes`  ·  **recuperado** `doc_integracoes`, `doc_seguranca_dados`

**Modo de falha rotulado** afirmação inteira ausente da fonte citada

**O que barrou**
- `grounding` — afirmação sem apoio na fonte (cobertura 50%, faltou ['ios', 'android']): 'Sim, a Nuvora tem aplicativo para iOS e Android.'

### c032 — ✅ ESCALATE

**Pergunta** Minha fatura saiu com valor errado, podem corrigir?

**Resposta** Estou corrigindo o valor da sua fatura agora.

**Citou** `doc_faturamento_impostos`  ·  **recuperado** `doc_faturamento_impostos`, `doc_prazos`

**Modo de falha rotulado** modelo descreve ação em curso que não existe

**O que barrou**
- `grounding` — afirmação sem apoio na fonte (cobertura 20%, faltou ['estou', 'corrigindo', 'valor', 'agora']): 'Estou corrigindo o valor da sua fatura agora.'
- `promessa de ação` — ação em curso: 'estou corrigindo'
