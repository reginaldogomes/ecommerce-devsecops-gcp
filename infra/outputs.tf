output "workload_identity_provider" { value = google_iam_workload_identity_pool_provider.github.name }
output "deployer_service_account" { value = google_service_account.deployer.email }
output "runtime_service_account" { value = google_service_account.runtime.email }
output "artifact_registry_repository" { value = google_artifact_registry_repository.images.id }
