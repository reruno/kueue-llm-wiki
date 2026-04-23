# Issue #825: Missing rbac role for RayJob

**Summary**: Missing rbac role for RayJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/825

**Last updated**: 2023-06-06T18:56:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-05-31T20:15:41Z
- **Updated**: 2023-06-06T18:56:34Z
- **Closed**: 2023-06-06T15:28:13Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

**What happened**:

Job and MPIJob have roles in https://github.com/kubernetes-sigs/kueue/blob/main/config/components/rbac,
RayJobs don't have one

**What you expected to happen**:

RayJob should have roles

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

IIRC, these roles were manually created. Perhaps as output from kubebuilder, but they are not recreated with codegen.
Please double check.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-31T20:15:48Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2023-06-06T08:34:38Z

@alculquicondor , they look to be created manually. I, personally,  don't find the added value of having them to be significant. The important part, in my opinion, is to have the manager able to work with the job types which is done by kubebuilder. 

If we insist to have them, I could do it for rayJobs as well.

(also a more clean approach wold be to have `mpijob_editor_role.yaml` defined as an aggregate on `rbac.authorization.kubeflow.org/aggregate-to-kubeflow-mpijobs-admin: "true"`)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T15:25:49Z

we do aggregate user roles using labels https://github.com/kubernetes-sigs/kueue/blob/6e3852c9c5eec15d3454f6b37c54d952e989248f/config/components/rbac/job_editor_role.yaml#L6-L8

### Comment by [@trasc](https://github.com/trasc) — 2023-06-06T17:48:46Z

> we do aggregate user roles using labels
> 
> https://github.com/kubernetes-sigs/kueue/blob/6e3852c9c5eec15d3454f6b37c54d952e989248f/config/components/rbac/job_editor_role.yaml#L6-L8

What I meant to say was that in something like `mpijob_editor_role.yaml` intead of writing Kinds and verbes, write an aggregator rule that selects the "official" (defined in kubeflow) mpijob-editor role.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-06T18:56:34Z

Ah, I see what you mean.

yeah, I would be ok dropping the individual roles from the frameworks that provide them and add the selector to the aggregated role.
