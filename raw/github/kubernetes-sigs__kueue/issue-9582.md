# Issue #9582: Cluster deletion for kueue populator fails occasionally

**Summary**: Cluster deletion for kueue populator fails occasionally

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9582

**Last updated**: 2026-04-17T16:54:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-27T15:13:37Z
- **Updated**: 2026-04-17T16:54:17Z
- **Closed**: 2026-04-17T16:54:16Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 7

## Description


**Which test is flaking?**:

ERROR: failed to delete cluster "kueue-populator-e2e": failed to delete nodes: command "docker rm -f -v kueue-populator-e2e-control-plane" failed with error: exit status 1


**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9580/pull-kueue-populator-test-e2e-main/2027397028140552192
**Failure message or logs**:
```
Deleting cluster "kueue-populator-e2e" ...
ERROR: failed to delete cluster "kueue-populator-e2e": failed to delete nodes: command "docker rm -f -v kueue-populator-e2e-control-plane" failed with error: exit status 1
Command Output: Error response from daemon: cannot remove container "kueue-populator-e2e-control-plane": could not kill container: tried to kill container, but did not receive an exit event
make[1]: *** [Makefile:116: test-e2e] Error 1
make[1]: Leaving directory '/home/prow/go/src/sigs.k8s.io/kueue/cmd/experimental/kueue-populator'
make: *** [Makefile-kueue-populator.mk:27: kueue-populator-test-e2e] Error 2
```

**Anything else we need to know?**:
Kueue populator does no support cluster deletion with retry in https://github.com/kubernetes-sigs/kueue/blob/main/cmd/experimental/kueue-populator/run-e2e.sh

We should reuse the cluster deletion retry mechanism, see related PR: https://github.com/kubernetes-sigs/kueue/pull/9577/changes

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T15:15:25Z

cc @Sebastianhayashi would you like to follow up here too? 

cc @j-skiba

### Comment by [@Sebastianhayashi](https://github.com/Sebastianhayashi) — 2026-02-27T15:24:11Z

Thanks for the cc — I can follow up on this.

My current idea is to update [run-e2e.sh](app://-/index.html?hostId=local#) to use the same cluster-deletion retry behavior as [e2e-common.sh](app://-/index.html?hostId=local#):

- retry kind delete cluster with backoff (up to 5 attempts),
- treat unknown cluster as success,
- fail only after max retries.

### Comment by [@Sebastianhayashi](https://github.com/Sebastianhayashi) — 2026-02-27T15:25:51Z

> cc [@Sebastianhayashi](https://github.com/Sebastianhayashi) would you like to follow up here too?
> 
> cc [@j-skiba](https://github.com/j-skiba)

This should address the Docker exit-event race seen in the failing log.

Does this scope look good, or would you prefer we factor this through a shared helper instead of implementing it locally in [run-e2e.sh](app://-/index.html?hostId=local#)?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T15:37:43Z

we ceratinly need to commonize the code

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-17T09:32:57Z

Another occurrence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/10556/pull-kueue-populator-test-e2e-release-0-17/2045069220688957440

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-17T16:54:10Z

/close
This is likely fixed by https://github.com/kubernetes-sigs/kueue/pull/9597

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-17T16:54:17Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9582#issuecomment-4269814884):

>/close
>This is likely fixed by https://github.com/kubernetes-sigs/kueue/pull/9597


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
