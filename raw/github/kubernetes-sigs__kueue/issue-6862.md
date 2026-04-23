# Issue #6862: A follow-up to variadic option list to the Patch and PatchStatus

**Summary**: A follow-up to variadic option list to the Patch and PatchStatus

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6862

**Last updated**: 2025-09-17T07:22:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-09-16T17:34:29Z
- **Updated**: 2025-09-17T07:22:14Z
- **Closed**: 2025-09-17T07:22:14Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 1

## Description

This is a follow up to: https://github.com/kubernetes-sigs/kueue/pull/6792

This refactoring introduce in the above PR is a bit confusing. I understand the intent, to generalize patch options into a specific type so they can be passed as variadic arguments, but it feels premature. To justify this pattern, we should ideally have more than one option, right now there is only `WithNonStrict`.

It also looks like the options are limited by [`patchCommon`](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/client/client.go#L43) only effectively handling a single option. 
```go
func patchCommon(obj client.Object, update func() (client.Object, bool, error), patchFunc func(patch client.Patch) error, options ...ClientPatchOption) error {
	opts := DefaultClientPatchOptions()
	for _, opt := range options {
		opt(opts)
	}
	strict := opts.Strict // <-- unpacking a single option, and ignoring the rest.
	return updateAndPatch(obj, strict, update, patchFunc)
}
```

* pass a list of options,
* merge them with default list of options,
* unpack "Strict" option, ignoring all the rest (assuming there will be more than 1)

I get that we might add more fields later. If so, the current shape encourages “unpacking” each field before calling the next helper, which scales poorly. For example:

```go
type ClientPatchOptions struct {
    Strict bool
    Foo    int
    Bar    string
}
```

Current approach:

```go
func patchCommon(
    obj client.Object,
    update func() (client.Object, bool, error),
    patchFunc func(patch client.Patch) error,
    options ...ClientPatchOption,
) error {
    opts := DefaultClientPatchOptions()
    for _, opt := range options {
        opt(opts)
    }
    strict := opts.Strict
    foo := opts.Foo
    bar := opts.Bar
    return updateAndPatch(obj, strict, foo, bar, update, patchFunc)
}
```

A more scalable alternative, avoid extrapolating fields and pass the struct through:

```go
func patchCommon(
    obj client.Object,
    update func() (client.Object, bool, error),
    patchFunc func(patch client.Patch) error,
    options ...ClientPatchOption,
) error {
    opts := DefaultClientPatchOptions()
    for _, opt := range options {
        opt(opts)
    }
    return updateAndPatch(obj, opts, update, patchFunc)
}
```

And downstream:

```go
func updateAndPatch(
    obj client.Object,
    opts ClientPatchOptions,
    update func() (client.Object, bool, error),
    patchFn func(client.Patch) error,
) error {
    objOriginal := getOriginalObject(obj, opts)
    objPatched, updated, err := update()
    if err != nil || !updated {
        return err
    }
    patch, err := createPatch(objOriginal, objPatched)
    if err != nil {
        return err
    }
    return patchFn(patch)
}
```

And down:
```go
func getOriginalObject(obj client.Object, opts ClientPatchOptions) client.Object {
	objOriginal := obj.DeepCopyObject().(client.Object)
	if opts.Strict { // <-- Use option(s).
		// Clearing ResourceVersion from the original object to make sure it is included in the generated patch.
		objOriginal.SetResourceVersion("")
	}
	return objOriginal
}
```

**Summary:** with only a single option today, the change increases cognitive load without a clear payoff. 

If we do proceed with an options type, I recommend passing the options struct down the call chain rather than unpacking individual fields at each layer. This keeps call sites stable as more options are added and reduces boilerplate.

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-16T17:36:05Z

+ @mszadkow 

Please let me know if this issue makes sense. I’d really value your thoughts on the proposed “pushing options down” alternative, and whether you see it as a cleaner approach going forward.
