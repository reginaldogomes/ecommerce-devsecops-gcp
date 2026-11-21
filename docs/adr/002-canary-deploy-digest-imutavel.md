# ADR 002: Canary Deploy por Digest Imutável no Cloud Run

## Contexto

Implantar diretamente com tags mutáveis e direcionar 100% do tráfego na mesma operação aumenta o risco de indisponibilidade caso a nova revisão apresente falhas de inicialização ou regressão de saúde.

## Decisão

1. Encadear o workflow de CD ao de CI via `workflow_call` como gate obrigatório.
2. Capturar o **digest SHA-256** retornado pelo `docker push` e implantar no Cloud Run usando a referência imutável (`@sha256:...`).
3. Subir a revisão com `--no-traffic --tag canary`, executar *smoke tests* autenticados (Identity Token OIDC) em `/health/live` e `/health/ready` e somente após sucesso promover 100% do tráfego.

## Consequências

- Garantia criptográfica de que a imagem implantada é idêntica à validada no pipeline.
- Falhas nos endpoints de saúde interrompem a promoção antes de afetar usuários finais.
