# Issue #9058: [flaky test ] Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay]

**Summary**: [flaky test ] Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9058

**Last updated**: 2026-02-10T21:55:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-09T12:33:35Z
- **Updated**: 2026-02-10T21:55:19Z
- **Closed**: 2026-02-10T21:55:18Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 8

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
 
Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay]

**Link to failed CI job or steps to reproduce locally**:

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-e2e-k8s-main-was

**Failure message or logs**:
```
End To End Suite: k8s-main:latest: [It] Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay] expand_less	9m31s
{Timed out after 300.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/kuberay_test.go:340 with:
Expected exactly 1 pods with 'workers' in the name
Expected
    <[]string | len:0, cap:0>: nil
to have length 1 failed [FAILED] Timed out after 300.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/kuberay_test.go:340 with:
Expected exactly 1 pods with 'workers' in the name
Expected
    <[]string | len:0, cap:0>: nil
to have length 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/kuberay_test.go:345 @ 02/09/26 11:50:55.211
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T12:33:44Z

cc @hiboyang ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T12:34:11Z

maybe @sohankunkerkar or @mbobrovskyi would also have some ideas

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-09T22:10:46Z

/assign

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-09T22:30:26Z

Maybe we should make the rayjob in this test running longer after scaling down, so there will be longer time with 1 pod after scaling down? e.g. for this line https://github.com/kubernetes-sigs/kueue/blob/9a1de0101409e94adf3bc6ccc4e02831f587f987/test/e2e/singlecluster/kuberay_test.go#L187 , change `range(16)` to `range(32)`?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-10T05:57:27Z

> Maybe we should make the rayjob in this test running longer after scaling down, so there will be longer time with 1 pod after scaling down? e.g. for this line
> 
> [kueue/test/e2e/singlecluster/kuberay_test.go](https://github.com/kubernetes-sigs/kueue/blob/9a1de0101409e94adf3bc6ccc4e02831f587f987/test/e2e/singlecluster/kuberay_test.go#L187)
> 
> Line 187 in [9a1de01](/kubernetes-sigs/kueue/commit/9a1de0101409e94adf3bc6ccc4e02831f587f987)
> 
>  print([ray.get(my_task.remote(i, 1)) for i in range(16)])`, 
> , change `range(16)` to `range(32)`?

Yeah, that's the right fix. @hiboyang would you like to raise a PR for this?

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-02-10T06:24:06Z

> > Maybe we should make the rayjob in this test running longer after scaling down, so there will be longer time with 1 pod after scaling down? e.g. for this line
> > [kueue/test/e2e/singlecluster/kuberay_test.go](https://github.com/kubernetes-sigs/kueue/blob/9a1de0101409e94adf3bc6ccc4e02831f587f987/test/e2e/singlecluster/kuberay_test.go#L187)
> > Line 187 in [9a1de01](/kubernetes-sigs/kueue/commit/9a1de0101409e94adf3bc6ccc4e02831f587f987)
> > print([ray.get(my_task.remote(i, 1)) for i in range(16)])`,  , change `range(16)`to`range(32)`?
> 
> Yeah, that's the right fix. [@hiboyang](https://github.com/hiboyang) would you like to raise a PR for this?

Yes, I put this test change into my this PR: https://github.com/kubernetes-sigs/kueue/pull/9077.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-10T21:55:14Z

#9077 has merged.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-10T21:55:19Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9058#issuecomment-3880946965):

>#9077 has merged.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
