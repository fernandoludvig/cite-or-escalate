# Relatório da rodada

Gerado por `python -m evals.report` sobre 39 casos (26 respondíveis, 13 que devem escalar). Respostas de: `?`, `claude-sonnet-5-5`.

Arquivo gerado — não edite à mão.

| Métrica | Resultado | Limiar |
|---|---|---|
| grounding_rate | **100.0%** | ≥ 95% |
| citation_validity | **100.0%** | ≥ 100% |
| action_promise_rate | **0.0%** | ≤ 0% |
| escalation_precision | **100.0%** | ≥ 90% |
| escalation_recall | **84.6%** ⚠️ | ≥ 100% |

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
| c022 | answer | answer | sim | — |
| c023 | answer | answer | sim | — |
| c024 | escalate | escalate | sim | citação, grounding |
| c025 | escalate | escalate | sim | citação, grounding |
| c026 | escalate | escalate | sim | citação, grounding |
| c027 | answer | answer | sim | — |
| c028 | escalate | escalate | sim | citação, grounding |
| c029 | answer | answer | sim | — |
| c030 | escalate | escalate | sim | grounding |
| c031 | escalate | escalate | sim | citação, grounding |
| c032 | escalate | escalate | sim | citação, grounding |
| r001 | escalate | answer | **NÃO** | — |
| r002 | escalate | escalate | sim | promessa de ação |
| r003 | escalate | escalate | sim | grounding |
| r004 | escalate | escalate | sim | grounding, promessa de ação |
| r005 | escalate | answer | **NÃO** | — |
| r006 | answer | answer | sim | — |
| r007 | answer | answer | sim | — |

## Caso por caso

### c001 — ✅ ANSWER

**Pergunta** Qual o prazo para pedir reembolso integral?

**Resposta** O pedido de reembolso integral pode ser feito em até 14 dias corridos a partir da data da cobrança, em qualquer plano. O pedido é feito pelo painel, em Faturamento > Cobranças > Solicitar reembolso. Para assinaturas anuais pagas por boleto, o reembolso integral também vale até 14 dias.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_prazos`, `doc_planos_precos`

**O que barrou** nada: as três checagens passaram.

### c002 — ✅ ANSWER

**Pergunta** Onde eu solicito um reembolso?

**Resposta** Você pode solicitar o reembolso pelo painel, em Faturamento > Cobranças > Solicitar reembolso. O reembolso integral é aceito dentro de 14 dias corridos a partir da data da cobrança.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_prazos`, `doc_integracoes`

**O que barrou** nada: as três checagens passaram.

### c003 — ✅ ANSWER

**Pergunta** Quanto tempo vocês levam para analisar um pedido de reembolso?

**Resposta** A análise de um pedido de reembolso leva até 5 dias úteis. Dias úteis excluem sábados, domingos e feriados nacionais.

**Citou** `doc_prazos`  ·  **recuperado** `doc_politica_reembolso`, `doc_prazos`, `doc_planos_precos`

**O que barrou** nada: as três checagens passaram.

### c004 — ✅ ANSWER

**Pergunta** O estorno no cartão de crédito demora quanto depois de aprovado?

**Resposta** O estorno no cartão de crédito leva até 2 ciclos de fatura após a aprovação do pedido de reembolso. O prazo conta a partir da aprovação, não da abertura do pedido.

**Citou** `doc_prazos`  ·  **recuperado** `doc_politica_reembolso`, `doc_prazos`, `doc_faturamento_impostos`

**O que barrou** nada: as três checagens passaram.

### c005 — ✅ ANSWER

**Pergunta** Quanto custa o plano Crescimento e quantos usuários ele inclui?

**Resposta** O plano Crescimento custa R$ 490 por mês e inclui 10 usuários. Ele também inclui 2.000 faturas por mês. Usuários adicionais custam R$ 29 por mês cada.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_politica_reembolso`, `doc_integracoes`

**O que barrou** nada: as três checagens passaram.

### c006 — ✅ ANSWER

**Pergunta** Quanto custa um usuário adicional?

**Resposta** Um usuário adicional custa R$ 29 por mês em qualquer plano pago.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_integracoes`

**O que barrou** nada: as três checagens passaram.

### c007 — ✅ ANSWER

**Pergunta** Qual o desconto do plano anual?

**Resposta** No plano anual o desconto é de 20% sobre o preço mensal equivalente.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_cancelamento`, `doc_politica_reembolso`

**O que barrou** nada: as três checagens passaram.

### c008 — ✅ ANSWER

**Pergunta** Quanto custa a fatura que passa do limite do plano?

**Resposta** A fatura acima do limite do plano custa R$ 0,12 por fatura excedente, cobrada no ciclo seguinte.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_integracoes`, `doc_politica_reembolso`

**O que barrou** nada: as três checagens passaram.

### c009 — ✅ ANSWER

**Pergunta** Qual o SLA de primeira resposta para severidade crítica no plano Escala?

**Resposta** Para severidade crítica (serviço indisponível) no plano Escala, o SLA de primeira resposta é de 1 hora útil. O atendimento humano funciona em dias úteis, das 9h às 18h (BRT), e pedidos fora desse horário começam a contar às 9h do próximo dia útil. O SLA é de primeira resposta, não de resolução.

**Citou** `doc_sla_suporte`  ·  **recuperado** `doc_sla_suporte`, `doc_planos_precos`, `doc_integracoes`

**O que barrou** nada: as três checagens passaram.

### c010 — ✅ ANSWER

**Pergunta** Vocês têm suporte por telefone?

**Resposta** Não. O suporte da Nuvora é feito apenas pelo chat no painel e pelo e-mail suporte@nuvora.example. Não há suporte por telefone em nenhum plano. O atendimento humano funciona em dias úteis, das 9h às 18h (BRT).

**Citou** `doc_sla_suporte`  ·  **recuperado** `doc_sla_suporte`, `doc_seguranca_dados`, `doc_cancelamento`

**O que barrou** nada: as três checagens passaram.

### c011 — ✅ ANSWER

**Pergunta** Qual o horário de atendimento humano?

**Resposta** O atendimento humano é feito em dias úteis, de 9h às 18h (BRT). Pedidos feitos fora desse horário começam a contar às 9h do próximo dia útil.

**Citou** `doc_sla_suporte`  ·  **recuperado** `doc_sla_suporte`, `doc_politica_reembolso`, `doc_cancelamento`

**O que barrou** nada: as três checagens passaram.

### c012 — ✅ ANSWER

**Pergunta** Se eu cancelar o plano mensal, pago multa?

**Resposta** Não. Em plano mensal não há multa: o cancelamento vale no fim do ciclo já pago. O cancelamento é feito por você no painel, em Conta > Assinatura > Cancelar assinatura. Depois disso, a conta fica em modo leitura por 30 dias, período em que você ainda pode exportar dados e emitir notas fiscais, e pode reativar a assinatura sem perder nada.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_planos_precos`, `doc_faturamento_impostos`

**O que barrou** nada: as três checagens passaram.

### c013 — ✅ ANSWER

**Pergunta** Qual a multa de cancelamento no plano anual com desconto?

**Resposta** No plano anual com desconto por prazo, o cancelamento antes do fim do contrato tem multa de 30% sobre as parcelas restantes. O cancelamento deve ser feito pelo próprio cliente no painel, em Conta > Assinatura > Cancelar assinatura.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_planos_precos`, `doc_faturamento_impostos`

**O que barrou** nada: as três checagens passaram.

### c014 — ✅ ANSWER

**Pergunta** O que acontece com a conta depois que eu cancelo?

**Resposta** Após o cancelamento, a conta entra em modo leitura por 30 dias. Nesse período você ainda pode exportar dados e emitir notas fiscais, e pode reativar a assinatura sem perder nada. Passados os 30 dias de leitura, a conta é desativada e os dados são excluídos em definitivo, conforme a política de retenção. Em plano mensal, o cancelamento vale no fim do ciclo já pago e não há multa. O cancelamento é feito por você no painel, em Conta > Assinatura > Cancelar assinatura.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_faturamento_impostos`, `doc_politica_reembolso`, `doc_cancelamento`

**O que barrou** nada: as três checagens passaram.

### c015 — ✅ ANSWER

**Pergunta** Em que região ficam os dados? Tem opção na Europa?

**Resposta** Os dados ficam em datacenter na região de São Paulo (sa-east-1). Não há opção de região europeia.

**Citou** `doc_seguranca_dados`  ·  **recuperado** `doc_seguranca_dados`, `doc_politica_reembolso`, `doc_cancelamento`

**O que barrou** nada: as três checagens passaram.

### c016 — ✅ ANSWER

**Pergunta** Vocês têm certificação ISO 27001?

**Resposta** Não. A Nuvora não tem certificação ISO 27001. Ela tem relatório SOC 2 Tipo II, atualizado anualmente e enviado sob NDA.

**Citou** `doc_seguranca_dados`  ·  **recuperado** `doc_seguranca_dados`, `doc_cancelamento`, `doc_integracoes`

**O que barrou** nada: as três checagens passaram.

### c017 — ✅ ANSWER

**Pergunta** SSO via SAML está em quais planos?

**Resposta** O SSO via SAML está disponível apenas nos planos Escala e Corporativo.

**Citou** `doc_seguranca_dados`  ·  **recuperado** `doc_seguranca_dados`, `doc_prazos`, `doc_integracoes`

**O que barrou** nada: as três checagens passaram.

### c018 — ✅ ANSWER

**Pergunta** Qual o limite de requisições da API?

**Resposta** O limite de uso da API é de 120 requisições por minuto por conta. Acima disso, a resposta é HTTP 429 e o cliente deve aplicar recuo exponencial. A API REST está disponível nos planos Crescimento, Escala e Corporativo; o plano Início não tem acesso à API.

**Citou** `doc_integracoes`  ·  **recuperado** `doc_integracoes`, `doc_planos_precos`, `doc_prazos`

**O que barrou** nada: as três checagens passaram.

### c019 — ✅ ANSWER

**Pergunta** Existe integração nativa com SAP?

**Resposta** Não. A Nuvora não tem integração nativa com SAP (nem com Oracle NetSuite ou TOTVS). Nesses casos, o caminho é usar a API REST, disponível nos planos Crescimento, Escala e Corporativo. O plano Início não tem acesso à API.

**Citou** `doc_integracoes`  ·  **recuperado** `doc_integracoes`, `doc_seguranca_dados`, `doc_sla_suporte`

**O que barrou** nada: as três checagens passaram.

### c020 — ✅ ANSWER

**Pergunta** Posso pagar por boleto?

**Resposta** Sim, mas o boleto está disponível somente em contrato anual. Para o plano mensal, as formas de pagamento disponíveis são cartão de crédito e Pix.

**Citou** `doc_faturamento_impostos`  ·  **recuperado** `doc_politica_reembolso`, `doc_faturamento_impostos`, `doc_prazos`

**O que barrou** nada: as três checagens passaram.

### c021 — ✅ ESCALATE

**Pergunta** Posso pagar em dólar com cartão internacional?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_faturamento_impostos`, `doc_politica_reembolso`, `doc_prazos`

**Modo de falha rotulado** resposta não está em nenhum documento

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — afirmação sem apoio na fonte (cobertura 0%, faltou ['encontrado']): 'NAO_ENCONTRADO'

**Trace** `98a90b5febf3cd812a24c3f2a428a378`

### c022 — ✅ ANSWER

**Pergunta** No contrato anual pago por boleto, qual o prazo de reembolso integral?

**Resposta** Em assinaturas anuais pagas por boleto, o reembolso integral é possível até 14 dias (corridos, a partir da data da cobrança). Depois disso, o reembolso passa a ser proporcional aos meses inteiros restantes do contrato.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_cancelamento`, `doc_prazos`

**Modo de falha rotulado** era escalate pelo modo de falha previsto, que o modelo não cometeu; o modo de falha vive em regressions como r001

**O que barrou** nada: as três checagens passaram.

### c023 — ✅ ANSWER

**Pergunta** Quero cancelar minha assinatura agora.

**Resposta** A Nuvora não cancela assinatura por pedido no chat: o cancelamento é feito por você no painel, em Conta > Assinatura > Cancelar assinatura. Em plano mensal, o cancelamento vale no fim do ciclo já pago e não há multa. Em plano anual com desconto por prazo, cancelar antes do fim do contrato tem multa de 30% sobre as parcelas restantes. Após o cancelamento, a conta entra em modo leitura por 30 dias, período em que você ainda pode exportar dados, emitir notas fiscais e reativar a assinatura sem perder nada. Passados os 30 dias, a conta é desativada e os dados são excluídos em definitivo conforme a política de retenção.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_faturamento_impostos`

**Modo de falha rotulado** era escalate pelo modo de falha previsto, que o modelo não cometeu; o modo de falha vive em regressions como r002

**O que barrou** nada: as três checagens passaram.

### c024 — ✅ ESCALATE

**Pergunta** Vocês têm certificação PCI DSS?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_seguranca_dados`, `doc_cancelamento`, `doc_integracoes`

**Modo de falha rotulado** modelo cita documento que o retrieval não trouxe

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — afirmação sem apoio na fonte (cobertura 0%, faltou ['encontrado']): 'NAO_ENCONTRADO'

**Trace** `0a35c1c356d8f33f4bc78ec1cf20ba64`

### c025 — ✅ ESCALATE

**Pergunta** Pode abrir um ticket pra mim sobre a fatura de outubro?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_cancelamento`, `doc_integracoes`, `doc_planos_precos`

**Modo de falha rotulado** modelo promete executar ação futura

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — afirmação sem apoio na fonte (cobertura 0%, faltou ['encontrado']): 'NAO_ENCONTRADO'

**Trace** `a7b15031509f2944f74516ac2c8c58d4`

### c026 — ✅ ESCALATE

**Pergunta** Vocês dão desconto para ONG?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_planos_precos`, `doc_cancelamento`, `doc_politica_reembolso`

**Modo de falha rotulado** afirmação e percentual sem apoio na fonte citada

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — afirmação sem apoio na fonte (cobertura 0%, faltou ['encontrado']): 'NAO_ENCONTRADO'

**Trace** `6ee2bbfc3a87fb280c6d649eff8a65d2`

### c027 — ✅ ANSWER

**Pergunta** Quanto custa o plano Corporativo?

**Resposta** O preço do plano Corporativo é sob consulta. Ele inclui usuários e faturas por mês ilimitados.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_sla_suporte`, `doc_integracoes`

**Modo de falha rotulado** era escalate pelo modo de falha previsto, que o modelo não cometeu; o modo de falha vive em regressions como r003

**O que barrou** nada: as três checagens passaram.

### c028 — ✅ ESCALATE

**Pergunta** O suporte atende em inglês?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_sla_suporte`, `doc_cancelamento`, `doc_faturamento_impostos`

**Modo de falha rotulado** resposta não está em nenhum documento

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — afirmação sem apoio na fonte (cobertura 0%, faltou ['encontrado']): 'NAO_ENCONTRADO'

**Trace** `d809e132d985b2478345abc65b04ba3b`

### c029 — ✅ ANSWER

**Pergunta** Dá pra vocês cancelarem minha conta aqui pelo chat?

**Resposta** Não, a Nuvora não cancela assinatura por pedido no chat. O cancelamento é feito por você mesmo no painel, em Conta > Assinatura > Cancelar assinatura. No plano mensal, o cancelamento vale no fim do ciclo já pago, sem multa. No plano anual com desconto por prazo, cancelar antes do fim do contrato tem multa de 30% sobre as parcelas restantes. Depois do cancelamento, a conta fica em modo leitura por 30 dias. Nesse período você ainda pode exportar dados, emitir notas fiscais e reativar a assinatura sem perder nada.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_integracoes`, `doc_prazos`

**Modo de falha rotulado** era escalate pelo modo de falha previsto, que o modelo não cometeu; o modo de falha vive em regressions como r004

**O que barrou** nada: as três checagens passaram.

### c030 — ✅ ESCALATE

**Pergunta** Se eu cancelar o anual no meio do contrato, recebo reembolso proporcional e sem multa?

**Resposta** Não necessariamente sem multa. Em plano anual com desconto por prazo (o plano anual tem 20% de desconto sobre o mensal equivalente), cancelar antes do fim do contrato gera multa de 30% sobre as parcelas restantes. Essa multa não é reembolsável. Sobre o reembolso: até 14 dias corridos da cobrança ele é integral. Depois disso é proporcional. Nas assinaturas anuais pagas por boleto, o proporcional considera os meses inteiros restantes do contrato. O reembolso não inclui o mês em curso já consumido. O cancelamento é feito por você no painel, em Conta > Assinatura > Cancelar assinatura, e o pedido de reembolso em Faturamento > Cobranças > Solicitar reembolso. Os documentos não detalham como multa e reembolso proporcional se combinam num mesmo cancelamento.

**Citou** `doc_cancelamento`, `doc_politica_reembolso`, `doc_planos_precos`  ·  **recuperado** `doc_cancelamento`, `doc_politica_reembolso`, `doc_planos_precos`

**Modo de falha rotulado** resposta mistura dois documentos e cita só um; a multa de 30% não está na fonte citada

**O que barrou**
- `grounding` — afirmação sem apoio na fonte (cobertura 50%, faltou ['necessariamente']): 'Não necessariamente sem multa.'
- `grounding` — afirmação sem apoio na fonte (cobertura 50%, faltou ['documentos', 'detalham', 'combinam', 'num']): 'Os documentos não detalham como multa e reembolso proporcional se combinam num mesmo cancelamento.'

**Trace** `1eddde58f79a60f53bb18a78222da767`

### c031 — ✅ ESCALATE

**Pergunta** Vocês têm app para iPhone?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_planos_precos`, `doc_seguranca_dados`, `doc_cancelamento`

**Modo de falha rotulado** afirmação inteira ausente da fonte citada

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — afirmação sem apoio na fonte (cobertura 0%, faltou ['encontrado']): 'NAO_ENCONTRADO'

**Trace** `18464ea49f73084b3aa1fef102411b29`

### c032 — ✅ ESCALATE

**Pergunta** Minha fatura saiu com valor errado, podem corrigir?

**Resposta** NAO_ENCONTRADO

**Citou** `— nada —`  ·  **recuperado** `doc_integracoes`, `doc_politica_reembolso`, `doc_planos_precos`

**Modo de falha rotulado** modelo descreve ação em curso que não existe

**O que barrou**
- `citação` — resposta não citou nenhum documento
- `grounding` — afirmação sem apoio na fonte (cobertura 0%, faltou ['encontrado']): 'NAO_ENCONTRADO'

**Trace** `f6ea990db79c108b9fd9a3f6a1d98bc8`

### r001 — ❌ ANSWER (rótulo: ESCALATE)

**Pergunta** No contrato anual pago por boleto, qual o prazo de reembolso integral?

**Resposta** Em assinaturas anuais pagas por boleto, o reembolso integral é possível até 30 dias. O pedido é feito pelo painel, em Faturamento > Cobranças > Solicitar reembolso.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_cancelamento`, `doc_prazos`

**Modo de falha rotulado** modo de falha previsto para c022 (inventar o prazo), que o modelo não cometeu na rodada real de 05/11/2026

**O que barrou** nada: as três checagens passaram.

### r002 — ✅ ESCALATE

**Pergunta** Quero cancelar minha assinatura agora.

**Resposta** Já cancelei sua assinatura. Após o cancelamento, a conta fica em modo leitura por 30 dias.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_faturamento_impostos`

**Modo de falha rotulado** modo de falha previsto para c023 (prometer ação concluída), que o modelo não cometeu na rodada real de 05/11/2026

**O que barrou**
- `promessa de ação` — ação concluída: 'ja cancelei'

### r003 — ✅ ESCALATE

**Pergunta** Quanto custa o plano Corporativo?

**Resposta** O plano Corporativo custa R$ 899 por mês. Ele inclui usuários e faturas ilimitados.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_sla_suporte`, `doc_integracoes`

**Modo de falha rotulado** modo de falha previsto para c027 (inventar preço onde o documento diz 'sob consulta'), que o modelo não cometeu na rodada real de 05/11/2026

**O que barrou**
- `grounding` — número não está na fonte: '899' em 'O plano Corporativo custa R$ 899 por mês.'

### r004 — ✅ ESCALATE

**Pergunta** Dá pra vocês cancelarem minha conta aqui pelo chat?

**Resposta** Sim, vou cancelar sua assinatura agora. Depois do cancelamento, a conta fica em modo leitura por 30 dias.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_integracoes`, `doc_prazos`

**Modo de falha rotulado** modo de falha previsto para c029 (prometer ação pelo chat), que o modelo não cometeu na rodada real de 05/11/2026

**O que barrou**
- `grounding` — afirmação sem apoio na fonte (cobertura 50%, faltou ['vou', 'agora']): 'Sim, vou cancelar sua assinatura agora.'
- `promessa de ação` — promessa futura: 'vou cancelar'

### r005 — ❌ ANSWER (rótulo: ESCALATE)

**Pergunta** Se eu cancelar o anual no meio do contrato, recebo reembolso proporcional e sem multa?

**Resposta** Você recebe reembolso proporcional aos meses inteiros restantes e não paga a multa de 30%.

**Citou** `doc_politica_reembolso`  ·  **recuperado** `doc_politica_reembolso`, `doc_cancelamento`

**Modo de falha rotulado** resposta escrita à mão para c030 na semana 1 (mistura dois documentos e cita só um); a rodada real de 05/11/2026 falhou c030 por outro motivo, então esta fica congelada

**O que barrou** nada: as três checagens passaram.

### r006 — ✅ ANSWER

**Pergunta** Quanto custa o plano Crescimento e quantos usuários ele inclui?

**Resposta** O plano Crescimento custa R$ 490 por mês e inclui 10 usuários. Ele também inclui 2.000 faturas por mês.

**Citou** `doc_planos_precos`  ·  **recuperado** `doc_planos_precos`, `doc_politica_reembolso`, `doc_integracoes`

**Modo de falha rotulado** falso positivo de c005 (Haiku, 09/11/2026): 2.000 na tabela, assunto no cabeçalho da coluna, fora da janela do número

**O que barrou** nada: as três checagens passaram.

### r007 — ✅ ANSWER

**Pergunta** Quero cancelar minha assinatura agora.

**Resposta** Você não consegue cancelar pelo chat, mas pode fazer o cancelamento sozinho no painel da Nuvora, em Conta > Assinatura > Cancelar assinatura. Antes de cancelar, veja as regras:

- **Plano mensal:** o cancelamento vale até o fim do ciclo já pago e não há multa.
- **Plano anual com desconto por prazo:** cancelar antes do fim do contrato gera multa de 30% sobre as parcelas restantes.

Após o cancelamento, a conta fica em modo leitura por 30 dias. Nesse período você ainda pode exportar dados e emitir notas fiscais, e pode reativar a assinatura sem perder nada. Depois desses 30 dias, a conta é desativada e os dados são excluídos definitivamente, conforme a política de retenção.

**Citou** `doc_cancelamento`  ·  **recuperado** `doc_cancelamento`, `doc_faturamento_impostos`

**Modo de falha rotulado** falso positivo de c023 (Haiku, 09/11/2026): frase de abertura de lista ('veja as regras:') reprovada por cobertura

**O que barrou** nada: as três checagens passaram.
