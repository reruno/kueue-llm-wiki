# Issue #2978: [kjobctl] The example does not work as copy-paste

**Summary**: [kjobctl] The example does not work as copy-paste

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2978

**Last updated**: 2024-09-04T12:53:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-04T11:04:10Z
- **Updated**: 2024-09-04T12:53:24Z
- **Closed**: 2024-09-04T12:53:24Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

**What happened**:

I tried to use the example from kjobctl help as copy-paste

```
  kjobctl create job \ 
	--profile my-application-profile  \
	--cmd "sleep 5" \
	--parallelism 4 \
	--completions 4 \ 
	--request cpu=500m,ram=4Gi \
	--localqueue my-local-queue-name
```
but it fails with 
```
Error: Job.batch "sample-profile-5xcvd" is invalid: [spec.template.spec.containers[0].resources.requests[ram]: Invalid value: ram: must be a standard resource type or fully qualified, spec.template.spec.containers[0].resources.requests[ram]: Invalid value: ram: must be a standard resource for containers]
```
It works fine when replacing `ram` with `memory`.

**What you expected to happen**:

The examples should be copy-paste.

**How to reproduce it (as minimally and precisely as possible)**:

Use the example from the help.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T11:04:24Z

/assign @mbobrovskyi 
/cc @mwysokin
