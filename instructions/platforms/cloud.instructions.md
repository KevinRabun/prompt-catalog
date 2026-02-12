---
name: Cloud Architecture Platform Instructions
description: Platform-specific guidance for cloud-native application development across providers
---

<!-- Catalog Metadata
id: INST-PLAT-006
version: 1.0.0
scope: platform
applies_to: cloud-azure, cloud-aws, cloud-gcp, cloud-oracle, cloud-multi
priority: high
author: community
last_reviewed: 2026-02-12
-->

# Cloud Architecture — Platform Instructions

## Scope
These instructions apply when designing and building **cloud-native applications** across Azure, AWS, GCP, Oracle Cloud, and multi-cloud environments.

## Cloud-Agnostic Principles

### The Twelve-Factor App (Adapted for Cloud)
1. **Codebase**: One codebase tracked in version control
2. **Dependencies**: Explicitly declare and isolate dependencies
3. **Config**: Store config in the environment, not in code
4. **Backing Services**: Treat databases, queues, caches as attached resources
5. **Build, Release, Run**: Strictly separate build and run stages
6. **Processes**: Execute the app as stateless processes
7. **Port Binding**: Export services via port binding
8. **Concurrency**: Scale out via the process model
9. **Disposability**: Maximize robustness with fast startup and graceful shutdown
10. **Dev/Prod Parity**: Keep development, staging, and production as similar as possible
11. **Logs**: Treat logs as event streams
12. **Admin Processes**: Run admin/management tasks as one-off processes

### Well-Architected Framework Pillars
All major cloud providers share these pillars:
- **Operational Excellence**: Automate operations, monitor, improve continuously
- **Security**: Protect information, systems, and assets
- **Reliability**: Recover from failures, meet demand
- **Performance Efficiency**: Use resources efficiently
- **Cost Optimization**: Avoid unnecessary costs
- **Sustainability**: Minimize environmental impact (increasingly important)

## Service Mapping Across Providers

| Capability | Azure | AWS | GCP | Oracle Cloud |
|-----------|-------|-----|-----|-------------|
| **Compute - VMs** | Virtual Machines | EC2 | Compute Engine | Compute Instances |
| **Compute - Containers** | AKS, Container Apps | EKS, ECS, Fargate | GKE, Cloud Run | OKE |
| **Compute - Serverless** | Azure Functions | Lambda | Cloud Functions | OCI Functions |
| **Compute - PaaS** | App Service | Elastic Beanstalk | App Engine | Application Container |
| **Storage - Object** | Blob Storage | S3 | Cloud Storage | Object Storage |
| **Storage - File** | Azure Files | EFS | Filestore | File Storage |
| **Database - SQL** | Azure SQL, PostgreSQL | RDS, Aurora | Cloud SQL, AlloyDB | Autonomous DB |
| **Database - NoSQL** | Cosmos DB | DynamoDB | Firestore, Bigtable | NoSQL Database |
| **Messaging** | Service Bus | SQS/SNS | Pub/Sub | Streaming |
| **Events** | Event Grid | EventBridge | Eventarc | Events Service |
| **CDN** | Azure CDN, Front Door | CloudFront | Cloud CDN | CDN |
| **Identity** | Entra ID | IAM, Cognito | IAM, Identity Platform | IAM, IDCS |
| **Secrets** | Key Vault | Secrets Manager | Secret Manager | Vault |
| **Monitoring** | Monitor, App Insights | CloudWatch, X-Ray | Cloud Monitoring | Monitoring |
| **IaC** | Bicep, ARM, Terraform | CloudFormation, CDK, Terraform | Deployment Manager, Terraform | Resource Manager, Terraform |

## Cloud Architecture Patterns

### Microservices
- Use **container orchestration** (Kubernetes, managed container services)
- Implement **service mesh** for complex communication patterns
- Use **API gateways** for external traffic management
- Implement **circuit breakers** and **retry policies**
- Use **distributed tracing** for observability across services
- Design for **eventual consistency** where appropriate

### Serverless
- Design functions to be **stateless and idempotent**
- Handle **cold starts** — minimize dependencies and initialization
- Set appropriate **timeout and memory** configurations
- Use **managed services** for state (databases, queues, storage)
- Monitor **concurrency limits** and implement throttling
- Consider **cost at scale** — serverless is not always cheaper

### Event-Driven
- Use **managed message brokers** (Service Bus, SQS, Pub/Sub)
- Implement **dead letter queues** for failed message processing
- Design for **at-least-once delivery** — make handlers idempotent
- Use **event sourcing** where audit trail is important
- Implement **schema evolution** for events (backward compatible)

### Multi-Cloud / Hybrid
- Use **infrastructure as code** that supports multiple providers (Terraform, Pulumi)
- Abstract **provider-specific APIs** behind interfaces
- Consider **data gravity** — processing near the data is usually most efficient
- Plan for **different SLAs** across providers
- Implement **unified monitoring** across clouds
- Consider **egress costs** when designing cross-cloud data flows

## Data Sovereignty in the Cloud

```
BEFORE selecting cloud regions:
  1. Identify where your users are located
  2. Determine which regulations apply (GDPR, data localization laws)
  3. Map data categories to residency requirements
  4. Select regions that satisfy ALL requirements
  5. Design replication to avoid cross-border data flow violations
  6. Document region selection rationale
```

## Cloud Security Best Practices

- Use **managed identities** instead of credentials where possible
- Implement **network segmentation** (VNets, VPCs, private endpoints)
- Enable **encryption at rest** for all storage services
- Use **private endpoints** for PaaS services — avoid public internet exposure
- Implement **WAF** for public-facing web applications
- Enable **DDoS protection** for public endpoints
- Use **SIEM** integration for security event analysis
- Implement **Just-In-Time** access for privileged operations
- Follow **CIS Benchmarks** for cloud configuration
