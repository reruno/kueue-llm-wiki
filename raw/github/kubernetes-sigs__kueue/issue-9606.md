# Issue #9606: Create a Headlamp plugin for Kueue

**Summary**: Create a Headlamp plugin for Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9606

**Last updated**: 2026-03-04T18:56:25Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-03-01T19:54:25Z
- **Updated**: 2026-03-04T18:56:25Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

Headlamp is gaining traction for Kueue and it seems there is external interest for a plugin.

I'm not sure this is any action from Kueue folks but I wanted to create this issue to inform Kueue community.

Headlamp request kueue request: https://github.com/kubernetes-sigs/headlamp/issues/4678

WIP PR: https://github.com/headlamp-k8s/plugins/pull/530

One thing that may be worth considering is if we can consolidate efforts on Kueue-Viz and headlamp.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-02T05:59:21Z

/kind feature

### Comment by [@kimminw00](https://github.com/kimminw00) — 2026-03-04T14:41:20Z

I opened this issue because, from  a Kubernates engineer's perspective, we prefer a centralized dashboard  over deploying and maintaining separate web UIs for every single component.

Managing cross-cutting concerns like authentication (OIDC/SSO), and authorization (RBAC) individually for each component's dashboard creates significant operational overhead and security complexity. It is much more efficient to solve these problems once in a unified platform like Headlamp.

Instead of the Kueue team needing to reinvent the wheel for a web server and auth layer, integrating with Headlamp allows them to focus purely on the visualization logic while leveraging the platform's existing security and management features.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-04T18:56:25Z

> I opened this issue because, from a Kubernates engineer's perspective, we prefer a centralized dashboard over deploying and maintaining separate web UIs for every single component.

This makes sense to me. In Openshift we also have some challenges using kueue-viz because it doesn't integrate with our console stack.
