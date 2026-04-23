# Issue #1912: Scalability tests for Kueue scheduler

**Summary**: Scalability tests for Kueue scheduler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1912

**Last updated**: 2024-04-26T07:37:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-03-26T10:38:57Z
- **Updated**: 2024-04-26T07:37:09Z
- **Closed**: 2024-04-26T07:37:09Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Scalability tests (involving thousands of workloads) for Kueue scheduler, oriented on the performance of the Kueue algorithms, using the integration test layer to focus on the performance of the scheduler algorithms (for preemption and scheduling).

**Why is this needed**:

It can be handy to verify there is no regression when working on Fair sharing or Hierarchical cohorts features.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-26T10:42:12Z

I think it does not require KEP, since there is no API change. However, there are some non-obvious decisions, so I prepared an [initial design doc](https://docs.google.com/document/d/1iO8CGO6kgav2JL6RKYnNYvkeQIHpFqB-SQqJ7eUsjPs?tab=t.0#heading=h.e5jhgh56ju14), shared with batch-wg. Feel free to comment or request changes.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-26T10:43:41Z

/assign @trasc 
/cc @alculquicondor @mwielgus

### Comment by [@mimowo](https://github.com/mimowo) — 2024-03-27T10:55:48Z

Additionally (it might be a follow up issue) we would like to have a higher-level of scalability tests using a framework such as kwok. Since both layers of testing would cover slightly different use-cases (focus on algorithms vs focus on e2e throughput) we may add both.
