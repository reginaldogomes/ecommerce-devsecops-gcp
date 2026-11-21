# ADR 001: Autenticação OIDC via Workload Identity Federation

## Contexto

Pipelines de entrega contínua precisam autenticar no Google Cloud para enviar imagens ao Artifact Registry e implantar revisões no Cloud Run. A abordagem tradicional utiliza chaves JSON de Service Account armazenadas como secrets estáticos no GitHub.

## Decisão

Adotar **Workload Identity Federation (OIDC)** entre GitHub Actions e Google Cloud IAM, restringindo a federação ao repositório específico (`attribute.repository`) via `attribute_condition`, e segregando as identidades de deploy (`github-deployer`) e execução (`cloudrun-runtime`).

## Consequências

- Eliminação de credenciais estáticas de longa duração no repositório.
- Tokens temporários emitidos apenas durante a execução do workflow autorizado.
- Redução do raio de impacto em caso de comprometimento da conta de runtime, que não possui permissões de deploy.
