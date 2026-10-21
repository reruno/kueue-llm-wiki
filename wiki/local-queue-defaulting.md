# LocalQueue Defaulting

**Summary**: When the `LocalQueueDefaulting` feature gate is enabled, Kueue automatically injects the `kueue.x-k8s.io/queue-name: default` label onto jobs that lack a queue-name label, as long as a LocalQueue named `default` exists in the same namespace.

**Sources**: `raw/kueue/keps/2936-local-queue-defaulting/README.md`, `raw/kueue/keps/2936-local-queue-defaulting/kep.yaml`, pr-13375.md, raw/kueue/pkg/controller/jobframework/defaults.go

**Last updated**: 2026-10-21

---

> **Stage: Stable** — Feature gate `LocalQueueDefaulting`, GA in v0.17. (source: keps/2936-local-queue-defaulting/kep.yaml)

## Purpose

Without LocalQueue defaulting, users must explicitly label every job with `kueue.x-k8s.io/queue-name`. This requirement surprises new users and complicates onboarding. LocalQueue defaulting removes the burden for namespaces where a single queue is appropriate for all users. (source: keps/2936-local-queue-defaulting/README.md)

## How it works

1. The cluster admin creates a [[local-queue]] named `default` in each namespace that should benefit from defaulting.
2. The feature gate `LocalQueueDefaulting` is enabled.
3. Kueue's mutating webhook checks every new job: if the job lacks `kueue.x-k8s.io/queue-name` and a `default` LocalQueue exists in the job's namespace, the webhook injects `kueue.x-k8s.io/queue-name: default`.

The `default` LocalQueue must be created manually by the admin — Kueue does not create it automatically. (source: keps/2936-local-queue-defaulting/README.md)

## Interaction with manageJobsWithoutQueueName

`manageJobsWithoutQueueName` and `LocalQueueDefaulting` should not be used together. When LocalQueueDefaulting is active, Kueue adds the queue-name label before the webhook decides whether to manage the job — so `manageJobsWithoutQueueName` is redundant and may produce unexpected behavior. (source: keps/2936-local-queue-defaulting/README.md)

## Interaction with manage-jobs-selectively

[[manage-jobs-selectively]] (`managedJobsNamespaceSelector`) restricts which namespaces are subject to Kueue management. LocalQueueDefaulting works within whatever namespace scope is already filtered by the selector — it only injects the label; it does not override the namespace selector. (source: keps/2936-local-queue-defaulting/README.md)

## Common setup pattern

1. Label user namespaces with a selector (for `managedJobsNamespaceSelector`).
2. Create a `default` LocalQueue in each labeled namespace pointing to the appropriate [[cluster-queue]].
3. Enable `LocalQueueDefaulting`.

Users can submit jobs without any Kueue-specific labels and they will be automatically queued.

## Namespace selector is now consistently respected

`ManagedJobsNamespaceSelectorAlwaysRespected` (GA since 0.19) applies to both defaulting paths. `ApplyDefaultLocalQueue` was fixed first ([[pr-13375]], v0.20.0). Before that fix, the Job and `BaseWebhook` defaulters injected `queue-name: default` even in namespaces **excluded** by `managedJobsNamespaceSelector`; only the Pod webhook checked first. The labelled Job was then suspended, but the reconciler ignores excluded namespaces, so the Job hung suspended. The selector check now runs inside `ApplyDefaultLocalQueue`, after the cheap checks (a `default` LocalQueue exists, no queue name, owner not Kueue-managed). A Namespace read error is returned from the webhook (source: pr-13375.md, raw/kueue/pkg/controller/jobframework/defaults.go). **Correction (2026-10-21)**: the "Interaction with manage-jobs-selectively" section above described the intended behaviour; on releases before v0.20.0 defaulting did *not* respect the selector. The WorkloadPriorityClass defaulting path followed later, returning Namespace read errors from the webhook the same way; see [[workload-priority#Defaulting respects the namespace selector]] (source: pr-15851.md).

## Related pages

- [[local-queue]]
- [[cluster-queue]]
- [[webhooks]]
- [[manage-jobs-selectively]]
- [[integrations]]
