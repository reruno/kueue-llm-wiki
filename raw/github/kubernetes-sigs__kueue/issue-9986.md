# Issue #9986: Deleted/restarted pod for autoscaling RayJob stuck in scheduling gated status

**Summary**: Deleted/restarted pod for autoscaling RayJob stuck in scheduling gated status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9986

**Last updated**: 2026-04-10T11:32:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@hiboyang](https://github.com/hiboyang)
- **Created**: 2026-03-18T16:37:45Z
- **Updated**: 2026-04-10T11:32:53Z
- **Closed**: 2026-04-10T11:32:52Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

During a RayJob with [autoscaling enabled](https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/configuring-autoscaling.html) running time, if kill a worker pod, a new pod will be started but stuck in scheduling gate status. The new pod does not change to running state.

**What you expected to happen**:

After the new pod starts, Kueue should ungate it and switch it to running state.

**How to reproduce it (as minimally and precisely as possible)**:

1. Start a RayJob with autoscaling
2. Trigger autoscaling (e.g. scaling-up)
3. Delete a worker pod using kubectl delete
4. Watch the new worker pod created with scheduling gated
5. Keep watching the new worker pod, will see it stuck in scheduling gated, not change to running

**Anything else we need to know?**:

RayService seems have similar issue

**Environment**:
- Kubernetes version (use `kubectl version`): any
- Kueue version (use `git describe --tags --dirty --always`): 0.15, probably also in 0.16 and latest
- Cloud provider or hardware configuration: any
- OS (e.g: `cat /etc/os-release`): any
- Kernel (e.g. `uname -a`): any
- Install tools: KubeRay
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-18T16:48:24Z

Looks like the same root cause as https://github.com/kubernetes-sigs/kueue/issues/9879, I think the proper fix is to refactor the ungating mechanism

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-10T11:32:46Z

I think this should be already addressed by https://github.com/kubernetes-sigs/kueue/issues/10258
/close
let's re-open if not

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-10T11:32:53Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9986#issuecomment-4223456618):

>I think this should be already addressed by https://github.com/kubernetes-sigs/kueue/issues/10258
>/close
>let's re-open if not


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
