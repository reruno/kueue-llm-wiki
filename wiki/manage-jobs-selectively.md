# Managing Jobs Selectively

**Summary**: Kueue provides two configuration knobs — `manageJobsWithoutQueueName` and `managedJobsNamespaceSelector` — that together let cluster admins precisely control which jobs Kueue manages, scoped to namespaces rather than individual jobs.

**Sources**: `raw/kueue/keps/3589-manage-jobs-selectively/README.md`, `raw/kueue/keps/3589-manage-jobs-selectively/kep.yaml`

**Last updated**: 2026-04-28

---

> **Stage: Stable**. (source: keps/3589-manage-jobs-selectively/kep.yaml)

## The two configuration knobs

### manageJobsWithoutQueueName (boolean, default `false`)

When `false` (default): Kueue only manages jobs that carry the `kueue.x-k8s.io/queue-name` label.

When `true`: Kueue manages **all** jobs, even those without the label — suspending them and holding them until they are assigned a queue and admitted.

### managedJobsNamespaceSelector (LabelSelector, optional)

A namespace label selector that filters where `manageJobsWithoutQueueName` applies. When combined with `manageJobsWithoutQueueName: true`, only jobs in matching namespaces are managed without a label.

(source: keps/3589-manage-jobs-selectively/README.md)

## Behavior matrix

| `manageJobsWithoutQueueName` | `managedJobsNamespaceSelector` | `ManagedJobsNamespaceSelectorAlwaysRespected` gate | Result |
|---|---|---|---|
| `false` | any | any | Only labeled jobs managed, regardless of namespace |
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

## Common pitfall

A job is not managed by Kueue if:
1. It has no `kueue.x-k8s.io/queue-name` label, AND
2. `manageJobsWithoutQueueName` is `false` OR the namespace doesn't match the selector.

The job starts immediately without any quota check. Use `ManagedJobsNamespaceSelectorAlwaysRespected` (and enable the feature gate) to ensure that jobs in non-opted-in namespaces are never managed, even if someone manually labels them.

## Interaction with LocalQueue defaulting

[[local-queue-defaulting]] injects the queue-name label into jobs before the webhook decides whether to manage them. If defaulting is active, `manageJobsWithoutQueueName` becomes less relevant for the namespaces that have a `default` LocalQueue. (source: keps/3589-manage-jobs-selectively/README.md)

## Related pages

- [[local-queue]]
- [[local-queue-defaulting]]
- [[webhooks]]
- [[cluster-queue]]
- [[integrations]]
- [[integration-plain-pod]]
