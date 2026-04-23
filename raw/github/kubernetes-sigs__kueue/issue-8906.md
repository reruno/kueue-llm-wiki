# Issue #8906: Re-enable running make verify in parallel

**Summary**: Re-enable running make verify in parallel

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8906

**Last updated**: 2026-02-10T11:04:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-30T11:28:50Z
- **Updated**: 2026-02-10T11:04:01Z
- **Closed**: 2026-02-10T11:04:01Z
- **Labels**: `kind/bug`, `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 17

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

**What you expected to happen**:

No issue 

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8895/pull-kueue-verify-main/2017169977206902784

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T11:28:59Z

/cc @vladikkuzn

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T11:48:23Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T11:55:26Z

One more possible error:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8891/pull-kueue-verify-main/2017169642539192320.

```
make[1]: *** [Makefile-deps.mk:245: kueuectl-docs] Error 1
```

But I believe it's related.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T11:56:22Z

Probably it's happening due to race conditions introduced in https://github.com/kubernetes-sigs/kueue/pull/8731.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T11:56:40Z

@vladikkuzn could you please take a look?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T12:00:57Z

One more:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8894/pull-kueue-verify-main/2017169933586141184.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-30T12:14:11Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T13:16:20Z

@vladikkuzn, any ideas here? This issue happens very often – almost in every PR. If we don’t have a quick fix, I’d suggest reverting https://github.com/kubernetes-sigs/kueue/pull/8731 for now. WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T13:21:56Z

Good point, if we don't have a fix in 30min or so I suggest to revert and test well/ fix before re-applying the PR.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-30T13:48:28Z

Let me revert it then, I just can't spot it for now locally

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-30T13:55:42Z

https://github.com/kubernetes-sigs/kueue/pull/8916

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T13:57:28Z

or maybe better just reverting just use -j1?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T14:56:11Z

/retitle Re-enable running make verify in parallel
After we merged https://github.com/kubernetes-sigs/kueue/pull/8916 I think we can remove flake, let's call it 
/remove-kind flake

btw, is `E0130 14:30:16.594688   30912 types.go:298] External link source for 'k8s.io/client-go/tools/clientcmd/api.ExecConfig' is not found.` due to the same issue - parallel execution?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T14:57:32Z

/kind cleanup

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T15:42:10Z

> btw, is E0130 14:30:16.594688   30912 types.go:298] External link source for 'k8s.io/client-go/tools/clientcmd/api.ExecConfig' is not found. due to the same issue - parallel execution?

No. This is another one.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T15:56:07Z

Do you know which PR introduced the "ExecConfig" flake? I didn't see it before the "parallel make verify"

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T16:17:00Z

> Do you know which PR introduced the "ExecConfig" flake? I didn't see it before the "parallel make verify"

Actually, I’m not sure. But it’s just a warning, and I saw it a few months ago.
