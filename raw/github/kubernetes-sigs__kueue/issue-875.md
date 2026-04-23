# Issue #875: Build images using kube-cross

**Summary**: Build images using kube-cross

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/875

**Last updated**: 2023-06-26T12:35:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-19T12:02:17Z
- **Updated**: 2023-06-26T12:35:49Z
- **Closed**: 2023-06-26T12:35:49Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

**What would you like to be cleaned**:

Use image `registry.k8s.io/build-image/kube-cross` instead of golang.

**Why is this needed**:

The build/test bots are hitting a lot of quota issues with docker registry.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-06-19T12:24:26Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-06-20T13:32:13Z

One problem with `registry.k8s.io/build-image/kube-cross` is the image size which is approximately 7X bigger that the one we are currently using. 
![Screenshot from 2023-06-19 17-37-22](https://github.com/kubernetes-sigs/kueue/assets/55734665/4bf8ddd1-66da-4acd-a3df-c985adc1b364)

An alternative could be to run all the e2e in a single job,  resulting in replacing 4x6min jobs with 1x10min. (#879)
[sample-run](https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/879/pull-kueue-test-e2e-main-1-27/1671143445764247552)
