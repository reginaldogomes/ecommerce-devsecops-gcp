# Operação, observabilidade e rollback

## Logs

Console Google Cloud > Logging > Logs Explorer, filtrar por Cloud Run Revision e serviço `ecommerce-api`.

## Métricas

Console > Monitoring > Metrics Explorer: métricas de requisições, latência e instâncias do Cloud Run. Configurar alertas de erros 5xx e latência conforme o SLO definido pelo time (não provisionados automaticamente).

## Rollback

1. `gcloud run revisions list --service ecommerce-api --region "$REGION" --project "$PROJECT_ID"`
2. Identificar a revisão estável.
3. `gcloud run services update-traffic ecommerce-api --to-revisions REVISAO_ESTAVEL=100 --region "$REGION" --project "$PROJECT_ID"`

## Segurança e custos

Serviço privado: `curl` anônimo deve receber 403; para testar, use uma identidade com `roles/run.invoker` e token ID válido. Não armazene credenciais no Git. O Cloud Run pode gerar cobrança por requisições/recursos; Artifact Registry armazena imagens e pode gerar custos. Exclua recursos quando terminar o laboratório.
