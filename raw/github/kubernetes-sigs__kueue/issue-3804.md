# Issue #3804: Allow for feature gates to be configured via the configuration API

**Summary**: Allow for feature gates to be configured via the configuration API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3804

**Last updated**: 2024-12-11T14:28:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-12-10T20:47:46Z
- **Updated**: 2024-12-11T14:28:05Z
- **Closed**: 2024-12-11T14:28:05Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Feature gates should also be configurable via configuration API.

**Why is this needed**:

I am working on an operator to manage upgrades/configuring of Kueue. Since Kueue deployment uses a configmap I am able to "configure" kueue via changing values in the config map for other personas. 

My hope is to avoid changing the deployment spec of Kueue so I can keep the configuring and upgrades of kueue separate from having to change the deployment.

If users would like to enable feature gates, they would have to modify the CLI arguments of Kueue.

It would be ideal to have a corresponding API for feature gates in the configuration so one can specify either the CLI or the component config.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-11T07:54:41Z

This is the generic K8s way. For example, the kubeadm [ClusterConfiguration](https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/#kubeadm-k8s-io-v1beta4-ClusterConfiguration) has similar field.
So, we can accept this feature request.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T08:07:07Z

I can also see this useful. Currently adding the feature-gates to the Kueue Deployment in a script is a bit hacky, because it requires editing the command line "feature-gates" argument, which is not structured - so tricky to do with jq or yq.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T09:27:29Z

This change can also be used to adjust e2e configuration between suites, which can be helpful to finally e2e test manageJobsWithoutQueueName. cc @mbobrovskyi @dgrove-oss . In reference to https://github.com/kubernetes-sigs/kueue/issues/3767.
