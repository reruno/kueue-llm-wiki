# Issue #9051: ArgoCD fails to sync clusters with Kueue due to broken OpenAPI schema reference in visibility API

**Summary**: ArgoCD fails to sync clusters with Kueue due to broken OpenAPI schema reference in visibility API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9051

**Last updated**: 2026-02-09T06:43:35Z

---

## Metadata

- **State**: open
- **Author**: [@mpsanj](https://github.com/mpsanj)
- **Created**: 2026-02-09T06:39:01Z
- **Updated**: 2026-02-09T06:43:35Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

Hi Team,

Problem

  ArgoCD fails to load cluster state when Kueue is installed due to a broken OpenAPI schema reference in the visibility API
  (v1beta1.PendingWorkloadsSummary).

  Error Message

  Failed to load target state: failed to get cluster version for cluster "https://x.x.x.x":
  failed to get cluster info for "https://x.x.x.x": error synchronizing cache state:
  failed to load open api schema while syncing cluster cache: error getting openapi resources:
  SchemaError(sigs.k8s.io/kueue/apis/visibility/v1beta1.PendingWorkloadsSummary.items):
  unknown model in reference: "sigs.k8s.io~1kueue~1apis~1visibility~1v1beta1.PendingWorkload"

  Root Cause

  The PendingWorkloadsSummary CRD has an items field that references PendingWorkload, but the schema reference is malformed or missing from the
  OpenAPI spec. ArgoCD's schema parser fails to resolve this reference during cluster cache synchronization.

  Impact

  - ArgoCD cannot sync any applications to clusters with Kueue installed
  - Users must disable OpenAPI schema loading entirely (ARGOCD_CLUSTER_CACHE_LOAD_OPEN_API_SCHEMA=false) as a workaround
  - This workaround affects all CRDs, not just Kueue

  Environment

  - Kueue version: v0.16.0
  - Kubernetes version: 1.33.5

  Current Workaround

  Disable OpenAPI schema loading in ArgoCD:

  kubectl set env deployment/argocd-application-controller \
    -n argocd \
    ARGOCD_CLUSTER_CACHE_LOAD_OPEN_API_SCHEMA=false

  Expected Behavior

  Kueue's CRDs should have valid OpenAPI schema references that can be parsed by standard Kubernetes tooling.

  Suggested Fix

  Review and fix the OpenAPI schema definition for visibility.kueue.x-k8s.io/v1beta1 resources, specifically:
  - PendingWorkloadsSummary
  - PendingWorkload


Thank You !

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T06:43:08Z

Hi!

I think this is already fixed on the release branch and will be part of 0.16.1 this week.  

Are you able to test the release-0.16 branch or the main branch?

cc @mbobrovskyi @vladikkuzn

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-09T06:43:19Z

Hi, thank you for reporting this issue. This is duplicated with https://github.com/kubernetes-sigs/kueue/issues/8873.

Please check the comment. This fix patch will be released in this week.
