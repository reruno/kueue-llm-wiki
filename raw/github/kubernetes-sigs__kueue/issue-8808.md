# Issue #8808: Documentation gap: clearly document mutable fields per Kueue integration

**Summary**: Documentation gap: clearly document mutable fields per Kueue integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8808

**Last updated**: 2026-01-30T21:53:36Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2026-01-27T06:00:14Z
- **Updated**: 2026-01-30T21:53:36Z
- **Closed**: —
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 4

## Description

### Summary

Kueue documentation provides a very helpful set of task-oriented pages under:

[https://kueue.sigs.k8s.io/docs/tasks/run/](https://kueue.sigs.k8s.io/docs/tasks/run/)

These pages do a great job explaining **how to run** various workload types with Kueue. However, they do not clearly document **which fields are mutable vs immutable** for each supported integration object.

Given that mutability rules can vary across integrations, this makes it harder for users to reason about safe updates, especially post-creation or pre-admission.

### Problem statement

For each Kueue-supported integration (for example: Job, JobSet, LeaderWorkerSet, MPIJob, RayJob, etc.), there are implicit rules around:

* which fields are immutable after Workload creation,
* which fields may be mutated before admission,
* which fields may be mutated after admission, if any,
* and what the observable behavior is when a mutation is rejected or partially applied.

Today, users must infer these rules from:

* controller behavior,
* webhook validation errors,
* or by reading controller source code.

This creates room for confusion and inconsistent mental models, especially when different integrations behave differently.

### Proposal

Extend the documentation for each integration under `docs/tasks/run/` to explicitly list **mutable vs immutable properties**.

For example, for each integration page, add a small section such as:

#### Mutability contract

* **Immutable after creation**

  * `<field A>`
  * `<field B>`

* **Mutable before admission only**

  * `<field C>`

* **Mutable after admission**

  * `<field D>` (if applicable)

* **Notes**

  * Any special cases, caveats, or non-obvious behavior.

This does not need to be exhaustive at the field level initially, even documenting the *high-level expectations* would significantly improve clarity.

### Motivation

* Improves user experience and reduces surprises.
* Helps users design controllers and workflows that interact safely with Kueue-managed workloads.
* Makes behavioral differences between integrations explicit rather than implicit.
* Reduces the need to reverse-engineer behavior from source code.

#### Open questions

* Is there an agreed-upon mutability contract pattern across integrations today?
* Should this be standardized across all integrations, or documented on a per-integration basis?
* Would it make sense to codify these rules in a common section and reference them from each integration page?

I believe documenting this explicitly would be a valuable addition to the Kueue documentation and help set clearer expectations for users.

#### Related
* #8807

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-27T16:49:20Z

IMO I think this is by design.

Workload controllers decide what fields are mutable. Whatever we put in Kueue may be difficult to keep up with as mutability is being greatly relaxed across many controllers now.

For example, Job used to allow allow changing scheduling directives while it was suspended.

But then ElasticIndexedJob came about and folks were allowed to mutate completions/parallelism.

I introduced a KEP to allow for Job users to patch resources on suspended jobs.

Mutability also changes quite a bit for serving workloads like deployment/lws/statefulset as changing some of these fields could end up recration/redeploy of a new resource.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-27T16:51:01Z

It would be good to document what fields Kueue needs to modify as I think that has tripped us up a few times.

cc @tenzen-y @andreyvelich @astefanutti @mimowo

### Comment by [@astefanutti](https://github.com/astefanutti) — 2026-01-29T08:59:26Z

I agree this a gap in the documentation though I also agree with @kannon92 this is specific to each controller and the documentation for each of those controller may be more easily maintained in the respective projects.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-30T21:53:35Z

> Workload controllers decide which fields are mutable. Anything we encode in Kueue risks lagging behind upstream behavior, especially as mutability is being relaxed across many controllers.

This is the key concern. The Job API is user-facing, and in a standalone context there are existing, typically well-documented expectations about which fields are mutable and what semantic effects such mutations have.

> For example, Job used to allow changing scheduling directives while it was suspended.

I probably should clarify that my concerns about mutability applicable explicitly to not suspended (i.e. live/running) Jobs.
v1batch/Job is very good example, and one I ran into firsthand. It was surprising to observe workload termination behavior in response to changing `spec.parallelism`, a mutable field in the Job spec (on started jobs). It required code-level inspection to understand that while `spec.parallelism` is technically mutable, its handling and side effects differ significantly from what users expect in a standalone Job.

Arguably, a better approach would be one of the following:
A. Explicitly disallow `parallelism` mutation via a webhook, making the handling intentional and explicit.
B. Clearly document which fields are mutable and the consequences of mutating them.
C. Both A and B.

Today, Kueue documentation already provides a well-structured, user-facing place to capture this. The “Run workloads” section of the Kueue docs offers a clear and authoritative surface where immutability or mutability constraints, along with their handling and consequences, could be explicitly documented and kept up to date.
