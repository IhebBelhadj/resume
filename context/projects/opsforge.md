---
id: opsforge
name: OpsForge
url: "https://github.com/IhebBelhadj/OpsForge"
tags:
  [
    devops,
    infrastructure,
    networking,
    kubernetes,
    linux,
    ansible,
    observability,
    ci-cd,
  ]
stack:
  [
    Python,
    Bash,
    Incus,
    Linux,
    Ansible,
    K3s,
    Kubernetes,
    WireGuard,
    nftables,
    tc/netem,
    dnsmasq,
    Grafana,
    Flux,
    Docker,
  ]
repo: /home/iheb/projects/OpsForge
---

<!-- Raw facts: never rendered. Resume bullets are generated from this text per offer and
     must quote it as their source, so write everything down (scope, team, tools, numbers,
     what you only touched). Keep it true; vague is fine, inflated is not. -->

Personal project, built alone. Multi-site WAN lab on one Linux host.

## Goal

One command provisions a distributed environment spread over simulated distant sites (multi-cloud /
multi-region), connected through a simulated internet with configurable latency, jitter, packet loss
and bandwidth, NAT and partitions, so distributed systems can be built and broken under realistic WAN
conditions on one laptop with the smallest possible RAM footprint. Host: Arch Linux, 12 threads,
14 GB RAM, so RAM was the design constraint; RAM use is measured as the lab grows.

## Key design decisions (and why)

- **Incus system containers** as nodes instead of VMs: each node is a full machine (own network stack,
  systemd, sshd) sharing the host kernel; idle cluster estimated ≈ 1.2–1.8 GB vs ≈ 3–4 GB for tuned
  VMs, starts in seconds. KVM/libvirt kept as fallback substrate (clock skew, other kernels).
- Debian 13 minimal for nodes, Alpine for routers/gateways.
- **K3s** with embedded SQLite and bundled extras disabled (lightest conformant distro; SQLite avoids
  etcd's latency sensitivity). Control plane on one site, workers stretched across sites (etcd over a
  lossy WAN is an anti-pattern), plus a multi-cluster mode with one cluster per site.
- **Ansible from the host as controller**, inventory generated from the topology: manages "remote"
  machines the way real ops does, idempotent.
- Lightweight CI/CD (a fraction of the RAM of Jenkins/SonarQube/Nexus).
- Documented what containers cannot simulate: clock skew between nodes (shared host clock →
  `libfaketime` per process or one KVM node), per-node kernel versions; netem loses precision at
  multi-Gbit rates.
- Ownership split like Terraform vs config management: the opsforge CLI owns addressing, firewalls,
  sshd host keys and bastion forwarding; Ansible owns services and OS config.

## Architecture

- Each site modelled as a cloud VPC: private LAN (`10.10.0.0/24`, `10.20.0.0/24`, `10.30.0.0/24`)
  behind a **site gateway** (NAT, firewall, VPN endpoint) holding a "public" IP on a shared WAN transit
  network (`203.0.113.0/24`).
- A **wan-core router** (the "internet") connects the gateways and is the single place link conditions
  are applied. Each gateway reaches it over its own point-to-point uplink bridge and holds its public IP
  as a /32 with wan-core as on-link next hop, so gateways can never reach each other directly (a shared
  transit bridge would have let them ARP each other and bypass the shaping).
- wan-core gives the lab real internet access (masqueraded) but drops forwarding to private ranges, like
  the real internet: VPCs cannot reach each other or the host's LAN except via public IPs, port
  forwards or the site-to-site VPN. No lab bridge has a host address; the host neither routes between
  VPCs nor into them.
- Gateways: SNAT VPC → public IP, default-deny inbound (ping allowed), port forwards declared per node
  with `expose: ["<public>[:<private>][/tcp|udp]"]`.
- `topology.yml` is the single source of truth (sites, links, nodes, profiles), validated by a JSON
  Schema plus address-plan checks (reserved ranges for incusbr0, docker0, K3s pod/service CIDRs).
- `lab/render.py`: pure function topology → plan (Incus networks, instances with CPU/memory limits,
  generated nftables rulesets, boot scripts, the wan-core tc script, SSH config, Ansible inventory),
  no Incus calls; `opsforge render` prints it.
- Cached images built once by `up` (router image on Alpine with iproute2-tc, nftables, iperf3; node
  image on Debian), shipping sshd + python3 so Ansible manages every instance from first boot. SSH host
  keys stripped from images; `up` pushes per-instance keys generated on the host, so `known_hosts` is
  written in advance and strict host-key checking stays on.

## WAN link-condition model

- netem only shapes egress, so on wan-core each interface facing a site gets an **HTB root with one class
  per peer site**, classified by source gateway IP, each with a **netem** leaf. Unclassified traffic
  (real internet, wan-core's own) is not shaped.
- `rtt` is round-trip, applied as rtt/2 per direction so `ping` matches the configured value; `jitter`
  is the RTT standard deviation (ping's mdev), applied as jitter/√2 per direction with a normal
  distribution; `loss` and `rate` per direction.
- Every link always gets a netem `rate` (10gbit when none is set) because plain netem jitter reorders
  packets and wrecks TCP.
- `opsforge link a-b --rtt/--jitter/--loss/--rate` changes conditions live without recreating anything;
  state lives on wan-core and survives its restart.
- Default links: a-b 40 ms / 5 ms jitter / 0.1% loss / 100 Mbit; a-c 120 ms / 15 ms / 1% / 20 Mbit;
  b-c 90 ms / 10 ms / 0.5% / 50 Mbit.

## Management access, DNS, PKI

- The host enters the lab like an operator on the internet: SSH to a gateway's public IP through
  `incus exec wan-core -- nc` (no host route, no sudo), then `ProxyJump` through the gateway (the site's
  bastion) to the nodes. `up` renders the SSH config and Ansible inventory. Management path is
  unshaped so provisioning is fast and does not disturb experiments.
- Ansible roles: `base` (key-only sshd, minimal packages, journald capped at 32 MiB, apt timers masked),
  `dns` (dnsmasq on each gateway serving its zone `<site>.lab` and forwarding the other zones across the
  WAN, so a cross-site lookup pays the link's RTT; LLMNR/mDNS off), `pki` (ECDSA CA on the controller,
  per-node key generated on the node, cert with name/FQDN/IP SANs, CA trusted system-wide).
- Idempotent: a second `ansible-playbook site.yml` run reports `changed=0`. ansible-lint `production`
  profile passes.

## Site-to-site VPN

- WireGuard full mesh between gateways giving routed private reachability between VPCs (the
  multi-cloud "VPN between VPCs" pattern).
- Tunnel MTU set deliberately (e.g. 1420) with TCP MSS clamping, so MTU problems are visible and
  reproducible on demand; `interconnect: vpn | none` toggle in `topology.yml`.
- Between sites, wan-core only sees UDP/51820, and link conditions still apply to tunnel traffic.

## Stretched K3s cluster

- K3s server on site a (SQLite datastore, traefik/servicelb/metrics-server disabled, flannel VXLAN over
  the VPN with flannel MTU lowered for the double encapsulation VPN + VXLAN); agents on the other sites.
- Nodes labelled `topology.kubernetes.io/region` / `zone`; sample workload spread across regions with
  topology spread constraints.
- Kubelet tuning for small nodes: system/kube reserved resources, eviction thresholds, image garbage
  collection thresholds. Incus container config for K3s captured in a `k3s-node` profile.
- Partitioning a site makes its node NotReady and pods are rescheduled after the eviction timeout;
  healing recovers the node without manual intervention.

## WAN-aware observability

- Grafana with datasources and dashboards provisioned from the repo; node_exporter on all nodes and
  gateways; blackbox exporter probing every site pair (ICMP RTT, TCP connect, HTTP).
- Dashboards: site-to-site latency/loss matrix, node health, K3s overview. An RTT change made with
  `opsforge link` shows on the matrix within one scrape interval.

## Fault injection and scenarios

- CLI: `partition <site>`, `heal`, `flap <link> --period`, `degrade <link> --loss --rate`, `mtu <link> <n>`.
- Scripted scenarios, each run from one command and printing pass/fail against its expected outcome:
  partition a site during sustained writes (no data loss, recovery time measured); raise a link's RTT to
  300 ms (impact on cross-site API latency); path-MTU black hole (the classic "small requests work,
  large ones hang" bug).
- Clock-skew scenarios via `libfaketime`.

## Lightweight CI/CD (optional profile)

- Self-hosted Git + CI and a `registry:2` image registry on a CI node in site a.
- Flux on the cluster pulls manifests from the Git server (GitOps across the WAN).
- A reference workload (web app + database) deployed through the pipeline: a push builds an image,
  pushes it to the registry, and Flux rolls it out across sites.

## Multi-cluster

- One K3s cluster per site ("per cloud"), interconnected for cross-cluster services.
- Scenarios: cross-cluster service failover, geo-aware DNS, loss of an entire "cloud"; a service
  survives the total loss of the cluster it was primarily served from.

## Host setup and tooling

- `scripts/host-setup.sh` (idempotent, root): installs Incus, maps subuid/subgid, initialises Incus by
  preseed (btrfs pool on a sparse loop file for copy-on-write clones), persists kernel modules
  (`br_netfilter`, `overlay`, `nf_conntrack`, `wireguard`, `sch_netem`, `sch_htb`) and sysctls.
- Docker coexistence: a systemd unit inserts `DOCKER-USER` iptables accepts for the lab bridges and
  re-applies them on every Docker restart (Docker's FORWARD DROP policy otherwise drops Incus traffic).
- `opsforge` CLI in Python 3 (stdlib + PyYAML + jsonschema): `validate`, `preflight`, `smoke`, `up`,
  `down`, `status`, `link`, `verify`, `render`, `provision`, `ssh`, plus the fault-injection commands.
- `opsforge verify` runs acceptance checks against the live link state: latency per link, VPC
  isolation, internet access, bandwidth (iperf3), SSH, DNS (12 names per node), PKI.
- `make check`: shellcheck, yamllint, Python syntax, ansible-lint, topology validation.

## Numbers (measured on the base lab: wan-core + 3 gateways + 3 Debian nodes, before K3s)

- One Debian 13 container idles at 113 MiB.
- Idle lab **312 MiB**: wan-core 9 MiB, gateways 6 MiB each, nodes ~96 MiB each; router image
  5.8 MiB; `up` takes ~10 s with cached images.
- Provisioned and idle: Incus reports 1042 MiB, of which 921 MiB is reclaimable page cache;
  non-reclaimable (anon + kernel) **101 MiB** for the whole 7-instance lab. Images: node 126 MiB,
  router 21 MiB. From scratch: `up` ~50 s, first `provision` ~1 min, re-run ~20 s.
- Verified: ping between sites matches the configured RTT (≈40 ms a-b, ≈120 ms a-c), iperf3 tops out
  at the configured rate, VPCs cannot reach each other's private IPs, `down && up` reproduces the lab
  from scratch.
