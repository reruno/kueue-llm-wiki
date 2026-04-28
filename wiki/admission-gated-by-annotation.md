# Admission Gated By Annotation

**Summary**: The `kueue.x-k8s.io/admission-gated-by` annotation lets external controllers delay Kueue's admission of a job until the controller has finished preparing it, without requiring a webhook or blocking job creation.

**Sources**: `raw/kueue/keps/6915-scheduling-gated-by-annotation/README.md`, `raw/kueue/keps/6915-scheduling-gated-by-annotation/kep.yaml`

**Last updated**: 2026-04-28

---

> **Stage: Alpha** — Feature gate `AdmissionGatedBy`, disabled by default. (source: keps/6915-scheduling-gated-by-annotation/kep.yaml)

## Problem

Once Kueue observes a managed job, it immediately creates a [[workload]] and starts admission. An external controller that needs to patch the job first (e.g., adjust resource requests based on a prediction model) has a race condition: Kueue may admit the job before the patch is applied. (source: keps/6915-scheduling-gated-by-annotation/README.md)

## Solution

Annotate the job at creation time with the names of controllers that must clear their gate before admission proceeds:

```yaml
metadata:
  annotations:
    kueue.x-k8s.io/admission-gated-by: "example.com/predictor,example.com/resource-optimizer"
```

- **While the annotation is present**: Kueue creates the Workload but does not admit it. The Workload's `QuotaReserved` condition is `False` with reason `AdmissionGated`.
- **When the annotation is removed** (or a controller name is removed from the list): Kueue re-evaluates and admits normally.

(source: keps/6915-scheduling-gated-by-annotation/README.md)

## Annotation format

A comma-separated list of controller names. Each name must be in the form `<subdomain>/<label>` (RFC 1123 subdomain, RFC 3986 path), e.g. `example.com/mygate`. (source: keps/6915-scheduling-gated-by-annotation/README.md)

## Constraints

- The annotation can only be set **at job creation time**. Adding it after creation is rejected by the validation webhook.
- After creation, the annotation can only be **reduced** (controllers removed) or **fully removed**. It cannot be added to or have new controllers appended.
- Applies to all Kueue-managed job types (batch/v1 Job, JobSet, etc.).

(source: keps/6915-scheduling-gated-by-annotation/README.md)

## Observability

Kueue emits events on the Workload:
- `AdmissionGated` — when the workload is created with a non-empty `admission-gated-by` annotation.
- `AdmissionGateCleared` — when the annotation is removed and the workload proceeds to admission.

(source: keps/6915-scheduling-gated-by-annotation/README.md)

## Use case: resource prediction controller

```
1. ML researcher creates a job without resource requests + kueue.x-k8s.io/admission-gated-by: "example.com/predictor"
2. The prediction controller picks up the job, runs the model (~1s), patches resource requests.
3. The prediction controller removes "example.com/predictor" from the annotation.
4. Kueue admits the workload with the correct resource requests.
```

(source: keps/6915-scheduling-gated-by-annotation/README.md)

## How it propagates

The job reconciler copies the `kueue.x-k8s.io/admission-gated-by` annotation from the job to the corresponding Workload. The Workload's `IsAdmissible()` check returns `false` while the annotation is present. (source: keps/6915-scheduling-gated-by-annotation/README.md)

## Related pages

- [[workload]]
- [[admission]]
- [[admission-check]]
- [[webhooks]]
- [[feature-gates]]
