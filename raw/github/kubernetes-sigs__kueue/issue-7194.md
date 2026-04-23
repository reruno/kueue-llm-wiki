# Issue #7194: pull-kueue-test-integration-extended-main flakes with "unable to create CRD "workloadpriorityclasses.kueue.x-k8s.io"

**Summary**: pull-kueue-test-integration-extended-main flakes with "unable to create CRD "workloadpriorityclasses.kueue.x-k8s.io"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7194

**Last updated**: 2026-03-19T12:50:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-07T14:02:11Z
- **Updated**: 2026-03-19T12:50:11Z
- **Closed**: 2026-03-19T12:50:09Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 4

## Description

/kind flake

**What happened**:

unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7157/pull-kueue-test-integration-extended-main/1975555739745259520

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
Provisioning admission check suite: [BeforeSuite] expand_less
Run #0: Passed expand_more	20s
Run #1: Failed expand_less	14s
{Unexpected error:
    <*fmt.wrapError | 0xc000808340>: 
    unable to install CRDs onto control plane: unable to create CRD instances: unable to create CRD "workloadpriorityclasses.kueue.x-k8s.io": Post "https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions": unexpected EOF
    {
        msg: "unable to install CRDs onto control plane: unable to create CRD instances: unable to create CRD \"workloadpriorityclasses.kueue.x-k8s.io\": Post \"https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions\": unexpected EOF",
        err: <*fmt.wrapError | 0xc0008082c0>{
            msg: "unable to create CRD instances: unable to create CRD \"workloadpriorityclasses.kueue.x-k8s.io\": Post \"https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions\": unexpected EOF",
            err: <*fmt.wrapError | 0xc0008082a0>{
                msg: "unable to create CRD \"workloadpriorityclasses.kueue.x-k8s.io\": Post \"https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions\": unexpected EOF",
                err: <*url.Error | 0xc000ca5800>{
                    Op: "Post",
                    URL: "https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions",
                    Err: <*errors.errorString | 0x4bfefc0>{s: "unexpected EOF"},
                },
            },
        },
    }
occurred failed [FAILED] Unexpected error:
    <*fmt.wrapError | 0xc000808340>: 
    unable to install CRDs onto control plane: unable to create CRD instances: unable to create CRD "workloadpriorityclasses.kueue.x-k8s.io": Post "https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions": unexpected EOF
    {
        msg: "unable to install CRDs onto control plane: unable to create CRD instances: unable to create CRD \"workloadpriorityclasses.kueue.x-k8s.io\": Post \"https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions\": unexpected EOF",
        err: <*fmt.wrapError | 0xc0008082c0>{
            msg: "unable to create CRD instances: unable to create CRD \"workloadpriorityclasses.kueue.x-k8s.io\": Post \"https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions\": unexpected EOF",
            err: <*fmt.wrapError | 0xc0008082a0>{
                msg: "unable to create CRD \"workloadpriorityclasses.kueue.x-k8s.io\": Post \"https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions\": unexpected EOF",
                err: <*url.Error | 0xc000ca5800>{
                    Op: "Post",
                    URL: "https://127.0.0.1:44755/apis/apiextensions.k8s.io/v1/customresourcedefinitions",
                    Err: <*errors.errorString | 0x4bfefc0>{s: "unexpected EOF"},
                },
            },
        },
    }
occurred
In [BeforeSuite] at: /home/prow/go/src/sigs.k8s.io/kueue/vendor/github.com/onsi/ginkgo/v2/internal/suite.go:328 @ 10/07/25 13:41:52.738
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:46:57Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T12:48:19Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T12:50:03Z

/close
Looks like weird one off. I haven't seen it repeat. The logs are already gone. Let's open a new one if this repeats.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-19T12:50:11Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7194#issuecomment-4089910211):

>/close
>Looks like weird one off. I haven't seen it repeat. The logs are already gone. Let's open a new one if this repeats.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
