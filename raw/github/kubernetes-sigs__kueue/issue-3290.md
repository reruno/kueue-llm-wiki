# Issue #3290: Jobs flake on fetching dependencies during building image

**Summary**: Jobs flake on fetching dependencies during building image

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3290

**Last updated**: 2025-03-23T08:38:15Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-23T07:20:14Z
- **Updated**: 2025-03-23T08:38:15Z
- **Closed**: 2025-03-23T08:38:13Z
- **Labels**: `kind/bug`, `kind/flake`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

**What happened**:

Both periodic-kueue-test-multikueue-e2e-main and pull-kueue-test-multikueue-e2e-main flake, most often.

Example from pull-kueue-test-multikueue-e2e-main: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3256/pull-kueue-test-multikueue-e2e-main/1848686153683701760
Examples from periodic-kueue-test-multikueue-e2e-main: 
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-multikueue-e2e-main/1846795226719457280
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3256/pull-kueue-test-multikueue-e2e-main/1848686153683701760
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3284/pull-kueue-test-multikueue-e2e-main/1848739383822258176

However, analogous flake was also observed for `pull-kueue-test-unit-main` .

**What you expected to happen**:

No flakes

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

Example log:
```
go: sigs.k8s.io/kind@v0.24.0: Get "https://proxy.golang.org/sigs.k8s.io/kind/@v/v0.24.0.info": net/http: TLS handshake timeout
go: sigs.k8s.io/kind@: version must not be empty
```
or 
```
go: sigs.k8s.io/kustomize/kustomize/v5@v5.5.0: sigs.k8s.io/kustomize/kustomize/v5@v5.5.0: verifying module: sigs.k8s.io/kustomize/kustomize/v5@v5.5.0: Get "https://sum.golang.org/lookup/sigs.k8s.io/kustomize/kustomize/v5@v5.5.0": net/http: TLS handshake timeout
make: *** [Makefile-deps.mk:55: kustomize] Error 1
```
Example from `pull-kueue-test-unit-main `:
```
go: downloading gotest.tools/gotestsum v1.12.0
go: gotest.tools/gotestsum@v1.1[2](https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3292/pull-kueue-test-unit-main/1849084700195295232#1:build-log.txt%3A2).0: gotest.tools/gotestsum@v1.12.0: verifying module: gotest.tools/gotestsum@v1.12.0: Get "https://sum.golang.org/lookup/gotest.tools/gotestsum@v1.12.0": dial tcp 142.250.190.49:44[3](https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3292/pull-kueue-test-unit-main/1849084700195295232#1:build-log.txt%3A3): i/o timeout
make: *** [Makefile-deps.mk:70: gotestsum] Error 1
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-23T07:21:56Z

/kind flake
/cc @trasc @mbobrovskyi @alculquicondor 
I know this is not in test code but it looks like infra, still opened the issue as it seemingly only happens for e2e multikueue jobs. Maybe the job is bigger and resource constrained? In that case we could bump the resources in test-infra. Or maybe it is just bad "luck" - I don't know. Opening to hear some ideas.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-23T13:49:03Z

Actually, I spotted the similar failure today for unit tests: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3292/pull-kueue-test-unit-main/1849084700195295232
```
go: downloading gotest.tools/gotestsum v1.12.0
go: gotest.tools/gotestsum@v1.1[2](https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3292/pull-kueue-test-unit-main/1849084700195295232#1:build-log.txt%3A2).0: gotest.tools/gotestsum@v1.12.0: verifying module: gotest.tools/gotestsum@v1.12.0: Get "https://sum.golang.org/lookup/gotest.tools/gotestsum@v1.12.0": dial tcp 142.250.190.49:44[3](https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3292/pull-kueue-test-unit-main/1849084700195295232#1:build-log.txt%3A3): i/o timeout
make: *** [Makefile-deps.mk:70: gotestsum] Error 1
```
so, probably it affects all jobs :( not sure if there is anything we could do about it. cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-23T22:36:59Z

> /kind flake /cc @trasc @mbobrovskyi @alculquicondor I know this is not in test code but it looks like infra, still opened the issue as it seemingly only happens for e2e multikueue jobs. Maybe the job is bigger and resource constrained? In that case we could bump the resources in test-infra. Or maybe it is just bad "luck" - I don't know. Opening to hear some ideas.

It seems that resource usage for the multikueue e2e Jobs sometimes overload: https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-multikueue-e2e-main&var-build=All&refresh=30s

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-24T06:56:51Z

I've updated the title to reflect this is not just multikueue, even though it seems the most common there.

EDIT: also started a thread on k8s-infra: https://kubernetes.slack.com/archives/CCK68P2Q2/p1729753129367449

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-24T07:26:59Z

> I've updated the title to reflect this is not just multikueue, even though it seems the most common there.

Thanks.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-22T07:27:12Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-21T08:07:12Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-23T08:38:09Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-23T08:38:13Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3290#issuecomment-2746092326):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
