# Issue #9286: test-tas-e2e command doesn't work well

**Summary**: test-tas-e2e command doesn't work well

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9286

**Last updated**: 2026-02-16T15:22:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-02-16T13:32:14Z
- **Updated**: 2026-02-16T15:22:37Z
- **Closed**: 2026-02-16T15:22:36Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I executed `make kind-image-build test-tas-e2e`, but no valid kueue-controller-manager started.
The kueue-controller-manager keeps crashing due to the following logs:

```shell
ERROR   setup   kueue/main.go:343       Unable to create and start visibility server   {"error": "unable to apply VisibilityServerOptions: error creating self-signed certificates: error reading /visibility/apiserver.key, certificate and key must be supplied as a pair"}
main.main.func2
        /workspace/cmd/kueue/main.go:343
```

**What you expected to happen**:
Successfully started tests.

**How to reproduce it (as minimally and precisely as possible)**:
`make kind-image-build test-tas-e2e`

**Anything else we need to know?**:
The following is deployed Kueue Configuration:

```yaml
apiVersion: v1
data:
  controller_manager_config.yaml: |
    apiVersion: config.kueue.x-k8s.io/v1beta2
    kind: Configuration
    metrics:
      enableClusterQueueResources: true
    leaderElection:
      leaderElect: true
    controller:
      groupKindConcurrency:
        Job.batch: 5
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    fairSharing:
      preemptionStrategies: ["LessThanOrEqualToFinalShare", "LessThanInitialShare"]
    clientConnection:
      qps: 50
      burst: 100
    integrations:
      frameworks:
      - "batch/job"
      - "kubeflow.org/mpijob"
      - "ray.io/rayjob"
      - "ray.io/raycluster"
      - "jobset.x-k8s.io/jobset"
      - "kubeflow.org/paddlejob"
      - "kubeflow.org/pytorchjob"
      - "kubeflow.org/tfjob"
      - "kubeflow.org/xgboostjob"
      - "kubeflow.org/jaxjob"
      - "trainer.kubeflow.org/trainjob"
      - "workload.codeflare.dev/appwrapper"
      - "pod"
      - "deployment"
      - "statefulset"
      - "leaderworkerset.x-k8s.io/leaderworkerset"
    featureGates:
      LocalQueueMetrics: true
      ElasticJobsViaWorkloadSlices: true
    tls:
      minVersion: "VersionTLS12"
      # this is the default ciphersuite for golang 1.25
      cipherSuites:
        - TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
        - TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
        - TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256
        - TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256
        - TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
        - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
kind: ConfigMap
metadata:
  labels:
    app.kubernetes.io/name: kueue
    control-plane: controller-manager
  name: kueue-manager-config
  namespace: kueue-system
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T13:33:33Z

@mbobrovskyi @vladikkuzn Have you seen recently if `test-tas-e2e` works correctly?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T13:41:20Z

Hm, this worked well for me something like 10 days ago, not sure if broke recently.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T13:49:37Z

> Hm, this worked well for me something like 10 days ago, not sure if broke recently.

I'm not sure if this problem is a platform (MacOS) specific one.
IIRC, your development platform is Linux-based.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T15:22:25Z

I found the root cause.
My Docker Desktop VM volume is almost occupied, then failed to load the latest kueue-controller-manager image, then the outdated version is used during tests.

After I expanded the VM volume, the errors have gone away.
The curious thing is the reason why loading errors don't happen.

Anyway, let's close this issue. Thank you for taking care of this.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-16T15:22:31Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-16T15:22:37Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9286#issuecomment-3909057790):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
