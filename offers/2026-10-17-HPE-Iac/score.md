# Resume score: 3.3/10

_2026-10-17-HPE-Iac, scored by claude-opus-5-5_

I would not shortlist you. This is a TCP_05 Solution Architect role that asks for 10–15 years of experience, plus leadership of teams, customer pursuits and architecture ownership. Your dates show about three years, starting with an internship in June 2023, and your degree finished in Sep 2025. Within those three years the IaC evidence is real and concrete for your level. The Nexits freelance work covers Terraform stacks with S3 state and OIDC, CI guardrails with reviewer-gated applies and permissions boundaries, SSM-driven deploys with automatic rollback, and a host that can be rebuilt in about 10 minutes. The Horizon self-hosting adds Nginx, TLS and Keycloak. Several must-haves still have no evidence. Kubernetes is expected at expert level and only appears in your skills list. Ansible appears only in a personal project. There is no Chef, no custom modules or provider plugins, no bare-metal, SAN/NAS or enterprise networking, no team leadership or pre-sales solutioning, and no architecture diagrams. You have an adjacent junior DevOps/IaC profile, and the seniority gap rules you out for this posting. A mid-level DevOps or IaC engineer role at HPE or a similar company would fit you far better.

## Weaknesses

- Seniority is far below the bar. The offer asks for 10–15 years and an architect job level (TCP_05). Your resume shows about 3 years, starting with an internship in June 2023, and your engineering degree finished in Sep 2025. Nothing on the page can close this gap.
- Kubernetes is listed under 'Containers & Orchestration' but no experience or project mentions it. The offer wants expert-level Kubernetes with Helm, operators and GitOps. A skill listed without any supporting bullet reads as padding to a screener.
- Configuration management is thin. Ansible appears only in OpsForge, a personal Vagrant lab. There is no Chef, no playbooks or roles described in a work setting, and no Ansible custom modules or Terraform provider plugins, which the offer names explicitly.
- There is no evidence of leadership, mentoring or customer-facing solutioning. The only claim is 'Led the architecture and development' of an Airflow library at Talan, which is a data-engineering task and not team leadership. You list nothing about pursuits, architecture reviews or mentoring.
- The first third doesn't make the case for this role. The top entry is the Talan Data Engineering Consultant job: Airflow DAG libraries and Snowflake config builders, which are data engineering rather than infrastructure automation. Your strongest IaC material (Nexits freelance) is the fourth entry and starts below the middle of the page.
- Linux administration is a must-have but is never stated directly. It is only implied by 'EC2 Graviton Linux host' and Playpex's systemd/ufw packaging, and 'Linux' does not appear in your skills.
- Bare-metal, SAN/NAS storage and enterprise networking are completely absent. Everything you show is AWS VMs or self-hosted Docker Compose stacks.
- Most bullets are hedged. 'Worked on provisioning', 'worked on TLS', 'Worked with the team on the Terraform setup', 'Contributed to the GitHub Actions CI/CD' and 'Worked on zero-downtime API deploys' all read as participation rather than ownership, which hurts you for an 'own architectural decisions' role.
- Results are almost never quantified. The only outcome metric is 'rebuilt from Terraform in about 10 min'. There are no figures for deploy frequency, number of services or environments, cost, uptime or team size.
- Some content takes space without helping. The K-Rose bullet is about Vercel hosting and app logging, which is weak for an IaC role. The Nexits internship has an empty entry. The 12-item AWS list in skills dilutes the page. 'Freelance Job' is a vague title that undersells your most relevant experience.
- There are no architecture diagrams or reference architectures. The closest is 'Wrote the AWS deployment plan … cost-first launch profile and a later growth architecture'.
- The other named tools are missing too: GitLab CI or CircleCI, PowerShell, Go or Ruby, Azure or GCP, and the ELK Stack.

## Strengths

- Your Nexits freelance entry is concrete, senior-flavoured IaC work. It describes a layered Terraform setup (a bootstrap stack with S3 state and native locking, GitHub OIDC and CI IAM roles, then network, site, host, ECR, Route 53 and budget stacks) that maps directly onto 'architectural and implementation experience with IaC solutions using Terraform'.
- You show real evidence of 'standards and guardrails for automated provisioning and CI/CD integration': OIDC with least-privilege roles per workflow, a reviewer-gated Terraform apply, a permissions boundary and no long-lived keys.
- Your deployment automation shows operational maturity: SSM Run Command, images pinned by digest, a health check with automatic rollback, SSH closed, secrets in Parameter Store, CloudWatch auto-recover, EBS snapshots and a rebuild in about 10 minutes.
- Promoting images by digest from staging to prod behind an approval gate, and zero-downtime Docker Compose deploys (docker rollout, health checks), show container lifecycle work beyond the basics.
- The Talan internship covers self-hosted platform provisioning with shell scripts and Docker Compose, an Nginx gateway, TLS between instances, Keycloak role- and group-based access control and a VPN. This is relevant to the security and integration layers the offer mentions.
- Writing a deployment plan with a launch profile and a growth architecture is the closest thing on the page to solution-architecture work.
- OpsForge covers Ansible, Jenkins and Prometheus/Grafana, and Playpex shows Linux service packaging (systemd, ufw/firewalld, deb packages) and an OpenAPI REST API. Together they fill several tool checkboxes.
- The summary is on target and names IaC, Terraform, CI/CD, Docker Compose on Linux, and security. The skills section is grouped along the offer's own categories.

## Requirements

| | Requirement | Evidence in the resume |
|---|---|---|
| ❌ | 10–15 years of experience in software design, infrastructure automation, hybrid cloud and DevOps | — |
| ⚠️ | End-to-end solution architecture of scalable, reliable, secure systems | Wrote the AWS deployment plan for the Nexits landing site and Payload CMS (cost-first launch profile and a later growth architecture) |
| ⚠️ | Architectural and implementation experience with IaC (Terraform, Ansible) | Provisioned the infrastructure as code with Terraform: a bootstrap stack (S3 state with native locking, GitHub OIDC provider, CI IAM roles), then network, static site, host, ECR, Route 53 and budget stacks; Ansible only in OpsForge (personal project) |
| ⚠️ | Hands-on experience with multiple configuration management tools (playbooks, cookbooks, modules) | OpsForge: provisioned with Vagrant and Ansible (personal project); no Chef, no modules described |
| ❌ | Automation scripts using Ansible custom modules, Chef knife, Terraform provider plugins | — |
| ⚠️ | Programming for automation (Python, Go, Ruby and/or Java) | Scripting & Languages: Python, Bash, TypeScript, Java…; Python shown only in the Airflow library work, not in infrastructure automation |
| ⚠️ | RESTful APIs and API integration with automation tools | Playpex: a versioned OpenAPI REST API; automated deployments with GitHub webhooks and Bash scripts; no REST-driven infrastructure automation |
| ⚠️ | Strong Linux infrastructure and administration, CLI and shell scripting | Automated deployments to an EC2 Graviton Linux host through AWS SSM Run Command; provisioning … with shell scripts; Playpex headless entry under systemd, ufw/firewalld |
| ✅ | CI/CD pipelines and tools (Jenkins, GitLab, CircleCI) | GitHub Actions authenticates to AWS through OIDC… reviewer-gated Terraform apply; images built once and promoted by digest from staging to prod behind a manual approval gate; Jenkins CI/CD in OpsForge |
| ⚠️ | Expert-level Kubernetes, Docker and container lifecycle management | Docker: arm64 images on ECR pinned by digest, health check with automatic rollback; zero-downtime deploys with docker rollout. Kubernetes: skills list only |
| ⚠️ | Bare-metal servers, SAN/NAS storage, networking, security, enterprise business applications | Security and networking only: Nginx gateway, TLS between instances, Keycloak IAM, VPN, LAN; nothing on bare-metal or storage |
| ❌ | Leading teams and leading solutions during pursuit/solutioning | — |
| ❌ | Preparing end-to-end architecture diagrams | — |
| ⚠️ | Design and develop automation and DevSecOps solutions | least-privilege IAM roles per workflow… permissions boundary, so there are no long-lived keys; SonarQube in OpsForge |
| ✅ | Standards and guardrails for provisioning, configuration management and CI/CD | Set up guardrails for CI/CD: GitHub Actions authenticates to AWS through OIDC with least-privilege IAM roles per workflow, a reviewer-gated Terraform apply and a permissions boundary |
| ⚠️ | Reference architectures, design patterns, reusable frameworks | custom library that gives DAG developers a reusable framework; strategy pattern over Snowflake metadata tables (data engineering, not infrastructure) |
| ❌ | Technical guidance and mentorship | — |
| ❌ | Desired: Helm, operators, GitOps | — |
| ⚠️ | Desired: extensive Ansible, Terraform, Python, Bash, PowerShell | Terraform and Bash shown at work; Ansible only in a personal project; no PowerShell |
| ✅ | Desired: cloud (AWS, Azure, GCP) | AWS: EC2, ECR, S3, CloudFront, Route 53, IAM, SSM, RDS, CloudWatch, EventBridge; one account per environment under AWS Organizations |
| ⚠️ | Desired: monitoring and logging (Prometheus, Grafana, ELK) | Prometheus/Grafana monitoring (OpsForge); CloudWatch auto-recover; Axiom structured logging and Sentry |
| ❌ | Desired: lead technical discussions, architecture reviews, roadmap planning | — |

## To raise the score

- **high** · gap to close: The 10–15 year requirement can't be met by editing. Target mid-level DevOps, platform or IaC engineer roles (HPE has these in Tunisia too) rather than TCP_05 architect positions. Hold this kind of role for later in your career.
- **high** · gap to close: Get hands-on Kubernetes experience before claiming it: deploy one of your existing stacks (for example, the Horizon services or the Nexits CMS) on k3s or EKS with Helm charts and Argo CD or Flux GitOps. Then write a bullet about it. Until you do, either remove Kubernetes from your skills or label it as basic.
- **high** · resume edit: Put your IaC work on the first third of the page. Rename 'Freelance Job' to a descriptive title from your context file, if one exists (for example, a DevOps or cloud infrastructure title). Make the Nexits freelance entry the first thing a reader sees, either by changing the order or with a short 'Selected infrastructure work' lead. Trim the Talan data-engineering entry to one bullet, because Airflow and Snowflake config builders do little for this role.
- **medium** · resume edit: Replace hedged verbs with precise ones wherever your context supports it. 'Worked on provisioning' should become 'Provisioned' if you did it, and 'Worked on TLS between instances' should become 'Configured TLS…'. Where you only contributed, keep the hedge but state your specific part.
- **medium** · resume edit: Cut the empty Nexits internship entry, or merge it into the Nexits full-stack entry. Shorten the AWS list to the services used in your bullets, and drop or shorten the K-Rose Vercel bullet. Use the freed space for Linux and Ansible evidence.
- **medium** · add to context/ if true: If you have administered Linux hosts directly (systemd units, users and permissions, firewalls, package management, troubleshooting on EC2 or the Horizon hosts), add it to your context files and state it plainly in a bullet. Also add 'Linux' to skills.yaml so it can appear in your skills list.
- **medium** · add to context/ if true: If you have drawn architecture diagrams for the Nexits deployment plan or the Horizon platform, add them to your context and mention them in a bullet ('…with end-to-end architecture diagrams'). The offer names this explicitly.
- **medium** · add to context/ if true: If you have led or mentored anyone, add it with numbers: K-Rose PR reviews for two developers, the ENET'Com workshops, or guiding DAG developers on the Talan library. Right now the resume shows no leadership at all.
- **medium** · add to context/ if true: If you used REST APIs to automate infrastructure (the AWS APIs through scripts, the Keycloak admin API, GitHub webhook handlers, Airbyte or Airflow APIs), add it. 'Work with RESTful APIs to automate infrastructure' is a must-have and currently has no evidence.
- **medium** · gap to close: Do more work with Ansible beyond the lab: write roles or playbooks for a real host (for example, the Nexits EC2 or the Horizon instances), and ideally one custom module in Python. This covers the offer's 'playbooks, modules' and 'Ansible custom module' requirements.
- **low** · add to context/ if true: If you know which VPN Horizon used and whether it ran on Linux hosts, add both facts. They strengthen your Linux and security evidence.
- **low** · resume edit: Add outcome numbers you can support from context, such as the number of environments or stacks, how often you deployed, cost savings from the cost-first profile, or how many services sat behind Nginx and Keycloak.
