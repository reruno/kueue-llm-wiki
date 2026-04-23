# Issue #8606: Visibility server ignores recommended flags

**Summary**: Visibility server ignores recommended flags

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8606

**Last updated**: 2026-03-11T13:17:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2026-01-15T10:53:20Z
- **Updated**: 2026-03-11T13:17:43Z
- **Closed**: 2026-03-11T13:17:43Z
- **Labels**: `kind/bug`
- **Assignees**: [@olekzabl](https://github.com/olekzabl), [@Nilsachy](https://github.com/Nilsachy)
- **Comments**: 8

## Description

Kueue version: 0.15.0

### Observed error

When trying to deploy Kueue with a custom Kubeconfig (specified in the `--kubeconfig` command-line flag to the container command for `kueue-controller-manager`), I get an error:

```
Unable to create and start visibility server","error":"unable to apply VisibilityServerOptions: failed to get delegated authentication kubeconfig: failed to get delegated authentication kubeconfig: ...
```

where `...` is initially 
```
unable to load in-cluster configuration, KUBERNETES_SERVICE_HOST and KUBERNETES_SERVICE_PORT must be defined
```
which can be by-passed (at least in my case) by passing `localhost` and `443` as the values of env-vars for the container, but then the error comes back with `...` expanding to
```
open /var/run/secrets/kubernetes.io/serviceaccount/token: no such file or directory
```
which I haven't found a way (in my case) to work around easily.

### Analysis

The root cause, I think, is that the library used to set up the API client enters [this path](https://github.com/kubernetes/apiserver/blob/6b942bcbe7b5563399e5df3e37711e5438298413/pkg/server/options/authentication.go#L473) even though the `--kubeconfig` flag has been used, which should have led to entering [this `if`-branch](https://github.com/kubernetes/apiserver/blob/6b942bcbe7b5563399e5df3e37711e5438298413/pkg/server/options/authentication.go#L466-L469) instead.

That is because the `--kubeconfig` flag is ignored. It could be taken into account by [this code](https://github.com/kubernetes/apiserver/blob/6b942bcbe7b5563399e5df3e37711e5438298413/pkg/server/options/coreapi.go#L50-L52), but that is called only from [here](https://github.com/kubernetes/apiserver/blob/6b942bcbe7b5563399e5df3e37711e5438298413/pkg/server/options/recommended.go#L90), and that is called from no-where, at least when looking at the "Kueue+dependencies" codebase.

### Proposed fix

Add a call to `.AddFlags()` in the Kueue code setting up the visibility server (see #8605)

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-01-15T10:54:00Z

/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-01-15T15:42:22Z

Update: it seems [this fix](https://github.com/kubernetes-sigs/kueue/commit/b8d2700888440dbba9c4f087878b77c2cc9eb6d3) may work - but for now I'd like to continue testing.
(And to remove the logging stuff from that change).

### Comment by [@wzshiming](https://github.com/wzshiming) — 2026-01-23T11:17:26Z

> Update: it seems [this fix](https://github.com/kubernetes-sigs/kueue/commit/b8d2700888440dbba9c4f087878b77c2cc9eb6d3) may work - but for now I'd like to continue testing.


I'm having the same problem with https://github.com/kubernetes-sigs/kwok/pull/1513, I tested this patch and it worked for me.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T13:11:32Z

sounds great @wzshiming !

@olekzabl have you been able to test that too? It would be great to include the fix in 0.16.0 if we have a confirmation it works

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-01-23T13:19:27Z

* I also tested it locally and it worked _for my purpose_ - that is, passing `--kubeconfig` through.
* Before merging my fix, it'd be certainly good to remove my custom logging there.
* Other than that, I think we could merge.
  However, I have doubts if my fix is really "the good one".
  Because it pay special attention to `--kubeconfig`, which is just 1 flag.
  So I'm not sure "how complete fix" it is for this issue.

Anyway, I'll quickly remove the logs from that commit & send it out; then we can think.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T13:24:05Z

> However, I have doubts if my fix is really "the good one".
> Because it pay special attention to --kubeconfig, which is just 1 flag.

I think this is ok, it fixes the know failure modes, so we can improve the implementation as we realize there are more issues (eg. more flags need handling).

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-01-23T14:04:42Z

I found it easier to recreate than to rebase. #8761

### Comment by [@Nilsachy](https://github.com/Nilsachy) — 2026-02-27T13:58:31Z

/assign
