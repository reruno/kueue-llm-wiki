# Issue #1315: helm install Error using default controllerManagerConfigYaml

**Summary**: helm install Error using default controllerManagerConfigYaml

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1315

**Last updated**: 2023-11-09T15:54:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@B1F030](https://github.com/B1F030)
- **Created**: 2023-11-08T08:53:07Z
- **Updated**: 2023-11-09T15:54:21Z
- **Closed**: 2023-11-09T15:54:21Z
- **Labels**: `kind/bug`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When using Helm to install kueue, Error happens:
`# helm install kueue kueue/ --namespace kueue-system `
```
Error: INSTALLATION FAILED: template: kueue/templates/webhook/webhook.yaml:120:84:
executing "kueue/templates/webhook/webhook.yaml" at <$integrationsConfig.podOptions>:
wrong type for value; expected map[string]interface {}; got interface {}
```
in [webhook.yaml#L120:](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/templates/webhook/webhook.yaml#L120)

`{{- if and (hasKey $integrationsConfig "podOptions") (hasKey $integrationsConfig.podOptions "namespaceSelector") }}`

When [integrations.podOptions](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml#L97) is not set(by default), the expression above caused this Error below: 

`$integrationsConfig.podOptions got interface {}`

**What you expected to happen**:
This Error shoud not happen when default config is used.

**How to reproduce it (as minimally and precisely as possible)**:
```
$ git clone https://github.com/kubernetes-sigs/kueue.git
$ cd kueue/charts
$ helm install kueue kueue/ --create-namespace --namespace kueue-system
```

**Anything else we need to know?**:
related PR:
#1247


**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): main
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@stuton](https://github.com/stuton) — 2023-11-08T15:03:09Z

/assign
