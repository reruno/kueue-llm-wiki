# Issue #4729: e2e tests: control the specific image for k8s version in Kueue code

**Summary**: e2e tests: control the specific image for k8s version in Kueue code

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4729

**Last updated**: 2025-04-16T05:45:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-21T05:13:34Z
- **Updated**: 2025-04-16T05:45:07Z
- **Closed**: 2025-04-16T05:45:07Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 2

## Description

**What would you like to be cleaned**:

Introduce a mapping from the k8s minor version (set by test-infra) to the exact version of the image.

So, I imagine test-infra should only set `E2E_K8S_VERSION=1.31`. Then, Kueue makefile would map this value to the specific full version of the image like `kindest/node:v1.31.1`.

To make this pass on every step we probably need 3 steps:
1. introduce `E2E_K8S_VERSION` in test-infra along with `E2E_KIND_VERSION`
2. support `E2E_K8S_VERSION` in Kueue and map to `E2E_KIND_VERSION`
3. drop setting `E2E_KIND_VERSION`  in test-infra

**Why is this needed**:

Currently bumping the k8s node patch version is in the test-infra repo, and cannot be tested in kueue before merging. This makes it risky.

See https://github.com/kubernetes/test-infra/pull/34564#discussion_r2006322727.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T05:14:12Z

/cc @tenzen-y @mbobrovskyi @mszadkow @mykysha @vladikkuzn

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-03-23T21:56:18Z

/assign

I can take this if that's ok for you guys, since I've been working with `test-infra` in my last task. Let me know if anyone of you is already working on it and I'll unassign 👍🏻
