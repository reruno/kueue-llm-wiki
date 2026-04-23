# Issue #5719: Alpha integration with prerelease of Kubeflow Trainer v2

**Summary**: Alpha integration with prerelease of Kubeflow Trainer v2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5719

**Last updated**: 2025-09-16T20:11:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-23T10:56:39Z
- **Updated**: 2025-09-16T20:11:54Z
- **Closed**: 2025-09-16T19:12:12Z
- **Labels**: `kind/feature`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 16

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently, [Kubeflow Trainer v2 has prerelease](https://github.com/kubeflow/trainer/releases/tag/v2.0.0-rc.0), so it would be good to have an "alpha" integration to detect possible issues.

**Why is this needed**:

Short term to provide early feedback and make sure there are no roadblocks for the full integration in https://github.com/kubernetes-sigs/kueue/issues/3884

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T10:57:34Z

cc @tenzen-y @andreyvelich @mwysokin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-23T10:58:13Z

This is duplicated with https://github.com/kubernetes-sigs/kueue/issues/3884

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T11:01:17Z

> This is duplicated with https://github.com/kubernetes-sigs/kueue/issues/3884

I see, I'm ok to close then, but maybe we can rename as "Alpha integration with Kubeflow Trainer v2" using the pre-release for early feedback?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T11:01:35Z

/retitle Alpha integration with prerelease of Kubeflow Trainer v2

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-23T11:10:11Z

One big problem is that the TrainJob nodeSelector (`.spec.podSpecOverrides[*].nodeSelector`) and tolerarations (`.spec.podSpecOverrides[*].tolerations`) are immutable fields: https://github.com/kubeflow/trainer/blob/b71a69064fa033c2ca51f6a24dbe199b552cada9/pkg/apis/trainer/v1alpha1/trainjob_types.go#L113-L116

We need to relax this validation when TrainJob is suspended.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T11:19:30Z

Yes, so doing the Alpha integration may uncover more issues.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-23T11:22:19Z

> Yes, so doing the Alpha integration may uncover more issues.

Opened: https://github.com/kubeflow/trainer/issues/2679

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-04T07:07:34Z

The v2.0.0-rc.1 has already been released which is Kueue compatible version.
Additonally, I confirmed that both Trainer v1 and v2 versions could be imported to the Kueue repository, together.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-04T08:41:21Z

Awesome, thank you!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-04T09:18:03Z

Are there any volunteers in the community to prototype the integration? The goal would be not necessarily to squeeze it into 0.13, but rather to discover any potential blockers for the integration.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-07-04T10:50:51Z

/assign

This one sounds interesting so I volunteer to work on it :)

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2025-07-04T17:25:23Z

Thank you for your help @kaisoz! FYI, the integration for TrainJob might look similar as for JobSet given that we use similar job conditions: https://github.com/kubernetes-sigs/kueue/tree/main/pkg/controller/jobs/jobset

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T18:50:03Z

Is it not sufficient to use JobSet integration?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-04T06:08:21Z

First, to hide the technical detail of using JobSet by Trainer. 

However, there are also more pragmatic issues: 
1. MultiKueue support needs to create also other resources on the worker clusters which JobSet woudn't create 
2. There are issues synchronizing suspend on trainer and JobSet, which seems to go Trainer -> Jobset, but here we would need JobSet-> Trainer.

Actually I think @kaisoz performed already some experiments and hit issues due to (2.).

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-08-04T15:38:37Z

@mimowo @kannon92 

Yes! The main problem is that the child Jobset is created by the TrainJob controller, so when the Jobset integration suspends the Jobset, the Trainer reconciles it back to align its suspend state with the TrainJob. This is effectively a blocker, so I started implementing a native TrainJob integration.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-16T20:11:54Z

Follow ups are tracked here: https://github.com/kubernetes-sigs/kueue/issues/6865
