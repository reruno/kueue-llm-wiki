# Issue #232: Manage webhook cert internally

**Summary**: Manage webhook cert internally

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/232

**Last updated**: 2022-06-08T16:12:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-04-26T17:44:42Z
- **Updated**: 2022-06-08T16:12:23Z
- **Closed**: 2022-06-08T16:12:23Z
- **Labels**: `kind/feature`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 1

## Description

**What would you like to be added**:

#220 introduced a dependency on cert-manager.io to handle the certificates, as recommended by kubebuilder docs. It's useful to have our own certificate issuer internally.

Here is how HNC sets them up https://github.com/kubernetes-sigs/hierarchical-namespaces/blob/e3937b351d8cdc629f1063228236dd80413affe8/cmd/manager/main.go#L105

**Why is this needed**:

This simplifies deployment of kueue. cert-manager.io is a big dependency that we should try to avoid.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-05-17T01:57:38Z

I'm eager for this feature for some poc purposes, so I'd like to take a look first.
/assign
