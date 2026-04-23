# Issue #3695: Fleky Test: TopologyAwareScheduling for Pod group when Creating a Pod group

**Summary**: Fleky Test: TopologyAwareScheduling for Pod group when Creating a Pod group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3695

**Last updated**: 2024-12-04T14:45:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-12-02T06:55:38Z
- **Updated**: 2024-12-04T14:45:02Z
- **Closed**: 2024-12-04T14:45:02Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Periodic Tests failed on "End To End TAS Suite: kindest/node:v1.31.1: [It] TopologyAwareScheduling for Pod group when Creating a Pod group Should place pods based on the ranks-ordering".

```shell
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:91 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:91 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [AfterEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/pod_group_test.go:85 @ 12/01/24 16:48:43.849
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-tas-e2e-main/1863261324973182976

**Anything else we need to know?**:

<img width="1212" alt="Screenshot 2024-12-02 at 15 55 06" src="https://github.com/user-attachments/assets/74a928d3-4fa1-40b5-8136-5e7393c69278">

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-02T06:55:46Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-02T07:20:27Z

/cc @mbobrovskyi @PBundyra

### Comment by [@mykysha](https://github.com/mykysha) — 2024-12-02T09:00:34Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-03T10:56:49Z

/reopen

Still have flakes https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3714/pull-kueue-test-tas-e2e-main/1863895692108369920.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-03T10:56:54Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3695#issuecomment-2514216418):

>/reopen
>
>Still have flakes https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3714/pull-kueue-test-tas-e2e-main/1863895692108369920.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T08:37:41Z

I'm not sure this is the issue, but seeing "tas-flavor" exists makes me wonder the deletion from previous test failed. 

So, I'm thinking that we should use `ExpectObjectToBeDeleted` for all objects deleted, so that we can pin point which object wasn't deleted after all, because just `DeleteObject` sends delete request, but the object may stay as it is processed async, for example due to finalizers. wdyt @mbobrovskyi ?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-04T08:49:41Z

Yeah, agree. This also needs to be fixed in the other tas tests.
