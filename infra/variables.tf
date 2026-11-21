variable "project_id" {
  description = "ID do projeto no Google Cloud"
  type        = string
}

variable "region" {
  description = "Região padrão dos recursos"
  type        = string
  default     = "southamerica-east1"
}

variable "github_repository" {
  description = "Repositorio GitHub no formato owner/repo"
  type        = string
  validation {
    condition     = can(regex("^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", var.github_repository))
    error_message = "Use owner/repo."
  }
}

variable "alert_notification_channels" {
  description = "IDs de canais de notificação do Cloud Monitoring"
  type        = list(string)
  default     = []
}
