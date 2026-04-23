# Issue #4462: Flaky E2E Test: Should suspend the pods of a deployment created in the test namespace

**Summary**: Flaky E2E Test: Should suspend the pods of a deployment created in the test namespace

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4462

**Last updated**: 2025-03-04T10:25:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-03-03T11:15:07Z
- **Updated**: 2025-03-04T10:25:45Z
- **Closed**: 2025-03-04T10:25:45Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
End To End Custom Configs handling Suite: kindest/node:v1.31.1: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should suspend the pods of a deployment created in the test namespace 

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:312 with:
Expected object to be comparable, diff:   map[string]string{
- 	"app":                    "test-deploy-pod",
  	"kueue.x-k8s.io/managed": "true",
- 	"pod-template-hash":      "776f58548",
  }
 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:312 with:
Expected object to be comparable, diff:   map[string]string{
- 	"app":                    "test-deploy-pod",
  	"kueue.x-k8s.io/managed": "true",
- 	"pod-template-hash":      "776f58548",
  }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/skipjobswithoutqueuename_test.go:315 @ 03/03/25 10:47:10.881
}
```

**What you expected to happen**:
No error

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4457/pull-kueue-test-e2e-customconfigs-main/1896509651114004480

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-03T11:15:16Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-03T11:15:29Z

cc: @kaisoz

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-03-03T11:20:38Z

/assign

I'll have a look! Thanks for reporting!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-03T15:16:16Z

another occurance; https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4464/pull-kueue-test-e2e-customconfigs-main/1896574710532018176
