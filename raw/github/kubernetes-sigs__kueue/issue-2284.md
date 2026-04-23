# Issue #2284: Declare the versions of tools allowing for updates by dependabot

**Summary**: Declare the versions of tools allowing for updates by dependabot

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2284

**Last updated**: 2024-06-05T20:23:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-05-27T09:56:31Z
- **Updated**: 2024-06-05T20:23:47Z
- **Closed**: 2024-06-05T20:23:47Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow), [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 17

## Description

**What would you like to be cleaned**:

Declare the versions of the tools in `Makefile-deps` so that they are managed by dependabot ([example of hard-coded dependency](https://github.com/kubernetes-sigs/kueue/blob/ceaa3b1fff1e2d95a2d4695d16f99b0d9a8d4ec0/Makefile-deps.mk#L34)).

**Why is this needed**:

To reduce manual maintenance and make sure the tools are not lagging behind. This ensures Kueue is compatible with the latest versions of the tools.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-27T09:57:12Z

/cc @alculquicondor @tenzen-y 
Let me know if this was discussed or maybe there are some drawbacks.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-27T10:03:48Z

@mimowo Actually, we should move all tool versions into `hack/internal/tools`.

https://github.com/kubernetes-sigs/kueue/pull/882#pullrequestreview-1491398785

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-27T10:14:38Z

Yuki, thanks for the pointer. Will the `tools` dir have its own dedicated `go.mod` managed by dependabot, or the versions would be in the root `go.mod`?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-27T10:33:39Z

It indicates the root go.mod.
https://github.com/kubernetes-sigs/kueue/tree/a50d395c36a2cb3965be5232162cf1fded1bdb08/hack/internal/tools

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-27T10:44:59Z

sgtm, so IIUC we have the versions declared in the top `go.mod` and in the `hack/internal/tools` we import the tools sot that they are not removed by `go mod tidy`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-27T10:49:53Z

> sgtm, so IIUC we have the versions declared in the top `go.mod` and in the `hack/internal/tools` we import the tools sot that they are not removed by `go mod tidy`.

Exactly. It is similar approach as this: https://github.com/golang/go/wiki/Modules/6fe9f52ac7c4d92cb8fc878d8dee1bda0c63c8a5#how-can-i-track-tool-dependencies-for-a-module

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-28T09:28:36Z

Yes, for dependabot to be able to manage it - dependecies should be defined in go.mod
eg. Kustomize has all dev dependecies in hack: https://github.com/kubernetes-sigs/kustomize/blob/master/hack/go.mod

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-28T09:29:07Z

I can do
And that what was proposed in https://github.com/kubernetes-sigs/kueue/pull/2116 in "Special notes for your reviewer" section
Thanks for creating follow-up issue for that!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-28T12:12:39Z

/assign @vladikkuzn

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-05-29T09:16:16Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-06-04T12:32:30Z

#2334 is doing a good job to add the versions in the root `go.mod`, the problem is that in the future a module imported just for tool versioning (helm, kustomize, yq) will put unnecessary restrictions on modules we are actually using in the code. 
Then we should start thinking of having a dedicated  `hack/internal/tools/go.mod`. (we should be able to configure `.github/dependabot.yml` to manage that go.mod also)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-04T12:53:55Z

+1, we could follow up with the idea in the next PR

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-05T09:11:41Z

> +1, we could follow up with the idea in the next PR

SGTM

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-05T09:11:45Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2284#issuecomment-2149288463):

>> +1, we could follow up with the idea in the next PR
>
>SGTM
>
>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-05T12:29:49Z

@tenzen-y @mimowo @trasc 
Should we apply the same set of rules (ignores) in dependabot for tools?
Those are for root `go.mod`
```  - package-ecosystem: "gomod"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "ok-to-test"
      - "release-note-none"
    groups:
      kubernetes:
        patterns:
          - "k8s.io/*"
    ignore:
      # Ignore major and minor versions for dependencies updates
      # Allow patches and security updates.
      - dependency-name: k8s.io/*
        update-types: ["version-update:semver-major", "version-update:semver-minor"]
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-05T12:43:37Z

Yes, that seems appropriate

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-05T16:35:30Z

> @tenzen-y @mimowo @trasc Should we apply the same set of rules (ignores) in dependabot for tools? Those are for root `go.mod`
> 
> ```
>     directory: "/"
>     schedule:
>       interval: "weekly"
>     labels:
>       - "ok-to-test"
>       - "release-note-none"
>     groups:
>       kubernetes:
>         patterns:
>           - "k8s.io/*"
>     ignore:
>       # Ignore major and minor versions for dependencies updates
>       # Allow patches and security updates.
>       - dependency-name: k8s.io/*
>         update-types: ["version-update:semver-major", "version-update:semver-minor"]
> ```

SGTM, Thank you!
