# Issue #9229: Rename packages that conflict with Go standard library package names

**Summary**: Rename packages that conflict with Go standard library package names

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9229

**Last updated**: 2026-02-15T10:26:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-02-13T17:02:44Z
- **Updated**: 2026-02-15T10:26:01Z
- **Closed**: 2026-02-15T10:26:01Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 11

## Description

**What would you like to be cleaned**:

Several packages in the codebase use names that conflict with Go standard library packages, triggering the revive `var-naming` rule: *"avoid package names that conflict with Go standard library package names"*. These are currently suppressed via exclusion rules in `.golangci.yaml` (added in the golangci-lint v2.9.0 upgrade). The packages should be renamed to remove the exclusions.

ref: https://github.com/kubernetes-sigs/kueue/pull/9199

Affected packages fall into three categories:

**1. Utility packages shadowing stdlib (`pkg/util/`)**
- `pkg/util/cmp/` → conflicts with `cmp`
- `pkg/util/heap/` → conflicts with `container/heap`
- `pkg/util/maps/` → conflicts with `maps`
- `pkg/util/slices/` → conflicts with `slices`
- `pkg/util/strings/` → conflicts with `strings`
- `pkg/util/testing/` → conflicts with `testing`

**2. Test wrapper packages using `package testing` instead of their directory name (`pkg/util/testingjobs/`)**
- `jaxjob/`, `job/`, `mpijob/`, `pytorchjob/`, `tfjob/`, `trainjob/`, `xgboostjob/` all declare `package testing`

**3. Other packages**
- `cmd/kueuectl/app/list/` → conflicts with `container/list`
- `cmd/kueuectl/app/testing/` → conflicts with `testing`
- `cmd/kueuectl/app/version/` → conflicts with `go/version`
- `pkg/metrics/` → conflicts with `runtime/metrics`
- `pkg/version/` → conflicts with `go/version`
- `test/integration/singlecluster/importer/` → conflicts with `go/importer`

**Why is this needed**:

- Following Go best practices for package naming avoids confusion and potential shadowing issues.
- Removes 13 linter exclusion rules from `.golangci.yaml` that were added as a workaround during the golangci-lint v2.9.0 upgrade.
- Category 2 packages (testingjobs subdirs) are the simplest to fix — they just need their package declaration changed to match their directory name. Category 1 may require more thought on naming. Category 3 may or may not warrant renaming depending on the effort/disruption tradeoff.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-13T17:06:50Z

cc @tenzen-y @mbobrovskyi

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-13T17:10:45Z

Thank you for opening this tracking issue.
I want to evaluate if it would be worth replacing all those package names before proceeding.
Because I believe that some of those seem still well-named-scope.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-13T18:40:26Z

/kind cleanup

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-13T18:44:06Z

> Thank you for opening this tracking issue. I want to evaluate if it would be worth replacing all those package names before proceeding. Because I believe that some of those seem still well-named-scope.

Have we also checked if any of the utlities could be replaced by golang std lib?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-13T18:50:50Z

> > Thank you for opening this tracking issue. I want to evaluate if it would be worth replacing all those package names before proceeding. Because I believe that some of those seem still well-named-scope.
> 
> Have we also checked if any of the utlities could be replaced by golang std lib?

Yes, we have.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-13T19:06:30Z

I opened up a PR to address 2. https://github.com/kubernetes-sigs/kueue/pull/9236

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T18:30:26Z

I don't think that those changes are valuable. Indeed, we make an alias (`utilXYZ`) if it is the same std package name like `slices`. So, I would propose disabling this detection at all.

```yaml
linters:
  settings:
    revive:
      enable-default: true
      enable-default-rules: true
      rules:
        - name: var-naming
          arguments:
           - []
           - []
           - - skip-package-name-collision-with-go-std: true
```

https://revive.run/r#var-naming

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-14T19:17:16Z

Yea I was trying to address it and it seems to be difficult and not much value.

We already exclude this rule by adding exceptions where the failure occur. I think going forward having packages avoid conflicts with stdlib is a good change.

But I think maybe we should just close this issue as most of these I don't think are worth fixing.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T19:39:14Z

> Yea I was trying to address it and it seems to be difficult and not much value.
> 
> We already exclude this rule by adding exceptions where the failure occur. I think going forward having packages avoid conflicts with stdlib is a good change.
> 
> But I think maybe we should just close this issue as most of these I don't think are worth fixing.

I think that the avove my proposed golangci-lint.yaml could reduce redundant configurations. So, I think that replacing current redundant ones with the above would be better.

Indeed, enabling the stdlib collision check by default is still a topic of discussion. So, I would propose to disable that altogether.

https://github.com/mgechev/revive/issues/1637
https://github.com/mgechev/revive/issues/1602

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-14T19:42:53Z

Let me clarify my proposal:

1. Remove https://github.com/kubernetes-sigs/kueue/blob/9c069eab72732d108916b88ba07f401e9daba766/.golangci.yaml#L113-L160 configurations
2. Add the following configuration to disable std lib name collision check at all:

```yaml
linters:
  settings:
    revive:
      enable-default: true
      enable-default-rules: true
      rules:
        - name: var-naming
          arguments:
           - []
           - []
           - - skip-package-name-collision-with-go-std: true
```

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-15T03:44:33Z

@tenzen-y opened up https://github.com/kubernetes-sigs/kueue/pull/9244.
