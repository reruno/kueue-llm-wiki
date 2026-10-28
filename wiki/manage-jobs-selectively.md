# Managing Jobs Selectively

**Summary**: Kueue provides two configuration knobs — `manageJobsWithoutQueueName` and `managedJobsNamespaceSelector` — that together let cluster admins precisely control which jobs Kueue manages, scoped to namespaces rather than individual jobs.

**Sources**: `raw/kueue/keps/3589-manage-jobs-selectively/README.md`, `raw/kueue/keps/3589-manage-jobs-selectively/kep.yaml`, pr-13375.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md, pr-16982.md, pr-17843.md, pr-17869.md, issue-16974.md, raw/kueue/pkg/controller/jobframework/reconciler.go, raw/kueue/pkg/features/kube_features.go, raw/kueue/CHANGELOG/CHANGELOG-0.19.md

**Last updated**: 2026-10-28

---

> **Stage: Stable**. (source: keps/3589-manage-jobs-selectively/kep.yaml)

## The two configuration knobs

### manageJobsWithoutQueueName (boolean, default `false`)

When `false` (default): Kueue only manages jobs that carry the `kueue.x-k8s.io/queue-name` label.

When `true`: Kueue manages **all** jobs, even those without the label — suspending them and holding them until they are assigned a queue and admitted.

### managedJobsNamespaceSelector (LabelSelector, optional)

A namespace label selector that decides which namespaces Kueue manages at all; with `manageJobsWithoutQueueName: true`, unlabeled jobs are also managed only in matching namespaces.

(source: keps/3589-manage-jobs-selectively/README.md)

## Behavior matrix

| `manageJobsWithoutQueueName` | `managedJobsNamespaceSelector` | `ManagedJobsNamespaceSelectorAlwaysRespected` gate | Result |
|---|---|---|---|
| `false` | not set / set | any | Only labeled jobs managed (only in matching namespaces when the selector is set) |
| `true` | not set | any | All jobs managed in all namespaces |
| `true` | set | disabled | All labeled jobs managed everywhere; unlabeled jobs managed only in matching namespaces |
| `true` | set | **enabled** | Jobs in non-matching namespaces not managed at all (even if labeled); jobs in matching namespaces managed per `manageJobsWithoutQueueName` |

(source: keps/3589-manage-jobs-selectively/README.md)

## Common operator patterns

**Pattern 1 — exclude system namespaces**:
```yaml
managedJobsNamespaceSelector:
  matchExpressions:
  - key: kubernetes.io/metadata.name
    operator: NotIn
    values: [kube-system, kueue-system, monitoring]
```

**Pattern 2 — opt-in per namespace**:
```yaml
managedJobsNamespaceSelector:
  matchLabels:
    kueue.x-k8s.io/managed-namespace: "true"
```

Only namespaces explicitly labeled by the admin are subject to quota enforcement. Users cannot bypass quotas by moving workloads to an unlabeled namespace. (source: keps/3589-manage-jobs-selectively/README.md)

## Deprecation: podOptions.namespaceSelector

The old `integrations.podOptions.namespaceSelector` field, which applied only to Pod/Deployment/StatefulSet integrations, is deprecated in favor of the global `managedJobsNamespaceSelector`. It was removed in the `v1beta2` API migration. (source: keps/3589-manage-jobs-selectively/README.md)

## Integration webhooks default-exclude system namespaces (v0.18)

As of v0.18 the integration **webhooks** themselves carry a `namespaceSelector` that excludes `kube-system` and Kueue's install namespace by default, for *all* workload integrations (previously only Pod/Deployment/StatefulSet) — see [[webhooks]] ([[pr-11192]]). For Helm installs the default webhook `namespaceSelector` is derived from `managedJobsNamespaceSelector` when set, otherwise it falls back to a `NotIn [kube-system, .Release.Namespace]` expression. This means the namespace selector now gates both *whether Kueue manages a job* (this page's knobs) and *whether the webhook even fires*.

## kueue-populator inherits `managedJobsNamespaceSelector`

The experimental `kueue-populator` component (`cmd/experimental/kueue-populator/`) used to take its own separate Helm value for the namespace selector. [[pr-11218]] (fixes [[issue-7852]]) makes its Helm chart read Kueue's manager config (`controllerManagerConfigYaml`) and copy `managedJobsNamespaceSelector` into the populator config, so the populator operates on the same namespaces as the controller by default. An explicit `kueuePopulator.config.managedJobsNamespaceSelector` override is still honored to restrict the populator independently.

## Defaulting webhooks respect the selector (v0.20.0)

Before [[pr-13375]], LocalQueue defaulting ignored `managedJobsNamespaceSelector` for every integration except Pod. In an excluded namespace that had a `default` LocalQueue, a Job got `queue-name: default`, was suspended, and then was never reconciled. Since v0.20.0 both defaulting paths check the selector: `ApplyDefaultLocalQueue` (#13375) and `ApplyDefaultWorkloadPriorityClass` (#15851, also v0.18.10). Jobs in excluded namespaces are left unchanged. See [[local-queue-defaulting]] and [[workload-priority#Defaulting respects the namespace selector]] (source: pr-13375.md, raw/kueue/CHANGELOG/CHANGELOG-0.20.md).

## Common pitfall

A job is not managed by Kueue if:
1. It has no `kueue.x-k8s.io/queue-name` label, AND
2. `manageJobsWithoutQueueName` is `false` OR the namespace doesn't match the selector.

The job starts immediately without any quota check. `ManagedJobsNamespaceSelectorAlwaysRespected` makes sure jobs in non-opted-in namespaces are never managed, even if someone labels them by hand. It was Alpha in 0.13 and Beta (on) in 0.15. It is **GA and locked on since v0.19.0** (#13021), so the reconciler always checks the selector (source: raw/kueue/pkg/features/kube_features.go, raw/kueue/CHANGELOG/CHANGELOG-0.19.md). **Correction (2026-10-28)**: this paragraph said the gate has to be enabled.

## The reconciler's Namespace read retries on a cache miss

To apply the selector, `ReconcileGenericJob` reads the job's Namespace from the informer cache. On `NotFound` it used to return without error, so a job seen before its Namespace reached the cache stayed suspended with no Workload until a later event or informer resync. Since [[pr-16982]] the error is returned and the job is requeued with backoff. Releases: `main`, release-0.20 (pr-17843) and release-0.19 (pr-17869). None is in the v0.20.3 / v0.19.10 notes. Details: [[job-framework-interface#A Namespace missing from the cache requeues the job]] (source: pr-16982.md, issue-16974.md, raw/kueue/pkg/controller/jobframework/reconciler.go).

## Interaction with LocalQueue defaulting

[[local-queue-defaulting]] injects the queue-name label into jobs before the webhook decides whether to manage them. If defaulting is active, `manageJobsWithoutQueueName` becomes less relevant for the namespaces that have a `default` LocalQueue. (source: keps/3589-manage-jobs-selectively/README.md)

## Related pages

- [[local-queue]]
- [[local-queue-defaulting]]
- [[webhooks]]
- [[cluster-queue]]
- [[integrations]]
- [[integration-plain-pod]]
