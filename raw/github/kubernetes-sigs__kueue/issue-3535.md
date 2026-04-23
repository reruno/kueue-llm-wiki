# Issue #3535: [MultiKueue] Improve docs to link Multi-Cluster per CRD from Setup MultiKueue

**Summary**: [MultiKueue] Improve docs to link Multi-Cluster per CRD from Setup MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3535

**Last updated**: 2024-11-22T08:21:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-14T13:18:21Z
- **Updated**: 2024-11-22T08:21:31Z
- **Closed**: 2024-11-18T08:36:55Z
- **Labels**: `kind/documentation`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description


**What would you like to be added**:

Link https://kueue.sigs.k8s.io/docs/tasks/run/multikueue/ from https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/#in-the-manager-cluster.

In this section I think we can drop the JobSet installation and Kubeflow istallation and just say something like:
"for installation of CRDs compatible with MultiKueue please refer to the dedicated pages here".

**Why is this needed**:

To improve chances that users who go through "Setup MultiKueue" and want to use MPIJob or Kubeflow visit the dedicated pages.

This was the source of confusion here: https://kubernetes.slack.com/archives/C032ZE66A2X/p1731582793720509

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-14T13:18:36Z

/assign @mszadkow 
cc @mbobrovskyi @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-22T08:21:28Z

/kind documentation
/remove-kind feature
