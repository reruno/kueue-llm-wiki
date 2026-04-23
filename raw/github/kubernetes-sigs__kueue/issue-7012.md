# Issue #7012: Enable KAI linter for api review

**Summary**: Enable KAI linter for api review

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7012

**Last updated**: 2025-09-29T17:00:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-09-25T15:15:02Z
- **Updated**: 2025-09-29T17:00:19Z
- **Closed**: 2025-09-29T17:00:19Z
- **Labels**: _none_
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 6

## Description

https://github.com/kubernetes-sigs/kube-api-linter

Kubernetes has added a golangci-lint plugin to check on API reviews.

It would be great to add this in our lint pipeline and see what it says about our API.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-25T15:15:51Z

cc @JoelSpeed @everettraven 

We also discussed having an API-review for Kueue as we transition the APIs from v1beta1 -> v1beta2 -> v1.

My goal is to enable this linter check on the Kueue API and fix these as we promote.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T15:17:42Z

AFAIK, all lint rules do not align with the API convention, which means some rules align with the API convention, but some rules are recommendations.

So, I would like to select the rules to align with the API convention ones.

### Comment by [@everettraven](https://github.com/everettraven) — 2025-09-25T15:25:54Z

We are making a conscious effort to have the default set of lint rules to be ones that align with Kubernetes API conventions and apply to Kubernetes built-in types, but there are some differences when it comes to core Kube built-ins/aggregated APIs and CRDs that should be considered.

The current list of all linters and their possible configurations are documented in https://github.com/kubernetes-sigs/kube-api-linter/blob/main/docs/linters.md

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-25T15:32:07Z

I followed up with @everettraven offline for some examples on how ones enable kai in their CI.

- https://github.com/openshift/api/pull/2321 
- https://github.com/kubernetes-sigs/cluster-api/pull/11733 

Just listing some examples of how other projects have started using it.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-25T15:32:24Z

I believe its also being integrated into k/k.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-25T16:48:18Z

/assign
