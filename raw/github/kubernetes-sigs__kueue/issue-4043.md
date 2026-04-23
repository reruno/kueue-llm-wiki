# Issue #4043: Fail to enable batch jobs

**Summary**: Fail to enable batch jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4043

**Last updated**: 2025-02-05T00:19:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@octotocat](https://github.com/octotocat)
- **Created**: 2025-01-23T23:49:30Z
- **Updated**: 2025-02-05T00:19:38Z
- **Closed**: 2025-02-05T00:19:38Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 0

## Description

Kueue controller manager container failed to start if I enable batch: 
Config refers to https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/
```
managerConfig:
  controllerManagerConfigYaml: |-
...
  waitForPodsReady:
      enable: true
      timeout: 5m
      blockAdmission: true
      requeuingStrategy:
        timestamp: Eviction | Creation
        backoffLimitCount: 5 # null indicates infinite requeuing
        backoffBaseSeconds: 60
        backoffMaxSeconds: 3600
```
with pod integration: 
``` 
   integrations:
      frameworks:
      - "pod"
      - "deployment"
      podOptions:
        namespaceSelector:
          matchExpressions:
            - key: kubernetes.io/metadata.name
              operator: NotIn
              values: [ kube-system, kueue-system ]
            - key: kueue-job
              operator: In
              values: [ "true", "True", "yes" ]
```
Error: Back-off restarting failed container manager in pod kueue-controller-manager-xxx. No container log as container failed to start. 
Any clue? 
Version: v0.10.1. 
Same config used to work with v0.8.1. After upgraded to v10, didn't work, and when I downgraded to v8 again, still didn't work.
