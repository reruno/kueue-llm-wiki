# Issue #9872: Change workload name generation to ensure max 63 characters (fitting as label)

**Summary**: Change workload name generation to ensure max 63 characters (fitting as label)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9872

**Last updated**: 2026-03-26T18:58:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-13T15:09:18Z
- **Updated**: 2026-03-26T18:58:25Z
- **Closed**: 2026-03-26T18:58:25Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to change the workload name generation to cap them at 63 characters. 

I think this is not really breaking, because in Kueue we don't rely on the algorithm. We will just cut them shorter. 

Here is the algorithm generation: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/workload_names.go#L30-L34

For safety we should do it behind a feature gate.

**Why is this needed**:

Some users need to use workload names in external systems as labels.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T15:09:55Z

cc @tenzen-y @gabesaba @kannon92 @sohankunkerkar

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T15:11:10Z

I don't have any objections at all, but just curious about the motivation.
Just for readability?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T15:18:00Z

I'm reach out to folks to get more details, but for what I know this is not for readability, but fast lookups in some in-house system. Annotations unfortunately don't provide fast lookups.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-13T15:19:30Z

Hmm. This could be a problem for Jobset or sub Job integration as we base name on JobSet name plus replicated job name.

I'm not as familiar with this code but do we base the name on the actual workload. If so we could get conflicts if two jobs/jobsets have identical names up to the 64 characters.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T15:23:05Z

>  This could be a problem for Jobset or sub Job integration as we base name on JobSet name plus replicated job name.

We have the hash system in Kueue. So we truncate the job name at 57, and append 1 (-) + 5 characters for the hash.

Check the reference code: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/workload_names.go#L30-L34

Currently we truncate further.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T15:26:27Z

Actually, we probably already have a bug for that on MultiKueue and LWS because we use workload Name for the PrebuiltWorkloadName: https://github.com/kubernetes-sigs/kueue/blob/f09ca11fcf14f0253ef7aa8b2d2853b393e680ee/pkg/controller/jobs/leaderworkerset/leaderworkerset_pod_reconciler.go#L145

So, I think we could even consider this a bugfix, still certainly need to have a feature gate.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T18:58:40Z

> I'm reach out to folks to get more details, but for what I know this is not for readability, but fast lookups in some in-house system. Annotations unfortunately don't provide fast lookups.

I see, that sounds good to me.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-18T07:44:59Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-26T17:47:49Z

An analogous issue raised by another user: https://github.com/kubernetes-sigs/kueue/issues/10098. As I discuss it there, I'm leaning to have both appraoaches:
1. limit to 63 characters as opt-in
2. fix the bug for MK and LWS integrations by using annotations instead of labels even if the truncation to 63 characters is enabled
