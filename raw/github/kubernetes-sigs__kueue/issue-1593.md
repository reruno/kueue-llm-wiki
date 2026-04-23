# Issue #1593: Flaky E2E test for Pod replacement

**Summary**: Flaky E2E test for Pod replacement

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1593

**Last updated**: 2024-01-23T17:29:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-16T21:32:35Z
- **Updated**: 2024-01-23T17:29:05Z
- **Closed**: 2024-01-23T17:29:05Z
- **Labels**: `kind/bug`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 9

## Description

**What happened**:

Sometimes the Workload is never declared as Finished.

```
End To End Suite: kindest/node:v1.29.0: [It] Pod groups when Single CQ Failed Pod can be replaced in group expand_less	50s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:300 with:
it's finished failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:300 with:
it's finished
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:224 @ 01/16/24 20:19:48.709
}
```

Looking at the kube-scheduler logs, the Pod called `excess` got scheduled, which shouldn't have happened. This either means that some other Pod failed or was identified as an excess by Kueue.

**What you expected to happen**:

The workload to finish successfully

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1592/pull-kueue-test-e2e-main-1-29/1747351345448357888

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-16T21:33:00Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-17T05:53:32Z

This occurred here, again: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1542/pull-kueue-test-e2e-main-1-28/1747378071394062336

### Comment by [@B1F030](https://github.com/B1F030) — 2024-01-17T11:00:00Z

There are some similar flaky tests: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1385/pull-kueue-test-e2e-main-1-29/1747566443098017792

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-17T18:44:42Z

That last one doesn't seem related. It looks like there was a failure to delete a ResourceFlavor during cleanup.

Please file a separate bug if you can confirm that this is not related to your PR.

As for @tenzen-y's report, it didn't include log level 3 yet :(

I'll keep trying to repro.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-17T19:25:17Z

> That last one doesn't seem related. It looks like there was a failure to delete a ResourceFlavor during cleanup.
> 
> Please file a separate bug if you can confirm that this is not related to your PR.
> 
> As for @tenzen-y's report, it didn't include log level 3 yet :(
> 
> I'll keep trying to repro.

@B1F030

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-18T22:54:13Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-18T22:54:18Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1593#issuecomment-1899347762):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@B1F030](https://github.com/B1F030) — 2024-01-19T03:36:21Z

> > That last one doesn't seem related. It looks like there was a failure to delete a ResourceFlavor during cleanup.
> > Please file a separate bug if you can confirm that this is not related to your PR.
> > As for @tenzen-y's report, it didn't include log level 3 yet :(
> > I'll keep trying to repro.
> 
> @B1F030

Sorry, I'm not sure if this is related to my PR.
But that didn't happen again ever since the e2e test fixed, so I think [that](https://github.com/kubernetes-sigs/kueue/issues/1593#issuecomment-1895575380) is fixed too.
If I meet a flaky test again, I will open another issue.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-19T06:39:54Z

> > > That last one doesn't seem related. It looks like there was a failure to delete a ResourceFlavor during cleanup.
> > > Please file a separate bug if you can confirm that this is not related to your PR.
> > > As for @tenzen-y's report, it didn't include log level 3 yet :(
> > > I'll keep trying to repro.
> > 
> > 
> > @B1F030
> 
> But that didn't happen again ever since the e2e test fixed

This E2E issue isn't resolved, yet.
