# Issue #7170: Possible .dockerignore misconfiguration

**Summary**: Possible .dockerignore misconfiguration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7170

**Last updated**: 2025-10-14T07:33:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tomokinakamaru](https://github.com/tomokinakamaru)
- **Created**: 2025-10-06T05:20:20Z
- **Updated**: 2025-10-14T07:33:37Z
- **Closed**: 2025-10-14T07:33:37Z
- **Labels**: _none_
- **Assignees**: [@tomokinakamaru](https://github.com/tomokinakamaru)
- **Comments**: 2

## Description

Hello, and thank you for your work on this repository!

As part of my research, I am analyzing how developers configure .dockerignore in popular repositories.

During my analysis, I noticed that `/.dockerignore` might have been written under the assumption that .dockerignore and .gitignore follow the same pattern semantics, while they actually differ.[^1] In particular, the following pattern drew my attention:

https://github.com/kubernetes-sigs/kueue/blob/5d4deceddfb098361108c92f42225bbae1edfb2d/.dockerignore#L48

According to Docker's specification, this pattern matches `node_modules` only in the top-level directory. (To ignore `node_modules` in any directory, the .dockerignore file needs to list `**/node_modules`)

Was this pattern written intentionally? If not, I'd be happy to submit a pull request to adjust it.

And if possible, could you tell me whether you were aware of the difference between .dockerignore and .gitignore? (I would like to know whether the differences are generally well recognized, or if they tend to slip developers' minds.)

Thank you again for maintaining this repository!

[^1]: See [.gitignore doc](https://git-scm.com/docs/gitignore), [.dockerignore doc](https://docs.docker.com/build/concepts/context/#dockerignore-files), and [a blog post about the differences](https://zzz.buzz/2018/05/23/differences-of-rules-between-gitignore-and-dockerignore/)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T08:44:45Z

> According to Docker's specification, this pattern matches node_modules only in the top-level directory. (To ignore node_modules in any directory, the .dockerignore file needs to list **/node_modules)

Nice spot, thank you!

> Was this pattern written intentionally?

I don't think it was intentional. The code of frontend (iirc only module using node modules) is under /cmd/kueueviz/frontend, so the current line in the dockerfile is no-op

>  If not, I'd be happy to submit a pull request to adjust it.

Awesome, you are welcome.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T08:45:06Z

/assign tomokinakamaru
