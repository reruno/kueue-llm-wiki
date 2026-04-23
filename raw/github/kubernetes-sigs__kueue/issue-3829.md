# Issue #3829: Introduce sanity e2e tests for KubeRay

**Summary**: Introduce sanity e2e tests for KubeRay

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3829

**Last updated**: 2025-05-06T09:29:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-13T07:32:33Z
- **Updated**: 2025-05-06T09:29:15Z
- **Closed**: 2025-05-06T09:29:15Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 8

## Description

**What would you like to be added**:

Sanity e2e tests for KubeRay (RayJob and RayCluster). In particular the submitted Job mode as in https://github.com/kubernetes-sigs/kueue/pull/3729

**Why is this needed**:

To ensure the basic integration with KubeRay works. We can cover corner cases in integration and unit tests.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T07:34:41Z

cc @andrewsykim @mbobrovskyi @tenzen-y 

/assign @kaisoz 
tentatively, who might want to take it as an automated follow up to https://github.com/kubernetes-sigs/kueue/issues/1568 (though it is a bit different because testing the issue fully requires `manageJobsWithoutQueueName`, and so it also requires https://github.com/kubernetes-sigs/kueue/issues/3767)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-02T02:30:44Z

/remove-kind feature
/kind cleanup

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-01-16T13:26:43Z

/unassign 

I'm working on #3767 so better keep this one free for another contributor 😊

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2025-01-22T02:18:56Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-20T08:15:08Z

@bobsongplus any progress on that? If you don't have time to work on this, which is perfectly understandable, then I would suggest to unassign.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-27T13:43:35Z

/unassign @bobsongplus
It's been over a month, freeing up for other contributors. @bobsongplus let us know in case you are "in-progress".

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-27T14:42:18Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-27T14:43:35Z

IMHO most of the tests are there, we are lacking only single cluster e2e tests, tas is in [progress](https://github.com/kubernetes-sigs/kueue/pull/4341)
