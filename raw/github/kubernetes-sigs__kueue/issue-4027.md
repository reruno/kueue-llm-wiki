# Issue #4027: Integration tests fail after upgrade to 1.32

**Summary**: Integration tests fail after upgrade to 1.32

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4027

**Last updated**: 2025-01-22T12:00:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-21T08:14:25Z
- **Updated**: 2025-01-22T12:00:38Z
- **Closed**: 2025-01-22T12:00:38Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:

The integration tests fail due to new validation.

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main

**What you expected to happen**:

The integration tests should pass.

**How to reproduce it (as minimally and precisely as possible)**:

Every periodic build will fail. Also, run locally the integration tests with;

INTEGRATION_NPROCS=4 INTEGRATION_TARGET=./test/integration/controller/jobs/job make test-integration

**Anything else we need to know?**:

The tests are marked as "slow" so didn't fail the attempt to merge.
When marking Job as complete we need to also set the StartTime, Completion time and the SuccessCriteriaMet condition. Some tests already do it.

```
{Expected success, but got an error:
    <*errors.StatusError | 0xc0009443c0>: 
    Job.batch "test-job" is invalid: [status.completionTime: Required value: completionTime is required for Complete jobs, status.conditions: Invalid value: cannot set Complete=True condition without the SuccessCriteriaMet=true condition, status.startTime: Required value: startTime is required for finished job]
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
            Message: "Job.batch \"test-job\" is invalid: [status.completionTime: Required value: completionTime is required for Complete jobs, status.conditions: Invalid value: cannot set Complete=True condition without the SuccessCriteriaMet=true condition, status.startTime: Required value: startTime is required for finished job]",
            Reason: "Invalid",
            Details: {
                Name: "test-job",
                Group: "batch",
                Kind: "Job",
                UID: "",
                Causes: [
                    {
                        Type: "FieldValueRequired",
                        Message: "Required value: completionTime is required for Complete jobs",
                        Field: "status.completionTime",
                    },
                    {
                        Type: "FieldValueInvalid",
                        Message: "Invalid value: cannot set Complete=True condition without the SuccessCriteriaMet=true condition",
                        Field: "status.conditions",
                    },
                    {
                        Type: "FieldValueRequired",
                        Message: "Required value: startTime is required for finished job",
                        Field: "status.startTime",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 422,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0009443c0>: 
    Job.batch "test-job" is invalid: [status.completionTime: Required value: completionTime is required for Complete jobs, status.conditions: Invalid value: cannot set Complete=True condition without the SuccessCriteriaMet=true condition, status.startTime: Required value: startTime is required for finished job]
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
            Message: "Job.batch \"test-job\" is invalid: [status.completionTime: Required value: completionTime is required for Complete jobs, status.conditions: Invalid value: cannot set Complete=True condition without the SuccessCriteriaMet=true condition, status.startTime: Required value: startTime is required for finished job]",
            Reason: "Invalid",
            Details: {
                Name: "test-job",
                Group: "batch",
                Kind: "Job",
                UID: "",
                Causes: [
                    {
                        Type: "FieldValueRequired",
                        Message: "Required value: completionTime is required for Complete jobs",
                        Field: "status.completionTime",
                    },
                    {
                        Type: "FieldValueInvalid",
                        Message: "Invalid value: cannot set Complete=True condition without the SuccessCriteriaMet=true condition",
                        Field: "status.conditions",
                    },
                    {
                        Type: "FieldValueRequired",
                        Message: "Required value: startTime is required for finished job",
                        Field: "status.startTime",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 422,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/jobs/job/job_controller_test.go:275 @ 01/21/25 06:18:52.853

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-21T08:15:48Z

cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-21T08:55:38Z

/assign
