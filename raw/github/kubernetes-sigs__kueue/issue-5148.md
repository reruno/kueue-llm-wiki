# Issue #5148: Can't change workload priority class of deployment

**Summary**: Can't change workload priority class of deployment

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5148

**Last updated**: 2025-05-13T12:31:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Gab-Menezes](https://github.com/Gab-Menezes)
- **Created**: 2025-05-02T05:47:14Z
- **Updated**: 2025-05-13T12:31:25Z
- **Closed**: 2025-05-13T12:31:23Z
- **Labels**: `kind/bug`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: The label `kueue.x-k8s.io/priority-class` is immutable for deployments.

**What you expected to happen**: Be able to change the workload priority of a deployment.

The [docs](https://kueue.sigs.k8s.io/docs/reference/labels-and-annotations/#kueuex-k8siopriority-class) say:
> The label key in the workload holds the workloadPriorityClass name. This label is always mutable, as it may be useful for preemption...

**How to reproduce it (as minimally and precisely as possible)**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
    kueue.x-k8s.io/queue-name: user-queue
    kueue.x-k8s.io/priority-class: dev-priority # <-- try to change this
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: registry.k8s.io/nginx-slim:0.27
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: "500m"
```

Gives you the following error:
```
Error from server (Forbidden): error when applying patch:
<redacted>
to:
Resource: "apps/v1, Resource=deployments", GroupVersionKind: "apps/v1, Kind=Deployment"
Name: "<redacted>", Namespace: "default"
for: "<redacted>": error when patching "<redacted>": admission webhook "vdeployment.kb.io" denied the request: metadata.labels[kueue.x-k8s.io/priority-class]: Invalid value: "<redacted>": field is immutable
```

**Anything else we need to know?**: No

**Environment**:
- Kubernetes version (use `kubectl version`): 1.31.2
- Kueue version (use `git describe --tags --dirty --always`): 0.11.3
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@Gab-Menezes](https://github.com/Gab-Menezes) — 2025-05-02T08:04:38Z

Btw this also applies to `kueue.x-k8s.io/queue-name`, but idk if the queue name should always be mutable. The doc doesn't state it

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-02T12:25:40Z

Is it valid to patch labels for deployments without queue? 

It’s unclear if the webhook validation comes from Kueue or kube.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-02T18:29:56Z

Actually, the documentation is not valid. Additionally, immutable `kueue.x-k8s.io/queue-name` is intended during Job w/o suspended.

> The label key in the workload holds the workloadPriorityClass name. This label is always mutable, as it may be useful for preemption...

The workloadPriorityClass Name in Job is immutable, but WorkloadPriorityClass value (`.value`) is mutable.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-02T18:30:19Z

/kind documentation

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-05-08T19:53:20Z

This seems to be related to #5004. We're currently working on #5197, which should make the `kueue.x-k8s.io/priority-class` label mutable.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-05-13T08:50:58Z

@Gab-Menezes, the PR #5197 has been merged. I think that should fix this issue. The PR makes the `kueue.x-k8s.io/priority-class` label mutable as long as the workload is suspended. If unsuspended, the field becomes immutable.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-13T12:31:19Z

@IrvingMg Thank you for your work. Let us close this one.
@Gab-Menezes If you have another issue, feel free to open new ones.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-13T12:31:24Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5148#issuecomment-2876326099):

>@IrvingMg Thank you for your work. Let us close this one.
>@Gab-Menezes If you have another issue, feel free to open new ones.
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
