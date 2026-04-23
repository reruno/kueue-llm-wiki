# Issue #2682: manager unclosed action

**Summary**: manager unclosed action

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2682

**Last updated**: 2024-07-24T13:58:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@serhii-kuzniechykov](https://github.com/serhii-kuzniechykov)
- **Created**: 2024-07-23T20:32:49Z
- **Updated**: 2024-07-24T13:58:28Z
- **Closed**: 2024-07-24T13:55:02Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

Hello 
Sorry for reporting this small thing.

**What happened**: 
```
helm install kueue kueue/ --create-namespace --namespace kueue-system --set enableCertManager=true
Error: parse error at (kueue/templates/manager/manager.yaml:59): unclosed action
```

**What you expected to happen**:
```helm install kueue kueue/ --create-namespace --namespace kueue-system --set enableCertManager=true
NAME: kueue
LAST DEPLOYED: Tue Jul 23 23:20:02 2024
NAMESPACE: kueue-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

**Anything else we need to know?**:
```
    resources: {{- toYaml .Values.controllerManager.manager.resources | nindent 10
          }}
```
```
resources: {{- toYaml .Values.controllerManager.manager.resources | nindent 10 }}
```
**Environment**:
- Kubernetes version (use `kubectl version`): Client Version: v1.28.2
- Kueue version (use `git describe --tags --dirty --always`): v0.8.0-1-g78783a26-dirty
- Cloud provider or hardware configuration: Azure
- OS (e.g: `cat /etc/os-release`): Windows
- Kernel (e.g. `uname -a`):
- Install tools: Helm
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-24T05:54:16Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-24T13:58:26Z

@serhii-kuzniechykov Could you check with last changes? If you still have an issue, please reopen it.
