# Issue #4853: Flaky E2E test: MultiKueue when Creating a multikueue admission check Should run a RayCluster on worker if admitted

**Summary**: Flaky E2E test: MultiKueue when Creating a multikueue admission check Should run a RayCluster on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4853

**Last updated**: 2025-05-07T13:15:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-04-01T07:32:39Z
- **Updated**: 2025-05-07T13:15:21Z
- **Closed**: 2025-05-07T13:15:21Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
End To End MultiKueue Suite: kindest/node:v1.32.3: [It] MultiKueue when Creating a multikueue admission check Should run a RayCluster on worker if admitted

```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:828 with:
Expected
    <int32>: 0
to equal
    <int32>: 1 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:828 with:
Expected
    <int32>: 0
to equal
    <int32>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:830 @ 04/01/25 07:23:48.388
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4846/pull-kueue-test-e2e-multikueue-main/1906965243951583232

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-01T07:32:51Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-01T07:33:35Z

cc: @mszadkow

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2025-04-01T17:11:33Z

The `Readiness` probe succeeds [here](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4846/pull-kueue-test-e2e-multikueue-main/1906965243951583232/artifacts/run-test-multikueue-e2e-1.32.3/kind-worker1-control-plane/kubelet.log#:~:text=Apr%2001%2007%3A23%3A47%20kind%2Dworker1%2Dcontrol%2Dplane%20kubelet%5B775%5D%3A%20I0401%2007%3A23%3A47.744698%20%20%20%20%20775%20prober.go%3A116%5D%20%22Probe%20succeeded%22%20probeType%3D%22Readiness%22%20pod%3D%22multikueue%2D2db8t/raycluster1%2Dworkers%2Dgroup%2D0%2Dworker%2Dt94gd%22%20podUID%3D%221debb19f%2D6977%2D4287%2Da787%2Db9f3f2cf7ef2%22%20containerName%3D%22worker%2Dcontainer%22) in the Kubelet logs

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-04T09:13:44Z

Would waiting a bit longer help? Maybe we have a case for increasing the CPU to 12 actually. I think we set 10 before introducing Ray and AppWrapper operators, but it would be good to see it we are CPU constrained by the dashboard

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-16T17:53:34Z

It happens again https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5013/pull-kueue-test-e2e-multikueue-main/1912548758457946112.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-07T08:04:43Z

I found one more failed run here: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4917/pull-kueue-test-e2e-multikueue-main/1912169469686321152

I will investigate
/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-07T12:41:31Z

1. That was with the `rayproject/ray:2.9.0`. 
Now it's `ray-mini`, which allows to get up the ray cluster worker pods much faster. 
2. I would still increase timeout here from `LongTimeout` to `VeryLongTimeout` as only this one doesn't have extended timeout like other test.
Which makes perfect sense as the full ray image is still be used in `periodic` tests.
