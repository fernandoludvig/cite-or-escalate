# Integrações — Nuvora

Integrações nativas: Omie, Conta Azul, Bling, Shopify, Stripe e Google Sheets.

A API REST está disponível nos planos Crescimento, Escala e Corporativo. O plano
Início não tem acesso à API.

Limite de uso da API: 120 requisições por minuto por conta. Acima disso a
resposta é HTTP 429 e o cliente deve aplicar recuo exponencial.

Webhooks entregam eventos de fatura criada, fatura paga e fatura cancelada. A
Nuvora tenta reenviar um webhook falho 5 vezes, em intervalos crescentes, ao
longo de 24 horas.

Não há integração nativa com SAP, Oracle NetSuite ou TOTVS. Nesses casos o
caminho é a API.

Chaves de API são criadas em Conta > Desenvolvedor e podem ser revogadas pelo
cliente a qualquer momento.
