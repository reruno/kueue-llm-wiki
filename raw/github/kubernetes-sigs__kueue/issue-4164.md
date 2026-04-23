# Issue #4164: Support the use of Cert Manager

**Summary**: Support the use of Cert Manager

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4164

**Last updated**: 2025-04-24T18:29:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-02-06T14:43:32Z
- **Updated**: 2025-04-24T18:29:39Z
- **Closed**: 2025-04-24T18:29:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 19

## Description

For my workflow, we want to rely on Cert Manager for deploying Kueue.

We found a few problems with using the upstream manifests.

I opened up https://github.com/kubernetes-sigs/kueue/pull/4082 but there is some more work needed.

- [x] https://github.com/kubernetes-sigs/kueue/pull/4082 
   -  Fix cert manager manifests
- [x] make sure the cert-manager supports running webhooks for all Job CRDs (like JobSet, KubeRay, KubeflowJobs etc),
- [x] use for metrics endpoint. 
  As discussed also in the https://github.com/kubernetes-sigs/kueue/issues/3259#issuecomment-2578652710 and https://github.com/kubernetes-sigs/kueue/pull/4082#issuecomment-2623625040

- [x] Verify step for cert manager manifests
- [x] e2e test



Verify step can be as simple as confirming that kustomize build works with Cert Manager configs

E2E test should be a simple test to verify kueue deployment works and we can follow [4112](https://github.com/kubernetes-sigs/kueue/pull/4112) as a template for how to test custom configs.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-06T14:45:27Z

/kind feature

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-02-06T18:26:19Z

/assign sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-07T07:16:25Z

/retitle Support the use of Cert Manager

Proposal, I think "coverage" could be mistakenly understood as just tests.

I would also like to add to the requirements:
- use for metrics endpoint. As discussed also in the [comments](https://github.com/kubernetes-sigs/kueue/issues/3259#issuecomment-2578652710) and [here](https://github.com/kubernetes-sigs/kueue/pull/4082#issuecomment-2623625040)
- make sure the cert-manager supports running webhooks for all Job CRDs (like JobSet, KubeRay, KubeflowJobs etc), I'm not sure it was done as part of the work [here](https://github.com/kubernetes-sigs/kueue/pull/4082), @kannon92 ?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-24T14:21:52Z

I created https://github.com/kubernetes-sigs/kueue/issues/4377 for metrics endpoint. Right now one cannot use cert manager with prometheus as their are no options provided to configure it.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-02-25T21:32:07Z

>make sure the cert-manager supports running webhooks for all Job CRDs (like JobSet, KubeRay, KubeflowJobs etc),

I'm able to verify this by installing cert-manager using this [manifest](https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml) and running an e2e test suite for the single-cluster setup, which looks fine. Is there anything else I need to confirm? I will be writing an e2e test for this to further strengthen things.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-03-03T16:32:55Z

Is the idea here to enable cert-manager by default or make it opt-in?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-03T16:33:58Z

opt-in.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-03T16:46:41Z

I think the idea is to make sure we have some kind of CI protection that Cert Manager integration still works.

We can inject a custom config and run e2e tests just to make sure everything works as intended.

Correct @mimowo?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-03T16:52:03Z

Yes, automated E2e tests for the cert manager would be awesome. I think you can try to use the customconfigs CI job and the suite for the purpose.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T17:15:34Z

/reopen 
to complete the testing of the support

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-18T17:15:39Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4164#issuecomment-2734092653):

>/reopen 
>to complete the testing of the support


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-18T17:16:29Z

For posterity, https://github.com/kubernetes-sigs/kueue/pull/4579#issuecomment-2722262381.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T18:10:33Z

@sohankunkerkar I think ideally, we also have an e2e test (part of the new certmanager suite), but for metrics endpoint.

We already have some testing for metrics, but we use -k, as the certs are self-signed and not trusted, see [here](https://github.com/kubernetes-sigs/kueue/blob/016692ab8908263063e1ef252edcf232bfafd738/test/e2e/singlecluster/metrics_test.go#L577). wdyt?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-03-18T18:27:11Z

I think that's a good suggestion. I'll work on adding that.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-24T17:47:13Z

@sohankunkerkar @mimowo anything outstanding on this?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-24T18:21:40Z

not from me, I'm good to close, along with https://github.com/kubernetes-sigs/kueue/issues/3259

@kannon92 and @sohankunkerkar thank you for all the effort!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-24T18:26:09Z

thank you everyone. I'm fine with closing this one as well

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-24T18:29:33Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-24T18:29:38Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4164#issuecomment-2828528009):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
