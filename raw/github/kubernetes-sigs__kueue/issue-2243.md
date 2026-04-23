# Issue #2243: Pod controller: "when Using pod group Should keep the running pod group with the queue name if workload is evicted" flakes

**Summary**: Pod controller: "when Using pod group Should keep the running pod group with the queue name if workload is evicted" flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2243

**Last updated**: 2024-05-22T19:19:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-05-21T06:11:21Z
- **Updated**: 2024-05-22T19:19:24Z
- **Closed**: 2024-05-22T19:19:24Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake
**What happened**:
Integration Test failed on "Pod Controller Suite: [It] Pod controller when manageJobsWithoutQueueName is disabled when Using pod group Should keep the running pod group with the queue name if workload is evicted" 

```shell
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:685 with:
Expected
    <[]v1.PodSchedulingGate | len:1, cap:1>: [
        {
            Name: "kueue.x-k8s.io/admission",
        },
    ]
not to contain element matching
    <v1.PodSchedulingGate>: {
        Name: "kueue.x-k8s.io/admission",
    } failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:685 with:
Expected
    <[]v1.PodSchedulingGate | len:1, cap:1>: [
        {
            Name: "kueue.x-k8s.io/admission",
        },
    ]
not to contain element matching
    <v1.PodSchedulingGate>: {
        Name: "kueue.x-k8s.io/admission",
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/pod/pod_controller_test.go:705 @ 05/21/24 05:50:59.975
}
```

**What you expected to happen**:
No error happend.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2221/pull-kueue-test-integration-main/1792793854399746048

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-21T07:26:50Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-21T07:37:46Z

it also failed on the periodic build of the main branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1791879493841850368

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-21T08:26:05Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2236/pull-kueue-test-integration-main/1792832117407748096

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-21T09:40:14Z

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2248/pull-kueue-test-integration-main/1792846296294363136
