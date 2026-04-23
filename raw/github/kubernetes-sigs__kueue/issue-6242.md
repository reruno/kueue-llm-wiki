# Issue #6242: Add validation for PodSet Grouping

**Summary**: Add validation for PodSet Grouping

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6242

**Last updated**: 2025-10-15T07:37:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Created**: 2025-07-29T12:57:34Z
- **Updated**: 2025-10-15T07:37:03Z
- **Closed**: 2025-10-14T13:21:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
In https://github.com/kubernetes-sigs/kueue/pull/5845 we have added a possibility to schedule leader with workers. A new annotation "podset-group-name" has been introduced, but without explicit user-friendly validation. The goal of this issue is to have proper validation in place:
- Make sure that a specific PodSet Group name is used in 2 PodSets. If it is used in only 1 PodSet it does not make sense from the user perspective and suggests misconfiguration. At the same time algorithm is considering only 2 PodSets when grouping so it does not work for more than 2 PodSets.
- Make sure value PodSet Group name annotations adheres to regexp: [a-z][a-z0-9]*.
- The annotations "podset-required-topology"/"podset-preferred-topology" and value of them have to match in both grouped PodSets. In other words - both have to use the same required or preferred annotation and the requested topology in both has to match.
- Make sure that at least one of the PodSets has only 1 Pod
- PodSet Slices cannot be requested with PodSet Grouping

**Why is this needed**:
User might misconfigure the Leader and Workers co-location and it would not be obvious for them to debug what is wrong. Validation will surface any misconfigurations.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kshalot](https://github.com/kshalot) — 2025-08-28T10:18:29Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-02T17:06:56Z

If we want validation, should we make it a proper API rather than an annotation/label?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-02T17:51:31Z

This is a Pod annotation. We cannot add it to the API.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-02T23:36:10Z

> This is a Pod annotation. We cannot add it to the API.

Ah I see.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T15:50:53Z

@kshalot @PBundyra where are we with the status, it this accurate?

- [ ] Make sure that a specific PodSet Group name is used in 2 PodSets. If it is used in only 1 PodSet it does not make sense from the user perspective and suggests misconfiguration. At the same time algorithm is considering only 2 PodSets when grouping so it does not work for more than 2 PodSets.
- [x] Make sure value PodSet Group name annotations adheres to regexp: [a-z][a-z0-9]*.
- [ ] The annotations "podset-required-topology"/"podset-preferred-topology" and value of them have to match in both grouped PodSets. In other words - both have to use the same required or preferred annotation and the requested topology in both has to match.
- [ ] Make sure that at least one of the PodSets has only 1 Pod
- [x] PodSet Slices cannot be requested with PodSet Grouping

### Comment by [@kshalot](https://github.com/kshalot) — 2025-09-29T15:57:09Z

What you posted is accurate.

1. Name validation was added in #6708.
1. Slicing validation was added in #7051.

The rest is WIP, likely covered in a single PR, hopefully by EOD/tomorrow morning.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T07:37:03Z

After the picture looks complete: https://github.com/kubernetes-sigs/kueue/pull/7061

- [x] Make sure that a specific PodSet Group name is used in 2 PodSets. If it is used in only 1 PodSet it does not make sense from the user perspective and suggests misconfiguration. At the same time algorithm is considering only 2 PodSets when grouping so it does not work for more than 2 PodSets.
- [x] Make sure value PodSet Group name annotations adheres to regexp: [a-z][a-z0-9]*.
- [x] The annotations "podset-required-topology"/"podset-preferred-topology" and value of them have to match in both grouped PodSets. In other words - both have to use the same required or preferred annotation and the requested topology in both has to match.
- [x] Make sure that at least one of the PodSets has only 1 Pod
- [x] PodSet Slices cannot be requested with PodSet Grouping
