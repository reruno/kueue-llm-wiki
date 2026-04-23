# Issue #8837: Consolidate `jobframework.WebhookLogConstructor` and `roletracker.WebhookLogConstructor` into one.

**Summary**: Consolidate `jobframework.WebhookLogConstructor` and `roletracker.WebhookLogConstructor` into one.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8837

**Last updated**: 2026-02-26T07:16:50Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-27T18:18:18Z
- **Updated**: 2026-02-26T07:16:50Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@hungtruongOwolf](https://github.com/hungtruongOwolf)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

This is a follow-up of https://github.com/kubernetes-sigs/kueue/pull/8786#discussion_r2732145768.

I'd propose to consolidate 2 types of `WebhookLogConstructor` implemented in the following `jobframework` and `roletracker` packages into one.

- https://github.com/kubernetes-sigs/kueue/blob/aba66da127bbd338640b530f3e99befddd86cbe6/pkg/controller/jobframework/base_webhook.go#L120-L126
- https://github.com/kubernetes-sigs/kueue/blob/b16846e896cf07bc97205d2bd72fc1c6dff52104/pkg/util/roletracker/logger.go#L58-L64

I guess that we can add `gvk` argument to roletracker package one like the following:

- opt 1: static `gvk` argument:

```go
func WebhookLogConstructor(tracker *RoleTracker, gvk schema.GroupVersionKind) func(logr.Logger, *admission.Request) logr.Logger {
	return func(base logr.Logger, req *admission.Request) logr.Logger {
		log := admission.DefaultLogConstructor(base, req)
		return log.WithValues("replica-role", GetRole(tracker)).WithValues("webhookGroup", gvk.Group, "webhookKind", gvk.Kind)
	}
}
```

- opt 2: dynamic `keysAndValues` pattern:

```go
func WebhookLogConstructor(tracker *RoleTracker, keysAndValues ...any) func(logr.Logger, *admission.Request) logr.Logger {
	return func(base logr.Logger, req *admission.Request) logr.Logger {
		log := admission.DefaultLogConstructor(base, req).
			WithValues("replica-role", GetRole(tracker))
		if len(keysAndValues) != 0 {
			log = log.WithValues(keysAndValues...)
		}
		return log
	}
}
```

**Why is this needed**:

We currently have 2 types of `WebhookLogConstructor` in the`jobframework` and `roletracker` packages, which are duplicated across multiple packages, and the expected usages are mostly the same.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-27T18:18:34Z

cc @mszadkow

### Comment by [@hungtruongOwolf](https://github.com/hungtruongOwolf) — 2026-02-26T03:21:30Z

Hi @tenzen-y , is anyone currently working on this? If not, I'd like to be assigned.

### Comment by [@hungtruongOwolf](https://github.com/hungtruongOwolf) — 2026-02-26T04:10:42Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-26T07:16:37Z

> Hi [@tenzen-y](https://github.com/tenzen-y) , is anyone currently working on this? If not, I'd like to be assigned.

Thank you for your interest in this issue, feel free to work on this.
