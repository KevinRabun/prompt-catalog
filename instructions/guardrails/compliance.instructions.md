---
name: Compliance and Data Sovereignty Guardrails
description: Ensure AI agents consider regulatory compliance and data sovereignty in all recommendations
---

<!-- Catalog Metadata
id: INST-GUARD-005
version: 1.0.0
scope: guardrail
applies_to: all
priority: critical
author: community
last_reviewed: 2026-02-12
-->

# Compliance & Data Sovereignty Guardrails

## Objective
Software must respect **regulatory requirements** and **data sovereignty laws**. These guardrails ensure AI agents consider compliance obligations from the start, not as an afterthought.

## Core Principles

1. **Compliance is not optional** — Regulatory violations carry legal and financial consequences
2. **Data has a home** — Many jurisdictions require data to reside in specific locations
3. **Privacy by design** — Build privacy controls into the architecture, not on top of it
4. **Audit everything** — If you can't prove compliance, you're not compliant
5. **Stay current** — Regulations change; designs must accommodate change

## Key Regulatory Frameworks

### Data Protection & Privacy
| Regulation | Jurisdiction | Key Requirements |
|-----------|-------------|------------------|
| **GDPR** | EU/EEA | Consent, data minimization, right to erasure, DPO, breach notification |
| **CCPA/CPRA** | California, USA | Consumer rights, opt-out of sale, data access rights |
| **LGPD** | Brazil | Similar to GDPR, legal bases for processing, DPO requirement |
| **POPIA** | South Africa | Conditions for lawful processing, information officers |
| **PIPEDA** | Canada | Consent, purpose limitation, safeguards |
| **APPI** | Japan | Purpose specification, third-party transfer rules |
| **PDPA** | Singapore/Thailand | Consent, purpose limitation, access and correction rights |

### Industry-Specific
| Regulation | Industry | Key Requirements |
|-----------|---------|------------------|
| **PCI-DSS** | Payment card | Card data protection, network security, access control |
| **HIPAA** | Healthcare (US) | PHI protection, access controls, audit trails, BAAs |
| **SOX** | Public companies (US) | Financial reporting controls, audit trails |
| **SOC 2** | Service providers | Security, availability, processing integrity, confidentiality, privacy |
| **FISMA/FedRAMP** | US Government | Security controls, continuous monitoring, authorization |
| **MiFID II** | Financial (EU) | Transaction reporting, record keeping, best execution |
| **Basel III/IV** | Banking | Capital requirements, risk management, reporting |

### Data Sovereignty
| Region | Requirements |
|--------|-------------|
| **EU** | Data must not leave EU/EEA without adequate safeguards (SCCs, adequacy decisions) |
| **China** | Critical data and personal information may require in-country storage (PIPL, DSL) |
| **Russia** | Personal data of Russian citizens must be stored in Russia |
| **India** | Critical personal data must be processed in India (proposed DPDP Act) |
| **Australia** | Government data must remain onshore; APPs apply to personal information |
| **UAE** | Financial and health data often require in-country storage |

## Mandatory Compliance Rules

### Data Residency
```
ALWAYS:
  1. ASK where users/data subjects are located
  2. IDENTIFY which data sovereignty rules apply
  3. DESIGN architecture with data residency in mind
  4. CHOOSE cloud regions that satisfy residency requirements
  5. DOCUMENT data flows across borders

NEVER:
  1. Assume data can be stored/processed anywhere
  2. Replicate data across regions without considering sovereignty
  3. Use CDNs for sensitive data without checking residency rules
  4. Ignore data residency in disaster recovery design
```

### Personal Data Handling
```
ALWAYS:
  1. Minimize data collection — only collect what's needed
  2. Define a legal basis for processing (consent, contract, legitimate interest)
  3. Implement data subject rights (access, rectification, deletion, portability)
  4. Set data retention periods — delete data when no longer needed
  5. Encrypt personal data at rest and in transit
  6. Implement access controls — only authorized personnel access personal data
  7. Log access to personal data for audit purposes
  8. Plan for data breach notification (72 hours under GDPR)

NEVER:
  1. Collect personal data "just in case"
  2. Use personal data for purposes beyond the original consent
  3. Share personal data with third parties without proper agreements
  4. Store personal data longer than the defined retention period
  5. Log personal data in application logs without masking
```

### Audit and Evidence
```
ALWAYS:
  1. Log security-relevant events with timestamps and actor identification
  2. Protect audit logs from tampering (append-only, separate storage)
  3. Retain logs according to regulatory requirements
  4. Monitor for unauthorized access patterns
  5. Document compliance controls and their implementation
  6. Prepare for audits — evidence must be readily available

NEVER:
  1. Allow audit logs to be modified or deleted by the system being audited
  2. Store audit logs in the same account/system as the application
  3. Skip logging for administrative or privileged operations
  4. Assume compliance without evidence
```

## Architecture Patterns for Compliance

### Multi-Region with Data Sovereignty
```
Region A (EU):     [App Servers] ─── [EU Database] ─── [EU Storage]
                                                        ↕ (metadata only)
Region B (US):     [App Servers] ─── [US Database] ─── [US Storage]

Cross-region: Only non-PII metadata flows between regions
Encryption: All data encrypted with region-specific keys
Access: Region-specific RBAC with audit logging
```

### Data Classification Architecture
```
Public       → Standard storage, CDN-eligible, no special controls
Internal     → Access-controlled, encrypted in transit
Confidential → Encrypted at rest and in transit, audit logging, DLP
Restricted   → All of the above + data residency, key management, enhanced monitoring
```

## Compliance-by-Default Code Patterns

When generating code that handles personal or regulated data:
- Include **consent checking** before data processing
- Implement **data classification** tags/labels on data objects
- Add **retention policy** metadata to stored records
- Include **anonymization/pseudonymization** utilities
- Implement **audit trail** logging for data access and modification
- Support **data export** in portable formats (for data portability rights)
- Support **data deletion** including cascading deletes and backup cleanup

## Compliance Review Checklist

- [ ] Applicable regulations are identified and documented
- [ ] Data residency requirements are mapped to infrastructure regions
- [ ] Personal data processing has a documented legal basis
- [ ] Data subject rights are implementable in the architecture
- [ ] Data retention policies are defined and automated
- [ ] Audit logging covers all compliance-relevant operations
- [ ] Encryption meets regulatory requirements (algorithms, key sizes)
- [ ] Access controls enforce least-privilege and separation of duties
- [ ] Data breach notification process is documented and tested
- [ ] Third-party data processing agreements are in place
- [ ] Compliance evidence can be produced for audits
