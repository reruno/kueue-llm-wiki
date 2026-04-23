# Issue #8751: MultiKueue ClusterProfile credentials plugin cannot be mounted when using distroless non-root controller image

**Summary**: MultiKueue ClusterProfile credentials plugin cannot be mounted when using distroless non-root controller image

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8751

**Last updated**: 2026-01-23T13:45:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@morvencao](https://github.com/morvencao)
- **Created**: 2026-01-23T02:28:27Z
- **Updated**: 2026-01-23T13:45:52Z
- **Closed**: 2026-01-23T13:34:40Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What happened**:

I’m trying to use the MultiKueue ClusterProfile feature, which relies on the ClusterProfile credentials plugin to retrieve credentials from a ClusterProfile.
However, I’m running into issues mounting and executing the credentials plugin inside the kueue-controller-manager pod.
The controller manager image is based on a distroless base image and runs as non-root, which appears to prevent the plugin binary from being mounted or accessed correctly at runtime.
The plugin binary cannot be executed, even though it is present in the mounted volume.
```
getting credentials: exec: fork/exec /plugins/cp-creds: no such file or directory
```

**What you expected to happen**:

The Kueue controller manager should be able to discover and execute the ClusterProfile credentials plugin when the MultiKueueClusterProfile feature is enabled and the pligins binary is mounted to manager container.

**How to reproduce it (as minimally and precisely as possible)**:

I attempted to mount the credentials plugin using an image volume:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kueue-controller-manager
spec:
  template:
    spec:
      containers:
      - name: manager
        volumeMounts:
        - name: clusterprofile-plugins
          mountPath: "/plugins"
      volumes:
      - name: clusterprofile-plugins
        image:
          reference: <image_containing_clusterprofile_creds_plugin>
          pullPolicy: IfNotPresent
```

When the controller tries to execute the plugin, it fails with:

```shell
getting credentials: exec: fork/exec /plugins/cp-creds: no such file or directory
```

I also tried using an initContainer to copy the plugin binary into `/plugins`, but the issue still persists.

**Anything else we need to know?**:

Kueue Version: v0.15.3
It appears the issue is caused by the Kueue controller manager image:
- It is based on a distroless image
- It runs as a non-root user

The /plugins directory does not exist in the image filesystem, since the container is non-root, Kubernetes cannot create or change ownership of the mount path at runtime, as a result, the plugin binary cannot be mounted or accessed correctly.

/priority important-soon

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T07:46:43Z

cc @kshalot @mszadkow ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T07:48:33Z

Maybe you can try this https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/#kubernetes-135-mount-the-executable-using-an-image-volume, if you are on K8s 1.35+

### Comment by [@kshalot](https://github.com/kshalot) — 2026-01-23T10:59:13Z

Hey, thanks for the report. Intuitively, volume mounts should work since they are used to inject the manager config among other things, so maybe there is something more subtle at play here. I just did a quick test and it worked on my end.

> Maybe you can try this https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/#kubernetes-135-mount-the-executable-using-an-image-volume, if you are on K8s 1.35+

IIUC @morvencao tried both this and the `initContainers` method. One thing worth mentioning is that for me, on some versions of clusters (below 1.35), passing an image volume is accepted by the webhooks but the field just disappears from the Deployment spec later. So this approach silently fails in some cases - @morvencao you can confirm whether this is the case by checking if the defined volumes are still in the Deployment spec. This might be provider-specific though.

If the volume looks fine, we could try to confirm what the mounted plugin looks like in the container's filesystem. If you could run:
```sh
kubectl debug -it $KUEUE_MANAGER_POD \
    -n kueue-system  \
    --target=manager \
    --image=cgr.dev/chainguard/busybox:latest \
    -- sh
```
and check what's in `/proc/1/root` and `/proc/1/root/plugins`, then we'd know what was mounted.

### Comment by [@morvencao](https://github.com/morvencao) — 2026-01-23T13:34:40Z

thanks for the quick response — i really appreciate it. @mimowo @kshalot 
1. i’m running Kubernetes v1.35.0
2. when I run the debug command below, I found my plugin is acrually mounted:
```shell
# kubectl debug -it kueue-controller-manager-78fb457788-9pxjt \
    -n kueue-system  \
    --target=manager \
    --image=cgr.dev/chainguard/busybox:latest \
    -- sh
/ $ ls -l ls /proc/1/root/plugins/cp-creds
-rwxr-xr-x    1 root     root      27496632 Jan 23 13:24 /proc/1/root/plugins/cp-creds
```

I later realized the issue wasn’t that the plugin was missing, but that Linux refused to execute it. After checking the build command, I found the plugin binary was dynamically linked. Rebuilding it as a statically linked binary resolved the problem.

The error message was somewhat misleading.

Thanks anyway — I’ll close the issue.
