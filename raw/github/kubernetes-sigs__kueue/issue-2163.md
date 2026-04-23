# Issue #2163: Workload controller and JobReconciler thrash attempting to update a Workload

**Summary**: Workload controller and JobReconciler thrash attempting to update a Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2163

**Last updated**: 2024-05-10T01:10:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-05-08T15:18:30Z
- **Updated**: 2024-05-10T01:10:22Z
- **Closed**: 2024-05-10T01:09:39Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
We are running an instance of Kueue's JobReconciler in an external controller (to support AppWrappers).  In one of our 
test scenarios, we reliably see the JobReconciler running in the external controller and the Workload controller running in the
Kueue operator get into an endless reconciliation loop trying to update, delete, and recreate the Workload instance for a submitted AppWrapper.   The controllers get stuck in this state indefinitely with no progress being made by either controller (our test times out after 2 minutes).   I've attached 1 second of the logs from each of the two controllers, as you can see they are both stuck in rapid retry loops.

[kueue-1second-log.txt](https://github.com/kubernetes-sigs/kueue/files/15250877/kueue-1second-log.txt)
[codeflare-1second-log.txt](https://github.com/kubernetes-sigs/kueue/files/15250883/codeflare-1second-log.txt)

I am using the latest code on the 0.6-release branch (0a69bb718) for the Kueue controller and the 0.6.2 release of Kueue in the AppWrapper controller.

**What you expected to happen**:

We expect to see some reconciliation errors since there are two controllers running in separate processes modifying the object, but the reconciliation loops should properly handle the Workload object being changed by an external controller and backoff/retry so the system overall makes eventual progress.  

**How to reproduce it (as minimally and precisely as possible)**:

Unfortunately, reproduction requires running Kueue and the CodeFlare operator (which embeds the AppWrapper controller) along with the CodeFlare e2e test suite.  I'm mainly looking for suggestions of fixes to try locally or pointers to potential fixes in Kueue's main that aren't backported to the 0.6 branch.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): Server Version: version.Info{Major:"1", Minor:"25", GitVersion:"v1.25.3", GitCommit:"434bfd82814af038ad94d62ebe59b133fcb50506", GitTreeState:"clean", BuildDate:"2022-10-25T19:38:29Z", GoVersion:"go1.19.2", Compiler:"gc", Platform:"linux/arm64"}
- Kueue version (use `git describe --tags --dirty --always`): v0.6.2-12-g0a69bb71
- Cloud provider or hardware configuration: kind v0.22.0 go1.21.7 darwin/arm64 
- OS (e.g: `cat /etc/os-release`): macOS Sonoma
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-05-08T19:11:39Z

I verified that the bug is still present using Kueue main at 3c9810a2 (building both Kueue and the external AppWrapper controller using that commit hash).

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-05-10T01:09:39Z

The behavior is caused because the PodSpecTemplate returned by the AppWrapper inside the PodSet returned from `Job.PodSets()` was created via standard Go json deserialization from a slice of an Unstructured map[string]interface{}. Because it didn't go through the apimachinery serialization, default values from the Go struct tags were not being properly filled in.  In particular, the Job had ContainerPorts where the Job's PodSpecTemplate lacked the default `TCP` protocol while the Workload object had `TCP` filled in.

I'm going to close this as not really a bug in Kueue, but thought it was worth documenting the finding.   We can fix on the AppWrapper side by adjusting how we construct the PodSets from the Template.Raw that defines them
