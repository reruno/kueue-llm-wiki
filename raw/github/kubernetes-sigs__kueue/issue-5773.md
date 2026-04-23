# Issue #5773: `do-not-merge/invalid-commit-message` appears when creating a bump PR for dependencies with an @ prefix

**Summary**: `do-not-merge/invalid-commit-message` appears when creating a bump PR for dependencies with an @ prefix

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5773

**Last updated**: 2026-02-27T14:39:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-06-25T15:21:02Z
- **Updated**: 2026-02-27T14:39:28Z
- **Closed**: 2026-02-27T14:39:27Z
- **Labels**: `kind/bug`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 30

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
We need to manually create PRs for dependencies with an `@` prefix – such as `@mui/material` or `@vitejs/plugin-react` – because Prow adds the `do-not-merge/invalid-commit-message` label to PRs that contain `@` in the description.

**What you expected to happen**:
Don't add `do-not-merge/invalid-commit-message` label for Dependabot PRs.

**How to reproduce it (as minimally and precisely as possible)**:
It is creating automatically by Dependabot. For example https://github.com/kubernetes-sigs/kueue/pull/5767.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-25T15:21:31Z

cc @tenzen-y @mimowo

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-25T15:24:35Z

I also tried updating the commit automatically using a GitHub Action (https://github.com/mbobrovskyi/kueue/pull/29/commits/41b41ddf796e7320fb2ce4afa1255b7d9f007341), but Dependabot closes the PR after a force push.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-30T12:20:41Z

One more times https://github.com/kubernetes-sigs/kueue/pull/5808.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-30T12:28:43Z

would it need to be fixed in kueue repo or outside? Do you know where is the code rejecting commit messages with @?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-30T12:36:49Z

It looks like the Prow bot adds the label when it detects an `@` symbol in the commit message. However, I'm not sure how to configure Dependabot to avoid including `@` in its commit messages.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-30T12:55:14Z

Yeah, so it seems like 3 ways:
1. fix PRow not to validate it
2. configure dwpendabot to allow not doing this
3. use a GH action to override the commit message, go example replace all @with \@ or even with another char.

I think 1. would be the long term solution, it seems like an unnecesaary validation in prow. Short term im ok with 3

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-30T13:07:00Z

> use a GH action to override the commit message, go example replace all @with @ or even with another char.

I tried updating the commit and change @ with some other chart automatically using a GitHub Action (https://github.com/mbobrovskyi/kueue/commit/41b41ddf796e7320fb2ce4afa1255b7d9f007341), but Dependabot closes the PR after a force push. :(

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T07:51:23Z

I have opened the issue for dependabot: https://github.com/dependabot/dependabot-core/issues/13042

cc @mbobrovskyi @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-08T11:23:05Z

It seems the issue in dependabot isn't moving forward, and even if it was it would require engineering time + time to sink.

So, as an alternative I would like to consider the [renovate](https://github.com/apps/renovate) app with the dependency bot, similar to dependabot. For start we would just do it for the frontend dependencies [here](https://github.com/kubernetes-sigs/kueue/blob/main/.github/dependabot.yml#L87-L115). If we like it we could replace dependabot completely, but this is not needed now.

So, the renovate offers tweaking the commit message to remove special characters already, most conviniently just using `{{{depNameSanitized}}}` placeholder, see [here](https://docs.renovatebot.com/templates/#other-available-fields).

Wdyt @tenzen-y @gabesaba ? I think this is worth a shot, because each frontend dependency now requires a manual PR which is not maintainable.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-08T12:42:22Z

> It seems the issue in dependabot isn't moving forward, and even if it was it would require engineering time + time to sink.
> 
> So, as an alternative I would like to consider the [renovate](https://github.com/apps/renovate) app with the dependency bot, similar to dependabot. For start we would just do it for the frontend dependencies [here](https://github.com/kubernetes-sigs/kueue/blob/main/.github/dependabot.yml#L87-L115). If we like it we could replace dependabot completely, but this is not needed now.
> 
> So, the renovate offers tweaking the commit message to remove special characters already, most conviniently just using `{{{depNameSanitized}}}` placeholder, see [here](https://docs.renovatebot.com/templates/#other-available-fields).
> 
> Wdyt [@tenzen-y](https://github.com/tenzen-y) [@gabesaba](https://github.com/gabesaba) ? I think this is worth a shot, because each frontend dependency now requires a manual PR which is not maintainable.

SGTM, let's migrate the frontend component's dependencies management to renovate.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-08T14:07:09Z

We may learn for cilium, here is an example [PR](https://github.com/cilium/tetragon/pull/4148) but the bot there.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-14T19:01:02Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-17T11:21:29Z

Not to self-host renovate as it's done in [cilium/tetragon](https://github.com/cilium/tetragon), somebody should approve [installation of renovate](https://github.com/apps/renovate) to the kueue repo(I've already requested)
@mimowo can you help with this?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-10T15:43:49Z

> Not to self-host renovate as it's done in [cilium/tetragon](https://github.com/cilium/tetragon), somebody should approve [installation of renovate](https://github.com/apps/renovate) to the kueue repo(I've already requested) [@mimowo](https://github.com/mimowo) can you help with this?

It seems that the installation of Renovate is managed by kuberenestes-sigs organization level. So, even I or @mimowo can not approve the request. We might need to contact with GitHub organization admins.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-11-10T16:08:15Z

Before reaching out to GitHub organisation admins let me first test it locally, maybe we won't need that access
/hold

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-10T16:10:03Z

> Before reaching out to GitHub organisation admins let me first test it locally, maybe we won't need that access /hold

SGTM, thanks

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T07:24:17Z

> Not to self-host renovate as it's done in [cilium/tetragon](https://github.com/cilium/tetragon), somebody should approve [installation of renovate](https://github.com/apps/renovate) to the kueue repo(I've already requested)

How is it self-hosted there? Can you share links to the relevant places in code we would need to adjust?

> It seems that the installation of Renovate is managed by kuberenestes-sigs organization level. So, even I or @mimowo can not approve the request. We might need to contact with GitHub organization admins.

Do you know @tenzen-y who would that be? Maybe we could contact on slack?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-19T16:37:02Z

> > It seems that the installation of Renovate is managed by kuberenestes-sigs organization level. So, even I or @mimowo can not approve the request. We might need to contact with GitHub organization admins.
>
>Do you know @tenzen-y who would that be? Maybe we could contact on slack?

@mszadkow already has posted that in sig-docs, and it will be addressed. Thanks @mszadkow !

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-19T16:37:32Z

> > > It seems that the installation of Renovate is managed by kuberenestes-sigs organization level. So, even I or [@mimowo](https://github.com/mimowo) can not approve the request. We might need to contact with GitHub organization admins.
> > 
> > 
> > Do you know [@tenzen-y](https://github.com/tenzen-y) who would that be? Maybe we could contact on slack?
> 
> [@mszadkow](https://github.com/mszadkow) already has posted that in sig-docs, and it will be addressed. Thanks [@mszadkow](https://github.com/mszadkow) !

https://kubernetes.slack.com/archives/C1J0BPD2M/p1763108044690619

> Natali
>   [Friday at 10:34 PM](https://kubernetes.slack.com/archives/C1J0BPD2M/p1763127260230379?thread_ts=1763108044.690619&cid=C1J0BPD2M)
> us as SIG Docs leaders are currently at KubeCon in Atlanta, but we can check in on this later this weekend or early next week!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T10:52:39Z

/reopen
Let me reopen until we have confirmation that it works - first PRs opened by the bot

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-25T10:52:45Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5773#issuecomment-3575019265):

>/reopen
>Let me reopen until we have confirmation that it works - first PRs opened by the bot


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T08:11:16Z

The transition to renovate is taking too long and we cannot risk releasing 0.16 with outdated dependencies. 

So I propose for short term to revert https://github.com/kubernetes-sigs/kueue/pull/7887 and investigate deeper the options:
1. return to renovate but do it prepared - guidence from k8s infra folks and fixing of permissions. I think someone with appropriate permissions in kubernetes-sigs can only install it - I wasn't able to install, just sent request to install
2. investigate deeper self-hosted renovate (I need summary how much code / summary / maintanance is there)
3. work on updating dependabot community to sanitize commit messages as proposed in https://github.com/dependabot/dependabot-core/issues/13042
4. working with the k8s community on prow bot to configure it so that it accepts "@" - I have no idea if this validation is still needed, maybe it is just legacy. We can ask on slack (I would love to explore it more)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-05T08:13:36Z

@vladikkuzn could you please revert it?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-12-05T18:02:08Z

Looks like Renovate’s GitHub App tried to open the PR from a branch inside kubernetes-sigs/kueue, but repo only allows PRs from forks. When Renovate can’t push a branch to the upstream repo, GitHub returns integration-unauthorized, so the branch (and therefore the PR) creation fails.
Two options to fix it:
- [Configure Renovate to use a fork](https://docs.renovatebot.com/getting-started/running/#forking-renovate-app). That makes Renovate push the update branch to its own fork and open the PR from there. Also we would need to set:
[forkToken](https://docs.renovatebot.com/self-hosted-configuration/#forktoken)
[forkOrg](https://docs.renovatebot.com/self-hosted-configuration/#forkorg)
[forkCreation](https://docs.renovatebot.com/self-hosted-configuration/#forkcreation) 
[Reference](https://github.com/renovatebot/renovate/discussions/39263)
- Alternatively, give the Renovate bot a personal access token or account that actually has push permissions to the main repo—though this typically isn’t allowed in projects that enforce fork-only PRs. (insecure)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-05T18:29:13Z

We would need to do (1.) - we don't use private acoounts for sigs projects.

However, in this case we need to still install the Forking Renovate. I can try to request that, but typically it would probably need to be installed with someone with more permissions than me. Let me try. 

EDIT:nah it seems to still correlating my private account with the request, so I don't think this is the right path. I think this is should rather be installed by someone in managing GH for sigs projects.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-23T08:52:29Z

@vladikkuzn is this still an issue? I seem to remember last month some PR with frontend library getting merged. Not sure if this was an exception. Worth re-checking.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-23T09:43:12Z

I don't think so, it's fixed know, probably on prow side

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-23T09:54:11Z

Let's try to open a PR which contains "@" or "#" in the commit message to re-test.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-27T14:39:22Z

/close
I can see this is already not a problem based on this PR: https://github.com/kubernetes-sigs/kueue/pull/9558

Probably the robot got modified at the k8s side.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-27T14:39:28Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5773#issuecomment-3973300859):

>/close
>I can see this is already not a problem based on this PR: https://github.com/kubernetes-sigs/kueue/pull/9558
>
>Probably the robot got modified at the k8s side.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
