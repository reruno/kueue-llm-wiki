# Issue #5507: Automatically synchronize FGs and documentation FGs list

**Summary**: Automatically synchronize FGs and documentation FGs list

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5507

**Last updated**: 2026-01-23T07:05:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-04T17:47:58Z
- **Updated**: 2026-01-23T07:05:29Z
- **Closed**: 2026-01-23T07:05:29Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We want to investigate the way to automatically synchronize FGs and the documentation FGs list:

- FGs: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/features/kube_features.go
- Documentation FGs list: https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/installation/_index.md#feature-gates-for-alpha-and-beta-features

**Why is this needed**:
We want to avoid unsynchronized documentation.

**Completion requirements**:

Before we implement any Kueue repository specific scripts, we want to investigate if there are any existing tools.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T17:48:58Z

cc @mimowo

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-02T17:51:38Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-02T17:53:14Z

/remove-lifecycle stale

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-01T15:38:28Z

I haven’t found a tool that automatically keeps feature gates in sync between code and documentation, and these issues suggest such a tool doesn’t exist yet:

- https://github.com/kubernetes/website/issues/50992
- https://github.com/kubernetes/website/issues/52425

However, there is a tool in the Kubernetes repo that might help: 

- https://github.com/kubernetes/kubernetes/tree/v1.34.0/test/compatibility_lifecycle

This tool appears to generate a YAML file with feature gate information from the source code, which could serve as the source of truth. An example of this generated YAML file can be found here:
https://github.com/kubernetes/kubernetes/blob/master/test/compatibility_lifecycle/reference/versioned_feature_list.yaml

One approach for Kueue could be to generate this YAML file and then create a script to update the documentation based on it. Alternatively, we could build a script that updates the documentation directly from the source code in one step, without the intermediate YAML file.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T08:38:47Z

> One approach for Kueue could be to generate this YAML file and then create a script to update the documentation based on it. Alternatively, we could build a script that updates the documentation directly from the source code in one step, without the intermediate YAML file.

sgtm, this is similar to what @vladikkuzn is working on for metrics.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-11-25T13:31:07Z

/assign
