# Issue #435: Add dependabot for managing dependencies

**Summary**: Add dependabot for managing dependencies

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/435

**Last updated**: 2022-11-25T18:54:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2022-11-23T20:52:03Z
- **Updated**: 2022-11-25T18:54:05Z
- **Closed**: 2022-11-25T18:54:05Z
- **Labels**: `kind/feature`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We should add a bot to automatically upgrade our dependencies in go.mod.
**Why is this needed**:

Managing dependencies is tedious and can become a security problem if left alone for too long.
**Completion requirements**:

To do this, one just needs to add a dependabot.yml file to the .github

See below for an example:
https://github.com/kubernetes-sigs/controller-runtime/blob/master/.github/dependabot.yml

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-23T21:04:54Z

let's take kubernetes libraries as an example:

Would the bot update to 1.26 when it's released? Or would it update to 1.25 when 1.24 is out of support?

### Comment by [@kannon92](https://github.com/kannon92) — 2022-11-23T21:09:26Z

To be clear, it looks at what you have in your go.mod so it would upgrade k8s.io/client-go v0.24.3 to the latest when there is a release.  

We can tell the bot to ignore dependencies if you want to control kubernetes apis closer

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-23T21:11:05Z

if there is support for semantic versioning, it would be nice to upgrade to the latest patch version, but not minor.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-11-23T21:12:11Z

You can see an example of a PR it creates here https://github.com/G-Research/armada/pull/1670 and it has a decent amount of options.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-23T21:25:25Z

Ah, it's possible: https://github.blog/changelog/2021-05-21-dependabot-version-updates-can-now-ignore-major-minor-patch-releases/

### Comment by [@kannon92](https://github.com/kannon92) — 2022-11-25T17:58:17Z

/assign @kannon92 

I'll go ahead and add the yml.  If we don't like it, we can just remove it from repo very easily.
