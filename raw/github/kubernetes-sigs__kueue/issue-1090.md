# Issue #1090: [Flaky] Creating a Job In a Twostepadmission Queue [It] Should unsuspend a job only after all checks are cleared

**Summary**: [Flaky] Creating a Job In a Twostepadmission Queue [It] Should unsuspend a job only after all checks are cleared

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1090

**Last updated**: 2023-09-26T14:41:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-30T19:17:33Z
- **Updated**: 2023-09-26T14:41:25Z
- **Closed**: 2023-09-26T14:41:25Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 11

## Description

**What happened**:

```
Kueue when Creating a Job In a Twostepadmission Queue [It] Should unsuspend a job only after all checks are cleared
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/e2e_test.go:215
  [FAILED] Timed out after 30.001s.
  Expected
      <[]interface {} | len:2, cap:2>: [
          <bool>true,
          <map[string]string | len:0>nil,
      ]
  to equal
      <[]interface {} | len:2, cap:2>: [
          <bool>false,
          <map[string]string | len:1>{
              "instance-type": "on-demand",
          },
      ]
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/e2e_test.go:270 @ 08/30/23 19:13:45.757
```

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1031/pull-kueue-test-e2e-main-1-24/1696962388068143104

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-04T17:12:23Z

Same here: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1094/pull-kueue-test-e2e-main-1-24/1698634053189636096

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-04T17:15:30Z

Same: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1096/pull-kueue-test-e2e-main-1-24/1698634117425401856

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-05T13:12:17Z

@achernevskii could you take a look?

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-09-06T18:45:31Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-13T15:45:08Z

/unassign @achernevskii 
/assign @trasc 

This is flakying a lot, can you PTAL Traian?

### Comment by [@trasc](https://github.com/trasc) — 2023-09-13T16:50:10Z

Sure

### Comment by [@trasc](https://github.com/trasc) — 2023-09-18T05:42:10Z

#1127 should fix this particular case , however the main problem looks to be the fact the the eviction is not longer working as expected.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-18T12:29:52Z

Can you elaborate?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-26T10:05:50Z

> however the main problem looks to be the fact the the eviction is not longer working as expected.

@trasc Could you clarify the non-expected behavior in the eviction?

### Comment by [@trasc](https://github.com/trasc) — 2023-09-26T10:41:25Z

Even with the "false" admission, the flow wold have been , 

1. Admit(before first reconcile)
2. Evict (during the first reconcile when the ACs are added)
3. Readmit

However, at least in the configured timeout, the eviction is not ending and the readmission will not take place.   

If remember correctly, "Kueue when Creating a Job With Queueing Should readmit preempted job with workloadPriorityClass into a separate flavor" was flaky as well , but since we no longer test 1.24 and we no longer have access to the tests grid I'n not sure.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-26T14:19:18Z

> Even with the "false" admission, the flow wold have been ,
> 
> 1. Admit(before first reconcile)
> 2. Evict (during the first reconcile when the ACs are added)
> 3. Readmit
> 
> However, at least in the configured timeout, the eviction is not ending and the readmission will not take place.
> 
> If remember correctly, "Kueue when Creating a Job With Queueing Should readmit preempted job with workloadPriorityClass into a separate flavor" was flaky as well , but since we no longer test 1.24 and we no longer have access to the tests grid I'n not sure.

I see. Thanks for clarifying.
