# Issue #4514: Make WaitForActivePodsAndTerminate not racy

**Summary**: Make WaitForActivePodsAndTerminate not racy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4514

**Last updated**: 2025-03-12T11:53:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-06T12:07:04Z
- **Updated**: 2025-03-12T11:53:47Z
- **Closed**: 2025-03-12T11:53:47Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 6

## Description

**What would you like to be cleaned**:

Make the function WaitForActivePodsAndTerminate not racy. It is currently racy because:
1. it may be sending the /exit request to a Pending pods - and this would clearly fail as a Pending pod is not listening on the port
2. the pod might be Running, but still not listening on the port - then the /exit request most likely fails too (but we could check it)

I think, it might be hard to make sure the pod is already listening on the port, maybe we can verify by the failure message, or check pod readiness. If this is non-trivial we could just repeat the request and wait until the pod is terminated. Currently we just send the request and forget.

**Why is this needed**:

The fact that the WaitForActivePodsAndTerminate may send the request to a pod which is not listening and forgets makes it hard to reason about the test code.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T12:07:14Z

/assign @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-06T12:11:56Z

We can send "/healthz" request to the pod, if service is ready it should return with 200 
https://pkg.go.dev/k8s.io/kubernetes@v1.32.2/test/images/agnhost/netexec

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T12:21:53Z

probably ` "/readyz": Returns "200 OK" if the server is ready to receive traffic, `

but in any case it would be good to have it reproducible. Maybe you can try to re-complile agnhost locally with injected sleep 2s before this line: https://github.com/kubernetes/kubernetes/blob/master/test/images/agnhost/liveness/server.go#L66. Then, you will be able to reliably capture the situation when the pod is "Running", and "healthy", but not listening yet.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T12:23:56Z

I would suggest to start tackling the issue by removing `|| Pending`, which will already narrow down the scope of sending the request into void.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T12:29:18Z

Actually, maybe this is the reason for the recent flakes, where we expect the pod to end Succeeded, but it doesn't because the /exit 0 goes into void.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T12:16:40Z

I believe this failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4519/pull-kueue-test-e2e-main-1-30/1899056929494274048 was actually caused by the issue with WaitForActivePodsAndTerminate as the pods continue to be Running, so it seems as the /exit 1 request went into void, and the pods continue happily.
