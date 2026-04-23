# Issue #2902: Flaky Job controller interacting with scheduler Should schedule updated job and update the workload

**Summary**: Flaky Job controller interacting with scheduler Should schedule updated job and update the workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2902

**Last updated**: 2024-09-02T15:09:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-08-26T12:18:12Z
- **Updated**: 2024-09-02T15:09:16Z
- **Closed**: 2024-09-02T15:09:16Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

```
{Expected success, but got an error:
    <*errors.StatusError | 0xc00142b220>: 
    Operation cannot be fulfilled on jobs.batch "test-job": the object has been modified; please apply your changes to the latest version and try again
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "Operation cannot be fulfilled on jobs.batch \"test-job\": the object has been modified; please apply your changes to the latest version and try again",
            Reason: "Conflict",
            Details: {Name: "test-job", Group: "batch", Kind: "jobs", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc00142b220>: 
    Operation cannot be fulfilled on jobs.batch "test-job": the object has been modified; please apply your changes to the latest version and try again
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "Operation cannot be fulfilled on jobs.batch \"test-job\": the object has been modified; please apply your changes to the latest version and try again",
            Reason: "Conflict",
            Details: {Name: "test-job", Group: "batch", Kind: "jobs", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 409,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/job/job_controller_test.go:1744 @ 08/26/24 09:49:03.539
}
```

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/directory/pull-kueue-test-integration-main/1828004883333124096

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-26T12:44:30Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-26T14:16:09Z

/assign @mszadkow
