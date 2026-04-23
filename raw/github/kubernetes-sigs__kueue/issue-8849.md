# Issue #8849: Flaky Test: Setup Controllers Should setup controller and webhook after CRD installation

**Summary**: Flaky Test: Setup Controllers Should setup controller and webhook after CRD installation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8849

**Last updated**: 2026-01-28T07:27:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-28T07:10:02Z
- **Updated**: 2026-01-28T07:27:38Z
- **Closed**: 2026-01-28T07:27:37Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

Setup Controllers Suite: [It] Setup Controllers Should setup controller and webhook after CRD installation [controller:jobframework, area:jobs, slow]

```
{Unexpected error:
    <*fmt.wrapError | 0xc00109d900>: 
    jobFrameworkName "leaderworkerset.x-k8s.io/leaderworkerset": unable to create noop webhook: no kind is registered for the type v1.LeaderWorkerSet in scheme "sigs.k8s.io/kueue/test/integration/framework/framework.go:124"
    {
        msg: "jobFrameworkName \"leaderworkerset.x-k8s.io/leaderworkerset\": unable to create noop webhook: no kind is registered for the type v1.LeaderWorkerSet in scheme \"sigs.k8s.io/kueue/test/integration/framework/framework.go:124\"",
        err: <*runtime.notRegisteredErr | 0xc0005d2a20>{
            schemeName: "sigs.k8s.io/kueue/test/integration/framework/framework.go:124",
            gvk: {Group: "", Version: "", Kind: ""},
            target: nil,
            t: <*reflect.rtype | 0x3086440>{
                t: {Size_: 0x4c0, PtrBytes: 0x4b8, Hash: 3133746632, TFlag: 7, Align_: 8, FieldAlign_: 8, Kind_: 25, Equal: nil, GCData: 85, Str: 226583, PtrToThis: 5060096},
            },
        },
    }
occurred failed [FAILED] Unexpected error:
    <*fmt.wrapError | 0xc00109d900>: 
    jobFrameworkName "leaderworkerset.x-k8s.io/leaderworkerset": unable to create noop webhook: no kind is registered for the type v1.LeaderWorkerSet in scheme "sigs.k8s.io/kueue/test/integration/framework/framework.go:124"
    {
        msg: "jobFrameworkName \"leaderworkerset.x-k8s.io/leaderworkerset\": unable to create noop webhook: no kind is registered for the type v1.LeaderWorkerSet in scheme \"sigs.k8s.io/kueue/test/integration/framework/framework.go:124\"",
        err: <*runtime.notRegisteredErr | 0xc0005d2a20>{
            schemeName: "sigs.k8s.io/kueue/test/integration/framework/framework.go:124",
            gvk: {Group: "", Version: "", Kind: ""},
            target: nil,
            t: <*reflect.rtype | 0x3086440>{
                t: {Size_: 0x4c0, PtrBytes: 0x4b8, Hash: 3133746632, TFlag: 7, Align_: 8, FieldAlign_: 8, Kind_: 25, Equal: nil, GCData: 85, Str: 226583, PtrToThis: 5060096},
            },
        },
    }
occurred
In [BeforeEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobframework/setup/suite_test.go:54 @ 01/28/26 07:05:31.823
}
```

```
STEP: tearing down the test environment @ 01/28/26 07:05:31.824
  << Timeline
  [FAILED] Unexpected error:
      <*fmt.wrapError | 0xc00109d900>: 
      jobFrameworkName "leaderworkerset.x-k8s.io/leaderworkerset": unable to create noop webhook: no kind is registered for the type v1.LeaderWorkerSet in scheme "sigs.k8s.io/kueue/test/integration/framework/framework.go:124"
      {
          msg: "jobFrameworkName \"leaderworkerset.x-k8s.io/leaderworkerset\": unable to create noop webhook: no kind is registered for the type v1.LeaderWorkerSet in scheme \"sigs.k8s.io/kueue/test/integration/framework/framework.go:124\"",
          err: <*runtime.notRegisteredErr | 0xc0005d2a20>{
              schemeName: "sigs.k8s.io/kueue/test/integration/framework/framework.go:124",
              gvk: {Group: "", Version: "", Kind: ""},
              target: nil,
              t: <*reflect.rtype | 0x3086440>{
                  t: {Size_: 0x4c0, PtrBytes: 0x4b8, Hash: 3133746632, TFlag: 7, Align_: 8, FieldAlign_: 8, Kind_: 25, Equal: nil, GCData: 85, Str: 226583, PtrToThis: 5060096},
              },
          },
      }
  occurred
```

**What you expected to happen**:

No issue

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8843/pull-kueue-test-integration-extended-main/2016405455680573440

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-28T07:13:59Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-28T07:27:32Z

/close 

This is related issue for https://github.com/kubernetes-sigs/kueue/pull/8843.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-28T07:27:38Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8849#issuecomment-3809499791):

>/close 
>
>This is related issue for https://github.com/kubernetes-sigs/kueue/pull/8843.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
