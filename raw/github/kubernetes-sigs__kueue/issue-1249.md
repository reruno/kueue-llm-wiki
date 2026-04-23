# Issue #1249: Add pages with automatically generated API documentation

**Summary**: Add pages with automatically generated API documentation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1249

**Last updated**: 2023-10-27T14:50:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-24T13:15:17Z
- **Updated**: 2023-10-27T14:50:33Z
- **Closed**: 2023-10-27T14:32:43Z
- **Labels**: `kind/feature`, `kind/documentation`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 4

## Description

**What would you like to be added**:

API documentation auto-generated from the types.go files.

/kind documentation

**Why is this needed**:

This is an easy way to browse the definition of every field of the API.

We should investigate how kubernetes API reference is generated and use similar tools

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-24T13:17:21Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2023-10-26T08:16:13Z

Preview link (using kubernetes-sigs/reference-docs/genref) https://deploy-preview-1263--kubernetes-sigs-kueue.netlify.app/docs/reference/kueue.v1beta1/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-27T13:58:58Z

/assign stuton
Can you add links from each Concept page into the relevant Reference docs?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-27T14:50:33Z

/unassign stuton

I opened a separate issue #1281
