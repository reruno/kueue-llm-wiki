# Issue #64: Add user guide

**Summary**: Add user guide

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/64

**Last updated**: 2022-04-06T18:40:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-24T16:48:49Z
- **Updated**: 2022-04-06T18:40:26Z
- **Closed**: 2022-04-06T18:40:26Z
- **Labels**: `kind/feature`, `good first issue`, `help wanted`, `kind/documentation`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 8

## Description

/kind feature
/size M

Something more comprehensive that the existing README. Some of the use cases in bit.ly/kueue-apis can be dumped into samples/guides.

If possible, generate some documentation out of the APIs, similar to https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.23/

Contents (not necessarily each one will be a page, but they could be sections on existing pages).
- [x] Single CQ setup
- [x] Multiple flavors
- [x] Multiple CQ setup (cohorts)
- [x] Namespace selectors
- [ ] Cohorts
- [x] Running a Job
- [ ] Configuring RBAC
- [ ] Monitoring usage (kubectl describe)

## Discussion

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-20T11:52:23Z

Could we use github pages? or just a folder with markdown is ok for now? 
GitHub pages is easy to manage using prow automation

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-20T11:52:44Z

/kind documentation 
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-20T11:52:45Z

@ArangoGutierrez: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/64):

>/kind documentation 
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-21T13:20:59Z

We can probably start with markdown and move it to github pages when there is some useful content :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-22T18:27:26Z

I'll start this

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-28T20:19:57Z

I just added in the description a list of things I would like to cover. Anything else?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-28T20:45:22Z

for a v0.0.1 , we are ok i Think

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-05T15:36:06Z

one more thing to add to CQ concept is queueing strategy
