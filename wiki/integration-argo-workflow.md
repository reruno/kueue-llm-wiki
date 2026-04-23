# Integration: Argo Workflows

**Summary**: Argo Workflows runs multi-step DAGs where each step is a Pod. The Kueue integration gates the workflow at the Pod level, using Pod scheduling gates rather than `.spec.suspend` (Argo Workflows doesn't have a native suspend-the-whole-workflow semantics that matches Kueue's model).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Why Pod-level gating

A Workflow is not one object Kueue can toggle. Each step's Pod is what actually consumes quota; gating happens per Pod. Kueue attaches a scheduling gate to each step's Pod and removes it once a Workload has been admitted for that step.

This makes Argo Workflow integration a close relative of the [[integration-plain-pod]] path — both use scheduling gates.

## Quota per-step vs per-workflow

A design choice: the integration handles quota at the step (Pod) level. Each step becomes its own Workload. This is simpler but means fair-share at the workflow level isn't built in — if a workflow has 100 steps, they queue independently.

## Adoption

Argo Workflow support was added to Kueue's integration list more recently than JobSet / batch Job; representative tracking issues focus on consistent inclusion in documentation and MultiKueue support.

## Related pages

- [[integration-plain-pod]] — same scheduling-gate mechanism.
- [[integrations]] — integration mechanics.
- [[workload]] — one Workload per step.
