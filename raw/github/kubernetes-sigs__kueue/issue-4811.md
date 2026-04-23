# Issue #4811: Upgrade hugo version

**Summary**: Upgrade hugo version

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4811

**Last updated**: 2025-04-24T15:20:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-28T06:24:59Z
- **Updated**: 2025-04-24T15:20:33Z
- **Closed**: 2025-04-24T15:20:33Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@2000krysztof](https://github.com/2000krysztof)
- **Comments**: 27

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Upgrade hugo version to 0.133.0 same as k8s website: https://github.com/kubernetes/website/blob/041fa1cfe3c0f271ba47d9c56701742b8536cf27/netlify.toml#L11

**Why is this needed**:

Our version is a bit outdated https://github.com/kubernetes-sigs/kueue/blob/9be51c7e3563643aea96ce28b150489faa386996/netlify.toml#L7

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-28T10:13:54Z

As part of the issue I would like to investigate using dependabot to bump it regularly for us. If possible, this could be a follow up PR ofc.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-28T10:25:58Z

> As part of the issue I would like to investigate using dependabot to bump it regularly for us. If possible, this could be a follow up PR ofc.
> 

SGTM

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-07T09:23:58Z

Hi, this looks like a `good-first-issue`. If so, could we assign @2000krysztof to this issue? He will read the [contributing guidelines](https://github.com/kubernetes-sigs/kueue/blob/main/CONTRIBUTING.md) before getting started.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-07T09:29:51Z

+1, let's try, but it may not work if the contributor is not k/sigs member yet, let's see
/assign 2000krysztof

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-07T09:29:53Z

@mimowo: GitHub didn't allow me to assign the following users: 2000krysztof.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4811#issuecomment-2782688724):

>+1, let's try, but it may not work if the contributor is not k/sigs member yet, let's see
>/assign 2000krysztof 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-07T10:11:37Z

I've made a PR in the contributor-playground repository and just signed the CLA

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-07T10:13:49Z

/good-first-issue

@2000krysztof could you say `/assign` here?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-07T10:13:52Z

@tenzen-y: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4811):

>/good-first-issue
>
>@2000krysztof could you say `/assign` here?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-07T10:15:22Z

/assign

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-07T14:41:52Z

Should I make the PR for the version upgrade and then create a second issue for the dependabot bumping?

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-08T09:40:29Z

> As part of the issue I would like to investigate using dependabot to bump it regularly for us. If possible, this could be a follow up PR ofc.

I think that the dependabot is incompatible with the netlify.toml format. Alternatively we can set the version to "latest" instead of a specific version or we could make some kind of a github action.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T09:48:38Z

> I think that the dependabot is incompatible with the netlify.toml format. 

Could we ask dependabot to bump it in some other file format, and then propagate it by makefile to the toml as a parameter? The toml file seems parametrized, so maybe we could do the same with the version.

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-08T09:51:52Z

> Could we ask dependabot to bump it in some other file format, and then propagate it by makefile to the toml as a parameter? The toml file seems parametrized, so maybe we could do the same with the version.

I will look into that

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T09:56:40Z

Seems like we already declare some version here: https://github.com/kubernetes-sigs/kueue/blob/3fee4b61affb7a83f03b999aa6579f7392f99461/hack/internal/tools/go.mod#L6, then we read it here: https://github.com/kubernetes-sigs/kueue/blob/c3fca927a7d96210fe76bd1b49293c2253307eb3/Makefile-deps.mk#L37C1-L37C13

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-08T10:27:59Z

> Seems like we already declare some version here:
> 
> [kueue/hack/internal/tools/go.mod](https://github.com/kubernetes-sigs/kueue/blob/3fee4b61affb7a83f03b999aa6579f7392f99461/hack/internal/tools/go.mod#L6)
> 
> Line 6 in [3fee4b6](/kubernetes-sigs/kueue/commit/3fee4b61affb7a83f03b999aa6579f7392f99461)
> 
>  github.com/gohugoio/hugo v0.145.0 
> , then we read it here: https://github.com/kubernetes-sigs/kueue/blob/c3fca927a7d96210fe76bd1b49293c2253307eb3/Makefile-deps.mk#L37C1-L37C13

I think that this is auto generated by dependabot once the HUGO_VERSION in the netlify.toml changes. 
I think if we source it with gomod fully instead of netlify.toml this way the dependabot should be able to recognize it.

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-08T13:59:47Z

I've noticed that version of hugo that is in the toml file does not make  much of a difference. Because I have changed it to 0.133.0 but the version that is running is 0.145.0 which happens to be the latest version of hugo. So it seems like it will just pick the latest version regardless of what is in the toml file.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-09T05:55:55Z

I don’t think it’s possible to configure dependabot to update `netlify.toml`. Maybe we should create a separate GitHub workflow to automate this process and update netlify.toml HUGO_VERSION on Dependabot PR.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-09T05:56:04Z

> I've noticed that version of hugo that is in the toml file does not make much of a difference. Because I have changed it to 0.133.0 but the version that is running is 0.145.0 which happens to be the latest version of hugo.

How did you check version? As I can see from [doc](https://docs.netlify.com/frameworks/hugo/) this is correct way to set hugo version.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-09T06:04:29Z

To ensure version consistency, it would be great to automatically update and verify this version using `make verify`, similar to what we’ve done here https://github.com/kubernetes-sigs/kueue/blob/d57b40c9d5596f10c86de98feed5bb3a47bc219e/Makefile#L285.

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-09T08:38:36Z

> How did you check version? As I can see from [doc](https://docs.netlify.com/frameworks/hugo/) this is correct way to set hugo version.

If you run the make site-server command it will generate a bin folder in the project with the hugo binary, I then ran hugo version on that

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-09T08:47:29Z

> If you run the make site-server command it will generate a bin folder in the project with the hugo binary, I then ran hugo version on that

But this is a binary from bin directory. 

https://github.com/kubernetes-sigs/kueue/blob/7a15e4d4b97e0968615386230ff42ce0b5b0862e/Makefile#L257-L259

Locally we are not using netlify. We are using hugo version 0.145.0.

https://github.com/kubernetes-sigs/kueue/blob/7a15e4d4b97e0968615386230ff42ce0b5b0862e/hack/internal/tools/go.mod#L6 

Looks like correct, no?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-09T08:48:03Z

In netlify.toml we have v0.133.0.

https://github.com/kubernetes-sigs/kueue/blob/7a15e4d4b97e0968615386230ff42ce0b5b0862e/netlify.toml#L7C19-L7C26

So I think we should bump it.

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-09T08:57:31Z

Sorry my bad I didn't realize that the github one and the local one run on different versions. I will look into a way to bump it with sed in the makefile as you mentioned before.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-14T10:25:55Z

/reopen
Seems like still some issue with dependabot https://github.com/kubernetes-sigs/kueue/pull/4951

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-14T10:25:59Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4811#issuecomment-2801247804):

>/reopen
>Seems like still some issue with dependabot https://github.com/kubernetes-sigs/kueue/pull/4951


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@2000krysztof](https://github.com/2000krysztof) — 2025-04-14T10:31:26Z

It seems like a new version of hugo was released, but it did bump the version, the only thing is that the bot checks fail

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2025-04-14T10:46:43Z

Perhaps we need a separate workflow that runs if the PR is created by `dependabot` and if there's a diff in the Hugo version captured by `make verify`. This workflow would run `make sync-hugo-version` to sync the version in the .`toml` file and commit and push to the same PR.
