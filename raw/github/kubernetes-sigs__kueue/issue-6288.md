# Issue #6288: Automate steps of the release process

**Summary**: Automate steps of the release process

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6288

**Last updated**: 2026-01-27T17:32:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-30T14:14:45Z
- **Updated**: 2026-01-27T17:32:36Z
- **Closed**: 2026-01-27T17:32:35Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 55

## Description

**What would you like to be added**:

Context: here are the steps https://github.com/kubernetes-sigs/kueue/blob/main/.github/ISSUE_TEMPLATE/NEW_RELEASE.md

I would like to automate some steps, in particular automate PR creation for many of the steps here:
- Update the release branch:
- Update the main branch :

For now we don't want to automate anything that is "non-easily reversible" - no automation for approvals, pushing tags, etc. However, we can automate PR creation, similarly as we do in hack/cherry_pick_pull.sh

**Why is this needed**:

To reduce the toil on repeatable work which is error prone.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-30T14:14:59Z

cc @tenzen-y @kannon92 @mbobrovskyi

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-31T03:13:29Z

For update the release branch, what do you mean by "Update the CHANGELOG"?

Is there automation to update this or is that part of the makefile?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-31T15:00:32Z

> For update the release branch, what do you mean by "Update the CHANGELOG"?
> 
> Is there automation to update this or is that part of the makefile?

I guess that Michal means updating this one: https://github.com/kubernetes-sigs/kueue/tree/main/CHANGELOG

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T15:11:21Z

Yes, exactly, here is an example PR we would create manually https://github.com/kubernetes-sigs/kueue/pull/6212
when preparing the PR we just copy the notes from issue, here:

<img width="1086" height="361" alt="Image" src="https://github.com/user-attachments/assets/89ec0122-5bfc-43e3-a662-35a2daaa646f" />

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-01T16:21:11Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-04T13:49:52Z

I think we could also create a script in test-infra to automatically generate a new test configuration for the latest version and remove the previous one.

@mimowo WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T14:32:03Z

Yes, this will be great. I think also a script to await for the starting images, and prepare PR for image promotion.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-05T07:22:58Z

We have the first step done: https://github.com/kubernetes-sigs/kueue/pull/6410

I would like to follow up with the following:
1. Make the "prepare" PR to also update the Release Issue, as manually done here:

I think we could use some HTML TAG to replace like `<!-- PREPARE_PULL -->`
<img width="1149" height="235" alt="Image" src="https://github.com/user-attachments/assets/13f6a64f-db0f-465e-9864-545a975fb2e0" />

2. Automate waiting for the images to be present in staging, and then opening the PR against kubernetes/k8s.io for image promotion - also it would be great if the script could update the Release Issue

3. Automate creating PRs against test-infra for minor release to update the CI testing Jobs (again with links automatically added to the issue)

4. Update the [Release steps](https://github.com/kubernetes-sigs/kueue/blob/main/.github/ISSUE_TEMPLATE/NEW_RELEASE.md) to suggest the script, for now just as an alternative, long term we can simplify some points

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-05T07:24:04Z

I might be missing some improvements, but these come to my mind as nice to haves. We can probably learn more of what would help as we use the scripts for 0.13.2, probably early next week.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T08:40:41Z

Also, I would also love to have a script wrapper for this:

```
 Use https://github.com/kubernetes/release/tree/master/cmd/release-notes to gather notes. Example: release-notes --org kubernetes-sigs --repo kueue --branch release-0.3 --start-sha 4a0ebe7a3c5f2775cdf5fc7d60c23225660f8702 --end-sha a51cf138afe65677f5f5c97f8f8b1bc4887f73d2 --dependencies=false --required-author=""
```
something like `./hack/releasing/sync-notes.sh` which would not require `start-sha` and `end-sha` but determine them automatically and print. Ideally (might be follow up) it would update the Release Issue with the release notes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T13:09:17Z

I tried the https://github.com/kubernetes-sigs/kueue/blob/5173fb4e8d04385d735a16c201e8a852c7f8607a/hack/releasing/sync-notes.sh script with `./hack/releasing/sync-notes.sh v0.12.7`. But, the script generated the release note for main ... v0.12.6.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T16:07:29Z

> I tried the https://github.com/kubernetes-sigs/kueue/blob/5173fb4e8d04385d735a16c201e8a852c7f8607a/hack/releasing/sync-notes.sh script with `./hack/releasing/sync-notes.sh v0.12.7`. But, the script generated the release note for main ... v0.12.6.

@mbobrovskyi I confirmed that new script works as expected, thanks!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T16:16:10Z

> > I tried the https://github.com/kubernetes-sigs/kueue/blob/5173fb4e8d04385d735a16c201e8a852c7f8607a/hack/releasing/sync-notes.sh script with `./hack/releasing/sync-notes.sh v0.12.7`. But, the script generated the release note for main ... v0.12.6.
> 
> [@mbobrovskyi](https://github.com/mbobrovskyi) I confirmed that new script works as expected, thanks!

But, `./hack/releasing/sync-notes.sh v0.13.` does not work well. Can you check that?
It seem that the previous version detection is not correct:

```shell
++ echo main
+ HEAD_BRANCH=main
+ declare HEAD_BRANCH
++ find_previous_version v0.13.3
++ local release_version=v0.13.3
++ IFS=.
++ read -r major minor patch
+++ git tag -l
+++ grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$'
+++ sort -V -r
++ for tag in $(git tag -l | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -V -r)
++ IFS=.
++ read -r t_major t_minor t_patch
++ '[' 0 -lt 0 ']'
++ '[' 0 -eq 0 ']'
++ '[' 13 -lt 13 ']'
++ '[' 0 -eq 0 ']'
++ '[' 13 -eq 13 ']'
++ '[' 1 -lt 3 ']'
++ echo v0.13.1
++ return 0
+ PREVIOUS_VERSION=v0.13.1
+ declare PREVIOUS_VERSION
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-21T16:29:19Z

> > > I tried the https://github.com/kubernetes-sigs/kueue/blob/5173fb4e8d04385d735a16c201e8a852c7f8607a/hack/releasing/sync-notes.sh script with `./hack/releasing/sync-notes.sh v0.12.7`. But, the script generated the release note for main ... v0.12.6.
> > 
> > 
> > [@mbobrovskyi](https://github.com/mbobrovskyi) I confirmed that new script works as expected, thanks!
> 
> But, `./hack/releasing/sync-notes.sh v0.13.` does not work well. Can you check that? It seem that the previous version detection is not correct:
> 
> ++ echo main
> + HEAD_BRANCH=main
> + declare HEAD_BRANCH
> ++ find_previous_version v0.13.3
> ++ local release_version=v0.13.3
> ++ IFS=.
> ++ read -r major minor patch
> +++ git tag -l
> +++ grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$'
> +++ sort -V -r
> ++ for tag in $(git tag -l | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -V -r)
> ++ IFS=.
> ++ read -r t_major t_minor t_patch
> ++ '[' 0 -lt 0 ']'
> ++ '[' 0 -eq 0 ']'
> ++ '[' 13 -lt 13 ']'
> ++ '[' 0 -eq 0 ']'
> ++ '[' 13 -eq 13 ']'
> ++ '[' 1 -lt 3 ']'
> ++ echo v0.13.1
> ++ return 0
> + PREVIOUS_VERSION=v0.13.1
> + declare PREVIOUS_VERSION

After I executed `git fetch upstream --tags`, the above incorrect previous tag detection was resolved. It would be nice to execute the command inside script. But, I am seeing another unexpected behavior that unexpected commits are listed in release-notes.

The following `- ProvisioningRequest: Graduate ProvisioningACC feature to GA (#6382, @kannon92)` isn't correct as a release note for v0.13.3.

```
## Changes by Kind

### Feature

- ProvisioningRequest: Graduate ProvisioningACC feature to GA (#6382, @kannon92)

### Bug or Regression

- FS: Fixing a bug where a preemptor ClusterQueue was unable to reclaim its nominal quota when the preemptee ClusterQueue can borrow a large number of resources from the parent ClusterQueue / Cohort (#6617, @pajakd)
- KueueViz: Fix CORS configuration for development environments (#6603, @yankay)
- TAS: Fix a bug where new Workloads starve, caused by inadmissible workloads frequently requeueing due to unrelated Node LastHeartbeatTime update events. (#6570, @utam0k)
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-10T07:18:54Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-10T07:19:00Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6288#issuecomment-3273647636):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-12T15:26:05Z

Are we able to set up `gcloud` command in https://github.com/kubernetes-sigs/kueue/blob/main/hack/releasing/wait_for_images.sh?
Or, we might just check if `gcloud` command is installed before anything.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T17:21:11Z

I found also a small issue that this PR https://github.com/kubernetes-sigs/kueue/pull/6808 didn't have the step `make update-security-insights GIT_TAG=$VERSION`. I think we should generate it in a separate script later.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-15T07:16:04Z

> I found also a small issue that this PR [#6808](https://github.com/kubernetes-sigs/kueue/pull/6808) didn't have the step `make update-security-insights GIT_TAG=$VERSION`. I think we should generate it in a separate script later.

Fixed on https://github.com/kubernetes-sigs/kueue/pull/6826.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-15T07:18:42Z

> Are we able to set up `gcloud` command in https://github.com/kubernetes-sigs/kueue/blob/main/hack/releasing/wait_for_images.sh? Or, we might just check if `gcloud` command is installed before anything.

I don't think we should install `gcloud`, but checking for its availability is a good point.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-15T07:28:29Z

> Are we able to set up `gcloud` command in https://github.com/kubernetes-sigs/kueue/blob/main/hack/releasing/wait_for_images.sh? Or, we might just check if `gcloud` command is installed before anything.

Created PR https://github.com/kubernetes-sigs/kueue/pull/6827.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-16T02:12:20Z

> > Are we able to set up `gcloud` command in https://github.com/kubernetes-sigs/kueue/blob/main/hack/releasing/wait_for_images.sh? Or, we might just check if `gcloud` command is installed before anything.
> 
> I don't think we should install `gcloud`, but checking for its availability is a good point.

That makes sense.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T09:19:40Z

The script `/hack/releasing/sync-notes.sh` does not work for full (minor) releases, I tried today `/hack/releasing/sync-notes.sh v0.14.0`

and got: 

```
## Changes by Kind

### API Change

- Graduated TopologyAwareScheduling to Beta. (#6830, @mbobrovskyi)

### Feature

- Add an alpha integration for Kubeflow Trainer to Kueue. (#6597, @kaisoz)
- Added workload_priority_class label for kueue_admission_wait_time_seconds metric. (#6885, @mbobrovskyi)
- Added workload_priority_class label for kueue_evicted_workloads_once_total metric. (#6876, @mbobrovskyi)
- Added workload_priority_class label for kueue_evicted_workloads_total metric. (#6860, @mbobrovskyi)
- Added workload_priority_class label for kueue_quota_reserved_workloads_total metric. (#6882, @mbobrovskyi)
- TODO (#5873, @alaypatel07)

### Bug or Regression

- Fix the bug that a workload going repeatedly via the preemption and re-admission cycle would accumulate the
  "Previously" prefix in the condition message, eg: "Previously: Previously: Previously: Preempted to accommodate a workload ...". (#6819, @amy)
- Pod-integration now correctly handles pods stuck in the Terminating state within pod groups, preventing them from being counted as active and avoiding blocked quota release. (#6872, @ichekrygin)

### Other (Cleanup or Flake)

- Added workload_priority_class label for kueue_admitted_workloads_total metric. (#6795, @mbobrovskyi)
- Promote ConfigurableResourceTransformations feature gate to stable. (#6599, @mbobrovskyi)
- Support for Kubernetes 1.34 (#6689, @mbobrovskyi)
```
This looks like work from the last 0.13.4, not from 0.13.0. For minor releases we should use 1.13.0 as the basis.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T09:30:46Z

Or even better we should use v0.14.0-devel because it will be on the same history line

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T15:32:19Z

Looks better, but still the `Changes since `v0.14.0-devel`:` is not ideal. Should be changes since "v0.13.0"

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T15:09:39Z

the releasing preparation script does not work for a new minor release:
```
❯ ./hack/releasing/prepare_pull.sh v0.14.0
github.com
  ✓ Logged in to github.com account mimowo (GITHUB_TOKEN)
  - Active account: true
  - Git operations protocol: https
  - Token: ghp_************************************
  - Token scopes: 'admin:org', 'admin:public_key', 'audit_log', 'project', 'read:discussion', 'read:enterprise', 'read:gpg_key', 'read:packages', 'read:repo_hook', 'read:ssh_signing_key', 'repo', 'user', 'workflow'
+++ Updating remotes...
Fetching upstream
Fetching origin
From https://github.com/kubernetes-sigs/kueue
   a51fd3e70..438e12ca8  release-0.13 -> upstream/release-0.13
!!! No release issue found for version v0.14.0. Please create 'Release v0.14.0' issue first.
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T15:13:46Z

> the releasing preparation script does not work for a new minor release:
> 
> ```
> ❯ ./hack/releasing/prepare_pull.sh v0.14.0
> github.com
>   ✓ Logged in to github.com account mimowo (GITHUB_TOKEN)
>   - Active account: true
>   - Git operations protocol: https
>   - Token: ghp_************************************
>   - Token scopes: 'admin:org', 'admin:public_key', 'audit_log', 'project', 'read:discussion', 'read:enterprise', 'read:gpg_key', 'read:packages', 'read:repo_hook', 'read:ssh_signing_key', 'repo', 'user', 'workflow'
> +++ Updating remotes...
> Fetching upstream
> Fetching origin
> From https://github.com/kubernetes-sigs/kueue
>    a51fd3e70..438e12ca8  release-0.13 -> upstream/release-0.13
> !!! No release issue found for version v0.14.0. Please create 'Release v0.14.0' issue first.
> ```

That has already been fixed by https://github.com/kubernetes-sigs/kueue/pull/7079
If you can update local main branch, everything will work well.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T15:17:35Z

I tried with the latest main. You referenced PR fixing another of the scripts

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-30T15:39:32Z

I think we need to prepare the same fix for prepare_pull.sh.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T15:52:43Z

I would like to also have a script which (might be separate scripts):
- opens a PR against k8s.io for promotion
- waits until promoted, basically `Wait for the PR to be merged and verify that the image registry.k8s.io/kueue/kueue:$VERSION is available. (and other images)`

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-30T15:57:39Z

> I tried with the latest main. You referenced PR fixing another of the scripts

Ah, that makes sense.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T17:04:32Z

I tried to use the ci_pull script for this step "Create the presubmits and the periodic jobs for the next patch release:" but no luck:

```
❯ ./hack/releasing/ci_pull.sh v0.14.0
github.com
  ✓ Logged in to github.com account mimowo (GITHUB_TOKEN)
  - Active account: true
  - Git operations protocol: https
  - Token: ghp_************************************
  - Token scopes: 'admin:org', 'admin:public_key', 'audit_log', 'project', 'read:discussion', 'read:enterprise', 'read:gpg_key', 'read:packages', 'read:repo_hook', 'read:ssh_signing_key', 'repo', 'user', 'workflow'
!!! No release issue found for version v0.14.0. Please create 'Release v0.14.0' issue first.
❯ ./hack/releasing/ci_pull.sh v0.14.0
github.com
  ✓ Logged in to github.com account mimowo (GITHUB_TOKEN)
  - Active account: true
  - Git operations protocol: https
  - Token: ghp_************************************
  - Token scopes: 'admin:org', 'admin:public_key', 'audit_log', 'project', 'read:discussion', 'read:enterprise', 'read:gpg_key', 'read:packages', 'read:repo_hook', 'read:ssh_signing_key', 'repo', 'user', 'workflow'
+++ Creating local branch kueue-ci-0.14-1759251757
fatal: 'upstream/master' is not a commit and a branch 'kueue-ci-0.14-1759251757' cannot be created from it

+++ Returning to the kueue-add-milestone branch.
!!! No branches specified for cleanup.
```
not sure how to use it

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T17:28:05Z

after some help from @mbobrovskyi it goes further but still fails:
```
❯ DRY_RUN=true ./hack/releasing/ci_pull.sh v0.14.0
github.com
  ✓ Logged in to github.com account mimowo (GITHUB_TOKEN)
  - Active account: true
  - Git operations protocol: https
  - Token: ghp_************************************
  - Token scopes: 'admin:org', 'admin:public_key', 'audit_log', 'project', 'read:discussion', 'read:enterprise', 'read:gpg_key', 'read:packages', 'read:repo_hook', 'read:ssh_signing_key', 'repo', 'user', 'workflow'
+++ Creating local branch kueue-ci-0.14-1759253157
branch 'kueue-ci-0.14-1759253157' set up to track 'upstream/master'.
Switched to a new branch 'kueue-ci-0.14-1759253157'
find: warning: you have specified the global option -maxdepth after the argument -type, but global options are not positional, i.e., -maxdepth affects tests specified before it as well as those specified after it.  Please specify global options before other arguments.
./kueue-presubmits-release-0-12.yaml has version 0.12, which is lower than the latest supported 0.14.
./kueue-periodics-release-0-12.yaml has version 0.12, which is lower than the latest supported 0.14.
usage: yq [-h] [--yaml-output] [--yaml-roundtrip] [--yaml-output-grammar-version {1.1,1.2}] [--width WIDTH] [--indentless-lists] [--explicit-start] [--explicit-end] [--in-place] [--version] [jq_filter] [files ...]
yq: error: argument files: can't open '(.periodics[].extra_refs[].base_ref) = "release-0.14"': [Errno 2] No such file or directory: '(.periodics[].extra_refs[].base_ref) = "release-0.14"'

+++ Returning to the master branch.
!!! Skipping deletion of branch kueue-ci-0.14-1759253157 because DRY_RUN is set.
To delete this branch manually:
  git branch -D kueue-ci-0.14-1759253157
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T04:01:54Z

> the releasing preparation script does not work for a new minor release:
> 
> ```
> ❯ ./hack/releasing/prepare_pull.sh v0.14.0
> github.com
>   ✓ Logged in to github.com account mimowo (GITHUB_TOKEN)
>   - Active account: true
>   - Git operations protocol: https
>   - Token: ghp_************************************
>   - Token scopes: 'admin:org', 'admin:public_key', 'audit_log', 'project', 'read:discussion', 'read:enterprise', 'read:gpg_key', 'read:packages', 'read:repo_hook', 'read:ssh_signing_key', 'repo', 'user', 'workflow'
> +++ Updating remotes...
> Fetching upstream
> Fetching origin
> From https://github.com/kubernetes-sigs/kueue
>    a51fd3e70..438e12ca8  release-0.13 -> upstream/release-0.13
> !!! No release issue found for version v0.14.0. Please create 'Release v0.14.0' issue first.
> ```

@mimowo @mbobrovskyi I fixed the above errors for all scripts in https://github.com/kubernetes-sigs/kueue/pull/7103.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-08T09:04:26Z

One more ask, the `prepare_pull.sh` should update the release issue description to inject the link to the "Update main with the latest v0.14.1" PR. And good if the opened PR is put on hold automatically if possible.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T07:02:09Z

wait_for_images.sh does not work for release-candidates:

```
❯ ./hack/releasing/wait_for_images.sh v0.15.0-rc.0
!!! Invalid release version. It should be semantic version like v0.13.2
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-13T11:31:01Z

> wait_for_images.sh does not work for release-candidates:
> 
> ```
> ❯ ./hack/releasing/wait_for_images.sh v0.15.0-rc.0
> !!! Invalid release version. It should be semantic version like v0.13.2
> ```

Done in https://github.com/kubernetes-sigs/kueue/pull/7636.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T16:00:55Z

It would be lovely to add kueue-populator images to /hack/releasing/wait_for_images.sh
cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T16:09:51Z

I have used `./hack/releasing/promote_pull.sh v0.13.10` and it generated correct diff, but failed on pushing the branch as a PR:

```
+++ I'm about to do the following to push to GitHub (and I'm assuming origin is your personal fork):

  git push origin kueue-promote-0.13-1764259580:kueue-promote-0.13

+++ Proceed (anything other than 'y' aborts it)? [y/N] y
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 64 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 833 bytes | 833.00 KiB/s, done.
Total 6 (delta 3), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
remote: 
remote: Create a pull request for 'kueue-promote-0.13' on GitHub by visiting:
remote:      https://github.com/mimowo/k8s.io/pull/new/kueue-promote-0.13
remote: 
To https://github.com/mimowo/k8s.io.git
 * [new branch]          kueue-promote-0.13-1764259580 -> kueue-promote-0.13

+++ Creating a pull request on GitHub at mimowo:kueue-promote-0.13 for main
expected the "[HOST/]OWNER/REPO" format, got "//github.com/kubernetes/k8s.io"
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-27T16:37:45Z

In my case, the command worked fine.

```shell
$ GITHUB_USER=tenzen-y KUBERNETES_K8S_IO_PATH=../../k8s.io/k8s.io KUBERNETES_REPOS_PATH=../../k8s.io ./hack/releasing/promote_pull.sh v0.14.5
github.com
  ✓ Logged in to github.com account tenzen-y (keyring)
  - Active account: true
  - Git operations protocol: https
  - Token: gho_************************************
  - Token scopes: 'gist', 'read:org', 'repo', 'workflow'
+++ Creating local branch kueue-promote-0.14-1764260736
branch 'kueue-promote-0.14-1764260736' set up to track 'upstream/main'.
Switched to a new branch 'kueue-promote-0.14-1764260736'
+++ Insert image charts/kueue@0.14.5:sha256:1ffede210ca2ccb64ecb2899402e135d390240d167222e192f9986b36d370b49
+++ Insert image kueue@v0.14.5:sha256:6f8528d7184e2116046f9ab5382017499f7edaf4f49fdcd15b1cdb8716c1ba0e
+++ Insert image kueueviz-backend@v0.14.5:sha256:bd82e4fd5d42b167744275f4adf54fd585c7c55e9f4577f24313ea832cdf328d
+++ Insert image kueueviz-frontend@v0.14.5:sha256:4dfbabeca194b7e6542fe0dfb1bd29897bc515abfb6eeae727710b08894aa3ba
[kueue-promote-0.14-1764260736 8a5e478a5] Kueue: Promote 0.14
 1 file changed, 4 insertions(+)

+++ I'm about to do the following to push to GitHub (and I'm assuming origin is your personal fork):

  git push origin kueue-promote-0.14-1764260736:kueue-promote-0.14

+++ Proceed (anything other than 'y' aborts it)? [y/N] y
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 16 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 822 bytes | 822.00 KiB/s, done.
Total 6 (delta 3), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
remote: 
remote: Create a pull request for 'kueue-promote-0.14' on GitHub by visiting:
remote:      https://github.com/tenzen-y/k8s.io/pull/new/kueue-promote-0.14
remote: 
To github.com:tenzen-y/k8s.io.git
 * [new branch]          kueue-promote-0.14-1764260736 -> kueue-promote-0.14

+++ Creating a pull request on GitHub at tenzen-y:kueue-promote-0.14 for main

Creating pull request for tenzen-y:kueue-promote-0.14 into main in kubernetes/k8s.io

https://github.com/kubernetes/k8s.io/pull/8811
https://github.com/kubernetes-sigs/kueue/issues/7856

+++ Returning to the main branch.
!!! Deleting branch kueue-promote-0.14-1764260736.
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-28T06:16:27Z

@mimowo @tenzen-y Did we miss anything else here, or can we close it?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-28T06:30:30Z

Let's wait for full 0.15 last time I remember issues with full release with updates to test-infra

Also. do you know what might be the problem here in my run 


+++ Creating a pull request on GitHub at mimowo:kueue-promote-0.13 for main expected the "[HOST/]OWNER/REPO" format, got "//github.com/kubernetes/k8s.io"

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-28T06:31:19Z

Can we automate the https://github.com/kubernetes-sigs/kueue/blob/926717dcaec54daa01039e28aa4d86c8273883fb/.github/ISSUE_TEMPLATE/NEW_RELEASE.md?plain=1#L27-L42 step?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-28T06:32:31Z

> Let's wait for full 0.15 last time I remember issues with full release with updates to test-infra
> 
> Also. do you know what might be the problem here in my run
> 
> +++ Creating a pull request on GitHub at mimowo:kueue-promote-0.13 for main expected the "[HOST/]OWNER/REPO" format, got "//github.com/kubernetes/k8s.io"

As I mentioned in https://github.com/kubernetes-sigs/kueue/issues/6288#issuecomment-3586727526, you might need to specify the repository path via `KUBERNETES_K8S_IO_PATH` and `KUBERNETES_REPOS_PATH`.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-28T06:40:49Z

> Also. do you know what might be the problem here in my run

> +++ Creating a pull request on GitHub at mimowo:kueue-promote-0.13 for main expected the "[HOST/]OWNER/REPO" format, got "//github.com/kubernetes/k8s.io"

As we can see @tenzen-y command working fine:

```
GITHUB_USER=tenzen-y KUBERNETES_K8S_IO_PATH=../../k8s.io/k8s.io KUBERNETES_REPOS_PATH=../../k8s.io ./hack/releasing/promote_pull.sh v0.14.5
github.com
```

Probably you should add `GITHUB_USER=mimowo` variable.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-28T06:45:39Z

I’m also wondering if it’s possible to run the entire release process in GitHub Actions CI – just trigger each step manually (manual workflow dispatch for each step) or just CI waiting each step. It would definitely be a big improvement.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-28T07:24:36Z

I see, I would like to request that the script fails fast when required params are not supplied (with the message requesting them), rather than late.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-28T07:27:08Z

Automating the whole pipeline as a GH action sounds good when we have the scripting ready.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-28T10:39:40Z

> I see, I would like to request that the script fails fast when required params are not supplied (with the message requesting them), rather than late.

We already have it here: https://github.com/kubernetes-sigs/kueue/blob/main/hack/releasing/promote_pull.sh#L74-L77.
I think you already set this variable, but it was probably incorrect.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-01-20T14:26:15Z

We may update the release issue template to reference the script. WDYT @tenzen-y @mimowo ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-20T14:41:49Z

> We may update the release issue template to reference the script. WDYT [@tenzen-y](https://github.com/tenzen-y) [@mimowo](https://github.com/mimowo) ?

That sounds good 👍

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T17:25:01Z

I propose to close the issue, because the objective is covered, and most issues have been caught already in 0.16.0

Sure not everything is ideal, but we can improve in follow up Issues / PRs with clearly defined scope.

 So if something you consider missing I propose opening dedicated issue with "Release automation:", wdyt?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-27T17:27:44Z

> I propose to close the issue, because the objective is covered, and most issues have been caught already in 0.16.0
> 
> Sure not everything is ideal, but we can improve in follow up Issues / PRs with clearly defined scope.
> 
> So if something you consider missing I propose opening dedicated issue with "Release automation:", wdyt?

SGTM, @mbobrovskyi Thank you for tremendous work here!

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T17:32:29Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-27T17:32:36Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6288#issuecomment-3806527929):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
