# Issue #5455: managedJobsNamespaceSelector fails helm upgrade

**Summary**: managedJobsNamespaceSelector fails helm upgrade

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5455

**Last updated**: 2025-06-05T03:10:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Yienschwen](https://github.com/Yienschwen)
- **Created**: 2025-06-03T06:45:12Z
- **Updated**: 2025-06-05T03:10:50Z
- **Closed**: 2025-06-05T03:10:49Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
helm upgrade failed when `managedJobsNamespaceSelector` is specified in `managerConfig.controllerManagerConfigYaml` 

```
Error: YAML parse error on kueue/templates/webhook/manifests.yaml: error converting YAML to JSON: yaml: line 22: mapping values are not allowed in this context
helm.go:92: 2025-06-03 14:32:27.097675 +0800 CST m=+1.473521585 [debug] error converting YAML to JSON: yaml: line 22: mapping values are not allowed in this context
```

**What you expected to happen**:
(successful helm upgrade)

**How to reproduce it (as minimally and precisely as possible)**:

run `helm install --create-namespace -n kueue-system kueue oci://registry.k8s.io/kueue/charts/kueue --values kueue/values.yaml --version=0.12.1` with the following values:
```yaml
managerConfig:
  controllerManagerConfigYaml: |-
    apiVersion: config.kueue.x-k8s.io/v1beta1
    kind: Configuration
    managedJobsNamespaceSelector:
      matchLabels:
        kueue-managed: "true"
    integrations:
      frameworks:
      - "pod"
```

**Anything else we need to know?**:

It seems that the `-` at the end of each `{{- if (hasKey $managerConfig "managedJobsNamespaceSelector") -}}` is causing this bug, here's a sample piece of rendered yaml:
```yaml
# Source: kueue/templates/webhook/manifests.yaml

apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  labels:
    helm.sh/chart: kueue-0.12.1
    app.kubernetes.io/name: kueue
    app.kubernetes.io/instance: kueue
    control-plane: controller-manager
    app.kubernetes.io/version: "v0.12.1"
    app.kubernetes.io/managed-by: Helm
  name: 'kueue-mutating-webhook-configuration'
  namespace: 'default'
webhooks:
  - admissionReviewVersions:
      - v1
    clientConfig:
      service:
        name: 'kueue-webhook-service'
        namespace: 'default'
        path: /mutate-workload-codeflare-dev-v1beta2-appwrapper
    failurePolicy: Fail
    name: mappwrapper.kb.ionamespaceSelector: # <- newline missing
      matchLabels:
        kueue-managed: "true"
    rules:
# ...
```

Rendered yaml debug output:
[debug.yml.zip](https://github.com/user-attachments/files/20563481/debug.yml.zip)

**Environment**:
- Kubernetes version (use `kubectl version`): 
```
Client Version: v1.33.1
Kustomize Version: v5.6.0
Server Version: v1.32.5+rke2r1
```
- Kueue version (use `git describe --tags --dirty --always`): `v0.12.1`
- Cloud provider or hardware configuration: 
- OS (e.g: `cat /etc/os-release`): Rocky Linux 9.5
- Kernel (e.g. `uname -a`): `5.14.0-503.40.1.el9_5.x86_64 #1 SMP PREEMPT_DYNAMIC Wed Apr 30 17:38:54 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux`
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T07:01:20Z

@Yienschwen thank you for reporting. I believe this is already fixed and is waiting for release in 0.12.2: https://github.com/kubernetes-sigs/kueue/pull/5396

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T07:02:57Z

FYI: https://github.com/kubernetes-sigs/kueue/issues/5456

### Comment by [@Yienschwen](https://github.com/Yienschwen) — 2025-06-05T03:10:49Z

> [@Yienschwen](https://github.com/Yienschwen) thank you for reporting. I believe this is already fixed and is waiting for release in 0.12.2: [#5396](https://github.com/kubernetes-sigs/kueue/pull/5396)

Thank you for your reply. I tried out the new 0.12.2 release and the issue is fixed.
