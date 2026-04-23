# Issue #7597: Kueue doesn't propagate Pod template batch.kubernetes.io/job-name label to ProvReq's PodTemplate

**Summary**: Kueue doesn't propagate Pod template batch.kubernetes.io/job-name label to ProvReq's PodTemplate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7597

**Last updated**: 2025-11-17T12:31:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Created**: 2025-11-10T14:10:44Z
- **Updated**: 2025-11-17T12:31:40Z
- **Closed**: 2025-11-17T12:31:40Z
- **Labels**: `kind/bug`
- **Assignees**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Comments**: 1

## Description

**What happened**:
PodTemplate has a pod affinity rule to match batch.kubernetes.io/job-name label. The label wasn't present on (fake) pods which were created through ProvisioningRequests that leads to failed scale up simulation, however the label was present on Job PodTemplate object.

It happens because Kueue explicitly removes job-name label from PodTemplate: [link](https://www.google.com/url?q=https://github.com/kubernetes-sigs/kueue/pull/1358/files%23diff-f278bdcf60c86f048f29eeef3fa2ee16447d577a7d3d6d0a3dce33626ffed260R214&sa=D&source=buganizer&usg=AOvVaw0ap7PP_530moXxNqJKCwJ4)

## Discussion

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-11-10T14:10:55Z

/assign
