# Issue #7385: [Flaky E2E] MultiKueue when Creating a multikueue admission check Should run a kubeflow PyTorchJob on worker if admitted

**Summary**: [Flaky E2E] MultiKueue when Creating a multikueue admission check Should run a kubeflow PyTorchJob on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7385

**Last updated**: 2025-10-24T13:43:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-10-24T13:11:40Z
- **Updated**: 2025-10-24T13:43:37Z
- **Closed**: 2025-10-24T13:43:37Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

End To End MultiKueue Suite: kindest/node:v1.34.0: [It] MultiKueue when Creating a multikueue admission check Should run a kubeflow PyTorchJob on worker if admitted 

```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:1057 with:
Expected object to be comparable, diff:   &v1beta1.AdmissionCheckState{
  	... // 1 ignored and 2 identical fields
  	Message: strings.Join({
  		`The workload got reservation on "worker`,
- 		"1",
+ 		"2",
  		`"`,
  	}, ""),
  	PodSetUpdates: nil,
  }
 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:1057 with:
Expected object to be comparable, diff:   &v1beta1.AdmissionCheckState{
  	... // 1 ignored and 2 identical fields
  	Message: strings.Join({
  		`The workload got reservation on "worker`,
- 		"1",
+ 		"2",
  		`"`,
  	}, ""),
  	PodSetUpdates: nil,
  }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:690 @ 10/24/25 12:28:57.124
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7289/pull-kueue-test-e2e-multikueue-main/1981696318107553792

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-24T13:17:23Z

/assign
