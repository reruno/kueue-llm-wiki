# Issue #7482: Trainer v2: Remove temporary `runtimeInfo` wrapper

**Summary**: Trainer v2: Remove temporary `runtimeInfo` wrapper

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7482

**Last updated**: 2025-11-12T10:32:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-10-31T12:03:35Z
- **Updated**: 2025-11-12T10:32:59Z
- **Closed**: 2025-11-12T10:32:59Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I would like to remove the temporary `runtimeInfo` wrapper defined in https://github.com/kubernetes-sigs/kueue/blob/efda8192893ade0cda832c5e88e34f4585a63b9d/pkg/controller/jobs/trainjob/trainjob_controller.go#L189-L194 once we upgrade the Trainer dependency version to v2.1.

**Why is this needed**:

We introduced the function in https://github.com/kubernetes-sigs/kueue/pull/7132 so that we can bypass the thread-safe problems: https://github.com/kubeflow/trainer/issues/2873

However, we resolved the problem in https://github.com/kubeflow/trainer/pull/2877, then it will be shipped as part of the next Trainer v2.1

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-31T12:04:16Z

cc @mszadkow @mimowo @kaisoz

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T12:12:11Z

Awesome!

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-10T13:23:09Z

/assign
