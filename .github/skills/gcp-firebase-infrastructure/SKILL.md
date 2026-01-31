---
name: gcp-firebase-infrastructure
description: 'Manage Google Cloud Platform and Firebase infrastructure with Terraform. Use when: (1) Setting up Firebase projects, (2) Configuring GCP resources, (3) Managing multi-environment infrastructure (dev/staging/prod), (4) Deploying Firestore/Storage rules, (5) Configuring IAM permissions, (6) Managing secrets, or working with Terraform for GCP/Firebase. Keywords: firebase, gcp, terraform, firestore, cloud functions, infrastructure, environment, deployment, security rules.'
---

# GCP/Firebase Infrastructure Management

Manage Firebase and Google Cloud Platform infrastructure using Terraform and Firebase CLI, with support for multi-environment deployments.

## When to Use This Skill

- Setting up or modifying Firebase projects
- Creating or updating GCP resources (Cloud Functions, Firestore, Storage)
- Managing infrastructure across dev/staging/prod environments
- Deploying security rules for Firestore or Cloud Storage
- Configuring IAM permissions and secrets management
- Working with Terraform modules for GCP/Firebase

## Prerequisites

**Tools:** Firebase CLI, Google Cloud CLI, Terraform

**Authentication:**
```bash
firebase login
gcloud auth login
gcloud auth application-default login
```

## Multi-Environment Pattern

| Environment | Purpose | Resources |
|-------------|---------|-----------|
| **dev** | Local development | Firebase Emulator Suite |
| **staging** | Pre-production testing | Separate Firebase/GCP project |
| **prod** | Production | Production Firebase/GCP project |

**Environment Structure:**
## Core Workflows

### Firebase Operations

```bash
# Setup project
firebase use <project-id>
firebase init

# Deploy services
firebase deploy --only firestore:rules
firebase deploy --only functions
firebase deploy  # All services

# Test locally
firebase emulators:start
```

### Terraform Operations

```bash
cd terraform/environments/staging
terraform init
terraform plan
terraform apply
```

### Secrets Management

**GitHub:** Settings → Secrets → Add (reference as `${{ secrets.NAME }}`)

**GCP:**
```bash
echo -n "value" | gcloud secrets create NAME --data-file=-``

## Best Practices

✅ **DO:**
- Use separate Firebase projects for each environment
- Test in staging before deploying to production
- Use `terraform plan` before `terraform apply`
- Store secrets in Secret Manager (not environment files)
- Apply least-privilege IAM permissions
- Version control Terraform state with remote backend
- Document environment-specific variables
- Use Firestore indexes for complex queries

❌ **DON'T:**
- Commit `.tfstate` files or secret values to git
- Hardcode environment-specific values in code
- Grant overly broad IAM permissions
- Deploy to production without staging verification
- Modify production infrastructure without review
- Skip `terraform plan` before applying changes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Firebase CLI not authenticated | Run `firebase login` |
| Terraform state locked | `terraform force-unlock <lock-id>` |
| Permission denied on deploy | Check IAM roles for service account |
| Security rules rejected | Test with emulator first: `firebase emulators:start` |
| Function deployment fails | Check logs: `firebase functions:log` |
| Secret not accessible | Verify Secret Manager IAM bindings |

## Quick Reference

**Firebase CLI:**
```bash
firebase projects:list                    # List projects
firebase use <project-id>                 # Switch project
firebase deploy --only <service>          # Deploy specific service
firebase functions:log                    # View function logs
firebase emulators:start                  # Start local emulators
```

**Terraform:**
```bash
terraform init                            # Initialize
terraform plan                            # Preview changes
terraform apply                           # Apply changes
terraform destroy                         # Destroy resources
terraform state list                      # List resources
```

**gcloud:**
```bash
gcloud projects list                      # List projects
gcloud config set project <project-id>    # Set active project
gcloud secrets list                       # List secrets
gcloud iam service-accounts list          # List service accounts
```

## Detailed References

- **[Security Rules](references/security-rules.md)** - Firestore and Storage rules examples
- **[IAM & Permissions](references/iam-permissions.md)** - Service accounts and roles
- **[Terraform Patterns](references/terraform-patterns.md)** - Module structure and examples
- **[Secrets Management](references/secrets-management.md)** - Complete workflow

## Context7 Resources

- Firebase Admin: `@context7 /firebase/firebase-admin-node`
- Google Cloud: `@context7 /googleapis/google-cloud-node`
- Terraform GCP: `@context7 /hashicorp/terraform-provider-google`
Separate projects per environment, test in staging first, use `terraform plan`
❌ Don't commit `.tfstate` or secrets, grant minimal IAM permissions```bash
# Firebase
firebase use <project>
firebase deploy --only <service>
firebase functions:log

# Terraform
terraform plan
terraform apply
terraform state list

# gcloud
gcloud config set project <id>
gcloud secrets list