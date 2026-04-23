# Issue #7683: Getting unhandled exception for getting secrets at cluster level with latest main

**Summary**: Getting unhandled exception for getting secrets at cluster level with latest main

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7683

**Last updated**: 2025-11-17T16:42:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-11-16T21:53:57Z
- **Updated**: 2025-11-17T16:42:01Z
- **Closed**: 2025-11-17T16:42:00Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

```
  {"level":"error","ts":"2025-11-15T15:52:40.054785869Z","logger":"controller-runtime.cache.UnhandledError","caller":"runtime/runtime.go:221","msg":"Failed to watch","reflector":"sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114","type":"*v1.Secret","error":"failed to list *v1.Secret: secrets is forbidden: User \"system:serviceaccount:openshift-kueue-operator:kueue-controller-manager\" cannot list resource \"secrets\" in API group \"\" at the cluster scope
```

https://github.com/openshift/kueue-operator/pull/917

I am updating our openshift operator to point to main to test against latest main.

I was trying to see if I can run the e2e against an openshift kueue installation.

**What you expected to happen**:

I shouldnt see errors like this in our operator logs.

**How to reproduce it (as minimally and precisely as possible)**:

Openshift tend to be more restrictive about RBAC so you may be able to reproduce this if you deploy main to a OCP cluster. 

https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/test-platform-results/pr-logs/pull/openshift_kueue-operator/917/pull-ci-openshift-kueue-operator-main-test-e2e-4-18/1989716339769479168/artifacts/test-e2e-4-18/e2e-kueue/build-log.txt

**Anything else we need to know?**:

The failure happens on k8s 1.31, 1.32 and 1.33.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-16T21:59:54Z

I believe https://github.com/kubernetes-sigs/kueue/pull/7188 is the one patch related to this.

I tried to take deploy the rbac related to the secrets but I think some cache is still thinking that we need to list secrets across namespaces. :(

cc @mimowo @tenzen-y @sbgla-sas

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T06:24:27Z

This looks exactly the error I would expect the old version of Kueue would throw when new RBACs are installed. 

Can you double check the logs are thrown from the running container of the main branch?

Also please share more logs before that line to see at what context the error is thrown.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T07:30:32Z

Looking at the logs from https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/test-platform-results/pr-logs/pull/openshift_kueue-operator/917/pull-ci-openshift-kueue-operator-main-test-e2e-4-18/1989716339769479168/artifacts/test-e2e-4-18/e2e-kueue/build-log.txt
seems you are running not main, but a custom built image with some changes.

See **"gitVersion":"a073ed4-dirty",** in this log line:

```
 {"level":"info","ts":"2025-11-15T15:59:56.125628503Z","logger":"setup","caller":"kueue/main.go:150","msg":"Initializing","gitVersion":"a073ed4-dirty","gitCommit":"a073ed4cae46b221815ec56995a677c50d388ca5","buildDate":"2025-11-11T19:11:35Z"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T11:05:16Z

You could also try testing the v0.15.0-rc.0 for that which already includes the change too

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-17T12:24:06Z

I can't use tags. The custom build is because we have to patch builds to use Golang 1.24.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-17T12:24:41Z

I'm pretty sure this is using main as of 2-3 days ago.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T12:46:52Z

I see, still I would suggest to repeat to double check

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-17T12:53:13Z

Yea I'll see if I can install the rc onto a OCP cluster today also.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T13:38:47Z

FWIIW I tested today installing the latest main on a GKE cluster and haven't hit the issue

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-17T16:41:08Z

Thanks. I think this may be my issue to solve.

I also confirm that installing rc onto OCP I don't see this issue.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-17T16:41:54Z

/close

I think you are right. We may be using 0.14 binaries still.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-17T16:42:01Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7683#issuecomment-3542855550):

>/close
>
>I think you are right. We may be using 0.14 binaries still.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
