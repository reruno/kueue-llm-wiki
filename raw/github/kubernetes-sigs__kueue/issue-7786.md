# Issue #7786: [release-0.13] Flaky Integration Test: unable to start control plane itself

**Summary**: [release-0.13] Flaky Integration Test: unable to start control plane itself

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7786

**Last updated**: 2025-12-01T09:02:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-11-20T19:44:36Z
- **Updated**: 2025-12-01T09:02:10Z
- **Closed**: 2025-12-01T09:02:09Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Failure on periodic CI Job:

```shell
  [FAILED] Unexpected error:
      <*fmt.wrapError | 0xc000374280>: 
      unable to start control plane itself: failed to start the controlplane. retried 5 times: exec: "etcd": executable file not found in $PATH
      {
          msg: "unable to start control plane itself: failed to start the controlplane. retried 5 times: exec: \"etcd\": executable file not found in $PATH",
          err: <*fmt.wrapError | 0xc000374260>{
              msg: "failed to start the controlplane. retried 5 times: exec: \"etcd\": executable file not found in $PATH",
              err: <*exec.Error | 0xc0003741c0>{
                  Name: "etcd",
                  Err: <*errors.errorString | 0x4952ee0>{
                      s: "executable file not found in $PATH",
                  },
              },
          },
      }
  occurred
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-multikueue-release-0-13/1991558206182133760

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-20T19:44:56Z

/kind flake

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-21T07:55:41Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-21T08:37:15Z

I think it was infrastructure/network problem

```
unable to download requested version: unable fetch envtest-v1.33.0-linux-amd64.tar.gz (https://github.com/kubernetes-sigs/controller-tools/releases/download/envtest-v1.33.0/envtest-v1.33.0-linux-amd64.tar.gz) -- got status "503 Service Unavailable"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-21T08:42:47Z

Yeah, we have occasionally network issues on fetching dependencies. I'm wondering if there is a way to configure some kind of retry on network issues. Some tools like `curl` have parameters to retry a limited number of times, so this could help to mitigate the problems.

Please check, but if there is nothing available, then we can close the ticket. I wouldn't go into implementing the retry ourselves.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-21T09:24:59Z

It's being installed by `go install` no option for retry, only custom made retries.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-21T09:33:12Z

I see, makes sense. Since this problem keeps returning maybe you can ask on k8s-infra slack? Maybe there is a way to configure some proxy that would cache artifacts (but not sure)

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-21T09:51:32Z

https://kubernetes.slack.com/archives/CCK68P2Q2/p1763718686382369

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-01T08:47:02Z

According to the slack channel response there was GitHub incident and it was resolved, no cache for artefacts is present.
I think we can close this one

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T09:02:03Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T09:02:10Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7786#issuecomment-3595375991):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
