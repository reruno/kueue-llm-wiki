# Issue #9457: Unexpected role tracker role in logs

**Summary**: Unexpected role tracker role in logs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9457

**Last updated**: 2026-02-24T15:27:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-02-24T15:01:15Z
- **Updated**: 2026-02-24T15:27:39Z
- **Closed**: 2026-02-24T15:20:31Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Even though the leader selection is enabled and the number of replicas are more than 1, the kueue-controller-manager logs "replica-role" indicates "leader", "follower", and "standalone.

**What you expected to happen**:
The "standalone" role is not recorded. All kueue-controller-manager logs have `"replica-role": "leader"` or `"replica-role": "follower"`.

**How to reproduce it (as minimally and precisely as possible)**:
In my cluster, I have 3 replicas of kueue-controller-manager and leader election is enabled by the following Kueue Configuration:

```yaml
apiVersion: v1
data:
  controller_manager_config.yaml: |
    apiVersion: config.kueue.x-k8s.io/v1beta2
    kind: Configuration
    ...
    leaderElection:
      leaderElect: true
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.34.2
- Kueue version (use `git describe --tags --dirty --always`): v0.16.1
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-24T15:02:35Z

@IrvingMg IIUC, the standalone replica is recorded only when the number of kueue-controller-manager is 1 or leader election is disabled. Is this intended role tracker behavior? Am I missing anything?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-24T15:05:22Z

Can you share @tenzen-y which controller records specifically as "standalone"? Maybe we just have a bug in the controller

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-24T15:08:16Z

Yeah, it sounds like a controller is missing the roleTracker. A similar issue was fixed here: https://github.com/kubernetes-sigs/kueue/pull/9433 for `NonTasUsageReconciler`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-24T15:14:35Z

> Can you share [@tenzen-y](https://github.com/tenzen-y) which controller records specifically as "standalone"? Maybe we just have a bug in the controller

As my analysis with level 8 log, the only `tas-non-tas-usage-controller` recorded `standalone` replica.

> Yeah, it sounds like a controller is missing the roleTracker. A similar issue was fixed here: https://github.com/kubernetes-sigs/kueue/pull/9433 for NonTasUsageReconciler.

Oh, what a time. I didn't find the PR. I believe that this issue is resolved by https://github.com/kubernetes-sigs/kueue/pull/9433.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-24T15:16:12Z

@IrvingMg Could you tie this issue to your PR `Fixes` section, then close this issue?

```
Which issue(s) this PR fixes:
Fixes #9457
```

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-24T15:20:24Z

> [@IrvingMg](https://github.com/IrvingMg) Could you tie this issue to your PR `Fixes` section, then close this issue?

Done :) 

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-24T15:20:32Z

@IrvingMg: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9457#issuecomment-3952879252):

>> [@IrvingMg](https://github.com/IrvingMg) Could you tie this issue to your PR `Fixes` section, then close this issue?
>
>Done :) 
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-24T15:27:14Z

> > [@IrvingMg](https://github.com/IrvingMg) Could you tie this issue to your PR `Fixes` section, then close this issue?
> 
> Done :)
> 
> /close

Awesome, thank you!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-24T15:27:37Z

/assign @IrvingMg
