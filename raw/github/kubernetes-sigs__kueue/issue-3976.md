# Issue #3976: Examples directory not where README says it is

**Summary**: Examples directory not where README says it is

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3976

**Last updated**: 2025-01-16T11:46:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@cortadocodes](https://github.com/cortadocodes)
- **Created**: 2025-01-15T15:40:27Z
- **Updated**: 2025-01-16T11:46:34Z
- **Closed**: 2025-01-16T11:46:34Z
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 6

## Description

**What happened**:
The link to the examples in the [README usage](https://github.com/kubernetes-sigs/kueue?tab=readme-ov-file#usage) section takes me to [this](https://github.com/kubernetes-sigs/kueue/blob/main/examples). Relatedly, the usage code snippets also assume an `examples` directory at the top level which is a link to the same place instead of (what I think is) the [actual examples directory](https://github.com/kubernetes-sigs/kueue/tree/main/site/static/examples).

**What you expected to happen**:
I think it's supposed to link [here](https://github.com/kubernetes-sigs/kueue/tree/main/site/static/examples).

**How to reproduce it (as minimally and precisely as possible)**:
Click on the "examples" link in the "Usage" section of the README (see above).

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-15T22:18:07Z

It may have went away with the move to the site. Do the links in the website work for you?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-15T22:33:44Z

https://github.com/kubernetes-sigs/kueue/blob/main/examples is a symbolic link, and that is our expectation.
I'm open to replacing the README link with the actual place.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-16T09:06:35Z

Indeed, the link from the README page does not work in a browser. Replacing the link with `https://github.com/kubernetes-sigs/kueue/tree/main/site/static/examples` sgtm. Would you like to submit a PR @cortadocodes ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-16T09:07:16Z

/kind documentation
/remove-kind bug

### Comment by [@cortadocodes](https://github.com/cortadocodes) — 2025-01-16T09:20:58Z

@kannon92 I looked in the docs but couldn't find the page corresponding to that part of the README

@mimowo I'll make one now

### Comment by [@cortadocodes](https://github.com/cortadocodes) — 2025-01-16T09:34:03Z

Here's the PR! https://github.com/kubernetes-sigs/kueue/pull/3982
