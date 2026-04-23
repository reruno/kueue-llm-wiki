# Issue #4869: Alpha API Cohorts are not guarded by a feature gate

**Summary**: Alpha API Cohorts are not guarded by a feature gate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4869

**Last updated**: 2025-04-08T05:56:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-04-06T02:30:43Z
- **Updated**: 2025-04-08T05:56:41Z
- **Closed**: 2025-04-08T05:56:41Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 3

## Description

We would like to avoid supporting/shipping any alpha APIs in Kueue. We remove Topology/Cohorts in our deployment of Kueue. TAS is feature gates so this causes no issue.

It looks like Cohorts are expected to exist for the cohort controller. Is it possible to introduce a feature gate for cohort usage? Ideally we would like to not start the Cohort Controller if we don’t want any alpha functionality in Kueue. 

We see errors in the logs if we remove cohort CRD because the controller still gets started in the core set of controllers.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-07T06:34:15Z

I see, I'm totally ok to guard the controller by a feature gate. We probably would use a beta feature gate (even though the API is alpha), so that it does not require a new manual step from users. I think we can consider it as a fully backward compatible bugfix then.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-07T10:17:35Z

SGTM

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-07T14:07:28Z

Sounds good. I have https://github.com/kubernetes-sigs/kueue/pull/4870.
