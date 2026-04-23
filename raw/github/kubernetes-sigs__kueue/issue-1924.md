# Issue #1924: Investigate and use RetryWatcher (if feasible) to handle connections closed by the API server

**Summary**: Investigate and use RetryWatcher (if feasible) to handle connections closed by the API server

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1924

**Last updated**: 2024-04-11T07:14:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-03-28T09:20:41Z
- **Updated**: 2024-04-11T07:14:55Z
- **Closed**: 2024-04-11T07:14:54Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The craft in MultiKueue to handle error logging when API server closes the connection. Here is the upstream summary of the issue: https://github.com/kubernetes/client-go/issues/1340, and the corresponding summary in Kueue: https://github.com/kubernetes-sigs/kueue/pull/1823#issuecomment-2022454868. 

Until the issue is fixed upstream we could investigate the use of RetryWatcher, which seems to take care of that: https://github.com/kubernetes/kubernetes/blob/f4e246bc93ffb68b33ed67c7896c379efa4207e7/staging/src/k8s.io/client-go/tools/watch/retrywatcher.go#L211-L214. As a higher level abstraction it may also help us with other corner cases not discovered yet.

**Why is this needed**:

To simplify the code by eliminating our custom logic to do not log the errors. Here is the logic, which uses the `V(3).Info` instead of `Error` (or `V(2)`), which means we may actually be covering some real errors:  https://github.com/kubernetes-sigs/kueue/blob/c8078b507d3342c0a6c2772f0451ede7a2c04864/pkg/controller/admissionchecks/multikueue/multikueuecluster.go#L202-L207

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-04T14:52:50Z

/assign @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-04-09T07:34:52Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-04-09T11:09:37Z

@mimowo in case of multikueue we are doing the retry in any cases, what we can take from https://github.com/kubernetes/kubernetes/blob/f4e246bc93ffb68b33ed67c7896c379efa4207e7/staging/src/k8s.io/client-go/tools/watch/retrywatcher.go#L211-L214 is just skip the logging if `http.StatusGatewayTimeout, http.StatusInternalServerError`.

The problem in my opinion is that `http.StatusInternalServerError` is very generic in my opinion and I'm not sure which is better:
- Ignore all `http.StatusInternalServerError` and potentially miss error that is not related to this timeout.
- Keep it as is and continue to receive a "false positive" error until this gets a fix upstream.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-09T11:56:28Z

I see, if this is just for silencing the error, then I'm ok to park it.

I was hoping it could also replace our custom logic for retries, would it be feasible?

### Comment by [@trasc](https://github.com/trasc) — 2024-04-09T13:59:54Z

We are already retrying, it's just a matter of logging.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-09T14:37:22Z

I know, but maybe it is worth to take a look how much we could simplify the code by reusing this helper? 

If we cannot simplify much then I guess we can close the issue, but the class seems to be solving a similar problem.

### Comment by [@trasc](https://github.com/trasc) — 2024-04-10T05:51:48Z

The problem is that the helper wraps a different kind of `Watcher` interface.

### Comment by [@trasc](https://github.com/trasc) — 2024-04-11T07:14:49Z

Let's not do this for now.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-11T07:14:54Z

@trasc: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1924#issuecomment-2049064553):

>Let's not do this for now.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
