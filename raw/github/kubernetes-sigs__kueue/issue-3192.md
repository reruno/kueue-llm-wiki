# Issue #3192: ☂️ Release v0.9.0 requirements

**Summary**: ☂️ Release v0.9.0 requirements

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3192

**Last updated**: 2024-11-05T21:30:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-04T13:14:00Z
- **Updated**: 2024-11-05T21:30:44Z
- **Closed**: 2024-11-05T21:30:42Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 11

## Description

We are targeting the release for the first week of Nov 2024, with a release candidate in the second half of Oct.

```[tasklist]
### Must Haves
- [x] https://github.com/kubernetes-sigs/kueue/pull/2909
- [x] https://github.com/kubernetes-sigs/kueue/pull/2864
- [x] https://github.com/kubernetes-sigs/kueue/issues/2973
- [ ] https://github.com/kubernetes-sigs/kueue/issues/2937
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3095
- [ ] https://github.com/kubernetes-sigs/kueue/issues/2717
- [ ] https://github.com/kubernetes-sigs/kueue/issues/2724
- [ ] https://github.com/kubernetes-sigs/kueue/issues/1353
```

Note that at #2717, we may need to drop LWS support.

```[tasklist]
### Nice To Haves
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3094
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3125 
- [ ] https://github.com/kubernetes-sigs/kueue/issues/2778 
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3174 
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3122
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3232
- [ ] https://github.com/kubernetes-sigs/kueue/issues/3257
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-04T13:14:55Z

/cc @tenzen-y @alculquicondor @mwielgus @mwysokin @dgrove-oss 
PTAL and let me know if something is missing or needs to be re-prioritized

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-04T13:17:55Z

/cc @trasc

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-04T13:26:59Z

/cc @andrewsykim

### Comment by [@kannon92](https://github.com/kannon92) — 2024-10-04T20:17:08Z

Could we maybe add an API promotion to this release or the next one? https://github.com/kubernetes-sigs/kueue/issues/768

I have been asked to find out how stable the Kueue API is and when can we expect stability.

(I think it should be fine but folks would like to know what kinds of guarantees we would have with using Kueue).

It seems that the project is pretty stable and has a lot of users. Can we discuss about stabilizing the core API?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-07T07:34:33Z

+1, thanks for raising this. Given we are just a month away from the planned 0.9 release it is unlikely to be included, as it would increase the risk of extending the release timeline. I would consider this as one of the major themes for the next release. 

We will use this release to give a deprecation warning for some APIs we want to drop, like https://github.com/kubernetes-sigs/kueue/issues/2437, https://github.com/kubernetes-sigs/kueue/issues/2256 or https://github.com/kubernetes-sigs/kueue/issues/3094.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-07T10:17:14Z

I would like to move #768 after the HierarchyCohort and TAS graduate to beta since both features introduce significant changes to the Kueue, and we can imagine evolving the API based on user feedback on both features.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-17T14:18:16Z

Additionally, this is a lightweight nice to have: https://github.com/kubernetes-sigs/kueue/issues/3257
But, this has a significant UX-improving impact on the MultiKueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-22T08:39:58Z

I make the following changes:
- moved https://github.com/kubernetes-sigs/kueue/issues/2724 and https://github.com/kubernetes-sigs/kueue/issues/1353 to must haves (based on the user requests we get)
- moved https://github.com/kubernetes-sigs/kueue/issues/3094 as nice to have (but still high priority)
- dropped https://github.com/kubernetes-sigs/kueue/issues/3231 and https://github.com/kubernetes-sigs/kueue/issues/3258

Also added nice to have https://github.com/kubernetes-sigs/kueue/issues/3257. Cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-24T13:54:47Z

FYI: opened the issue to track the release: https://github.com/kubernetes-sigs/kueue/issues/3302. For now, we have the release candidate, please test, report issues and propose fixes :)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T21:30:38Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-05T21:30:43Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3192#issuecomment-2458187345):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
