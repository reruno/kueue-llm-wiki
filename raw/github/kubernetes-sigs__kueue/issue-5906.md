# Issue #5906: Introduce a library for mocking in unit tests and consolidate current mocks

**Summary**: Introduce a library for mocking in unit tests and consolidate current mocks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5906

**Last updated**: 2025-09-08T07:15:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-08T17:28:48Z
- **Updated**: 2025-09-08T07:15:29Z
- **Closed**: 2025-09-08T07:15:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Use a library, like uber-go/mock to consolidate the mocking for GenericJob:
- testGenericJob in validation_test.go and (almost identical copy) in base_webhook_test.go

This was first proposed in https://github.com/kubernetes-sigs/kueue/pull/5510#discussion_r2183633446 

**Why is this needed**:

To simplify the test code, and avoid duplication for writing mocks per-test.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T17:28:58Z

cc @tenzen-y @ichekrygin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-08T17:57:55Z

Is it only for Unit Test, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-08T17:58:56Z

Yes, updated title

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-08T18:00:48Z

In terms of uber-go/mock vs testify, +1 on uber-go/mock since it is originally came from Go std library.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-28T09:12:23Z

/assign

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-04T22:17:41Z

Hi @mbobrovskyi, while working on an unrelated PR I came across a need to use a mock for the GenericJob interface.
I’m not sure if you’ve made progress on this issue yet, but if not, I have a PR almost ready that adds this functionality, so I was wondering if you would be open to me taking over this issue in that case?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-04T22:45:35Z

> Hi [@mbobrovskyi](https://github.com/mbobrovskyi), while working on an unrelated PR I came across a need to use a mock for the GenericJob interface.
> I’m not sure if you’ve made progress on this issue yet, but if not, I have a PR almost ready that adds this functionality, so I was wondering if you would be open to me taking over this issue in that case?

Please disregard. I had "outdated" view on the issue, and entirely missed your PR. I just closed mine.
