# Issue #1372: E2E tests startup is flaky

**Summary**: E2E tests startup is flaky

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1372

**Last updated**: 2023-12-19T19:56:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2023-11-28T13:57:24Z
- **Updated**: 2023-12-19T19:56:27Z
- **Closed**: 2023-12-19T19:56:27Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 20

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
During e2e tests webhooks are not ready which results in failing e2e tests

**What happened**:
E2E test failed on testing kueue readiness 

**What you expected to happen**:
E2E test to succeed 

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1365/pull-kueue-test-e2e-main-1-28/1729486888244350976

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2023-11-28T13:58:05Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2023-11-30T09:33:42Z

Looks like flaked again: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1378/pull-kueue-test-e2e-main-1-26/1730154566130864128

```
[0m[1m[BeforeSuite] [0m
[38;5;243m/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/suite_test.go:94[0m
  [38;5;9m[FAILED][0m in [BeforeSuite] - /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/suite_test.go:90 [38;5;243m@ 11/28/23 13:12:39.891[0m
[38;5;9m[BeforeSuite] [FAILED] [60.003 seconds][0m
[38;5;9m[1m[BeforeSuite] [0m
[38;5;243m/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/suite_test.go:94[0m

  [38;5;9m[FAILED] Timed out after 60.000s.
  Expected success, but got an error:
      <*errors.StatusError | 0xc00022e0a0>: 
      Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s": dial tcp 10.244.2.2:9443: connect: connection refused
      {
          ErrStatus: {
              TypeMeta: {Kind: "", APIVersion: ""},
              ListMeta: {
                  SelfLink: "",
                  ResourceVersion: "",
                  Continue: "",
                  RemainingItemCount: nil,
              },
              Status: "Failure",
              Message: "Internal error occurred: failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": dial tcp 10.244.2.2:9443: connect: connection refused",
              Reason: "InternalError",
              Details: {
                  Name: "",
                  Group: "",
                  Kind: "",
                  UID: "",
                  Causes: [
                      {
                          Type: "",
                          Message: "failed calling webhook \"mresourceflavor.kb.io\": failed to call webhook: Post \"https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s\": dial tcp 10.244.2.2:9443: connect: connection refused",
                          Field: "",
                      },
                  ],
                  RetryAfterSeconds: 0,
              },
              Code: 500,
          },
      }[0m
```

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-01T09:43:05Z

Another recent occurrence: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1378/pull-kueue-test-e2e-main-1-28/1730521196279107584

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-04T21:32:17Z

Uhm.... I wonder if we need to increase the timeout or cpu/memory of the job.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-04T23:09:51Z

According to the Grafana dashboard, resource requests seem to be sufficient. The max usage for CPU is 8.27 Core, and memory is 1.69 GiB.

https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-e2e-main-1-26&refresh=30s&var-build=All

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-04T23:11:28Z

I'm wondering if there are noisy neighbors 🤔

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-06T10:53:29Z

Another happening: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1412/pull-kueue-test-e2e-main-1-27/1732350401358860288

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-06T14:45:59Z

Should we just increase the timeout for waiting for the webhook?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-08T17:47:20Z

> Should we just increase the timeout for waiting for the webhook?

I think so since it seems that jobs have enough resource requests.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T21:28:30Z

It looks like jobset is still having issues.

We should start by increasing the visibility into what is pending. Perhaps obtaining the status of the kueue-controller Pod is enough.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T21:28:50Z

I'll take this for now
/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T21:43:53Z

Comparing the kueue logs from a [successful run](https://storage.googleapis.com/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-27/1734944715230416896/artifacts/run-test-e2e-1.27.3/kueue-controller-manager.log) with an [unsuccessful run](https://storage.googleapis.com/kubernetes-jenkins/logs/periodic-kueue-test-e2e-main-1-27/1733494602704359424/artifacts/run-test-e2e-1.27.3/kueue-controller-manager.log), something that catches my eye is the absence of the line `CA certs are injected to webhooks` in the failing one.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T18:03:21Z

The first relevant log line to be absent is
https://github.com/open-policy-agent/cert-controller/blob/01a9f146b6f1c2f5ed6d496c4ca78a84bde4325b/pkg/rotator/rotator.go#L857C32-L857C32

@astefanutti does this give any clues? What should be generating this file? What does it depend on?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T19:20:31Z

When the certs become ready, it doesn't take more than 5 seconds since the first kueue log line. So a greater timeout is unlikely to fix the issue.

I'm currently testing cert-controller 0.9 in an attempt to narrow down a culprit https://github.com/kubernetes-sigs/kueue/pull/1489

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T20:08:25Z

The E2E test is also failing with 0.9. I wanted to try 0.7, but there are some dependency issues that prevented me from trying.

I'm curious about whether the issue is related to https://github.com/open-policy-agent/cert-controller/pull/81

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-18T20:18:50Z

Uhm... I don't think so. I do see the message:

```
server certs refreshed
```

Meaning that an initial write was sent to the apiserver. It looks like what should happen next is that the kubelet watches the update of the Secret and updates the file.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-19T10:22:53Z

> The first relevant log line to be absent is https://github.com/open-policy-agent/cert-controller/blob/01a9f146b6f1c2f5ed6d496c4ca78a84bde4325b/pkg/rotator/rotator.go#L857C32-L857C32
> 
> @astefanutti does this give any clues? What should be generating this file? What does it depend on?

@alculquicondor That file has the following lifecycle (simplified with the relevant bits):

1. The `webhook-server-cert` Secret is mounted into the Kueue Deployment at `tmp/k8s-webhook-server/serving-certs`)
2. Concurrently:
    1. cert-controller generates the certificates and updates the `webhook-server-cert` Secret
        1. the kubelet propagates the update into the Secret volume mount from 1.
        1. cert-controller checks the server certificate is mounted and closes the `certsMounted` channel
    7. cert-controller injects the CA certificate into the admission webhooks and closes the `IsReady` channel (if `certsMounted` is also closes)
3. The Kueue webhooks are started along with the other controllers (gated by the `IsReady` channel)

In the failing runs, it's step 2.i.b. that fails to proceed. I initially though it could be the kubelet that takes too much time to propagate the Secret update to the volume mount (depending on the `configMapAndSecretChangeDetectionStrategy` kubelet configuration), but then the `ensureCertsMounted` method should print `max retries for checking certs existence`.

I still fail to understand what could cause to break what seems to be the two invariants of the `ensureCertsMounted` method, that are either log:
* `certs are ready in /tmp/k8s-webhook-server/serving-certs`
* Or `max retries for checking certs existence`

I'll keep digging, but it may be more productive to create a "DO NOT MERGE" PR with some added data points that could help nailing down why that `ensureCertsMounted` invariants are broken. How does that sound to you?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-19T11:08:13Z

I realise with the exponential backoff configuration that's used in the `ensureCertsMounted` method:

```
wait.Backoff{ Duration: 1 * time.Second, Factor: 2, Jitter: 1, Steps: 10}
```

The tests time out before the backoff in the `ensureCertsMounted` method does.

So it's still a possibility the update made to the Secret by cert-controller isn't propagated as expected into the volume mount by the kubelet.

### Comment by [@astefanutti](https://github.com/astefanutti) — 2023-12-19T11:23:49Z

I've just found https://ahmet.im/blog/kubernetes-secret-volumes-delay/ that seems to corroborate the long Secret volume mount update propagation hypothesis.

@alculquicondor Based on that article, to validate the test timeout increase approach as in #1491, a value as long as two minutes might be needed.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-19T15:36:51Z

That article is very useful, thanks!

Yes, it sounds like 2 minutes should be the target (how annoying).

Otherwise, I wonder if I can cause a Pod status update (to trigger kubelet sync) using the readiness probes more smartly. But I'll leave that as a follow up. It sounds like something like this might be happening most of the time, as we get the secrets updated within 5s when the test passes.
