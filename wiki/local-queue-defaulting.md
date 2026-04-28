# LocalQueue Defaulting

**Summary**: When the `LocalQueueDefaulting` feature gate is enabled, Kueue automatically injects the `kueue.x-k8s.io/queue-name: default` label onto jobs that lack a queue-name label, as long as a LocalQueue named `default` exists in the same namespace.

**Sources**: `raw/kueue/keps/2936-local-queue-defaulting/README.md`, `raw/kueue/keps/2936-local-queue-defaulting/kep.yaml`

**Last updated**: 2026-04-28

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

## Related pages

- [[local-queue]]
- [[cluster-queue]]
- [[webhooks]]
- [[manage-jobs-selectively]]
- [[integrations]]
