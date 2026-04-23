# Issue #3028: Flaky Test: MultiKueue when Creating a multikueue admission check Should run a MPIJob on worker if admitted.

**Summary**: Flaky Test: MultiKueue when Creating a multikueue admission check Should run a MPIJob on worker if admitted.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3028

**Last updated**: 2024-09-12T08:21:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-09-12T02:46:23Z
- **Updated**: 2024-09-12T08:21:14Z
- **Closed**: 2024-09-12T08:21:14Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:
Flaky Test for: End To End MultiKueue Suite: kindest/node:v1.30.0: [It] MultiKueue when Creating a multikueue admission check Should run a MPIJob on worker if admitted.

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:475 with:
Expected object to be comparable, diff:   &v2beta1.ReplicaStatus{
  	Active:        0,
- 	Succeeded:     0,
+ 	Succeeded:     1,
  	Failed:        0,
  	LabelSelector: nil,
  	Selector:      "",
  }
 failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:475 with:
Expected object to be comparable, diff:   &v2beta1.ReplicaStatus{
  	Active:        0,
- 	Succeeded:     0,
+ 	Succeeded:     1,
  	Failed:        0,
  	LabelSelector: nil,
  	Selector:      "",
  }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:484 @ 09/12/24 02:38:06.695
}
```

**What you expected to happen**:
It never happened any errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3027/pull-kueue-test-multikueue-e2e-main/1834056129936625664

**Anything else we need to know?**:
This happens after https://github.com/kubernetes-sigs/kueue/pull/2880.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
