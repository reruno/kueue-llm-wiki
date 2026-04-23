# Issue #4555: Add environment variable to control logging verbosity in integration tests

**Summary**: Add environment variable to control logging verbosity in integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4555

**Last updated**: 2025-03-17T08:05:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nasedil](https://github.com/nasedil)
- **Created**: 2025-03-11T11:34:13Z
- **Updated**: 2025-03-17T08:05:52Z
- **Closed**: 2025-03-17T08:05:52Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add support to control logging verbosity in integration tests via environment variable.
**Why is this needed**:
Right now it's needed to change the code to change verbosity:
https://github.com/kubernetes-sigs/kueue/blob/f8015cb273f9115c34f9be32b35f7e1308c16459/test/integration/framework/framework.go#L72

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-11T11:40:08Z

/remove-kind feature
/kind cleanup

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-13T00:31:31Z

Shouldn't this ginkgo option enough?

```
  --vv 
    If set, emits with maximal verbosity - includes skipped and pending tests.
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-13T06:25:24Z

> Shouldn't this ginkgo option enough?
> 
> ```
>   --vv 
>     If set, emits with maximal verbosity - includes skipped and pending tests.
> ```

The `--vv` flag increasing only ginkgo verbosity. 

We already have `API_LOG_LEVEL` variable and we are using it to change testEnv verbosity. 

https://github.com/kubernetes-sigs/kueue/blob/c5dae03dc28beb0d3f47fa1da08f1134140d49fb/test/integration/framework/framework.go#L93-L97

Maybe we should set `API_LOG_LEVEL` value on `ctrl.SetLogger()` as well.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T07:00:31Z

Yeah, I think we could reuse "API_LOG_LEVEL", but the name seems confusing as it already does more than the log level to api-server. Maybe we just rename `API_LOG_LEVEL` to `INTEGRATION_VLEVEL`, and use it for kube-apiserver and kueue test code?

IIUC `API_LOG_LEVEL` is only used for integration tests anyway. Another name could be `INTEGRATION_LOG_LEVEL`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-13T07:04:07Z

> > Shouldn't this ginkgo option enough?
> > ```
> >   --vv 
> >     If set, emits with maximal verbosity - includes skipped and pending tests.
> > ```
> 
> The `--vv` flag increasing only ginkgo verbosity.
> 
> We already have `API_LOG_LEVEL` variable and we are using it to change testEnv verbosity.
> 
> [kueue/test/integration/framework/framework.go](https://github.com/kubernetes-sigs/kueue/blob/c5dae03dc28beb0d3f47fa1da08f1134140d49fb/test/integration/framework/framework.go#L93-L97)
> 
> Lines 93 to 97 in [c5dae03](/kubernetes-sigs/kueue/commit/c5dae03dc28beb0d3f47fa1da08f1134140d49fb)
> 
>  if level, err := strconv.Atoi(os.Getenv("API_LOG_LEVEL")); err == nil && level > 0 { 
>  	f.testEnv.ControlPlane.GetAPIServer().Configure().Append("v", strconv.Itoa(level)) 
>  	f.testEnv.ControlPlane.GetAPIServer().Out = ginkgo.GinkgoWriter 
>  	f.testEnv.ControlPlane.GetAPIServer().Err = ginkgo.GinkgoWriter 
>  } 
> Maybe we should set `API_LOG_LEVEL` value on `ctrl.SetLogger()` as well.

Good point, I agree with you

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-13T07:04:30Z

> Yeah, I think we could reuse "API_LOG_LEVEL", but the name seems confusing as it already does more than the log level to api-server. Maybe we just rename `API_LOG_LEVEL` to `INTEGRATION_VLEVEL`, and use it for kube-apiserver and kueue test code?
> 
> IIUC `API_LOG_LEVEL` is only used for integration tests anyway. Another name could be `INTEGRATION_LOG_LEVEL`.

+1

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-13T07:15:11Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-13T07:22:13Z

> Yeah, I think we could reuse "API_LOG_LEVEL", but the name seems confusing as it already does more than the log level to api-server. Maybe we just rename `API_LOG_LEVEL` to `INTEGRATION_VLEVEL`, and use it for kube-apiserver and kueue test code?
> 
> IIUC `API_LOG_LEVEL` is only used for integration tests anyway. Another name could be `INTEGRATION_LOG_LEVEL`.

It also used on E2E tests.

https://github.com/kubernetes-sigs/kueue/blob/c5dae03dc28beb0d3f47fa1da08f1134140d49fb/test/e2e/singlecluster/suite_test.go#L61

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T07:36:27Z

Is the `API_LOG_LEVEL` used in e2e tests? Maybe for e2e tests we could have E2ETEST_LOG_LEVEL?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-13T07:58:28Z

> Is the `API_LOG_LEVEL` used in e2e tests? Maybe for e2e tests we could have E2ETEST_LOG_LEVEL?

Do you think we need to split between E2E and integration?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T08:02:03Z

Not necessarily, do you have an alternative proposal?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-13T08:05:20Z

Umm, I think I understand what the `API_LOG_LEVEL` variable does.

https://github.com/kubernetes-sigs/kueue/blob/c5dae03dc28beb0d3f47fa1da08f1134140d49fb/Makefile-test.mk#L45-L47

This isn’t a log level; it’s a verbosity level, and it’s disabled by default.

So we still need to keep it and create a new one.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-13T08:06:00Z

> Not necessarily, do you have an alternative proposal?

I think `LOG_LEVEL` is good.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T08:06:53Z

Maybe `TEST_LOG_LEVEL`?
