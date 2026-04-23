# Issue #3664: [Multikueue] Fail e2e-test due to expected empty strings on Creating a multikueue admission check Should run a job on worker if admitted

**Summary**: [Multikueue] Fail e2e-test due to expected empty strings on Creating a multikueue admission check Should run a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3664

**Last updated**: 2024-11-27T13:30:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2024-11-27T09:32:04Z
- **Updated**: 2024-11-27T13:30:06Z
- **Closed**: 2024-11-27T09:48:57Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

In addition to #3600, it was found this issue while running `Creating a multikueue admission check Should run a job on worker if admitted` test. This error is returned **every time** the tests is ran:

```
MultiKueue when Creating a multikueue admission check [It] Should run a job on worker if admitted
/Users/Irving_Mondragon/Documents/git/kueue/test/e2e/multikueue/e2e_test.go:190

  [FAILED] Expected
      <[]v1.JobCondition | len:3, cap:4>: [
          {
              Type: "Suspended",
              Status: "False",
              LastProbeTime: {
                  Time: 2024-11-27T10:12:44+01:00,
              },
              LastTransitionTime: {
                  Time: 2024-11-27T10:12:44+01:00,
              },
              Reason: "JobResumed",
              Message: "Job resumed",
          },
          {
              Type: "SuccessCriteriaMet",
              Status: "True",
              LastProbeTime: {
                  Time: 2024-11-27T10:12:53+01:00,
              },
              LastTransitionTime: {
                  Time: 2024-11-27T10:12:53+01:00,
              },
              Reason: "CompletionsReached",
              Message: "Reached expected number of succeeded pods",
          },
          {
              Type: "Complete",
              Status: "True",
              LastProbeTime: {
                  Time: 2024-11-27T10:12:53+01:00,
              },
              LastTransitionTime: {
                  Time: 2024-11-27T10:12:53+01:00,
              },
              Reason: "CompletionsReached",
              Message: "Reached expected number of succeeded pods",
          },
      ]
  to contain element matching
      <*matchers.BeComparableToMatcher | 0x14000a920f0>: {
          Expected: <v1.JobCondition>{
              Type: "Complete",
              Status: "True",
              LastProbeTime: {
                  Time: 0001-01-01T00:00:00Z,
              },
              LastTransitionTime: {
                  Time: 0001-01-01T00:00:00Z,
              },
              Reason: "",
              Message: "",
          },
          Options: [
              <*cmp.pathFilter | 0x14000a90048>{
                  core: {},
                  fnc: 0x1009c58c0,
                  opt: <cmp.ignore>{core: {}},
              },
          ],
      }
  In [It] at: /Users/Irving_Mondragon/Documents/git/kueue/test/e2e/multikueue/e2e_test.go:267 @ 11/27/24 10:12:53.521
```

**What you expected to happen**:
Not to happen

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): macOS
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T09:36:56Z

You say the test fails every time, but the board is green recently: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-multikueue-e2e-main. Ah, I see, the `SuccessCriteriaMet` condition is added by k8s 1.31+, while we run the periodic tests on 1.30. I think we could update the test to only check the presence of the `Complete` condition.

EDIT: ah we already use ContainElement to check only the Complete condition, the issue is that the "Reason" is changed between the versions.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-27T09:40:55Z

cc @tenzen-y as the reason is changed after the SuccessPolicy graduated to Beta in 1.31. I think it is safe to ignore the reason from asserts as the purpose of the test is to check MultiKueue integration (the job completes) rather than k8s reason.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-11-27T09:43:16Z

> You say the test fails every time, but the board is green recently: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-multikueue-e2e-main. Ah, I see, the `SuccessCriteriaMet` condition is added by k8s 1.31+, while we run the periodic tests on 1.30. I think we could update the test to only check the presence of the `Complete` condition.
> 
> EDIT: ah we already use ContainElement to check only the Complete condition, the issue is that the "Reason" is changed between the versions.

Yes, I'm also planning to open a PR in kubernetes/test-infra to use 1.31 on tests.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-27T13:29:56Z

> cc @tenzen-y as the reason is changed after the SuccessPolicy graduated to Beta in 1.31. I think it is safe to ignore the reason from asserts as the purpose of the test is to check MultiKueue integration (the job completes) rather than k8s reason.

+1 on this. Here the Complete reason is not what we really want to verify in the testings.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-27T13:30:03Z

/kind flake
