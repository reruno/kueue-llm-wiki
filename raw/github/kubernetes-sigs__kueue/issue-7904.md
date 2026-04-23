# Issue #7904: Unauthorized error when running renovate

**Summary**: Unauthorized error when running renovate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7904

**Last updated**: 2025-12-19T09:53:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-11-26T10:48:01Z
- **Updated**: 2025-12-19T09:53:23Z
- **Closed**: 2025-12-19T09:53:22Z
- **Labels**: `kind/bug`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 17

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When running the `update-versions-with-renovate` action, we’re getting an “unauthorized” error:

```
INFO: Repository started (repository=kubernetes-sigs/kueue)
       "renovateVersion": "42.22.0"
 WARN: Cannot access vulnerability alerts. Please ensure permissions have been granted. (repository=kubernetes-sigs/kueue)
       "url": "https://docs.renovatebot.com/configuration-options/#vulnerabilityalerts"
 INFO: Dependency extraction complete (repository=kubernetes-sigs/kueue, baseBranch=main)
       "stats": {
         "managers": {"npm": {"fileCount": 1, "depCount": 13}},
         "total": {"fileCount": 1, "depCount": 13}
       }
 INFO: Branch created (repository=kubernetes-sigs/kueue, branch=renovate/frontend-minor-and-patch)
       "commitSha": "52fbb7fc1847bfcc47cd6ad12bd1d8a2ddb8d4c2"
 WARN: Could not ensure issue (repository=kubernetes-sigs/kueue)
       "err": {
         "message": "integration-unauthorized",
         "stack": "Error: integration-unauthorized\n    at handleGotError (/usr/local/renovate/lib/util/http/github.ts:129:12)\n    at GithubHttp.handleError (/usr/local/renovate/lib/util/http/github.ts:344:11)\n    at GithubHttp.request (/usr/local/renovate/lib/util/http/http.ts:258:12)\n    at processTicksAndRejections (node:internal/process/task_queues:103:5)\n    at GithubHttp.requestJsonUnsafe (/usr/local/renovate/lib/util/http/github.ts:358:20)\n    at GithubHttp.requestJson (/usr/local/renovate/lib/util/http/http.ts:359:17)\n    at Proxy.ensureIssue (/usr/local/renovate/lib/modules/platform/github/index.ts:1452:36)\n    at ensureDependencyDashboard (/usr/local/renovate/lib/workers/repository/dependency-dashboard.ts:621:5)\n    at Object.renovateRepository (/usr/local/renovate/lib/workers/repository/index.ts:146:9)\n    at attributes.repository (/usr/local/renovate/lib/workers/global/index.ts:188:11)\n    at start (/usr/local/renovate/lib/workers/global/index.ts:173:7)\n    at /usr/local/renovate/lib/renovate.ts:19:22"
       }
 INFO: Repository finished (repository=kubernetes-sigs/kueue)
       "cloned": true,
       "durationMs": 52236,
       "result": "done",
       "status": "onboarded",
       "enabled": true,
       "onboarded": true
 INFO: Renovate was run at log level "info". Set LOG_LEVEL=debug in environment variables to see extended debug logs.
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
Trigger an action https://github.com/kubernetes-sigs/kueue/actions/workflows/update-versions-with-renovate.yaml.

**Anything else we need to know?**:

https://github.com/kubernetes-sigs/kueue/actions/runs/19700975198

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-26T10:48:17Z

/cc @mimowo @tenzen-y @vladikkuzn

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-26T10:49:52Z

Also I didn't got what does it mean `dry-run on PRs` (https://github.com/kubernetes-sigs/kueue/blob/f5e53f9afff62c75ddd08bcee731c020c2c2739b/.github/workflows/update-versions-with-renovate.yaml#L19C29-L19C43).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-26T11:00:04Z

>  WARN: Could not ensure issue (repository=kubernetes-sigs/kueue)
>        "err": {
>          "message": "integration-unauthorized",
>          "stack": "Error: integration-unauthorized\n    at handleGotError (/usr/local/renovate/lib/util/http/github.ts:129:12)\n    at GithubHttp.handleError (/usr/local/renovate/lib/util/http/github.ts:344:11)\n    at GithubHttp.request (/usr/local/renovate/lib/util/http/http.ts:258:12)\n    at processTicksAndRejections (node:internal/process/task_queues:103:5)\n    at GithubHttp.requestJsonUnsafe (/usr/local/renovate/lib/util/http/github.ts:358:20)\n    at GithubHttp.requestJson (/usr/local/renovate/lib/util/http/http.ts:359:17)\n    at Proxy.ensureIssue (/usr/local/renovate/lib/modules/platform/github/index.ts:1452:36)\n    at ensureDependencyDashboard (/usr/local/renovate/lib/workers/repository/dependency-dashboard.ts:621:5)\n    at Object.renovateRepository (/usr/local/renovate/lib/workers/repository/index.ts:146:9)\n    at attributes.repository (/usr/local/renovate/lib/workers/global/index.ts:188:11)\n    at start (/usr/local/renovate/lib/workers/global/index.ts:173:7)\n    at /usr/local/renovate/lib/renovate.ts:19:22"
>        }

What about adding `issues: write` permission to https://github.com/kubernetes-sigs/kueue/blob/f5e53f9afff62c75ddd08bcee731c020c2c2739b/.github/workflows/update-versions-with-renovate.yaml#L13-L15?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-26T11:27:01Z

Not sure I got why we should create issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-26T11:44:33Z

> Not sure I got why we should create issue.

IIUC, renovate creates issue to manage dependencies: https://github.com/cilium/cilium/issues/33550

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-11-26T18:56:00Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-11-27T00:45:04Z

/reopen
@mbobrovskyi @tenzen-y @mimowo can somebody from approvers pls run the action manually, so I can see if the fix actually works?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-27T00:45:10Z

@vladikkuzn: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7904#issuecomment-3583663781):

>/reopen
>@mbobrovskyi @tenzen-y @mimowo can somebody from approvers pls run the action manually?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-27T02:38:10Z

I manually triggered that.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-27T04:27:20Z

The same error:

```
DEBUG: Error retrieving vulnerability alerts (repository=kubernetes-sigs/kueue)
       "err": {
         "message": "integration-unauthorized",
         "stack": "Error: integration-unauthorized\n    at handleGotError (/usr/local/renovate/lib/util/http/github.ts:129:12)\n    at GithubHttp.handleError (/usr/local/renovate/lib/util/http/github.ts:344:11)\n    at GithubHttp.request (/usr/local/renovate/lib/util/http/http.ts:258:12)\n    at processTicksAndRejections (node:internal/process/task_queues:103:5)\n    at GithubHttp.requestJsonUnsafe (/usr/local/renovate/lib/util/http/github.ts:358:20)\n    at GithubHttp.requestJson (/usr/local/renovate/lib/util/http/http.ts:359:17)\n    at Proxy.getVulnerabilityAlerts (/usr/local/renovate/lib/modules/platform/github/index.ts:2077:7)\n    at detectVulnerabilityAlerts (/usr/local/renovate/lib/workers/repository/init/vulnerability.ts:65:18)\n    at initRepo (/usr/local/renovate/lib/workers/repository/init/index.ts:73:12)\n    at /usr/local/renovate/lib/workers/repository/index.ts:80:18\n    at Object.renovateRepository (/usr/local/renovate/lib/workers/repository/index.ts:54:42)\n    at attributes.repository (/usr/local/renovate/lib/workers/global/index.ts:188:11)\n    at start (/usr/local/renovate/lib/workers/global/index.ts:173:7)\n    at /usr/local/renovate/lib/renovate.ts:19:22"
       }
 WARN: Cannot access vulnerability alerts. Please ensure permissions have been granted. (repository=kubernetes-sigs/kueue)
       "url": "https://docs.renovatebot.com/configuration-options/#vulnerabilityalerts"
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-27T04:27:53Z

Did we install renovate APP https://docs.renovatebot.com/getting-started/installing-onboarding/?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-11-27T11:44:21Z

It should have opened onboarding PR:

<img width="1728" height="894" alt="Image" src="https://github.com/user-attachments/assets/a38dfbe1-8ae3-42d6-956d-be90d6218ff3" />

But probably due to some permissions it didn't
Dashboard is created though: https://github.com/kubernetes-sigs/kueue/issues/7928#issuecomment-3583987230

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-11-27T11:46:35Z

> Did we install renovate APP https://docs.renovatebot.com/getting-started/installing-onboarding/?

In my fork I didn't need to install it
Maybe it's still in review, I'm not sure how to check https://github.com/kubernetes-sigs/kueue/issues/5773#issuecomment-3553666366

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-02T09:30:16Z

I have just experimentally triggered the installation for Kueue. I haven't got any permission error. How to check if this works now?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-12-02T09:39:09Z

Сan you pls attach the link to the run? I don't see it here: http://github.com/kubernetes-sigs/kueue/actions/workflows/update-versions-with-renovate.yaml?query=branch%3Amain

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:53:18Z

/close
as we for now suspend working on Renovate

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-19T09:53:23Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7904#issuecomment-3674353331):

>/close
>as we for now suspend working on Renovate


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
