# Issue #9110: Provide example config map for RayJob autoscaling

**Summary**: Provide example config map for RayJob autoscaling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9110

**Last updated**: 2026-02-23T09:15:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-11T09:30:18Z
- **Updated**: 2026-02-23T09:15:49Z
- **Closed**: 2026-02-23T09:15:49Z
- **Labels**: `kind/documentation`
- **Assignees**: [@nerdeveloper](https://github.com/nerdeveloper)
- **Comments**: 1

## Description

<!-- Please use this template for documentation-related issues -->

**What would you like to be documented or improved**:

I would like to provide an example configMap. Maybe as the one use for e2e tests:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ray-job-autoscaling-code-sample
data:
  sample_code.py: |
    import ray
    import os

    ray.init()

    @ray.remote
    def my_task(x, s):
        import time
        time.sleep(s)
        return x * x

    # run tasks in sequence to avoid triggering autoscaling in the beginning
    print([ray.get(my_task.remote(i, 1)) for i in range(4)])

    # run tasks in parallel to trigger autoscaling (scaling up)
    print(ray.get([my_task.remote(i, 4) for i in range(16)]))

    # run tasks in sequence to trigger scaling down
    print([ray.get(my_task.remote(i, 1)) for i in range(32)])

```
https://kueue.sigs.k8s.io/docs/tasks/run/rayjobs/#example-rayjob-with-autoscaling
**Location** (URL, file path, or section if applicable):

## Discussion

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2026-02-16T03:36:14Z

/assign
