# Terraform Patterns Reference

## Directory Structure

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── production/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
└── modules/
    ├── firebase/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   └── README.md
    ├── cloud-functions/
    └── networking/
```

## Firebase Module Example

### modules/firebase/main.tf

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

resource "google_project" "project" {
  name       = var.project_name
  project_id = var.project_id
  org_id     = var.org_id
}

resource "google_firebase_project" "firebase" {
  provider = google
  project  = google_project.project.project_id
}

resource "google_firestore_database" "database" {
  project     = google_project.project.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  
  depends_on = [google_firebase_project.firebase]
}
```

### modules/firebase/variables.tf

```hcl
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "project_name" {
  description = "Project display name"
  type        = string
}

variable "org_id" {
  description = "GCP Organization ID"
  type        = string
}

variable "region" {
  description = "Default region for resources"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}
```

### modules/firebase/outputs.tf

```hcl
output "project_id" {
  description = "The project ID"
  value       = google_project.project.project_id
}

output "project_number" {
  description = "The project number"
  value       = google_project.project.number
}
```

## Environment Configuration

### environments/staging/main.tf

```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state-staging"
    prefix = "terraform/state"
  }
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "firebase" {
  source = "../../modules/firebase"
  
  project_id   = var.project_id
  project_name = var.project_name
  org_id       = var.org_id
  region       = var.region
  environment  = "staging"
}
```

### environments/staging/variables.tf

```hcl
variable "project_id" {
  description = "GCP Project ID for staging"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "org_id" {
  description = "GCP Organization ID"
  type        = string
}

variable "region" {
  description = "Default region"
  type        = string
  default     = "us-central1"
}
```

### environments/staging/terraform.tfvars

```hcl
project_id   = "my-app-staging"
project_name = "My App (Staging)"
org_id       = "123456789"
region       = "us-central1"
```

## Common Operations

### Initialize and Apply

```bash
cd terraform/environments/staging

# Initialize (first time or after adding providers)
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply

# Target specific resource
terraform apply -target=module.firebase.google_firebase_project

# Apply with auto-approve (CI/CD)
terraform apply -auto-approve
```

### State Management

```bash
# List resources in state
terraform state list

# Show specific resource
terraform state show module.firebase.google_project.project

# Move resource in state
terraform state mv OLD_ADDRESS NEW_ADDRESS

# Remove resource from state (keep in cloud)
terraform state rm ADDRESS
```

### Import Existing Resources

```bash
# Import existing GCP project
terraform import google_project.project PROJECT_ID

# Import Firestore database
terraform import google_firestore_database.database projects/PROJECT_ID/databases/(default)
```

## Best Practices

### Remote State

Always use remote state for team collaboration:

```hcl
terraform {
  backend "gcs" {
    bucket  = "my-terraform-state"
    prefix  = "env/staging"
  }
}
```

### Variable Management

**DON'T commit sensitive values:**
- Use `terraform.tfvars` for non-sensitive config (gitignored)
- Use environment variables for secrets: `TF_VAR_secret_key`
- Use Secret Manager for runtime secrets

### Workspace Strategy

**Option 1: Separate directories** (Recommended)
```
environments/
├── dev/
├── staging/
└── production/
```

**Option 2: Terraform workspaces**
```bash
terraform workspace new staging
terraform workspace select staging
```

### Module Versioning

For shared modules, use version tags:

```hcl
module "firebase" {
  source = "git::https://github.com/org/terraform-modules.git//firebase?ref=v1.2.0"
}
```
