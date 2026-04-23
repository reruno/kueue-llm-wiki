# Issue #4137: Problem serializing some Kueue types for logging

**Summary**: Problem serializing some Kueue types for logging

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4137

**Last updated**: 2025-03-04T13:07:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-02-03T14:26:18Z
- **Updated**: 2025-03-04T13:07:44Z
- **Closed**: 2025-03-04T13:07:44Z
- **Labels**: `kind/bug`
- **Assignees**: [@nasedil](https://github.com/nasedil)
- **Comments**: 8

## Description

**What happened**:
Observing error messages like the following in logs:

```
"nominatedAssignmentError": "json: unsupported type: resources.FlavorResourceQuantities"
"resourcesError": "json: unsupported type: resources.FlavorResourceQuantities"
"resourcesRequiringPreemptionError": "json: unsupported type: sets.Set[[sigs.k8s.io/kueue/pkg/resources.FlavorResource](http://sigs.k8s.io/kueue/pkg/resources.FlavorResource)]"
"usageError": "json: unsupported type: resources.FlavorResourceQuantities"
```

here are the lines, corresponding to v0.10.0
```
cache/snapshot.go:64
cache/snapshot.go:73
preemption/preemption.go:346
scheduler/logging.go:43
```

**What you expected to happen**:
These types should be serialized properly

**How to reproduce it (as minimally and precisely as possible)**:
Run integration tests with higher log verbosity, grep for json: unsupported type

**Anything else we need to know?**:
The scope of this bug includes identifying other types we fail to serialize - the list above is not necessarily exhaustive - and fixing those too

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`): v0.10.0

## Discussion

### Comment by [@nasedil](https://github.com/nasedil) — 2025-02-26T13:34:09Z

/assign

### Comment by [@nasedil](https://github.com/nasedil) — 2025-02-26T14:30:36Z

I've changed verbosity for integration tests in Makefile to '-vv' and ran `make test-integration | grep "unsupported"` but output is empty.  Could it be that I search for logs in a wrong place or run the tests incorrectly?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-26T14:33:17Z

Maybe try to adjust log level at the framework level (eg. -3 -> -5): https://github.com/kubernetes-sigs/kueue/blob/f8015cb273f9115c34f9be32b35f7e1308c16459/test/integration/framework/framework.go#L72

### Comment by [@nasedil](https://github.com/nasedil) — 2025-02-26T16:50:28Z

Thanks @mimowo that worked.

I can see only "resources.FlavorResourceQuantities" and "sets.Set[sigs.k8s.io/kueue/pkg/resources.FlavorResource]" appear in logs.  In code I see there is no serialization for any types.

For "sets.Set[sigs.k8s.io/kueue/pkg/resources.FlavorResource]" to be serializebale the type `k8s.io/apimachinery/pkg/util/sets.Set` should be serializable, from the upstream repository: https://github.com/kubernetes/apimachinery/blob/master/pkg/util/sets/set.go

I've created an issue there to sync: https://github.com/kubernetes/apimachinery/issues/187

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-26T16:52:38Z

Ok, but until done upstream we can probably just convert the set to slice easily.

EDIT: I other words I think we can just have the String function on our type which will do the custom serialization. I think logger checks on the object if its type implements the custom String.

### Comment by [@nasedil](https://github.com/nasedil) — 2025-02-26T17:45:13Z

For example, here is a place where it's logged:
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/preemption/preemption.go#L362 — here it unsuccessfully tries to serialize `preemptionCtx.frsNeedPreemption`

And here is how the `preemptionCtx.frsNeedPreemption` defined:
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/preemption/preemption.go#L73

Do you suggest passing to logger something like `preemptionCtx.getFrsNeedPreemptionString()` which converts `preemptionCtx.frsNeedPreemption` to a serializable format?

> Ok, but until done upstream we can probably just convert the set to slice easily.
> 
> EDIT: I other words I think we can just have the String function on our type which will do the custom serialization. I think logger checks on the object if its type implements the custom String.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-26T17:56:14Z

> Do you suggest passing to logger something like preemptionCtx.getFrsNeedPreemptionString() which converts preemptionCtx.frsNeedPreemption to a serializable format?

No, I was thinking to wrap the set into a type with "String" function, something like:

type sets.Set[resources.FlavorResource] FlavorResourceSet

func (s *FlavorResourceSet) String() string {
  return "xyz"
}

would this work? I haven't tried, so it might not actually work, dunno.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-26T18:10:54Z

> Thanks [@mimowo](https://github.com/mimowo) that worked.
> 
> I can see only "resources.FlavorResourceQuantities" and "sets.Set[sigs.k8s.io/kueue/pkg/resources.FlavorResource]" appear in logs. In code I see there is no serialization for any types.
> 
> For "sets.Set[sigs.k8s.io/kueue/pkg/resources.FlavorResource]" to be serializebale the type `k8s.io/apimachinery/pkg/util/sets.Set` should be serializable, from the upstream repository: https://github.com/kubernetes/apimachinery/blob/master/pkg/util/sets/set.go
> 
> I've created an issue there to sync: [kubernetes/apimachinery#187](https://github.com/kubernetes/apimachinery/issues/187)

NOTE: The library issue was migrated to https://github.com/kubernetes/kubernetes/issues/130452
