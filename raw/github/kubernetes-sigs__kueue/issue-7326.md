# Issue #7326: [flaky test] PyTorch integration when PyTorch created should admit group with leader only

**Summary**: [flaky test] PyTorch integration when PyTorch created should admit group with leader only

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7326

**Last updated**: 2025-10-24T10:47:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-20T12:50:04Z
- **Updated**: 2025-10-24T10:47:36Z
- **Closed**: 2025-10-24T10:47:36Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7325/pull-kueue-test-e2e-main-1-31/1980248809606746112

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.31.12: [It] PyTorch integration when PyTorch created should admit group with leader only expand_less	1m29s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pytorchjob_test.go:115 with:
Unexpected number of active Worker replicas
Expected
    <int32>: 1
to equal
    <int32>: 2 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pytorchjob_test.go:115 with:
Unexpected number of active Worker replicas
Expected
    <int32>: 1
to equal
    <int32>: 2
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pytorchjob_test.go:124 @ 10/20/25 12:36:47.088
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-20T12:50:12Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T06:34:51Z

Ok I analyzed logs based on  this build: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7341/pull-kueue-test-e2e-main-1-31/1981043923610505216

take a look here: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7341/pull-kueue-test-e2e-main-1-31/1981043923610505216/artifacts/run-test-e2e-singlecluster-1.31.12/kind-worker/kubelet.log

We have:

```
\"alpine:3.10\""
Oct 22 17:17:42 kind-worker kubelet[277]: I1022 17:17:42.011896     277 provider.go:82] Docker config file not found: couldn't find valid .dockercfg after checking in [/var/lib/kubelet   /]
Oct 22 17:17:42 kind-worker kubelet[277]: I1022 17:17:42.011925     277 kuberuntime_image.go:51] "Pulling image without credentials" image="alpine:3.10"
Oct 22 17:17:42 kind-worker kubelet[277]: I1022 17:17:42.021229     277 event.go:389] "Event occurred" object="pytorch-e2e-fcjhp/pytorch-simple-worker-1" fieldPath="spec.initContainers{init-pytorch}" kind="Pod" apiVersion="v1" type="Normal" reason="Pulling" message="Pulling image \"alpine:3.10\""
```
So this looks like pulling external image alpine:3.10 from unit container.

And I found that PyTorch is adding that to all Jobs with workers, see links:
- https://github.com/kubeflow/trainer/blob/v1.9.3/pkg/controller.v1/pytorch/initcontainer.go#L57 
- https://github.com/kubeflow/trainer/blob/v1.9.3/pkg/config/config.go#L28C7-L28C50

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T06:37:46Z

To solve the issue I consider:
1. don't create any Workers in the e2e tests
2. pre-pull the image
3. increase timeout

TBH I'm leaning to 1., because the mechanism from Kueue PoV looks the same.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T06:41:24Z

I could see this issue affecting a couple branches, seems like the most common flake currently.
Another example: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7226/pull-kueue-test-e2e-main-1-31/1981042931980570624

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-24T09:47:55Z

Also likely related https://github.com/kubernetes-sigs/kueue/issues/7382
