# Issue #5983: Graduate ManagedJobsNamespaceSelector to GA

**Summary**: Graduate ManagedJobsNamespaceSelector to GA

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5983

**Last updated**: 2025-07-17T05:28:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-07-15T16:22:41Z
- **Updated**: 2025-07-17T05:28:25Z
- **Closed**: 2025-07-17T05:28:25Z
- **Labels**: _none_
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 6

## Description

This is a very useful feature and I like to discuss what would be needed to graduate this feature to GA.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-16T02:55:01Z

/assign

Opened up https://github.com/kubernetes-sigs/kueue/pull/5987.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-16T07:36:50Z

@kannon92 @mimowo Will we graduate only ManagedJobsNamespaceSelector to GA in v0.13, and drop ManagedJobsNamespaceSelectorAlwaysRespected in v0.14?

https://github.com/kubernetes-sigs/kueue/blob/f4a78e032c0d116860d7dff15d445952a65e6904/keps/3589-manage-jobs-selectively/kep.yaml#L26-L28

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T08:09:56Z

I prefer to give users more time to provide feedback before GA-ing ManagedJobsNamespaceSelectorAlwaysRespected, so I would suggest 0.15.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-16T09:18:00Z

> I prefer to give users more time to provide feedback before GA-ing ManagedJobsNamespaceSelectorAlwaysRespected, so I would suggest 0.15.

SGTM

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-16T10:13:24Z

I see them as different features. And given that we are building upon the OP feature I wanted to see if we should graduate this feature.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-16T13:34:24Z

> I see them as different features. And given that we are building upon the OP feature I wanted to see if we should graduate this feature.

IIUC, the ManagedJobsNamespaceSelectorAlwaysRespected was introduced for making migraion period.
So, I'm ok with removing it in the v0.15. If @kannon92 want to keep it for a while, it is also ok for me.
