# ADR 003: Arquitetura em Camadas, Repository Pattern e Idempotência

## Contexto

Manter rotas, validação, regras de negócio e dados em um único módulo dificulta testes isolados, evolução para banco relacional e padronização de erros.

## Decisão

1. Separar a aplicação em `core` (configuração, logging JSON, exceções RFC 9457), `schemas`, `repositories`, `services` e `api`.
2. Definir o contrato `CatalogRepository` via `Protocol`, permitindo substituir `InMemoryCatalogRepository` por PostgreSQL sem alterar a camada de serviço.
3. Suportar o header `Idempotency-Key` em `POST /orders` com reserva atômica de estoque.

## Consequências

- Facilidade de testes unitários e cobertura acima de 90%.
- Padronização de erros (`application/problem+json`) e rastreabilidade via `X-Request-ID` e `X-Cloud-Trace-Context`.
- Retentativas de rede no endpoint de pedidos não geram duplicidade de cobrança ou baixa dupla de estoque.
