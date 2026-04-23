# Issue #4445: Helm cannot automatically detect the latest version of the chart in registry.k8s.io

**Summary**: Helm cannot automatically detect the latest version of the chart in registry.k8s.io

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4445

**Last updated**: 2025-03-18T04:02:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nojnhuh](https://github.com/nojnhuh)
- **Created**: 2025-03-01T00:32:23Z
- **Updated**: 2025-03-18T04:02:24Z
- **Closed**: 2025-03-14T10:13:49Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Invoking `helm` commands against the chart in registry.k8s.io fails to find the latest version of the chart when no version is specified, or a matching version when a non-literal constraint is specified.

**What you expected to happen**:

Helm is able to operate on the tags in the registry as semvers.

**How to reproduce it (as minimally and precisely as possible)**:

```console
% helm show chart oci://registry.k8s.io/charts/kueue
Error: Unable to locate any tags in provided repository: oci://registry.k8s.io/charts/kueue
% helm show chart oci://registry.k8s.io/charts/kueue --version ^0.10
Error: Unable to locate any tags in provided repository: oci://registry.k8s.io/charts/kueue
```

Specifying an exact version does work:
```console
% helm show chart oci://registry.k8s.io/charts/kueue:v0.10.2
Pulled: registry.k8s.io/charts/kueue:v0.10.2
...
% helm show chart oci://registry.k8s.io/charts/kueue --version v0.10.2
Pulled: registry.k8s.io/charts/kueue:v0.10.2
...
```

**Anything else we need to know?**:

I'm reasonably certain the issue is the leading "v" in the tag names on the Helm chart OCI artifacts. The [parsing function Helm uses](https://github.com/helm/helm/blob/fd69bf6f32ce2b485a080f0924768773dffd9d3d/pkg/registry/client.go#L801-L804) doesn't seem to like those: https://go.dev/play/p/Uiq7yp4YsCF

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
    ```
    % helm version
    version.BuildInfo{Version:"v3.17.1", GitCommit:"980d8ac1939e39138101364400756af2bdee1da5", GitTreeState:"", GoVersion:"go1.24.0"}
    ```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-13T21:54:47Z

Thank you for reporting this!
@mimowo What about promoting additional tags to align Helm specification in https://github.com/kubernetes/k8s.io/blob/6e5ebe6c15d81e5674416bc93dc0968d5a613a15/registry.k8s.io/images/charts/images.yaml#L4-L9 like

```
- name: kueue
  dmap:
    "sha256:b7730869b937cf6e412140eec7403b4d32fd28bce5fcb014a349032a0ecdc7e4": ["v0.10.2", "0.10.2"]
    "sha256:56acd0d3805fee0ec8f071e0dfa41b926d4e5b6f5cf60436ffa42300f6dc17d5": ["v0.10.1", "0.10.1"]
    "sha256:bc238183a94983d85483dcb028f2c6dbffe5dee8d9f2b46988680049eb708df9": ["v0.9.4", "0.9.4"]
    "sha256:577b280e31a978a82d82da097c236b8ec4ae8323f1c3bfcc06d25eed45d0d874": ["v0.9.3", "0.9.3"]
```

And we promote only tag without `v` prefix for the next release like `"sha256:xyz": ["0.11.0"]`

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T07:16:24Z

+1, good idea, and moving forward would we only publish without "v" or both?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T07:20:31Z

> +1, good idea, and moving forward would we only publish without "v" or both?

Since the v0.11.0, only without `v` is enough, IMO

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T07:32:49Z

sgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T10:16:38Z

I verified this works fine :)

```shell
$ helm show chart oci://registry.k8s.io/charts/kueue
Pulled: registry.k8s.io/charts/kueue:0.10.2
Digest: sha256:b7730869b937cf6e412140eec7403b4d32fd28bce5fcb014a349032a0ecdc7e4
apiVersion: v2
appVersion: v0.10.2
description: Kueue is a set of APIs and controller for job queueing. It is a job-level
  manager that decides when a job should be admitted to start (as in pods can be created)
  and when it should stop (as in active pods should be deleted).
name: kueue
type: application
version: v0.10.2
$ helm show chart oci://registry.k8s.io/charts/kueue --version ^0.10
Pulled: registry.k8s.io/charts/kueue:0.10.2
Digest: sha256:b7730869b937cf6e412140eec7403b4d32fd28bce5fcb014a349032a0ecdc7e4
apiVersion: v2
appVersion: v0.10.2
description: Kueue is a set of APIs and controller for job queueing. It is a job-level
  manager that decides when a job should be admitted to start (as in pods can be created)
  and when it should stop (as in active pods should be deleted).
name: kueue
type: application
version: v0.10.2
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T04:02:23Z

I know JobSet uses the same mechanism for Helm Chart.
So, @kannon92 is probably interested in this.
