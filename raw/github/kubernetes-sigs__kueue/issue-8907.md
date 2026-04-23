# Issue #8907: External link source for 'k8s.io/client-go/tools/clientcmd/api.ExecConfig' is not found

**Summary**: External link source for 'k8s.io/client-go/tools/clientcmd/api.ExecConfig' is not found

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8907

**Last updated**: 2026-02-02T11:32:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-30T11:34:16Z
- **Updated**: 2026-02-02T11:32:36Z
- **Closed**: 2026-02-02T11:32:36Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 15

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When running `make generate-apiref` we have a warning:

```
E0130 09:47:04.566212   30664 types.go:298] External link source for 'k8s.io/client-go/tools/clientcmd/api.ExecConfig' is not found.
```

**What you expected to happen**:

No warnings

**How to reproduce it (as minimally and precisely as possible)**:

Run:

```
make generate-apiref`
```

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T11:35:48Z

/cc @mszadkow

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T11:37:20Z

/remove-kind bug
/kind cleanup

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T14:59:10Z

I'm wondering if the root cause here was maybe also the parallel verify: https://github.com/kubernetes-sigs/kueue/issues/8906, wdyt?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:11:31Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:12:15Z

/kind bug
Well, builds should fail to it, so it is a bug

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T16:12:51Z

> I'm wondering if the root cause here was maybe also the parallel verify: https://github.com/kubernetes-sigs/kueue/issues/8906, wdyt?

No, this isn’t an error – it’s a warning. We’ve already seen this before.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T16:13:42Z

/remove-kind bug

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:16:41Z

Hmm, I thought my build failed on that one:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8913/pull-kueue-verify-main/2017242111480434688

PTAL:

```
Generating lister code for 5 targets
No depcheck issue
Generating informer code for 5 targets
I0130 14:29:32.561875   30912 main.go:325] Output written to /home/prow/go/src/sigs.k8s.io/kueue/site/content/en/docs/reference/kueue-config.v1beta1.md
I0130 14:29:32.561911   30912 main.go:142] Parsing go packages in sigs.k8s.io/kueue/apis/config/v1beta2
E0130 14:30:16.594688   30912 types.go:298] External link source for 'k8s.io/client-go/tools/clientcmd/api.ExecConfig' is not found.
I0130 14:30:16.603525   30912 main.go:325] Output written to /home/prow/go/src/sigs.k8s.io/kueue/site/content/en/docs/reference/kueue-config.v1beta2.md
make[1]: Leaving directory '/home/prow/go/src/sigs.k8s.io/kueue'
make: *** [Makefile-verify.mk:56: verify] Error 2
```
but maybe indeed the underlying issue was different

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:18:02Z

/remove-kind flake
if this is not causing builds to fail then indeed just cleanup. It would be great to cleanup the warning to avoid confusion, +1.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:20:14Z

Indeed, my build was executing the verify in parallel: `make -j 8 verify-tree-prereqs verify-checks` in https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8913/pull-kueue-verify-main/2017242111480434688/build-log.txt

So likely the underlying failure for my build was indeed https://github.com/kubernetes-sigs/kueue/issues/8906, and not `go/tools/clientcmd/api.ExecConfig'`

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T16:21:21Z

> Hmm, I thought my build failed on that one:
>
> https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8913/pull-kueue-verify-main/2017242111480434688



No, it failed because of this:

```
make[1]: *** [Makefile-deps.mk:245: kueuectl-docs] Error 1
```

Now that we have parallel targets, the logs appear in random order instead of at the end.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T16:22:39Z

Look here https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8913/pull-kueue-verify-main/2017242111480434688#1:build-log.txt%3A764.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T16:23:29Z

As I mentioned on the PR description you can catch this warning running `make generate-apiref`.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T16:24:33Z

Awesome, ok, we need to be more careful before re-enabling concurrent make verify. Probably worth running in a loop for over night :)

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-01T10:53:44Z

/assign
