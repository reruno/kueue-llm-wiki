# Issue #4249: ☂️ Release v0.11.0 features

**Summary**: ☂️ Release v0.11.0 features

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4249

**Last updated**: 2025-03-19T11:35:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-12T15:05:12Z
- **Updated**: 2025-03-19T11:35:41Z
- **Closed**: 2025-03-19T11:35:39Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 7

## Description

We are targeting the release on 17th March.

```[tasklist]
### Priorities
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3761
- [ ] https://github.com/kubernetes-sigs/kueue/pull/4228
- [ ] https://github.com/kubernetes-sigs/kueue/pull/3953
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3232
- [ ] https://github.com/kubernetes-sigs/kueue/issues/2341
- [ ] https://github.com/kubernetes-sigs/kueue/issues/2732
```

```[tasklist]
### Nice To Haves
- [ ] https://github.com/kubernetes-sigs/kueue/issues/4106
- [ ] https://github.com/kubernetes-sigs/kueue/issues/2552
- [ ] https://github.com/kubernetes-sigs/kueue/pull/3992
- [ ] https://github.com/kubernetes-sigs/kueue/pull/4174
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3822
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3754
- [ ] https://github.com/kubernetes-sigs/kueue/issues/4474
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T15:07:37Z

cc @tenzen-y @dgrove-oss @PBundyra @gabesaba @kannon92 @mwielgus @mwysokin 

Opening the issue to start compiling the list of features for visibility. I put what was on the top of my head, please let me know what is missing.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T15:11:19Z

cc @mbobrovskyi @mszadkow

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-12T20:36:45Z

Not sure if you need to list them, since I think they are both just pending final review but we should get #3992 and #4174 into 0.11

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-08T15:59:41Z

I have two requests for 0.11.

- https://github.com/kubernetes-sigs/kueue/pull/4385
- https://github.com/kubernetes-sigs/kueue/pull/4337

Could we add these to must haves for this release?

They are considered very important for my team.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-08T18:50:30Z

#4385 can probably be finalized with all things. But I do not think so for #4337 since, as I left comments on PR, there is some lack of consideration.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T11:35:35Z

/close
I think we are all set as the release is planned for tomorrow. We will track the release process itself in https://github.com/kubernetes-sigs/kueue/issues/4533

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T11:35:41Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4249#issuecomment-2736313461):

>/close
>I think we are all set as the release is planned for tomorrow. We will track the release process itself in https://github.com/kubernetes-sigs/kueue/issues/4533


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
