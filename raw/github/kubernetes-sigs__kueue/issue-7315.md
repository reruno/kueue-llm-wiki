# Issue #7315: Align the Kueue KEP template with the K8s KEP template

**Summary**: Align the Kueue KEP template with the K8s KEP template

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7315

**Last updated**: 2026-02-16T18:28:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kshalot](https://github.com/kshalot)
- **Created**: 2025-10-17T16:07:31Z
- **Updated**: 2026-02-16T18:28:02Z
- **Closed**: 2026-02-16T18:28:02Z
- **Labels**: `lifecycle/rotten`, `kind/documentation`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 4

## Description

**Type:**
/kind documentation

**Description:**
The [Kueue KEP template](https://github.com/kubernetes-sigs/kueue/tree/main/keps/NNNN-template) is misaligned with the [Kubernetes KEP template](https://github.com/kubernetes/enhancements/tree/master/keps/NNNN-kep-template). For consistency, we should re-sync **the relevant sections** of the template so it's a subset of the K8s one.

See discussion under #7313 for more context.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T16:13:53Z

The diff: https://www.diffchecker.com/ycYduSlF/

Here is the summary for the ToC differences:

<img width="2233" height="907" alt="Image" src="https://github.com/user-attachments/assets/16d8f767-436e-4b96-b56f-f8496e0ae301" />

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-15T16:26:46Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-14T16:41:06Z

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

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-16T09:47:48Z

/assign

I'll see what needs to be added, it's a quick one.
