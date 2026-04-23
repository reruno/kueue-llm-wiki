# Issue #1601: Utilize and expose functions for starting up the manager

**Summary**: Utilize and expose functions for starting up the manager

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1601

**Last updated**: 2026-01-31T09:19:43Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-01-17T17:31:33Z
- **Updated**: 2026-01-31T09:19:43Z
- **Closed**: 2026-01-31T09:19:42Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 28

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I would like to utilize and expose the below functions for starting up the manager:
We can probably cut an `initialize` package under the `pkg` directory, and then we can put the below functions there.

https://github.com/kubernetes-sigs/kueue/blob/60177bf1ace328629bafae6ac3dcbe9ff5568aac/cmd/kueue/main.go#L194

https://github.com/kubernetes-sigs/kueue/blob/60177bf1ace328629bafae6ac3dcbe9ff5568aac/cmd/kueue/main.go#L221

https://github.com/kubernetes-sigs/kueue/blob/60177bf1ace328629bafae6ac3dcbe9ff5568aac/cmd/kueue/main.go#L317

https://github.com/kubernetes-sigs/kueue/blob/60177bf1ace328629bafae6ac3dcbe9ff5568aac/cmd/kueue/main.go#L343

https://github.com/kubernetes-sigs/kueue/blob/60177bf1ace328629bafae6ac3dcbe9ff5568aac/cmd/kueue/main.go#L365

https://github.com/kubernetes-sigs/kueue/blob/60177bf1ace328629bafae6ac3dcbe9ff5568aac/cmd/kueue/main.go#L369

https://github.com/kubernetes-sigs/kueue/blob/60177bf1ace328629bafae6ac3dcbe9ff5568aac/cmd/kueue/main.go#L373

https://github.com/kubernetes-sigs/kueue/blob/60177bf1ace328629bafae6ac3dcbe9ff5568aac/cmd/kueue/main.go#L403

**Why is this needed**:

When the platform developers implement the managers for the in-house custom jobs, they can avoid copying and pasting those functions to their manager.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-17T17:31:41Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-17T18:14:58Z

Some of them don't seem to be necessary for a custom integration, unless you are essentially forking kueue?

My general recommendation would be run the custom integration in a separate binary that can be released independently, similar to https://github.com/kubernetes-sigs/kueue/blob/main/cmd/experimental/podtaintstolerations/main.go

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-17T18:24:09Z

> My general recommendation would be run the custom integration in a separate binary that can be released independently, similar to https://github.com/kubernetes-sigs/kueue/blob/main/cmd/experimental/podtaintstolerations/main.go

Yes, I meant a separate binary. Currently, separate main function can not import functions like `setupProbeEndpoints` since those functions aren't exported.

It means that the platform developer implements the main function like the following:
I would like to avoid copying these similar functions. @alculquicondor Does this make sense?

```golang
func main() {
...
	ctx := ctrl.SetupSignalHandler()
	setupIndexes(ctx, mgr)
	setupProbeEndpoints(mgr)
	go setupControllers(mgr, certsReady, &cfg)

	setupLog.Info("starting manager")
	if err := mgr.Start(ctx); err != nil {
		setupLog.Error(err, "could not run manager")
		os.Exit(1)
	}

func setupIndexes(ctx context.Context, mgr ctrl.Manager) {
	err := jobframework.ForEachIntegration(func(name string, cb jobframework.IntegrationCallbacks) error {
		if err := cb.SetupIndexes(ctx, mgr.GetFieldIndexer()); err != nil {
			return fmt.Errorf("integration %s: %w", name, err)
		}
		return nil
	})
	if err != nil {
		setupLog.Error(err, "unable to setup jobs indexes")
	}
}

func setupProbeEndpoints(mgr ctrl.Manager) {
	defer setupLog.Info("probe endpoints are configured on healthz and readyz")

	if err := mgr.AddHealthzCheck("healthz", healthz.Ping); err != nil {
		setupLog.Error(err, "unable to set up health check")
		os.Exit(1)
	}
	if err := mgr.AddReadyzCheck("readyz", healthz.Ping); err != nil {
		setupLog.Error(err, "unable to set up ready check")
		os.Exit(1)
	}
}

func setupControllers(mgr ctrl.Manager, certsReady chan struct{}, cfg *configapi.Configuration) {
...
	opts := []jobframework.Option{
		jobframework.WithManageJobsWithoutQueueName(cfg.ManageJobsWithoutQueueName),
		jobframework.WithWaitForPodsReady(waitForPodsReady(cfg)),
	}
	err := jobframework.ForEachIntegration(func(name string, cb jobframework.IntegrationCallbacks) error {
		log := setupLog.WithValues("jobFrameworkName", name)
		if err := cb.NewReconciler(
			mgr.GetClient(),
			mgr.GetEventRecorderFor(fmt.Sprintf("%s-%s-controller", name, constants.ManagerName)),
			opts...,
...
	if err != nil {
		os.Exit(1)
	}
	// +kubebuilder:scaffold:builder
}

func waitForPodsReady(cfg *configapi.Configuration) bool {
	return cfg.WaitForPodsReady != nil && cfg.WaitForPodsReady.Enable
}
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-17T18:41:45Z

oh I see. So you have a single binary to add multiple integrations. Then it might make sense to export things like `SetupIndexes` and `SetupControllers`.

But I don't think you should be using Kueue's Configuration API. You should probably have your own.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-17T18:51:30Z

> oh I see. So you have a single binary to add multiple integrations. Then it might make sense to export things like SetupIndexes and SetupControllers.

Yes, I will expose the only needed functions.

> But I don't think you should be using Kueue's Configuration API. You should probably have your own.

In my env, I deployed another ConfigMap embedded [Kueue Config](https://github.com/kubernetes-sigs/kueue/blob/d21995757b9307aaa4cf8c8caad60dd8a3557fda/config/components/manager/controller_manager_config.yaml#L1-L2) to cluster and then the another Kueue Config is mounted on the inhouse kueue manager.

It means that I have 2 configMaps embedded kueue config.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-17T18:59:31Z

I think we shouldn't make the same assumption in the exported functions. The functions could take some specific fields.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-17T19:18:02Z

> I think we shouldn't make the same assumption in the exported functions. The functions could take some specific fields.

Maybe, I couldn't understand correctly what you want to mean.

> But I don't think you should be using Kueue's Configuration API. You should probably have your own.

Does this mean that you suggested not mounting another Kueue's Configuration on the in-house Kueue manager?
Or you meant that we shouldn't expose functions with Kueue's Configuration as args?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-17T19:19:47Z

I think we should export something like `SetupControllers(mgr ctrl.Manager, certsReady chan struct{}, opts... jobframework.Options)`, without making assumptions about how your configuration API looks like.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-17T19:21:20Z

> I think we should export something like `SetupControllers(mgr ctrl.Manager, certsReady chan struct{}, opts... jobframework.Options)`, without making assumptions about how your configuration API looks like.

Ah, it makes sense. Thank you for the clarifications!

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-07T14:05:03Z

@tenzen-y I see https://github.com/kubernetes-sigs/kueue/pull/1630 merged. Is there more to do, or we can close?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-07T14:07:44Z

> @tenzen-y I see #1630 merged. Is there more to do, or we can close?

I'm still working on this, but I'm not sure if we can finalize this by the deadline for v0.6.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-07T15:45:27Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-07T15:46:29Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-05T16:34:58Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-05T16:36:54Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-03T17:28:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T06:22:21Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-02T06:41:04Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-02-02T08:24:10Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-03T08:54:50Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T06:26:47Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-04T07:02:36Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-03T07:04:35Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-03T07:46:21Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-02T07:53:26Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-01T08:35:11Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-31T09:19:37Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-31T09:19:43Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1601#issuecomment-3827977943):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
