# Issue #4755: Document KueueViz installation in a production suitable documentation

**Summary**: Document KueueViz installation in a production suitable documentation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4755

**Last updated**: 2025-07-21T08:38:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@akram](https://github.com/akram)
- **Created**: 2025-03-22T19:32:23Z
- **Updated**: 2025-07-21T08:38:34Z
- **Closed**: 2025-07-21T08:38:34Z
- **Labels**: `good first issue`, `help wanted`, `kind/documentation`, `area/dashboard`
- **Assignees**: [@samzong](https://github.com/samzong)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Document KueueViz installation in a production suitable documentation

**Why is this needed**:

KueueViz is getting promoted form experimental to non-experimental and aims to reach production release.
For this to happen, users need a properly documentation installation process available on kueue website.

## Discussion

### Comment by [@akram](https://github.com/akram) — 2025-03-22T19:33:01Z

/kind dashboard

### Comment by [@akram](https://github.com/akram) — 2025-03-22T19:33:32Z

/kind documentation

### Comment by [@kafonek](https://github.com/kafonek) — 2025-03-24T16:04:25Z

@akram if it helps, here's my experience deploying KueueViz:

Local (docker-desktop) deployment: 
  - `kubectl port-forward svc/kueue-kueue-viz-frontend -n kueue-system 8080`
  - `kubectl port-forward svc/kueue-kueue-viz-backend  -n kueue-system 8081:8080`
  - Edit the `kueue-viz-frontend` Deployment to set env `REACT_APP_WEBSOCKET_URL=ws://localhost:8081`


For a multi-user cluster that controls ingress through Twingate-style software defined perimeter, the setup was roughly the same just switch out `kubectl port-forward` with defined uris. One small quality of life change would be defining the backend uri in the helm chart.

### Comment by [@akram](https://github.com/akram) — 2025-03-31T16:47:32Z

@kafonek thank you for the feedback. This is also what I use for local testing. And I want to document the different cases like:
- vanilla kubernetes with ingress controller installed
- kubernetes without ingress controller
- optionally OpenShift

all these 3 scenarios works but requires a bit of guidance

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-14T21:20:31Z

/remove-kind cleanup

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-13T15:40:55Z

/help wanted
I think this could be a subpage under https://kueue.sigs.k8s.io/docs/tasks/manage/, say "Enable KueueViz". 

cc @kannon92 @akram do you know some folks with cycles to prepare such a doc?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-13T15:41:48Z

/help-wanted

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-13T15:42:33Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-13T15:42:35Z

@mimowo: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://www.kubernetes.dev/docs/guide/help-wanted/#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4755):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@samzong](https://github.com/samzong) — 2025-07-15T00:34:38Z

/assign samzong

This may take some time. I need to set up the local environment for kueue, and I also hope to make more types of contributions.

### Comment by [@samzong](https://github.com/samzong) — 2025-07-16T04:34:04Z

- #5988

I have completed the initial the doc. help review it pls.

thanks.
