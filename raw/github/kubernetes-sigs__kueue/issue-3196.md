# Issue #3196: Running `make test`  on MacOS Sonoma with golang go1.22.5 errors with `has malformed LC_DYSYMTAB` error

**Summary**: Running `make test`  on MacOS Sonoma with golang go1.22.5 errors with `has malformed LC_DYSYMTAB` error

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3196

**Last updated**: 2024-10-09T11:12:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@akram](https://github.com/akram)
- **Created**: 2024-10-07T21:24:24Z
- **Updated**: 2024-10-09T11:12:26Z
- **Closed**: 2024-10-09T11:12:26Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description



**What happened**:
run `make test` it will crash with the following error:

```
=== Errors
ld: warning: '/private/var/folders/36/kbjrd7bn4cbgz8dpt50n5k5w0000gp/T/go-link-3088648823/000014.o' has malformed LC_DYSYMTAB, expected 98 undefined symbols to start at index 1626, found 95 undefined symbols starting at index 1626
ld: warning: '/private/var/folders/36/kbjrd7bn4cbgz8dpt50n5k5w0000gp/T/go-link-845880015/000014.o' has malformed LC_DYSYMTAB, expected 98 undefined symbols to start at index 1626, found 95 undefined symbols starting at index 1626
ld: warning: '/private/var/folders/36/kbjrd7bn4cbgz8dpt50n5k5w0000gp/T/go-link-99404289/000014.o' has malformed LC_DYSYMTAB, expected 98 undefined symbols to start at index 1626, found 95 undefined symbols starting at index 1626
ld: warning: '/private/var/folders/36/kbjrd7bn4cbgz8dpt50n5k5w0000gp/T/go-link-2652475332/000014.o' has malformed LC_DYSYMTAB, expected 98 undefined symbols to start at index 1626, found 95 undefined symbols starting at index 1626
```

**What you expected to happen**:
the build to succeed
**How to reproduce it (as minimally and precisely as possible)**:

run `make test`

**Anything else we need to know?**:

**Environment**:
- Kubernetes version:  v1.24.0
- Kueue version : 64edc866
- Cloud provider or hardware configuration: kind
- OS (e.g: `cat /etc/os-release`): Sonoma Mac OS M1
- Kernel :  Darwin Kernel Version 23.3.0: Wed Dec 20 21:30:44 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T6000 arm64
- Install tools:
- Others:

## Discussion

### Comment by [@akram](https://github.com/akram) — 2024-10-07T21:26:21Z

Setting GOFLAGS to the following value make it run properly.

```
GOFLAGS=-ldflags=-extldflags=-Wl,-ld_classic make test
``` 


seen on the following issue: https://github.com/golang/go/issues/61229#issuecomment-1952798326

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-10-08T00:10:19Z

As mentioned in https://github.com/golang/go/issues/61229#issue-1793742809 as well, those are **just warnings, not errors**. Therefore,  even if you see those messages in Kueue, they are not crashing the tests.

> # NOTE -- please read
> If you see lines starting with `ld: warning` but not other outputs, they are _just warnings, not errors_. You should still get a working binary, if there is no other output. Please only report if you see a link error, or a broken binary, or a warning that is not mentioned in the "warnings" section below. Thanks.
> 
> See [#61229 (comment)](https://github.com/golang/go/issues/61229#issuecomment-1988965927) for more notes about `malformed LC_DYSYMTAB` warning. Thanks.

### Comment by [@akram](https://github.com/akram) — 2024-10-08T12:40:09Z

thanks @IrvingMg 

You are correct, they are not crashing; I was thinking it was crashing, but they are just in error in my case:
 ```
=== Errors
ld: warning: '/private/var/folders/36/kbjrd7bn4cbgz8dpt50n5k5w0000gp/T/go-link-3088648823/000014.o' has malformed LC_DYSYMTAB, expected 98 undefined symbols to start at index 1626, found 95 undefined symbols starting at index 1626
ld: warning: '/private/var/folders/36/kbjrd7bn4cbgz8dpt50n5k5w0000gp/T/go-link-845880015/000014.o' has malformed LC_DYSYMTAB, expected 98 undefined symbols to start at index 1626, found 95 undefined symbols starting at index 1626
ld: warning: '/private/var/folders/36/kbjrd7bn4cbgz8dpt50n5k5w0000gp/T/go-link-99404289/000014.o' has malformed LC_DYSYMTAB, expected 98 undefined symbols to start at index 1626, found 95 undefined symbols starting at index 1626
ld: warning: '/private/var/folders/36/kbjrd7bn4cbgz8dpt50n5k5w0000gp/T/go-link-2652475332/000014.o' has malformed LC_DYSYMTAB, expected 98 undefined symbols to start at index 1626, found 95 undefined symbols starting at index 1626

DONE 1585 tests, 4 errors in 50.377s
```
where, if I run the case with the mentioned parameters they will run without any erro


```
(base) akram@wadez-m1 kueue % GOFLAGS=-ldflags=-extldflags=-Wl,-ld_classic make test
[...]
∅  apis/kueue/v1alpha1 (18ms) (coverage: 0.0% of statements)
∅  apis/kueue/v1beta1 (19ms) (coverage: 0.0% of statements)
∅  apis/visibility/v1alpha1/openapi (21ms) (coverage: 0.0% of statements)
[...]
✓  pkg/util/useragent (1.589s) (coverage: 0.0% of statements in ./...)
✓  pkg/util/wait (1.565s) (coverage: 0.1% of statements in ./...)
✓  pkg/visibility/api/rest (1.597s) (coverage: 2.1% of statements in ./...)
✓  pkg/webhooks (1.725s) (coverage: 2.3% of statements in ./...)
✓  pkg/workload (1.584s) (coverage: 2.9% of statements in ./...)
✓  pkg/scheduler (7.321s) (coverage: 12.9% of statements in ./...)

DONE 1585 tests in 22.354s
```

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-10-08T17:25:21Z

@akram Yes,  the `malformed LC_DYSYMTAB` warning has been discussed by Go team https://github.com/golang/go/issues/61229#issuecomment-1988965927 as well. 

> A note about the `malformed LC_DYSYMTAB` warning: take a look at the object file name that is warned on:
> 
> * if it is `.../go.o`, it is the object of the Go code. This is already fixed in recent versions of Go 1.20.x, 1.21.x, and 1.22.x, and should not appear with an up-to-date version of Go.
> * if it is `.../00NNNN.o` with some 6-digit number, it is a C object.
>   
>   * if you pass `-race` and you're using Go 1.22.x, it is probably the race detector's C code, as mentioned above [cmd/link: issues with Apple's new linker in Xcode 15 beta #61229 (comment)](https://github.com/golang/go/issues/61229#issuecomment-1954706803)
>   * otherwise it is from user C code
> 
> The warning on the race detector C object is not really a bug in Go. Maybe we can fix in the upstream TSAN (also see [#61229 (comment)](https://github.com/golang/go/issues/61229#issuecomment-1954706803)). To work around, you could try
> 
> * passing `-ldflags=-extldflags=-Wl,-ld_classic` to force the old Apple linker
> * passing `-ldflags=-linkmode=internal` to force using Go linker to do the whole linking (although it is not guaranteed to be able to handle all C objects)
> * also, an IDE should NOT treat warning as error by default.
> 
> Thanks.

So, as this is a non-issue, I wouldn't consider it as a Kueue bug.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-09T09:49:52Z

/assign
