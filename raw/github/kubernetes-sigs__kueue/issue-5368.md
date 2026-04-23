# Issue #5368: Fix the GitVersion reported by Kueue to only contain tag

**Summary**: Fix the GitVersion reported by Kueue to only contain tag

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5368

**Last updated**: 2025-06-04T12:58:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-26T17:54:01Z
- **Updated**: 2025-06-04T12:58:38Z
- **Closed**: 2025-06-04T12:58:38Z
- **Labels**: `kind/bug`, `kind/regression`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 6

## Description

**What happened**:

The release 0.12.0 of Kueue reports GitVersion as "v20250526-v0.12.0". The commit "b4306accba45a46b19c1aecc014de269dfeb9e13" is correct.

**What you expected to happen**:

the version reported in GitVersion should be "v0.12.0" as for "v0.11.5".

**How to reproduce it (as minimally and precisely as possible)**:

Run
```
> docker run -it registry.k8s.io/kueue/kueue:v0.12.0
{"level":"info","ts":"2025-05-26T17:52:32.290334192Z","logger":"setup","caller":"kueue/main.go:468","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-05-26T17:52:32.290482621Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v20250526-v0.12.0","gitCommit":"b4306accba45a46b19c1aecc014de269dfeb9e13"}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-26T17:54:32Z

/kind regression 
since it was ok in 0.11.5
```
> docker run -it registry.k8s.io/kueue/kueue:v0.11.5
{"level":"info","ts":"2025-05-26T17:53:28.425701711Z","logger":"setup","caller":"kueue/main.go:464","msg":"Successfully loaded configuration","config":"apiVersion: config.kueue.x-k8s.io/v1beta1\nclientConnection:\n  burst: 30\n  qps: 20\nhealth:\n  healthProbeBindAddress: :8081\nintegrations:\n  frameworks:\n  - batch/job\ninternalCertManagement:\n  enable: true\n  webhookSecretName: kueue-webhook-server-cert\n  webhookServiceName: kueue-webhook-service\nkind: Configuration\nleaderElection:\n  leaderElect: true\n  leaseDuration: 15s\n  renewDeadline: 10s\n  resourceLock: leases\n  resourceName: c1f6bfd2.kueue.x-k8s.io\n  resourceNamespace: \"\"\n  retryPeriod: 2s\nmanageJobsWithoutQueueName: false\nmanagedJobsNamespaceSelector:\n  matchExpressions:\n  - key: kubernetes.io/metadata.name\n    operator: NotIn\n    values:\n    - kube-system\n    - kueue-system\nmetrics:\n  bindAddress: :8443\nmultiKueue:\n  gcInterval: 1m0s\n  origin: multikueue\n  workerLostTimeout: 15m0s\nnamespace: kueue-system\nqueueVisibility:\n  clusterQueues:\n    maxCount: 10\n  updateIntervalSeconds: 5\nwebhook:\n  port: 9443\n"}
{"level":"info","ts":"2025-05-26T17:53:28.426163811Z","logger":"setup","caller":"kueue/main.go:146","msg":"Initializing","gitVersion":"v0.11.5","gitCommit":"7a3498f047900c8a66ac3f86fb4248cbca1edc5c"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-26T17:54:42Z

cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T05:38:40Z

I think this is the PR causing the regression https://github.com/kubernetes-sigs/kueue/pull/5210/files 

let me assign tentatively, I think we can fix it and simplify the release flow
/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-27T05:55:02Z

I think this happens because we're setting environment variables in `cloudbuild.yaml` using the format `vYYYYMMDD-hash` https://github.com/kubernetes-sigs/kueue/blob/main/cloudbuild.yaml#L15-L23  and it's replacing the tag with the new changes from https://github.com/kubernetes-sigs/kueue/pull/5210.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T06:02:25Z

Yes, I don't think we even want the cloud build variable at all. it makes reasoning really hard because GIT_TAG is different locally and on CI. The local git command ( `git describe --tags --dirty --always`, used in Makefile as fallback) already generates unique tag so I don't see any reason for using the cloudbuild variable

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-27T06:31:43Z

Just to confirm that the `kueuectl` version is correct.

```
$ wget https://github.com/kubernetes-sigs/kueue/releases/download/v0.12.0/kubectl-kueue-darwin-arm64
$ chmod +x ./kubectl-kueue-darwin-arm64
$ ./kubectl-kueue-darwin-arm64 version 
Client Version: v0.12.0
Kueue Controller Manager Image: us-central1-docker.pkg.dev/k8s-staging-images/kueue/kueue:v0.12.0
```
