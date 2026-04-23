# PR #2: Add kueue scheduler and job-controller

**Summary**: Add kueue scheduler and job-controller

**Sources**: https://github.com/kubernetes-sigs/kueue/pull/2

**Last updated**: 2022-02-17T22:03:04Z

---

## Metadata

- **State**: closed (merged)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Branch**: `merged` → `main`
- **Created**: 2022-02-17T21:58:20Z
- **Updated**: 2022-02-17T22:03:04Z
- **Merged**: 2022-02-17T22:03:04Z
- **Closed**: 2022-02-17T22:03:04Z
- **Labels**: `lgtm`, `size/XXL`, `approved`, `cncf-cla: yes`
- **Assignees**: [@ahg-g](https://github.com/ahg-g)
- **Requested reviewers**: [@ahg-g](https://github.com/ahg-g)
- **Changed files**: 73   **+16131 / -1**

## Description

Implemented:

- Basic FIFO queueing
- Borrowing from unused capacity in the cohort
- Resource flavor flexibility
- Integration with batch/v1.Job

See [bit.ly/kueue-controller-design](https://bit.ly/kueue-controller-design) for an overview of the design, although not all the features described there are implemented. Notable features missing:
- Job suspension
- Flavor matching (via node affinity)
- Job priorities

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-02-17T21:58:31Z

[APPROVALNOTIFIER] This PR is **APPROVED**

This pull-request has been approved by: *<a href="https://github.com/kubernetes-sigs/kueue/pull/2#" title="Author self-approved">alculquicondor</a>*

The full list of commands accepted by this bot can be found [here](https://go.k8s.io/bot-commands?repo=kubernetes-sigs%2Fkueue).

The pull request process is described [here](https://git.k8s.io/community/contributors/guide/owners.md#the-code-review-process)

<details >
Needs approval from an approver in each of these files:

- ~~[OWNERS](https://github.com/kubernetes-sigs/kueue/blob/main/OWNERS)~~ [alculquicondor]

Approvers can indicate their approval by writing `/approve` in a comment
Approvers can cancel approval by writing `/approve cancel` in a comment
</details>
<!-- META={"approvers":[]} -->

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-17T21:58:58Z

/assign @ahg-g

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-17T22:01:09Z

/lgtm
