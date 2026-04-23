# Issue #7841: Make verify fails if invoked twice locally due to kal-linter

**Summary**: Make verify fails if invoked twice locally due to kal-linter

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7841

**Last updated**: 2025-12-19T09:58:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-24T10:40:38Z
- **Updated**: 2025-12-19T09:58:15Z
- **Closed**: 2025-12-19T09:58:14Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What happened**:

`make verify` fails on 
```
❯ make verify
go mod tidy
git --no-pager diff --exit-code go.mod go.sum
find . -path ./site -prune -false -o -name go.mod -exec dirname {} \; | xargs -I {} sh -c 'cd "{}" && /xyz/go/src/sigs.k8s.io/kueue/bin/golangci-lint run  --timeout 15m0s --config "/xyz/go/src/sigs.k8s.io/kueue/.golangci.yaml"'
0 issues.
0 issues.
0 issues.
0 issues.
cd hack/kal-linter; /xyz/go/src/sigs.k8s.io/kueue/bin/golangci-lint custom; mv bin/golangci-lint-kube-api-linter /xyz/go/src/sigs.k8s.io/kueue/bin
Error: build process: clone golangci-lint: git clone --branch v2.4.0 --single-branch --depth 1 -c advice.detachedHead=false -q https://github.com/golangci/golangci-lint.git: exit status 128
The command is terminated due to an error: build process: clone golangci-lint: git clone --branch v2.4.0 --single-branch --depth 1 -c advice.detachedHead=false -q https://github.com/golangci/golangci-lint.git: exit status 128
make: *** [Makefile-deps.mk:77: golangci-lint-kal] Error 3
```


**What you expected to happen**:

It does not fail on the folder pre-existing. Either remove it each time, or just ignore if pre-existing.

**How to reproduce it (as minimally and precisely as possible)**:

Run `make verify` twice locally

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T10:40:49Z

cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T20:07:07Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T20:13:39Z

/unassign

I can't reproduce this.

I ran `make verify` twice and I got no error.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-24T20:14:19Z

Your path seems odd.

```
/xyz/go/src/sigs.k8s.io/kueue/bin/golangci-lint
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T10:30:32Z

Yeah, I just put /xyz instead my full path on the machine, other than that it looks normal, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:58:09Z

/close
To avoid distactions, maybe this is just my env. I will investigate locally and report again maybe later

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-19T09:58:15Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7841#issuecomment-3674371714):

>/close
>To avoid distactions, maybe this is just my env. I will investigate locally and report again maybe later


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
