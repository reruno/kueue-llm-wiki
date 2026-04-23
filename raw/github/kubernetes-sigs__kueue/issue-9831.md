# Issue #9831: Proactively prepare an upgrade to Kubeflow Trainer 2.2

**Summary**: Proactively prepare an upgrade to Kubeflow Trainer 2.2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9831

**Last updated**: 2026-03-27T12:46:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-12T13:44:38Z
- **Updated**: 2026-03-27T12:46:57Z
- **Closed**: 2026-03-27T12:46:57Z
- **Labels**: `kind/feature`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 3

## Description

**What would you like to be added**:

Kubeflow Trainer 2.2 is coming: https://github.com/kubeflow/trainer/issues/3116

The idea is to integrate it without unnecessary delay, by preparing the necessary branch and testing proactively using the staging images / branches.

**Why is this needed**:

To integrate with the latest kubeflow, and to avoid unnecessary delays for the integration.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-12T13:44:57Z

cc @kaisoz @tenzen-y @andreyvelich @astefanutti

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-03-12T13:51:03Z

/assign

I'd like to own this one since I'm monitoring other Trainer relates issues 🙂

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-03-13T23:12:32Z

Hi Folks, KF Trainer `v2.2.0-rc.0` is ready:
```bash
helm install kubeflow-trainer oci://ghcr.io/kubeflow/charts/kubeflow-trainer \
    --namespace kubeflow-system \
    --create-namespace \
    --version 2.2.0-rc.0
    --set runtimes.defaultEnabled=true
```
