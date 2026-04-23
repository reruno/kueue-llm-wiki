# Issue #4681: Support webhook reinvocationPolicy configuration in kueue helm chart

**Summary**: Support webhook reinvocationPolicy configuration in kueue helm chart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4681

**Last updated**: 2025-06-20T04:31:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yuvalaz99](https://github.com/yuvalaz99)
- **Created**: 2025-03-19T09:49:22Z
- **Updated**: 2025-06-20T04:31:02Z
- **Closed**: 2025-06-20T04:31:01Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: [@yuvalaz99](https://github.com/yuvalaz99)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
An option in the Helm chart to configure the webhook with `reinvocationPolicy: IfNeeded`
Currently, Kueue does not configure `reinvocationPolicy` in the chart, so it defaults to `Never`.

**Why is this needed**:
In our setup, we configure Kueue to manage only workloads with the `kueue.x-k8s.io/queue-name` label.
We use mutation webhooks (e.g., Kyverno) to add fields to objects, including `kueue.x-k8s.io/queue-name`.

To ensure that Kueue’s mutation webhook is invoked after our own webhooks and can properly manage those workloads, we need a robust solution. If Kueue’s webhook runs before our webhook (which adds the label), it will not be able to manage any workload.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T09:59:33Z

cc @mbobrovskyi @mszadkow @mykysha

### Comment by [@yuvalaz99](https://github.com/yuvalaz99) — 2025-03-20T10:18:48Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-18T11:11:22Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T04:30:57Z

This has been done by https://github.com/kubernetes-sigs/kueue/pull/5063

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-20T04:31:02Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4681#issuecomment-2989763545):

>This has been done by https://github.com/kubernetes-sigs/kueue/pull/5063
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
