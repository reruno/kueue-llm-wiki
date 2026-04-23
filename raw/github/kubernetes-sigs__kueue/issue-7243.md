# Issue #7243: Update hugo library

**Summary**: Update hugo library

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7243

**Last updated**: 2025-11-20T10:26:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-13T12:15:21Z
- **Updated**: 2025-11-20T10:26:04Z
- **Closed**: 2025-11-20T10:26:04Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Update hugo library for website buillding, as the bump by dependabot is failing https://github.com/kubernetes-sigs/kueue/pull/7235

**Why is this needed**:

To unblock bumping of the important library

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T11:35:35Z

Might be related to https://github.com/gohugoio/hugo/issues/14103#issuecomment-3472039834 as found by @tenzen-y 

PTAL: https://github.com/kubernetes-sigs/kueue/pull/7396#issuecomment-3472625656

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T11:36:49Z

cc @mbobrovskyi @tenzen-y

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-01T06:02:12Z

Not sure where we can change the build image — probably in the repository settings?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-06T14:28:07Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-10T11:06:25Z

Seems that the solution had been found - https://github.com/kubernetes/website/issues/53108

> > Netlify's older Ubuntu 20.04 (Focal) image has GLIBC 2.31 so any newer Hugo will fail. The fix is to move the site to the newer build image that includes newer GLIBC. Can you please try the following:
> > Switch the build image to Ubuntu 22.04 (Jammy) via your Netlify dashboard > Site settings > Build & deploy > Environment > Build image selection > Choose Ubuntu 22.04 (Jammy)
>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-10T15:36:19Z

> Seems that the solution had been found - [kubernetes/website#53108](https://github.com/kubernetes/website/issues/53108)
> 
> > > Netlify's older Ubuntu 20.04 (Focal) image has GLIBC 2.31 so any newer Hugo will fail. The fix is to move the site to the newer build image that includes newer GLIBC. Can you please try the following:
> > > Switch the build image to Ubuntu 22.04 (Jammy) via your Netlify dashboard > Site settings > Build & deploy > Environment > Build image selection > Choose Ubuntu 22.04 (Jammy)

Yes, that's right. As I mentioned in the referenced link, we need to find a way to change the base image.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-12T09:07:32Z

@tenzen-y It seems the only way is to use Netlify UI - https://answers.netlify.com/t/please-read-end-of-support-for-xenial-build-image-everything-you-need-to-know/68239/27

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-14T08:14:24Z

https://kubernetes.slack.com/archives/C1J0BPD2M/p1763108044690619
/cc @mimowo @tenzen-y
