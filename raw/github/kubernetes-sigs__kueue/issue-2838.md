# Issue #2838: [Flaky] when Creating a multikueue admission check Should run a kubeflow XGBoostJob

**Summary**: [Flaky] when Creating a multikueue admission check Should run a kubeflow XGBoostJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2838

**Last updated**: 2024-11-05T12:31:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-08-15T13:04:57Z
- **Updated**: 2024-11-05T12:31:04Z
- **Closed**: 2024-11-05T12:31:02Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 9

## Description

**What happened**:

```
End To End MultiKueue Suite: kindest/node:v1.30.0: [It] MultiKueue when Creating a multikueue admission check Should run a kubeflow XGBoostJob on worker if admitted expand_less	9s
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:688 with:
Expected object to be comparable, diff:   &v1.ReplicaStatus{
- 	Active:        1,
+ 	Active:        0,
- 	Succeeded:     0,
+ 	Succeeded:     1,
  	Failed:        0,
  	LabelSelector: nil,
  	Selector:      "",
  }
 failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:688 with:
Expected object to be comparable, diff:   &v1.ReplicaStatus{
- 	Active:        1,
+ 	Active:        0,
- 	Succeeded:     0,
+ 	Succeeded:     1,
  	Failed:        0,
  	LabelSelector: nil,
  	Selector:      "",
  }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/e2e_test.go:703 @ 08/15/24 06:05:55.326
}
```

**What you expected to happen**:

Test to pass

**How to reproduce it (as minimally and precisely as possible)**:

- https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-multikueue-e2e-main/1823962283705896960
- https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-multikueue-e2e-main/1821968118130413568

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-15T13:05:21Z

/assign @mszadkow

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-15T13:09:05Z

/kind flake

The XGBoostJob has some state transition bugs. So, maybe we need to remove the test case from Kueue or fix the root bug in the training-operator.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-15T13:25:54Z

I see, thanks for the context.

@mszadkow any chance you can take a look in the training-operator code?
In the meantime, let's disable this test by calling `ginkgo.Skip()` with an accompanying comment.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-08-16T11:30:09Z

@tenzen-y Can you explain more about the transition bug, is it known one?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-08-16T12:07:13Z

Yes, sure I can have a look there but like you said will skip it for now.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-16T14:24:17Z

> @tenzen-y Can you explain more about the transition bug, is it known one?

Depending on historical reasons, we just used to rerun the failed flaky tests in the TrainingOperator. 
So, we do not have a dedicated issue for specific transitions.

But, we explained the transition issue a little bit here: https://github.com/kubeflow/training-operator/issues/1711

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-11-05T12:12:48Z

The test for XGBoost was removed completely, only PyTorch test case is left as mostly used option.
Should we consider this ticket closed?
@tenzen-y @alculquicondor @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T12:30:58Z

Since the test is removed I suggest closing it as obsolete.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-05T12:31:03Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2838#issuecomment-2457047195):

>Since the test is removed I suggest closing it as obsolete.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
