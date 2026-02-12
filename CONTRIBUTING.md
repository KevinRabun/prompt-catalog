# Contributing to Prompt Catalog

Thank you for your interest in contributing! This project thrives on community input across diverse platforms, domains, and skill levels.

## How to Contribute

### Adding a New Prompt

1. **Fork** this repository and create a feature branch
2. **Choose the right directory** based on SDLC phase (`prompts/planning/`, `prompts/development/`, etc.)
3. **Use the prompt template** — copy `prompts/_template.yaml` as your starting point
4. **Follow the schema** — validate against `schema/prompt.schema.json`
5. **Test your prompt** — try it with at least two different AI models
6. **Submit a PR** with a clear description of what the prompt does and who it helps

### Prompt Quality Standards

Every prompt must meet these criteria before merging:

- [ ] **Follows the YAML schema** with all required fields populated
- [ ] **Has a clear, specific purpose** — not too broad, not too narrow
- [ ] **Includes variables** for customization where appropriate
- [ ] **Specifies skill level** accurately (beginner / intermediate / advanced / expert)
- [ ] **Tested with at least one AI model** with results documented in the PR
- [ ] **Does not hallucinate** — prompts should instruct the AI to verify, cite, and admit uncertainty
- [ ] **Adversarial evaluation included** — prompts should include `adversarial_tests` with scenarios that challenge the AI output
- [ ] **Security-conscious** — does not encourage insecure patterns
- [ ] **Platform-appropriate** — tagged with correct platforms and tested on them
- [ ] **Well-documented** — description and expected_output are clear

### Improving Existing Prompts

Found a prompt that could be better? Great! Here's how:

1. **Open an issue** describing the improvement
2. **Reference the prompt ID** (e.g., `PLAN-REQ-001`)
3. **Provide examples** of current output vs. desired output
4. **Submit a PR** with the improvement and bump the `version` field

### Adding Domain Coverage

New industry domains are particularly welcome:

1. Create a new directory under `prompts/domains/`
2. Include at least 3-5 prompts covering the domain basics
3. Add domain-specific instruction files under `instructions/platforms/` if needed
4. Update `prompts/index.json` with the new domain

### Adding Instruction Files

Instruction files are critical guardrails. When contributing:

1. Follow the existing format in `instructions/`
2. Be specific and actionable — avoid vague guidance
3. Include examples of what to do AND what not to do
4. Test with an AI agent to ensure the instructions are followed

## Naming Conventions

### Prompt IDs
Format: `{CATEGORY}-{SUBCATEGORY}-{NUMBER}`

| Category | Prefix |
|----------|--------|
| Planning | `PLAN` |
| Architecture | `ARCH` |
| Development | `DEV` |
| Testing | `TEST` |
| Security | `SEC` |
| Deployment | `DEPLOY` |
| Operations | `OPS` |
| Domain | `DOM` |

Examples: `PLAN-REQ-001`, `ARCH-MICRO-003`, `DEV-WEB-012`, `DOM-FINTECH-002`

### File Names
- Prompts: `{id-in-lowercase}.yaml` (e.g., `plan-req-001.yaml`)
- Instructions: `{topic}.instructions.md` (e.g., `security.instructions.md`)

## Versioning

- Prompts use [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`
  - **MAJOR**: Breaking changes to prompt structure or intent
  - **MINOR**: Added variables, expanded scope, improved output
  - **PATCH**: Typo fixes, clarifications, minor wording changes

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming and inclusive experience for everyone.

## Review Process

1. **Automated validation** — Schema validation runs on all PRs
2. **Adversarial evaluation** — Prompts are tested with adversarial inputs and judged against rubrics
3. **Peer review** — At least one maintainer reviews content quality
4. **AI testing** — Prompts are tested against representative scenarios
5. **Merge** — Approved PRs are merged and the index is updated

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
