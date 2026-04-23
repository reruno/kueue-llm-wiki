# Issue #5244: A down kueue deployment will block all jobs

**Summary**: A down kueue deployment will block all jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5244

**Last updated**: 2025-05-15T15:46:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-05-14T00:14:07Z
- **Updated**: 2025-05-15T15:46:32Z
- **Closed**: 2025-05-15T15:46:30Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

If kueue deployment is unavailable or down for some reason, Kueue will block all jobs.

Even if Job does not have a queue label, a down kueue deployment will block the submission of batch jobs.

```bash
k create -f sample-no-label.yaml 
Error from server (InternalError): error when creating "jobs/sample-no-label.yaml": Internal error occurred: failed calling webhook "mjob.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s": dial tcp 10.96.58.56:443: connect: connection refused

```

**What you expected to happen**:

Jobs without queueName specified should still be submitted if Kueue is down.

**How to reproduce it (as minimally and precisely as possible)**:

a. deploy kueue normally.
b. create localqueue/cq/rf.
c. scale kueue deployment to 0 (kubectl scale --current-replicas 1 --replicas 0 -n kueue-system kueue-controller-manager
d. create the file below.
```sample-no-label.yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: no-label-job-
  namespace: default
spec:
  parallelism: 3
  completions: 3
  template:
    spec:
      containers:
      - name: dummy-job
        image: registry.k8s.io/e2e-test-images/agnhost:2.53
        args: ["entrypoint-tester", "hello", "world"]
        resources:
          requests:
            cpu: 1
            memory: "200Mi"
      restartPolicy: Never

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-14T05:17:01Z

This is not a bug. The behavior comes from the admission controller specifications. The only mitigation way is leveraging leader election mechanism by `replica: 2`. 

To mitigate this problem as much as possible, we minimize the lease switching duration by `LeaderElectionReleaseOnCancel`.

https://github.com/kubernetes-sigs/kueue/blob/4cafd5fbad492983c9e3b8fde2dea2823712d44f/pkg/config/config.go#L131-L135

/remove-kind bug
/kind support

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-14T15:08:13Z

The main concern is that if a job is not managed by Kueue (no queue-label and no ManagedJobWithoutQueueName) a down kueue deployment will still block the submission of non kueue jobs.

That does seem like a bug to me.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-14T15:13:26Z

In that case, you can specify the objectSelector (or namespaceSelector) in webhook configurations. However, it will relax the quata management since it provides the way to skip suspending / quota checking restriction.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-14T15:16:53Z

or you could configure in the webhook failurePolicy: Ingore. However, the downside is that jobs using kueue would bypass kueue and start to run.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-14T15:21:00Z

> or you could configure in the webhook failurePolicy: Ingore. However, the downside is that jobs using kueue would bypass kueue and start to run.

Yeah, failurePolicy could be potential solution. However it is very aggressive and dangerous, IMO. When webhook call request will fail based on non deployment down reason, they can bypass our every system checkings.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-14T15:33:01Z

yes, this is why our recommendation to users is to use HA mode as mentioned before. I don't know what else we could do. I would welcome a contribution to add a subpage to [Productization page](https://kueue.sigs.k8s.io/docs/tasks/manage/productization/), such as "Best practices" and mention this aspect of configuring Kueue.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-14T17:34:55Z

> yes, this is why our recommendation to users is to use HA mode as mentioned before.

Should that be our default deployment for kustomize/helm?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T15:46:26Z

Let's consider the discussion in a new issue: #5250 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-15T15:46:30Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5244#issuecomment-2884302769):

>Let's consider the discussion in a new issue: #5250 
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
