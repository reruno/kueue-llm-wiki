# Issue #6525: [Flaky e2e] MultiKueue when Incremental mode Should run a job on worker if admitted

**Summary**: [Flaky e2e] MultiKueue when Incremental mode Should run a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6525

**Last updated**: 2025-08-12T07:12:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-11T12:40:37Z
- **Updated**: 2025-08-12T07:12:57Z
- **Closed**: 2025-08-12T07:12:56Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

/kind flake

**What happened**:

faiilure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6436/pull-kueue-test-e2e-multikueue-main/1954872287161225216

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:904 with:
Expected object to be comparable, diff:   &v1beta1.AdmissionCheckState{
  	Name:  "ac1",
- 	State: "Pending",
+ 	State: "Ready",
  	... // 1 ignored field
- 	Message:       "",
+ 	Message:       `The workload got reservation on "worker2"`,
  	PodSetUpdates: nil,
  }
 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:904 with:
Expected object to be comparable, diff:   &v1beta1.AdmissionCheckState{
  	Name:  "ac1",
- 	State: "Pending",
+ 	State: "Ready",
  	... // 1 ignored field
- 	Message:       "",
+ 	Message:       `The workload got reservation on "worker2"`,
  	PodSetUpdates: nil,
  }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:910 @ 08/11/25 12:01:48.477
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T16:37:41Z

cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T16:41:04Z

This failed on 10s timeout, which often isn't enough for e2e tests when the machines are under load.

So, I would probably suggest to just bump timeout to LongTimeout and see if this repeats.

Unless there are other / better ideas.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T17:16:09Z

iiuc this is done here https://github.com/kubernetes-sigs/kueue/pull/6546

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-12T07:12:51Z

/close 
Let's reopen if this re-occurs despite the extended timeout.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-12T07:12:57Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6525#issuecomment-3177998412):

>/close 
>Let's reopen if this re-occurs despite the extended timeout.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
