# Issue #3880: Add configuration parameters to kueue-viz backend (listen-port, logs, verbosity, etc...)

**Summary**: Add configuration parameters to kueue-viz backend (listen-port, logs, verbosity, etc...)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3880

**Last updated**: 2026-04-06T02:41:08Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@akram](https://github.com/akram)
- **Created**: 2024-12-18T12:26:30Z
- **Updated**: 2026-04-06T02:41:08Z
- **Closed**: —
- **Labels**: `kind/feature`, `good first issue`, `help wanted`, `area/dashboard`
- **Assignees**: [@manidharanupoju24](https://github.com/manidharanupoju24)
- **Comments**: 15

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add configuration parameters to kueue-viz backend (listen-port, logs, verbosity, etc...)

**Why is this needed**:
In the evenutality of grouping frontend and backend containers into the same pod, listen ports should be parametrizable.
Currently they are hardcoded both for frontend and backend to 8080; making it impossible to have frontend and backend in the same pod.

**Completion requirements**:
Have a parameter `--listen=0.0.0.0:8181` to the backend and other startup parameters.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@akram](https://github.com/akram) — 2024-12-18T12:28:06Z

/help
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-18T12:28:09Z

@akram: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3880):

>/help
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@SD-13](https://github.com/SD-13) — 2024-12-18T16:32:11Z

Hey @akram, I am new to this project and want to work on this issue.

I have a few doubts -
what would be the default backend port? 8181?
where else we need to update to use parameter values?
- https://github.com/kubernetes-sigs/kueue/blob/f98a2f99d49e0ffcd8c8c7515e1328ffd398f1c9/cmd/experimental/kueue-viz/backend/main.go#L49
- the backend dockerfile
- docs

### Comment by [@vihaan-that](https://github.com/vihaan-that) — 2024-12-18T17:48:17Z

Dear @akram I would like to know if the issue is still up, as I want to take my chance at solving it.

Thank you

### Comment by [@akram](https://github.com/akram) — 2024-12-18T20:33:41Z

> Hey @akram, I am new to this project and want to work on this issue.
> 
> I have a few doubts - what would be the default backend port? 8181? where else we need to update to use parameter values?
> 
> * https://github.com/kubernetes-sigs/kueue/blob/f98a2f99d49e0ffcd8c8c7515e1328ffd398f1c9/cmd/experimental/kueue-viz/backend/main.go#L49
> * the backend dockerfile
> * docs

hi @SD-13 ,

initially the default port was `8080` . You can keep this value as default or use `8181` . The thing is that, in the future we may have `kueue-viz-frontend` and  `kueue-viz-backend` live in the same pod, so they must use different ports. `frontend` already uses `8080` as a default port. So, use `8181` by default for  `backend` would allow to have no configuration.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-24T11:34:30Z

/kind dashboard

### Comment by [@lekaf974](https://github.com/lekaf974) — 2025-02-09T04:26:55Z

@akram I proposed a configuration based approach with my PR can you take a look and give feedback

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-03T12:47:11Z

/reopen
As the issue seems to suggest more things should be configurable that just the port.
I will let @akram to close the issue when it can be considered done.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-03T12:47:16Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3880#issuecomment-2694287795):

>/reopen
>As the issue seems to suggest more things should be configurable that just the port.
>I will let @akram to close the issue when it can be considered done.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@lekaf974](https://github.com/lekaf974) — 2025-03-05T23:53:26Z

@akram I can enhance the starting point, what would be the list of variables to handle ?

### Comment by [@Smuger](https://github.com/Smuger) — 2025-09-06T10:56:29Z

@akram @lekaf974 

My PR is removing some hardcoded dashboard configuration. Should I just add your stuff too?

https://github.com/kubernetes-sigs/kueue/pull/6682

### Comment by [@lekaf974](https://github.com/lekaf974) — 2025-09-06T13:07:24Z

@Smuger Not sure because the request which impacting more the code itself and your PR is more k8s, hlem related. But I am not deeply involve in this project to give a vlear answer

### Comment by [@schnell3526](https://github.com/schnell3526) — 2026-02-04T15:35:09Z

Hi @akram @lekaf974,

Is anyone still actively working on this? I'd like to pick up the remaining work:

- Add CLI flags (e.g., `--listen`, `--log-level`)
- Make logs and verbosity configurable

I'm thinking of using cobra/pflag alongside the existing viper setup to support both CLI flags and environment variables.

Let me know if this approach sounds good, or if there's anything else that should be included.

### Comment by [@manidharanupoju24](https://github.com/manidharanupoju24) — 2026-04-06T02:36:59Z

/assign

### Comment by [@manidharanupoju24](https://github.com/manidharanupoju24) — 2026-04-06T02:41:08Z

Hi @akram! I'm assigned to this issue. 
The linked PR #4178 seems to have addressed the listen-port requirement.

Are there remaining items still needed that I should work on? Happy to continue if so!
