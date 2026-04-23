# Issue #8017: Duplicated reference docs

**Summary**: Duplicated reference docs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8017

**Last updated**: 2025-12-01T15:58:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@MichalZylinski](https://github.com/MichalZylinski)
- **Created**: 2025-12-01T09:46:42Z
- **Updated**: 2025-12-01T15:58:27Z
- **Closed**: 2025-12-01T15:58:27Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: Current reference documentation (https://kueue.sigs.k8s.io/docs/reference/) has duplicated articles covering Kueue API and Kueue Configuration API for beta v1 and beta v2.

**What you expected to happen**:

There should be only one article for each of these items, presenting only the most recent (beta v2) version of the API.

**How to reproduce it (as minimally and precisely as possible)**:

See: https://kueue.sigs.k8s.io/docs/reference/

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T09:47:31Z

@mbobrovskyi @mszadkow

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-01T11:04:26Z

/assign @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T15:12:31Z

I propose for a while to maintain v1beta1 reference, posted the comment there: https://github.com/kubernetes-sigs/kueue/pull/8023#discussion_r2577484029
