# Issue #4928: Helm: inconsistency between version in repo and chart metadata

**Summary**: Helm: inconsistency between version in repo and chart metadata

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4928

**Last updated**: 2025-04-15T14:11:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@j-vizcaino](https://github.com/j-vizcaino)
- **Created**: 2025-04-11T11:35:44Z
- **Updated**: 2025-04-15T14:11:12Z
- **Closed**: 2025-04-15T14:11:12Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What happened**:

Installing `kueue` Helm chart using Helm Terraform provider leads to errors.

**What you expected to happen**:

Installation should work as expected.

**How to reproduce it (as minimally and precisely as possible)**:

Snippet:

```hcl
resource "helm_release" "kueue" {
  chart   = "oci://registry.k8s.io/kueue/charts/kueue"
  version = "0.11.3"

  name      = "kueue"
  namespace = "kueue-system"
  create_namespace = true
}
```

When running `terraform apply`, the Helm release turns `0.11.3` into `v0.11.3` which leads to the chart failing to download.

```
Error: could not download chart: registry.k8s.io/kueue/charts/kueue:v0.11.3: not found
```

**Anything else we need to know?**:

The issue is caused by an inconsistency between the `version` field, reported in the `Chart.yaml` and the actual version used for publishing in the OCI registry.

Example: registry uses `0.11.3` but `Chart.yaml` indicates `version: v0.11.3`

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): 0.11.3
- Cloud provider or hardware configuration: AWS/EKS
- Install tools: Terraform 1.8.2, Helm provider 2.17.0

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-11T12:13:21Z

cc @tenzen-y ptal
