# Issue #671: Docs on installing kueue from main branch fails on Zsh Terminals

**Summary**: Docs on installing kueue from main branch fails on Zsh Terminals

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/671

**Last updated**: 2023-04-04T12:29:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@moficodes](https://github.com/moficodes)
- **Created**: 2023-04-03T17:17:31Z
- **Updated**: 2023-04-04T12:29:55Z
- **Closed**: 2023-04-04T12:29:55Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When installing kueue from Github main branch

```bash
kubectl apply -k github.com/kubernetes-sigs/kueue/config/default?ref=main
```

On a mac with zsh terminal we get the output

```bash
zsh: no matches found: github.com/kubernetes-sigs/kueue/config/default?ref=main
```

**What you expected to happen**:

Install Kueue on the k8s cluster.

**How to reproduce it (as minimally and precisely as possible)**:

Any zsh terminal.

Adding the url in `""` would fix this.
