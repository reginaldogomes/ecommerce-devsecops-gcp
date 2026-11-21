terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  # Para uso em equipe ou execução em CI, habilite o backend remoto no GCS:
  # backend "gcs" {
  #   bucket = "seu-bucket-terraform-state"
  #   prefix = "ecommerce_devsecops_gcp/prod"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
