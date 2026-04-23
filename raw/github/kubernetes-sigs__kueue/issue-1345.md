# Issue #1345: Failed to perform "go list -modfile=./go.mod -m all"

**Summary**: Failed to perform "go list -modfile=./go.mod -m all"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1345

**Last updated**: 2024-03-25T20:57:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-11-20T03:00:29Z
- **Updated**: 2024-03-25T20:57:58Z
- **Closed**: 2024-03-25T20:57:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
I could not perform `go list -modfile=./go.mod -m all` to get all dependencies list, and I faced the following errors:

```shell
$ go list -modfile=./go.mod -m all
go: k8s.io/dynamic-resource-allocation@v0.0.0: invalid version: unknown revision v0.0.0
go: k8s.io/kube-scheduler@v0.0.0: invalid version: unknown revision v0.0.0
go: k8s.io/kubectl@v0.0.0: invalid version: unknown revision v0.0.0
go: k8s.io/legacy-cloud-providers@v0.0.0: invalid version: unknown revision v0.0.0
```

**What you expected to happen**:
The command is successful.

**How to reproduce it (as minimally and precisely as possible)**:
We can reproduce with `go list -modfile=./go.mod -m all` on our local.

**Anything else we need to know?**:
I guess that the error was caused by cluster-autoscaler dependencies. Actually, once I remove the cluster-autoscaler dependencies from our `go.mod`, and then the above error went away.

Also, I found that we can avoid the above error once I specify the module versions in the following:

```diff
go 1.21

require (
...
	sigs.k8s.io/structured-merge-diff/v4 v4.4.1
)

+replace (
+	k8s.io/dynamic-resource-allocation => k8s.io/dynamic-resource-allocation v0.28.3
+	k8s.io/kube-scheduler => k8s.io/kube-scheduler v0.28.3
+	k8s.io/kubectl => k8s.io/kubectl v0.28.3
+	k8s.io/legacy-cloud-providers => k8s.io/legacy-cloud-providers v0.28.3
+)
...
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-20T03:18:09Z

If you use Goland (JetBrains), you could face this error, and your local gopls and definition jumpings will stop working since Goland automatically runs the following commands every time:

```shell
go list -modfile=${GOPATH}/src/sigs.k8s.io/kueue/go.mod -m -json -mod=mod all`
```

I tried to avoid the above error, and then I couldn't find any way to resolve the issue completely.

However, I found that we can temporarily avoid the above error by disabling Goland's Go Module Integrations.
I left the way:

1. Select "Disable for current project, enable for other projects" in "Settings > Go > GO Modules > Download Go module dependencies"
2. Select External changes in "Settings > Build, Execution, Deployment > Build Tools > Reload project after changes in the build scripts"
3. Disable the following items in "Settings > Editor > Inspections > Go modules > General":
    1. dependency update available
    2. Deprecated dependency
    3. Retracted dependency version

Also, you needs to add the following dependencies to the go.mod, 

```
replace (
	k8s.io/dynamic-resource-allocation => k8s.io/dynamic-resource-allocation v0.28.3
	k8s.io/kube-scheduler => k8s.io/kube-scheduler v0.28.3
	k8s.io/kubectl => k8s.io/kubectl v0.28.3
	k8s.io/legacy-cloud-providers => k8s.io/legacy-cloud-providers v0.28.3
)
```

and then run `go list -modfile=${GOPATH}/src/sigs.k8s.io/kueue/go.mod -m -json -mod=mod all` to gather indexes for modules, then remove the added modules in the above.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-20T03:22:16Z

I'm on the fence about whether or not we should have kubernetes dependency versions in our go modules only for "go list".
@alculquicondor @trasc @kerthcet @mimowo WDYT?

> ```
> ...
> replace (
> 	k8s.io/dynamic-resource-allocation => k8s.io/dynamic-resource-allocation v0.28.3
> 	k8s.io/kube-scheduler => k8s.io/kube-scheduler v0.28.3
> 	k8s.io/kubectl => k8s.io/kubectl v0.28.3
> 	k8s.io/legacy-cloud-providers => k8s.io/legacy-cloud-providers v0.28.3
> )
> ```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-20T14:04:58Z

The dependency is coming from cluster-autoscaler, which imports k/k to reuse the scheduler logic.

I think the best solution is for cluster-autoscaler to put their APIs in a separate go module.
cc @x13n @kisieland

I thought maybe we could put the provisioning-request controller in a separate go module, but that would lead to the same dependency tree.

### Comment by [@x13n](https://github.com/x13n) — 2023-11-20T15:59:05Z

Yeah, if CA APIs are imported in other components, it makes sense to extract them to a separate module with trimmed-down dependencies. We'd still keep CA & API modules versioning in sync, but it would address the dependency problem.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-20T16:01:10Z

@tenzen-y is this something you could work on in k/autoscaling?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-21T03:50:25Z

> @tenzen-y is this something you could work on in k/autoscaling?

@alculquicondor Yes, I can.

> it makes sense to extract them to a separate module with trimmed-down dependencies

@x13n That makes sense.

### Comment by [@B1F030](https://github.com/B1F030) — 2023-11-21T08:45:58Z

I'm facing the same problem in GoLand too.
Hope this could be fixed soon.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-21T09:22:15Z

> I'm facing the same problem in GoLand too. Hope this could be fixed soon.

@B1F030  I'm starting now: https://github.com/kubernetes/autoscaler/issues/6307
You can temporary avoid this issue by this workaround: https://github.com/kubernetes-sigs/kueue/issues/1345#issuecomment-1818164133

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-21T20:33:24Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-19T21:23:13Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-20T04:04:54Z

/remove-lifecycle stale
