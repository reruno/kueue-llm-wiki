# Issue #1612: The cloudbuild doesn't include the git version and commit

**Summary**: The cloudbuild doesn't include the git version and commit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1612

**Last updated**: 2024-02-07T21:21:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-18T20:42:34Z
- **Updated**: 2024-02-07T21:21:54Z
- **Closed**: 2024-02-07T20:32:19Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What happened**:

From the cloudbuild logs:
```
#16 [linux/amd64 builder 7/7] RUN make build GO_BUILD_ENV='CGO_ENABLED=0 GOOS=linux GOARCH=${TARGETARCH}'
#16 0.159 fatal: not a git repository (or any of the parent directories): .git
#16 0.169 fatal: not a git repository (or any of the parent directories): .git
#16 0.170 CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-X 'sigs.k8s.io/kueue/pkg/version.GitVersion=' -X 'sigs.k8s.io/kueue/pkg/version.GitCommit='" -o bin/manager cmd/kueue/main.go
#16 ...
```

Whereas when building locally, the information is properly passed:

```
 => [linux/amd64->arm64 builder 7/7] RUN make build GO_BUILD_ENV='CGO_ENABLED=${CGO_ENABLED} GOOS=linux GOARCH=${TARGETARCH}'                                                                                                                                                                     9.1s
 => => # CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -ldflags="-X 'sigs.k8s.io/kueue/pkg/version.GitVersion=v0.6.0-devel-184-g155d225' -X 'sigs.k8s.io/kueue/pkg/version.GitCommit=155d22540caf241ff45dda36a5591e50d98b4f2f'" -o bin/manager cmd/kueue/main.g
```

**What you expected to happen**:

The cloudbuild to include the git information

**How to reproduce it (as minimally and precisely as possible)**:

https://storage.googleapis.com/kubernetes-jenkins/logs/post-kueue-push-images/1748070353755705344/artifacts/build.log

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-02-07T09:35:11Z

I see two ways to try and fix this:

1. add  `--with-git-dir` in the args lit of https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/k8s-staging-kueue.yaml.
2.  try to push the git info as Dokerfile args

1 is the easiest, the only downsize being that the content of the source tar will be aprox. 2x larger. If you are OK with this unhold kubernetes/test-infra#31870

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-07T16:45:34Z

> 1 is the easiest, the only downsize being that the content of the source tar will be aprox. 2x larger.

That should be fine... The tar is not part of the final image.

### Comment by [@trasc](https://github.com/trasc) — 2024-02-07T20:32:14Z

/close
Solved by https://github.com/kubernetes/test-infra/pull/31870

https://storage.googleapis.com/kubernetes-jenkins/logs/post-kueue-push-images/1755324624721154048/artifacts/build.log

```
Step #0: 
Step #0: #16 [linux/amd64->arm64 builder 7/7] RUN make build GO_BUILD_ENV='CGO_ENABLED=${CGO_ENABLED} GOOS=linux GOARCH=${TARGETARCH}'
Step #0: #16 0.251 CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -ldflags="-X 'sigs.k8s.io/kueue/pkg/version.GitVersion=v0.6.0-rc.1-38-g90fa327' -X 'sigs.k8s.io/kueue/pkg/version.GitCommit=90fa327609f86cd8e1b875e6307db28c51a22dd5'" -o bin/manager cmd/kueue/main.go
Step #0: #16 ...
Step #0: 
Step #0: #17 [linux/amd64 builder 7/7] RUN make build GO_BUILD_ENV='CGO_ENABLED=${CGO_ENABLED} GOOS=linux GOARCH=${TARGETARCH}'
Step #0: #0 0.253 CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-X 'sigs.k8s.io/kueue/pkg/version.GitVersion=v0.6.0-rc.1-38-g90fa327' -X 'sigs.k8s.io/kueue/pkg/version.GitCommit=90fa327609f86cd8e1b875e6307db28c51a22dd5'" -o bin/manager cmd/kueue/main.go
Step #0: #17 ...
Step #0: 
```

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-07T20:32:20Z

@trasc: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1612#issuecomment-1932818324):

>/close
>Solved by https://github.com/kubernetes/test-infra/pull/31870
>
>https://storage.googleapis.com/kubernetes-jenkins/logs/post-kueue-push-images/1755324624721154048/artifacts/build.log
>
>```
>Step #0: 
>Step #0: #16 [linux/amd64->arm64 builder 7/7] RUN make build GO_BUILD_ENV='CGO_ENABLED=${CGO_ENABLED} GOOS=linux GOARCH=${TARGETARCH}'
>Step #0: #16 0.251 CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -ldflags="-X 'sigs.k8s.io/kueue/pkg/version.GitVersion=v0.6.0-rc.1-38-g90fa327' -X 'sigs.k8s.io/kueue/pkg/version.GitCommit=90fa327609f86cd8e1b875e6307db28c51a22dd5'" -o bin/manager cmd/kueue/main.go
>Step #0: #16 ...
>Step #0: 
>Step #0: #17 [linux/amd64 builder 7/7] RUN make build GO_BUILD_ENV='CGO_ENABLED=${CGO_ENABLED} GOOS=linux GOARCH=${TARGETARCH}'
>Step #0: #0 0.253 CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-X 'sigs.k8s.io/kueue/pkg/version.GitVersion=v0.6.0-rc.1-38-g90fa327' -X 'sigs.k8s.io/kueue/pkg/version.GitCommit=90fa327609f86cd8e1b875e6307db28c51a22dd5'" -o bin/manager cmd/kueue/main.go
>Step #0: #17 ...
>Step #0: 
>```


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-07T21:21:53Z

```sh
$ docker run --rm gcr.io/k8s-staging-kueue/kueue:v0.6.0-rc.2                                                     
{"level":"info","ts":"2024-02-07T21:21:17.325515508Z","logger":"setup","caller":"kueue/main.go:122","msg":"Initializing","gitVersion":"v0.6.0-rc.2","gitCommit":"90fa327609f86cd8e1b875e6307db28c51a22dd5"}
```

😄
