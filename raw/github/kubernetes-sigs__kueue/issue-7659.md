# Issue #7659: Add Helm Chart values to disable ingress resources for KueueViz

**Summary**: Add Helm Chart values to disable ingress resources for KueueViz

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7659

**Last updated**: 2026-02-05T09:16:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@vladmirtxrx](https://github.com/vladmirtxrx)
- **Created**: 2025-11-14T10:43:31Z
- **Updated**: 2026-02-05T09:16:41Z
- **Closed**: 2026-02-05T09:16:41Z
- **Labels**: `kind/feature`, `priority/important-longterm`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A Helm Chart values to disable Ingress creation. 
Currently, when enabling KueueViz, Ingress manifests for both backend and frontend are installed unconditionally. 

**Why is this needed**:
To use other ingress solutions (e.g. Istio's Gateway and VirtualService API)

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Helm Chart Ingress templates/values update

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-18T11:13:29Z

/area dashboard

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:33:57Z

/priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T19:40:22Z

FYI this is also needed for another user: https://github.com/kubernetes-sigs/kueue/issues/8969#issuecomment-3843169983

@vladmirtxrx are you considering a bugfix PR for this?
