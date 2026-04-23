# Issue #1903: Helm chart: setting `integrations.podOptions.namespaceSelector` results in webhook selector being erased

**Summary**: Helm chart: setting `integrations.podOptions.namespaceSelector` results in webhook selector being erased

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1903

**Last updated**: 2024-04-30T17:52:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rhaps0dy](https://github.com/rhaps0dy)
- **Created**: 2024-03-25T19:30:25Z
- **Updated**: 2024-04-30T17:52:50Z
- **Closed**: 2024-04-30T17:52:50Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What happened**:

I added the following to `managerConfig.controllerManagerConfigYaml` in my Helm chart configuration:

```yaml
integrations:
  frameworks:
  - ...
  - "pod"
  podOptions:
    namespaceSelector:
      matchExpressions:
      - key: kubernetes.io/metadata.name
        operator: NotIn
        values: ["kube-system", "kueue-system"]
```


**What you expected to happen**:

The pod MutatingWebhook stays correct.

**How to reproduce it (as minimally and precisely as possible)**:

- modify the `managerConfig.controllerManagerConfigYaml` in `charts/kueue/values.yaml` to the value above. **Make sure that podOptions is a child of `integrations`, this has bitten me in the past.**

- Run:
```sh
helm template -n kueue-system my-release . less
```
and search for `mpod.kb.io` and `vpod.kb.io`. It looks like this:

```yaml
    name: mpod.kb.io
    namespaceSelector:    # <- NOTE: WRONG INDENTATION
    matchExpressions:
    - key: kubernetes.io/metadata.name
      operator: NotIn
      values:
      - kube-system
      - kueue-system
```

```yaml
    name: vpod.kb.io
    namespaceSelector:
    matchExpressions:
    - key: kubernetes.io/metadata.name
      operator: NotIn
      values:
      - kube-system
      - kueue-system

```

**Anything else we need to know?**:

To solve this, just change `nindent 4` to `nindent 6` in `add_webhook_pod_mutate` and `add_webhook_pod_validate` of `hack/update-helm.sh`, and in the corresponding part of the helm chart.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-15T13:43:13Z

@rhaps0dy if you fixed this, could you open a PR?

### Comment by [@rhaps0dy](https://github.com/rhaps0dy) — 2024-04-30T17:52:50Z

Looks like #2086 fixed this.
