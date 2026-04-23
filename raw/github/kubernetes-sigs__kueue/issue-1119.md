# Issue #1119: Commonize KubeflowJob Tests

**Summary**: Commonize KubeflowJob Tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1119

**Last updated**: 2023-11-16T13:27:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-09-14T08:27:08Z
- **Updated**: 2023-11-16T13:27:30Z
- **Closed**: 2023-11-16T13:27:30Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
We should commonize integration tests for KubeflowJobs and move test cases depending on kubeflow frameworks (TFJob, PyTorchJob...) to unit tests.

Follow-up: https://github.com/kubernetes-sigs/kueue/pull/1114#discussion_r1324240711

**Why is this needed**:
The KubeflowJobs's reconciler is commonized in https://github.com/kubernetes-sigs/kueue/blob/e5692d83fd841a57e9b41c50b48ba6776c7c134e/pkg/controller/jobs/kubeflow/kubeflowjob/kubeflowjob_controller.go, and some integration test cases are overkill.

## Discussion

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-10-03T13:09:04Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-27T13:55:44Z

/unassign @yaroslava-serdiuk
/assign @stuton 
Anton, could you follow up with the rest of the Kubeflow integration tests, in a similar manner to #1191 ?

### Comment by [@stuton](https://github.com/stuton) — 2023-10-27T14:12:43Z

For sure, I will have a look
