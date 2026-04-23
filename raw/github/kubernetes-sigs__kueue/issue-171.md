# Issue #171: Add webhook for APIs defaulting and validation

**Summary**: Add webhook for APIs defaulting and validation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/171

**Last updated**: 2022-09-01T20:36:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-04-04T21:07:52Z
- **Updated**: 2022-09-01T20:36:16Z
- **Closed**: 2022-09-01T20:36:16Z
- **Labels**: `kind/feature`, `priority/important-soon`, `kind/productionization`
- **Assignees**: [@knight42](https://github.com/knight42)
- **Comments**: 26

## Description


A webhook for APIs defaulting and validation; see example: https://book.kubebuilder.io/cronjob-tutorial/webhook-implementation.html

## Discussion

### Comment by [@knight42](https://github.com/knight42) — 2022-04-13T14:40:48Z

@ahg-g Hi! I would like to volunteer!
/assign

Could you please tell me the defaulting rule and the validation rule, such as which values needs defaulting?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-13T15:15:09Z

In terms of defaulting, we are using CRD defaults, like this one: https://github.com/kubernetes-sigs/kueue/blob/f8e104a886599c075fd1521c71eb063d64a6663e/apis/core/v1alpha1/workload_types.go#L66

That works if you don't set it through a yaml. But I think it doesn't work if you submit the object through the client, like we do in https://github.com/kubernetes-sigs/kueue/blob/425bf7f9e9499df0fc20edd717be7071e200979d/pkg/controller/workload/job/job_controller.go#L330

So you could start adding those defaults.

Next, we can look into validation. We don't have an exhaustive list yet, but you could start validating all the enums and integers (most of them should only be positive). You can go through all the APIs and check what makes sense to validate.

### Comment by [@knight42](https://github.com/knight42) — 2022-04-13T15:27:50Z

@alculquicondor Hi! Thanks for your comments, that would definitely be a good start!

I am trying to follow the steps described in https://book.kubebuilder.io/cronjob-tutorial/webhook-implementation.html to scaffold the webhook, but I failed:
```
$ git diff PROJECT
diff --git PROJECT PROJECT
index bab428b..93389ef 100644
--- PROJECT
+++ PROJECT
@@ -12,7 +12,7 @@ resources:
   domain: x-k8s.io
   group: kueue
   kind: Queue
-  path: sigs.k8s.io/kueue/api/v1alpha1
+  path: sigs.k8s.io/kueue/apis/core/v1alpha1
   version: v1alpha1
 - api:
     crdVersion: v1

$ kubebuilder create webhook --group kueue --version v1alpha1 --kind Queue --defaulting --programmatic-validation
Writing kustomize manifests for you to edit...
Error: failed to create webhook: unable to scaffold with "kustomize.common.kubebuilder.io/v1": error updating resource: unable to update Resource (Path "sigs.k8s.io/kueue/apis/core/v1alpha1") with another with non-matching Path "sigs.k8s.io/kueue/apis/kueue/v1alpha1"
...
```
It seems the current project layout confused `kubebuilder`, shall we rename `apis/core` to `apis/kueue`? Or am I missing something?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-13T17:11:19Z

It seems that we didn't do a good job keeping the `PROJECT` file in-sync with the renames. It looks like you have to change:

```
group: core
```

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T17:50:47Z

Changing to the group to `core` is going to produce `core.x-k8s.io` as the group name for future apis (including crd file names) instead of `kueue.x-k8s.io`; so I don't think we should change the group.

perhaps only update the paths.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T17:59:46Z

I think for kubebuilder tool to work smoothly we indeed need to move `core` to `kueue`, which sounds redundant, but might unfortunately be necessary if we want to continue to rely on the kubebuilder tool

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-13T18:43:24Z

Opened #219

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-08T16:35:56Z

Now that we started with `Workload`, do we believe we are done with defaulting and validation for that resource? Should some fields be marked immutable (e.g., PodSets)?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-09T13:20:54Z

as a hole? Are we sold on the idea of not adding the node affinities to the Workload, but add them directly to the Job?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-09T13:59:36Z

>  Are we sold on the idea of not adding the node affinities to the Workload

Is there a setup where we would consider adding affinities to the workload itself?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-09T19:00:26Z

I'm trying to think of ways to avoid the custom controllers to look at the ResourceFlavors and only look at the Workload.

Although, just directly modifying the Workload's pod specs is probably not the best idea. Maybe at admission time we can add the node labels somewhere in the `.spec.admission` struct.

So, you are right, making the PodSpecs immutable makes sense.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-10T00:04:58Z

Adding the labels to spec.admission makes sense I think.

ok, lets round up the workload validation with making the spec immutable and then perhaps we focus on the next one, queue is probably the easier?

@knight42 would you like to send a PR validating that the PodSet is immutable?

### Comment by [@knight42](https://github.com/knight42) — 2022-05-10T03:24:22Z

> @knight42 would you like to send a PR validating that the PodSet is immutable?

Yeah I am glad to do that!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-12T20:01:52Z

Did you already add a webhook for Queue? It would be useful to make `.spec.clusterQueue` immutable.

### Comment by [@knight42](https://github.com/knight42) — 2022-05-13T15:03:35Z

> Did you already add a webhook for Queue? It would be useful to make `.spec.clusterQueue` immutable.

Nope, now there is only webhook for `Workload`. I will add it in upcoming days.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-06T20:15:10Z

We should also validate Workload updates. We probably want to make most of the fields immutable. Also, we should disallow changing the queue of an Admitted workload.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-13T19:22:49Z

To track what is left, lets try and list the validations we want to do:

- [x] **Workload validation**
1. Queue and Admitted fields are immutable on update once set. 

- [x] **Queue validation** https://github.com/kubernetes-sigs/kueue/pull/264

1. ClusterQueue is a valid name.
1. ClusterQueue is immutable

- [ ] **ClusterQueue validation**

1. Two resources can either have completely different flavors or they must share all flavors and their order. 
2. Resource name is a valid name
3. NamespaceSelector is a valid selector
4. Quota: max > min
5. Resource flavor name is a valid name

- [x] **ResourceFlavor validation** https://github.com/kubernetes-sigs/kueue/pull/299
1. Validate labels

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-13T19:23:09Z

@alculquicondor  anything else?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-13T19:35:01Z

edited the comment above

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-07-19T11:35:02Z

/cc

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-27T16:18:51Z

@kerthcet do you want to send a PR for CQ validation?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-07-27T16:41:23Z

Yes, I'll finish it soon.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-28T23:59:08Z

Almost there, only one left is validating CQ

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-09T10:27:10Z

FYI: We only leave one validation now.

`Two resources can either have completely different flavors or they must share all flavors and their order.`

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-08-09T18:29:17Z

> FYI: We only leave one validation now.
> 
> `Two resources can either have completely different flavors or they must share all flavors and their order.`

We need to do that as well, we have scheduling logic assuming that this is validated.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-01T20:36:16Z

Done
