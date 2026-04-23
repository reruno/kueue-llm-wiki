# Issue #8970: Flaky test: AppWrapper E2E tests fail

**Summary**: Flaky test: AppWrapper E2E tests fail

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8970

**Last updated**: 2026-02-09T07:30:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2026-02-03T19:59:51Z
- **Updated**: 2026-02-09T07:30:36Z
- **Closed**: 2026-02-09T07:30:35Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
  - AppWrapper [It] Should admit Workload for Job                                                                                                                            
  - AppWrapper [It] Should admit Workload for Deployment Pods
 
**First observed in** (PR or commit, if known):
 PR #8865 (but not caused by the PR changes)                                                                                             
                                                                                                                                                                                                                                                                                         

**Link to failed CI job or steps to reproduce locally**:
  https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8865/pull-kueue-test-e2e-main-1-32/2018758549450002432

**Failure message or logs**:
```
End To End Suite: kindest/node:v1.32.11: [It] AppWrapper Should admit Workload for Deployment Pods [area:singlecluster, feature:appwrapper] expand_less	1s
{Expected success, but got an error:
    <*errors.StatusError | 0xc0007035e0>: 
    Internal error occurred: failed calling webhook "vappwrapper.kb.io": failed to call webhook: Post "https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s": EOF
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "Internal error occurred: failed calling webhook \"vappwrapper.kb.io\": failed to call webhook: Post \"https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s\": EOF",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"vappwrapper.kb.io\": failed to call webhook: Post \"https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s\": EOF",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0007035e0>: 
    Internal error occurred: failed calling webhook "vappwrapper.kb.io": failed to call webhook: Post "https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s": EOF
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "Internal error occurred: failed calling webhook \"vappwrapper.kb.io\": failed to call webhook: Post \"https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s\": EOF",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"vappwrapper.kb.io\": failed to call webhook: Post \"https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s\": EOF",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/appwrapper_test.go:144 @ 02/03/26 19:00:16.708
}
[open stderropen_in_new](https://prow.k8s.io/spyglass/lens/junit/iframe?req=%7B%22artifacts%22%3A%5B%22artifacts%2Frun-test-e2e-singlecluster-1.32.11%2Fjunit.xml%22%5D%2C%22index%22%3A2%2C%22src%22%3A%22gs%2Fkubernetes-ci-logs%2Fpr-logs%2Fpull%2Fkubernetes-sigs_kueue%2F8865%2Fpull-kueue-test-e2e-main-1-32%2F2018758549450002432%22%7D&topURL=https%3A//prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8865/pull-kueue-test-e2e-main-1-32/2018758549450002432&lensIndex=2#)
End To End Suite: kindest/node:v1.32.11: [It] AppWrapper Should admit Workload for Job [area:singlecluster, feature:appwrapper] expand_less	1s
{Expected success, but got an error:
    <*errors.StatusError | 0xc0009226e0>: 
    Internal error occurred: failed calling webhook "vappwrapper.kb.io": failed to call webhook: Post "https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s": EOF
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "Internal error occurred: failed calling webhook \"vappwrapper.kb.io\": failed to call webhook: Post \"https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s\": EOF",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"vappwrapper.kb.io\": failed to call webhook: Post \"https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s\": EOF",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0009226e0>: 
    Internal error occurred: failed calling webhook "vappwrapper.kb.io": failed to call webhook: Post "https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s": EOF
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "Internal error occurred: failed calling webhook \"vappwrapper.kb.io\": failed to call webhook: Post \"https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s\": EOF",
            Reason: "InternalError",
            Details: {
                Name: "",
                Group: "",
                Kind: "",
                UID: "",
                Causes: [
                    {
                        Type: "",
                        Message: "failed calling webhook \"vappwrapper.kb.io\": failed to call webhook: Post \"https://appwrapper-webhook-service.appwrapper-system.svc:443/validate-workload-codeflare-dev-v1beta2-appwrapper?timeout=10s\": EOF",
                        Field: "",
                    },
                ],
                RetryAfterSeconds: 0,
            },
            Code: 500,
        },
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/appwrapper_test.go:98 @ 02/03/26 19:00:16.708
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-04T16:40:36Z

@sohankunkerkar it seems you already investigated a bit the issue: https://github.com/kubernetes-sigs/kueue/pull/8865#issuecomment-3843312743

Could you please maybe open an issue in the AppWrapper to track it there too

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-04T21:00:38Z

/assign @PannagaRao

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-04T21:00:41Z

@sohankunkerkar: GitHub didn't allow me to assign the following users: PannagaRao.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8970#issuecomment-3849718379):

>/assign @PannagaRao 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T10:52:10Z

Ok I checked the logs too, and can confirm that AppWrapper was crashing on startup. 

from [logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8865/pull-kueue-test-e2e-main-1-32/2018758549450002432/artifacts/run-test-e2e-singlecluster-1.32.11/kind-worker/pods/appwrapper-system_appwrapper-controller-manager-79757b844b-xsnf8_e26b99aa-5849-49fd-bfd1-64f2ff75de0c/manager/0.log)
```
2026-02-03T19:00:16.662074027Z stderr F 2026-02-03T19:00:16.661797884Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Applying defaults	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"appwrapper-e2e-xm5tm"}, "namespace": "appwrapper-e2e-xm5tm", "name": "appwrapper", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "kubernetes-admin", "requestID": "4cac2617-20b5-4ae4-9374-9f5f8939ef98", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "appwrapper-e2e-xm5tm", "name": "appwrapper"}}
2026-02-03T19:00:16.662136858Z stderr F 2026-02-03T19:00:16.661821114Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Applying defaults	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"aw","namespace":"appwrapper-e2e-2hhjd"}, "namespace": "appwrapper-e2e-2hhjd", "name": "aw", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "kubernetes-admin", "requestID": "ecd19c47-b967-4fe8-8a01-d6ed54efaa2b", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "appwrapper-e2e-2hhjd", "name": "aw"}}
2026-02-03T19:00:16.676801709Z stderr F 2026-02-03T19:00:16.676598587Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Validating create	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"appwrapper","namespace":"appwrapper-e2e-xm5tm"}, "namespace": "appwrapper-e2e-xm5tm", "name": "appwrapper", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "kubernetes-admin", "requestID": "355521c1-2e22-437b-b783-27004f2dd651", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "appwrapper-e2e-xm5tm", "name": "appwrapper"}}
2026-02-03T19:00:16.677207523Z stderr F 2026-02-03T19:00:16.677068732Z	LEVEL(-2)	admission	logr@v1.4.2/logr.go:280	Validating create	{"webhookGroup": "workload.codeflare.dev", "webhookKind": "AppWrapper", "AppWrapper": {"name":"aw","namespace":"appwrapper-e2e-2hhjd"}, "namespace": "appwrapper-e2e-2hhjd", "name": "aw", "resource": {"group":"workload.codeflare.dev","version":"v1beta2","resource":"appwrappers"}, "user": "kubernetes-admin", "requestID": "f2ccc905-31d2-4ea3-90bc-d49bc82c9f22", "job": {"apiVersion": "workload.codeflare.dev/v1beta2", "kind": "AppWrapper", "namespace": "appwrapper-e2e-2hhjd", "name": "aw"}}
2026-02-03T19:00:16.67870267Z stderr F fatal error: concurrent map writes
2026-02-03T19:00:16.681953925Z stderr F 
2026-02-03T19:00:16.681965326Z stderr F goroutine 313 [running]:
2026-02-03T19:00:16.681969566Z stderr F github.com/project-codeflare/appwrapper/internal/webhook.(*appWrapperWebhook).lookupResource(0xc00052e540, 0xc000bef140)
2026-02-03T19:00:16.681973606Z stderr F 	/workspace/internal/webhook/appwrapper_webhook.go:292 +0x2e8
2026-02-03T19:00:16.681977556Z stderr F github.com/project-codeflare/appwrapper/internal/webhook.(*appWrapperWebhook).validateAppWrapperCreate(0xc00052e540, {0x240c8d0, 0xc000beed80}, 0xc00097e780)
2026-02-03T19:00:16.681980936Z stderr F 	/workspace/internal/webhook/appwrapper_webhook.go:173 +0xb47
2026-02-03T19:00:16.682011656Z stderr F github.com/project-codeflare/appwrapper/internal/webhook.(*appWrapperWebhook).ValidateCreate(0xc00052e540, {0x240c8d0, 0xc000beed80}, {0x23f3640?, 0xc00097e780})
2026-02-03T19:00:16.682021826Z stderr F 	/workspace/internal/webhook/appwrapper_webhook.go:108 +0x130
2026-02-03T19:00:16.682068917Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*validatorForType).Handle(_, {_, _}, {{{0xc0007d10e0, 0x24}, {{0xc000d0b860, 0x16}, {0xc000631e50, 0x7}, {0xc000631e60, ...}}, ...}})
2026-02-03T19:00:16.682076257Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/admission/validator_custom.go:94 +0x2b6
2026-02-03T19:00:16.682127707Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*Webhook).Handle(_, {_, _}, {{{0xc0007d10e0, 0x24}, {{0xc000d0b860, 0x16}, {0xc000631e50, 0x7}, {0xc000631e60, ...}}, ...}})
2026-02-03T19:00:16.682139367Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/admission/webhook.go:181 +0x224
2026-02-03T19:00:16.682162738Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*Webhook).ServeHTTP(0xc000448410, {0x7f4e849d7d50, 0xc0003eaa50}, 0xc000bc0dc0)
2026-02-03T19:00:16.682172438Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/admission/http.go:119 +0xaf0
2026-02-03T19:00:16.682189288Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook/internal/metrics.InstrumentedHook.InstrumentHandlerInFlight.func1({0x7f4e849d7d50, 0xc0003eaa50}, 0xc000bc0dc0)
2026-02-03T19:00:16.682197238Z stderr F 	/go/pkg/mod/github.com/prometheus/client_golang@v1.21.1/prometheus/promhttp/instrument_server.go:60 +0xbc
2026-02-03T19:00:16.682249929Z stderr F net/http.HandlerFunc.ServeHTTP(0x3572240?, {0x7f4e849d7d50?, 0xc0003eaa50?}, 0xc00081b8d8?)
2026-02-03T19:00:16.682256729Z stderr F 	/usr/local/go/src/net/http/server.go:2220 +0x29
2026-02-03T19:00:16.682269279Z stderr F github.com/prometheus/client_golang/prometheus/promhttp.InstrumentHandlerCounter.func1({0x23ff350?, 0xc00027efc0?}, 0xc000bc0dc0)
2026-02-03T19:00:16.682274299Z stderr F 	/go/pkg/mod/github.com/prometheus/client_golang@v1.21.1/prometheus/promhttp/instrument_server.go:147 +0xc3
2026-02-03T19:00:16.682295319Z stderr F net/http.HandlerFunc.ServeHTTP(0x1f66cc0?, {0x23ff350?, 0xc00027efc0?}, 0xc00081ba20?)
2026-02-03T19:00:16.682309949Z stderr F 	/usr/local/go/src/net/http/server.go:2220 +0x29
2026-02-03T19:00:16.68232257Z stderr F github.com/prometheus/client_golang/prometheus/promhttp.InstrumentHandlerDuration.func2({0x23ff350, 0xc00027efc0}, 0xc000bc0dc0)
2026-02-03T19:00:16.68234317Z stderr F 	/go/pkg/mod/github.com/prometheus/client_golang@v1.21.1/prometheus/promhttp/instrument_server.go:109 +0xc2
2026-02-03T19:00:16.68235577Z stderr F net/http.HandlerFunc.ServeHTTP(0xc0002f8c40?, {0x23ff350?, 0xc00027efc0?}, 0x3?)
2026-02-03T19:00:16.68237119Z stderr F 	/usr/local/go/src/net/http/server.go:2220 +0x29
2026-02-03T19:00:16.682437161Z stderr F net/http.(*ServeMux).ServeHTTP(0x410725?, {0x23ff350, 0xc00027efc0}, 0xc000bc0dc0)
2026-02-03T19:00:16.682447281Z stderr F 	/usr/local/go/src/net/http/server.go:2747 +0x1ca
2026-02-03T19:00:16.682451681Z stderr F net/http.serverHandler.ServeHTTP({0x23f3cd8?}, {0x23ff350?, 0xc00027efc0?}, 0x6?)
2026-02-03T19:00:16.682477111Z stderr F 	/usr/local/go/src/net/http/server.go:3210 +0x8e
2026-02-03T19:00:16.682482241Z stderr F net/http.(*conn).serve(0xc000ad0bd0, {0x240c8d0, 0xc00099d380})
2026-02-03T19:00:16.682491571Z stderr F 	/usr/local/go/src/net/http/server.go:2092 +0x5d0
2026-02-03T19:00:16.682495831Z stderr F created by net/http.(*Server).Serve in goroutine 203
2026-02-03T19:00:16.682505212Z stderr F 	/usr/local/go/src/net/http/server.go:3360 +0x485
2026-02-03T19:00:16.682509152Z stderr F 
2026-02-03T19:00:16.682517362Z stderr F goroutine 1 [select, 2 minutes]:
2026-02-03T19:00:16.682529742Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*controllerManager).Start(0xc000505180, {0x240c908, 0xc00013db30})
2026-02-03T19:00:16.682539412Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/internal.go:466 +0xadb
2026-02-03T19:00:16.682571682Z stderr F main.main()
2026-02-03T19:00:16.682581522Z stderr F 	/workspace/cmd/main.go:165 +0xe48
2026-02-03T19:00:16.682585852Z stderr F 
2026-02-03T19:00:16.682591012Z stderr F goroutine 80 [chan receive, 2 minutes]:
2026-02-03T19:00:16.682605713Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile(0xc0007b2e10)
2026-02-03T19:00:16.682614703Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:186 +0x45
2026-02-03T19:00:16.682623343Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).Start.func1 in goroutine 1
2026-02-03T19:00:16.682631883Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:139 +0xbf
2026-02-03T19:00:16.682639483Z stderr F 
2026-02-03T19:00:16.682648333Z stderr F goroutine 50 [syscall, 2 minutes]:
2026-02-03T19:00:16.682657213Z stderr F os/signal.signal_recv()
2026-02-03T19:00:16.682667433Z stderr F 	/usr/local/go/src/runtime/sigqueue.go:152 +0x29
2026-02-03T19:00:16.682676133Z stderr F os/signal.loop()
2026-02-03T19:00:16.682680183Z stderr F 	/usr/local/go/src/os/signal/signal_unix.go:23 +0x13
2026-02-03T19:00:16.682688724Z stderr F created by os/signal.Notify.func1.1 in goroutine 1
2026-02-03T19:00:16.682704204Z stderr F 	/usr/local/go/src/os/signal/signal.go:151 +0x1f
2026-02-03T19:00:16.682708274Z stderr F 
2026-02-03T19:00:16.682716854Z stderr F goroutine 43 [chan receive, 2 minutes]:
2026-02-03T19:00:16.682728774Z stderr F sigs.k8s.io/controller-runtime/pkg/manager/signals.SetupSignalHandler.func1()
2026-02-03T19:00:16.682733114Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/signals/signal.go:38 +0x27
2026-02-03T19:00:16.682745034Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager/signals.SetupSignalHandler in goroutine 1
2026-02-03T19:00:16.682752974Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/signals/signal.go:37 +0xc5
2026-02-03T19:00:16.682757014Z stderr F 
2026-02-03T19:00:16.682768624Z stderr F goroutine 46 [chan receive, 2 minutes]:
2026-02-03T19:00:16.682772824Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*Server).Start.func1()
2026-02-03T19:00:16.682784505Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/server.go:67 +0x6e
2026-02-03T19:00:16.682792445Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*Server).Start in goroutine 113
2026-02-03T19:00:16.682812645Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/server.go:66 +0x2f7
2026-02-03T19:00:16.682816835Z stderr F 
2026-02-03T19:00:16.682821035Z stderr F goroutine 54 [IO wait]:
2026-02-03T19:00:16.682838115Z stderr F internal/poll.runtime_pollWait(0x7f4e849efe20, 0x72)
2026-02-03T19:00:16.682847275Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.682858035Z stderr F internal/poll.(*pollDesc).wait(0xc00006a480?, 0xc000dbe000?, 0x0)
2026-02-03T19:00:16.682912866Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.682923836Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.682928016Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.682932156Z stderr F internal/poll.(*FD).Read(0xc00006a480, {0xc000dbe000, 0xa000, 0xa000})
2026-02-03T19:00:16.682935966Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:165 +0x27a
2026-02-03T19:00:16.682948206Z stderr F net.(*netFD).Read(0xc00006a480, {0xc000dbe000?, 0x9808d2?, 0xc0006a19a0?})
2026-02-03T19:00:16.682957176Z stderr F 	/usr/local/go/src/net/fd_posix.go:55 +0x25
2026-02-03T19:00:16.682980497Z stderr F net.(*conn).Read(0xc000432030, {0xc000dbe000?, 0xc00064a180?, 0xc000dbe005?})
2026-02-03T19:00:16.682994227Z stderr F 	/usr/local/go/src/net/net.go:189 +0x45
2026-02-03T19:00:16.683019637Z stderr F crypto/tls.(*atLeastReader).Read(0xc000a82cc0, {0xc000dbe000?, 0x0?, 0xc000a82cc0?})
2026-02-03T19:00:16.683032677Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:809 +0x3b
2026-02-03T19:00:16.683045247Z stderr F bytes.(*Buffer).ReadFrom(0xc0005fa638, {0x23e8220, 0xc000a82cc0})
2026-02-03T19:00:16.683057838Z stderr F 	/usr/local/go/src/bytes/buffer.go:211 +0x98
2026-02-03T19:00:16.683074408Z stderr F crypto/tls.(*Conn).readFromUntil(0xc0005fa388, {0x23e9a00, 0xc000432030}, 0xc0006a1a10?)
2026-02-03T19:00:16.683086398Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:831 +0xde
2026-02-03T19:00:16.683097878Z stderr F crypto/tls.(*Conn).readRecordOrCCS(0xc0005fa388, 0x0)
2026-02-03T19:00:16.683110048Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:629 +0x3cf
2026-02-03T19:00:16.683121748Z stderr F crypto/tls.(*Conn).readRecord(...)
2026-02-03T19:00:16.683129828Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:591
2026-02-03T19:00:16.683141338Z stderr F crypto/tls.(*Conn).Read(0xc0005fa388, {0xc0002cc000, 0x1000, 0xc000b256c0?})
2026-02-03T19:00:16.683153679Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:1385 +0x150
2026-02-03T19:00:16.683169739Z stderr F bufio.(*Reader).Read(0xc00078e060, {0xc0002f8200, 0x9, 0x35695b0?})
2026-02-03T19:00:16.683184659Z stderr F 	/usr/local/go/src/bufio/bufio.go:241 +0x197
2026-02-03T19:00:16.683220199Z stderr F io.ReadAtLeast({0x23e9f80, 0xc00078e060}, {0xc0002f8200, 0x9, 0x9}, 0x9)
2026-02-03T19:00:16.683231089Z stderr F 	/usr/local/go/src/io/io.go:335 +0x90
2026-02-03T19:00:16.68323829Z stderr F io.ReadFull(...)
2026-02-03T19:00:16.68324516Z stderr F 	/usr/local/go/src/io/io.go:354
2026-02-03T19:00:16.68326846Z stderr F golang.org/x/net/http2.readFrameHeader({0xc0002f8200, 0x9, 0x479a45?}, {0x23e9f80?, 0xc00078e060?})
2026-02-03T19:00:16.68328222Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/frame.go:237 +0x65
2026-02-03T19:00:16.68328711Z stderr F golang.org/x/net/http2.(*Framer).ReadFrame(0xc0002f81c0)
2026-02-03T19:00:16.68329943Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/frame.go:501 +0x85
2026-02-03T19:00:16.68330717Z stderr F golang.org/x/net/http2.(*clientConnReadLoop).run(0xc0006a1fa8)
2026-02-03T19:00:16.68332079Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:2258 +0xda
2026-02-03T19:00:16.683327331Z stderr F golang.org/x/net/http2.(*ClientConn).readLoop(0xc000685dc0)
2026-02-03T19:00:16.683334401Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:2127 +0x7c
2026-02-03T19:00:16.683343841Z stderr F created by golang.org/x/net/http2.(*Transport).newClientConn in goroutine 53
2026-02-03T19:00:16.683353681Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:912 +0xdfb
2026-02-03T19:00:16.683365601Z stderr F 
2026-02-03T19:00:16.683379791Z stderr F goroutine 96 [chan receive, 2 minutes]:
2026-02-03T19:00:16.683384501Z stderr F sigs.k8s.io/controller-runtime/pkg/metrics/server.(*defaultServer).Start.func1()
2026-02-03T19:00:16.683393581Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/metrics/server/server.go:253 +0x45
2026-02-03T19:00:16.683402421Z stderr F created by sigs.k8s.io/controller-runtime/pkg/metrics/server.(*defaultServer).Start in goroutine 62
2026-02-03T19:00:16.683409711Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/metrics/server/server.go:252 +0x859
2026-02-03T19:00:16.683416112Z stderr F 
2026-02-03T19:00:16.683419762Z stderr F goroutine 277 [sync.Cond.Wait]:
2026-02-03T19:00:16.683429622Z stderr F sync.runtime_notifyListWait(0xc0001864f8, 0x2a)
2026-02-03T19:00:16.683439662Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.683446722Z stderr F sync.(*Cond).Wait(0xc0005a8160?)
2026-02-03T19:00:16.683457042Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.683479202Z stderr F k8s.io/client-go/tools/cache.(*DeltaFIFO).Pop(0xc0001864d0, 0xc000115de0)
2026-02-03T19:00:16.683489252Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/delta_fifo.go:588 +0x231
2026-02-03T19:00:16.683498052Z stderr F k8s.io/client-go/tools/cache.(*controller).processLoop(0xc000186580)
2026-02-03T19:00:16.683506633Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:195 +0x30
2026-02-03T19:00:16.683519153Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.683532583Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.683544693Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0000d4de8, {0x23eab40, 0xc000bfea80}, 0x1, 0xc000a18a80)
2026-02-03T19:00:16.683556893Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.683581663Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc0000d4de8, 0x3b9aca00, 0x0, 0x1, 0xc000a18a80)
2026-02-03T19:00:16.683593693Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.683601654Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.683609484Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.683617244Z stderr F k8s.io/client-go/tools/cache.(*controller).Run(0xc000186580, 0xc000a18a80)
2026-02-03T19:00:16.683628994Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:166 +0x375
2026-02-03T19:00:16.683637114Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run(0xc0001862c0, 0xc000a18a80)
2026-02-03T19:00:16.683649274Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:508 +0x2a9
2026-02-03T19:00:16.683664114Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Cache).Start(0xc0000e58f0, 0x21d9910?)
2026-02-03T19:00:16.683675894Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:108 +0x72
2026-02-03T19:00:16.683684114Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked.func1()
2026-02-03T19:00:16.683692105Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:242 +0x75
2026-02-03T19:00:16.683700655Z stderr F created by sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked in goroutine 276
2026-02-03T19:00:16.683712025Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:240 +0x87
2026-02-03T19:00:16.683719545Z stderr F 
2026-02-03T19:00:16.683727735Z stderr F goroutine 61 [chan receive, 2 minutes]:
2026-02-03T19:00:16.683739215Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile(0xc0007b2bd0)
2026-02-03T19:00:16.683753485Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:186 +0x45
2026-02-03T19:00:16.683777495Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).Start.func1 in goroutine 1
2026-02-03T19:00:16.683782356Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:139 +0xbf
2026-02-03T19:00:16.683786366Z stderr F 
2026-02-03T19:00:16.683795296Z stderr F goroutine 62 [IO wait, 2 minutes]:
2026-02-03T19:00:16.683807616Z stderr F internal/poll.runtime_pollWait(0x7f4e849efbf0, 0x72)
2026-02-03T19:00:16.683813846Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.683828126Z stderr F internal/poll.(*pollDesc).wait(0xc000940280?, 0xc000c9ba38?, 0x0)
2026-02-03T19:00:16.683836776Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.683846696Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.683855116Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.683862956Z stderr F internal/poll.(*FD).Accept(0xc000940280)
2026-02-03T19:00:16.683870556Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:620 +0x295
2026-02-03T19:00:16.683879357Z stderr F net.(*netFD).accept(0xc000940280)
2026-02-03T19:00:16.683886907Z stderr F 	/usr/local/go/src/net/fd_unix.go:172 +0x29
2026-02-03T19:00:16.683894597Z stderr F net.(*TCPListener).accept(0xc000892040)
2026-02-03T19:00:16.683902737Z stderr F 	/usr/local/go/src/net/tcpsock_posix.go:159 +0x1e
2026-02-03T19:00:16.683911247Z stderr F net.(*TCPListener).Accept(0xc000892040)
2026-02-03T19:00:16.683919517Z stderr F 	/usr/local/go/src/net/tcpsock.go:372 +0x30
2026-02-03T19:00:16.683927537Z stderr F crypto/tls.(*listener).Accept(0xc000296618)
2026-02-03T19:00:16.683945517Z stderr F 	/usr/local/go/src/crypto/tls/tls.go:67 +0x27
2026-02-03T19:00:16.683958267Z stderr F net/http.(*Server).Serve(0xc0002170e0, {0x23fb548, 0xc000296618})
2026-02-03T19:00:16.683966908Z stderr F 	/usr/local/go/src/net/http/server.go:3330 +0x30c
2026-02-03T19:00:16.683985858Z stderr F sigs.k8s.io/controller-runtime/pkg/metrics/server.(*defaultServer).Start(0xc0002f88c0, {0x240c908, 0xc0003e9a90})
2026-02-03T19:00:16.683995608Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/metrics/server/server.go:265 +0x876
2026-02-03T19:00:16.684002558Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc0008020c0)
2026-02-03T19:00:16.684009358Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.684016038Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 61
2026-02-03T19:00:16.684027468Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.684031978Z stderr F 
2026-02-03T19:00:16.684040628Z stderr F goroutine 113 [IO wait]:
2026-02-03T19:00:16.684066089Z stderr F internal/poll.runtime_pollWait(0x7f4e849efd08, 0x72)
2026-02-03T19:00:16.684075459Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.684079889Z stderr F internal/poll.(*pollDesc).wait(0xc0007c9280?, 0x900000036?, 0x0)
2026-02-03T19:00:16.684088079Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.684092339Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.684102239Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.684120699Z stderr F internal/poll.(*FD).Accept(0xc0007c9280)
2026-02-03T19:00:16.684130539Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:620 +0x295
2026-02-03T19:00:16.684140109Z stderr F net.(*netFD).accept(0xc0007c9280)
2026-02-03T19:00:16.68414483Z stderr F 	/usr/local/go/src/net/fd_unix.go:172 +0x29
2026-02-03T19:00:16.68414908Z stderr F net.(*TCPListener).accept(0xc0003ad580)
2026-02-03T19:00:16.68415804Z stderr F 	/usr/local/go/src/net/tcpsock_posix.go:159 +0x1e
2026-02-03T19:00:16.68416236Z stderr F net.(*TCPListener).Accept(0xc0003ad580)
2026-02-03T19:00:16.68422096Z stderr F 	/usr/local/go/src/net/tcpsock.go:372 +0x30
2026-02-03T19:00:16.68422813Z stderr F net/http.(*Server).Serve(0xc0007a61e0, {0x23ff110, 0xc0003ad580})
2026-02-03T19:00:16.68423312Z stderr F 	/usr/local/go/src/net/http/server.go:3330 +0x30c
2026-02-03T19:00:16.684320171Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*Server).serve(0x2413f48?)
2026-02-03T19:00:16.684327662Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/server.go:106 +0x25
2026-02-03T19:00:16.684331142Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*Server).Start(0xc0003ad840, {0x240c908, 0xc0003e9a90})
2026-02-03T19:00:16.684334442Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/server.go:84 +0x332
2026-02-03T19:00:16.684337652Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc000802100)
2026-02-03T19:00:16.684340832Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.684344072Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 61
2026-02-03T19:00:16.684347402Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.684350412Z stderr F 
2026-02-03T19:00:16.684360712Z stderr F goroutine 115 [chan receive, 2 minutes]:
2026-02-03T19:00:16.684365392Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile(0xc0007b2c60)
2026-02-03T19:00:16.684369382Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:186 +0x45
2026-02-03T19:00:16.684373452Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).Start.func1 in goroutine 1
2026-02-03T19:00:16.684377412Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:139 +0xbf
2026-02-03T19:00:16.684381142Z stderr F 
2026-02-03T19:00:16.684384992Z stderr F goroutine 116 [chan receive, 2 minutes]:
2026-02-03T19:00:16.684395002Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile(0xc0007b2cf0)
2026-02-03T19:00:16.684398772Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:186 +0x45
2026-02-03T19:00:16.684402042Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).Start.func1 in goroutine 1
2026-02-03T19:00:16.684405272Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:139 +0xbf
2026-02-03T19:00:16.684408322Z stderr F 
2026-02-03T19:00:16.684431443Z stderr F goroutine 117 [chan receive, 2 minutes]:
2026-02-03T19:00:16.684439903Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).Start(0xc00037d900, {0x240c908, 0xc0003e9b30})
2026-02-03T19:00:16.684463583Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:223 +0x49
2026-02-03T19:00:16.684471503Z stderr F sigs.k8s.io/controller-runtime/pkg/cluster.(*cluster).Start(0x0?, {0x240c908?, 0xc0003e9b30?})
2026-02-03T19:00:16.684480683Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cluster/internal.go:104 +0x6a
2026-02-03T19:00:16.684489673Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc0008020a0)
2026-02-03T19:00:16.684493943Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.684497983Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 116
2026-02-03T19:00:16.684519904Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.684524254Z stderr F 
2026-02-03T19:00:16.684533844Z stderr F goroutine 178 [sync.Cond.Wait]:
2026-02-03T19:00:16.684538174Z stderr F sync.runtime_notifyListWait(0xc0009a40d8, 0x8)
2026-02-03T19:00:16.684546504Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.684563004Z stderr F sync.(*Cond).Wait(0xc000ec62a0?)
2026-02-03T19:00:16.684567344Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.684575704Z stderr F k8s.io/client-go/tools/cache.(*DeltaFIFO).Pop(0xc0009a40b0, 0xc000998610)
2026-02-03T19:00:16.684579804Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/delta_fifo.go:588 +0x231
2026-02-03T19:00:16.684588144Z stderr F k8s.io/client-go/tools/cache.(*controller).processLoop(0xc0009a4160)
2026-02-03T19:00:16.684596444Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:195 +0x30
2026-02-03T19:00:16.684600635Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.684608905Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.684621025Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc000b0ede8, {0x23eab40, 0xc00099c6f0}, 0x1, 0xc000a981c0)
2026-02-03T19:00:16.684632635Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.684652315Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc000b0ede8, 0x3b9aca00, 0x0, 0x1, 0xc000a981c0)
2026-02-03T19:00:16.684664895Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.684669205Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.684681065Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.684685255Z stderr F k8s.io/client-go/tools/cache.(*controller).Run(0xc0009a4160, 0xc000a981c0)
2026-02-03T19:00:16.684698036Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:166 +0x375
2026-02-03T19:00:16.684711016Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run(0xc000698630, 0xc000a981c0)
2026-02-03T19:00:16.684718716Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:508 +0x2a9
2026-02-03T19:00:16.684727276Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Cache).Start(0xc0000e4cb0, 0x0?)
2026-02-03T19:00:16.684737816Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:108 +0x72
2026-02-03T19:00:16.684742286Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked.func1()
2026-02-03T19:00:16.684751536Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:242 +0x75
2026-02-03T19:00:16.684758426Z stderr F created by sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked in goroutine 143
2026-02-03T19:00:16.684766656Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:240 +0x87
2026-02-03T19:00:16.684769966Z stderr F 
2026-02-03T19:00:16.684777166Z stderr F goroutine 129 [select, 2 minutes]:
2026-02-03T19:00:16.684789517Z stderr F sigs.k8s.io/controller-runtime/pkg/cache.(*multiNamespaceCache).Start(0xc0007f9bf0, {0x240c908, 0xc0003e9bd0})
2026-02-03T19:00:16.684800387Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/multi_namespace_cache.go:185 +0x2b5
2026-02-03T19:00:16.684812977Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc000795ea0)
2026-02-03T19:00:16.684825677Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.684834417Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 80
2026-02-03T19:00:16.684846537Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.684850117Z stderr F 
2026-02-03T19:00:16.684860197Z stderr F goroutine 121 [sync.Cond.Wait, 2 minutes]:
2026-02-03T19:00:16.684863837Z stderr F sync.runtime_notifyListWait(0xc00037b158, 0x2)
2026-02-03T19:00:16.684874008Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.684881708Z stderr F sync.(*Cond).Wait(0xc000802620?)
2026-02-03T19:00:16.684903038Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.684908288Z stderr F k8s.io/client-go/tools/cache.(*DeltaFIFO).Pop(0xc00037b130, 0xc00031e7b0)
2026-02-03T19:00:16.684916528Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/delta_fifo.go:588 +0x231
2026-02-03T19:00:16.684924028Z stderr F k8s.io/client-go/tools/cache.(*controller).processLoop(0xc00037b1e0)
2026-02-03T19:00:16.684931558Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:195 +0x30
2026-02-03T19:00:16.684939658Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.684946758Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.684960398Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0000d7de8, {0x23eab40, 0xc000150cf0}, 0x1, 0xc0004f8ee0)
2026-02-03T19:00:16.684973039Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.684986409Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc0000d7de8, 0x3b9aca00, 0x0, 0x1, 0xc0004f8ee0)
2026-02-03T19:00:16.684999079Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.685008439Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.685016249Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.685028399Z stderr F k8s.io/client-go/tools/cache.(*controller).Run(0xc00037b1e0, 0xc0004f8ee0)
2026-02-03T19:00:16.685037289Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:166 +0x375
2026-02-03T19:00:16.685049309Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run(0xc000187130, 0xc0004f8ee0)
2026-02-03T19:00:16.68505767Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:508 +0x2a9
2026-02-03T19:00:16.68506621Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Cache).Start(0xc0002d2380, 0x0?)
2026-02-03T19:00:16.68509975Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:108 +0x72
2026-02-03T19:00:16.68510782Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked.func1()
2026-02-03T19:00:16.6851168Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:242 +0x75
2026-02-03T19:00:16.68512131Z stderr F created by sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked in goroutine 133
2026-02-03T19:00:16.685150171Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:240 +0x87
2026-02-03T19:00:16.685158631Z stderr F 
2026-02-03T19:00:16.685162821Z stderr F goroutine 131 [chan receive, 2 minutes]:
2026-02-03T19:00:16.685174671Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).Start(0xc000718dc0, {0x240c908, 0xc0003e9bd0})
2026-02-03T19:00:16.685178781Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:223 +0x49
2026-02-03T19:00:16.685182661Z stderr F sigs.k8s.io/controller-runtime/pkg/cache.(*multiNamespaceCache).Start.func1()
2026-02-03T19:00:16.685186441Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/multi_namespace_cache.go:170 +0x35
2026-02-03T19:00:16.685190231Z stderr F created by sigs.k8s.io/controller-runtime/pkg/cache.(*multiNamespaceCache).Start in goroutine 129
2026-02-03T19:00:16.685213721Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/multi_namespace_cache.go:169 +0xd5
2026-02-03T19:00:16.685217751Z stderr F 
2026-02-03T19:00:16.685221591Z stderr F goroutine 132 [chan receive, 2 minutes]:
2026-02-03T19:00:16.685253452Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).Start(0xc000718c80, {0x240c908, 0xc0003e9bd0})
2026-02-03T19:00:16.685261392Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:223 +0x49
2026-02-03T19:00:16.685284582Z stderr F sigs.k8s.io/controller-runtime/pkg/cache.(*multiNamespaceCache).Start.func2({0xc00059a498, 0x11}, {0x2418b80?, 0xc0001b8708?})
2026-02-03T19:00:16.685289262Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/multi_namespace_cache.go:180 +0x53
2026-02-03T19:00:16.685293342Z stderr F created by sigs.k8s.io/controller-runtime/pkg/cache.(*multiNamespaceCache).Start in goroutine 129
2026-02-03T19:00:16.685302062Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/multi_namespace_cache.go:179 +0x14c
2026-02-03T19:00:16.685310222Z stderr F 
2026-02-03T19:00:16.685314492Z stderr F goroutine 133 [select, 2 minutes]:
2026-02-03T19:00:16.685326262Z stderr F github.com/open-policy-agent/cert-controller/pkg/rotator.(*CertRotator).Start(0xc0006091e0, {0x240c908, 0xc0003e9bd0})
2026-02-03T19:00:16.685334493Z stderr F 	/go/pkg/mod/github.com/open-policy-agent/cert-controller@v0.12.0/pkg/rotator/rotator.go:298 +0x3e6
2026-02-03T19:00:16.685342713Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc000795ec0)
2026-02-03T19:00:16.685350863Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.685361693Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 80
2026-02-03T19:00:16.685418413Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.685426334Z stderr F 
2026-02-03T19:00:16.685436484Z stderr F goroutine 134 [chan receive, 2 minutes]:
2026-02-03T19:00:16.685444044Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start(0x242b540, {0x240c908, 0xc0003e9bd0})
2026-02-03T19:00:16.685471254Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:261 +0x1a9
2026-02-03T19:00:16.685476304Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc000802040)
2026-02-03T19:00:16.685480344Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.685484364Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 80
2026-02-03T19:00:16.685493044Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.685497184Z stderr F 
2026-02-03T19:00:16.685501464Z stderr F goroutine 145 [select]:
2026-02-03T19:00:16.685509874Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc000d93ee0, {0x23eab40, 0xc0007b4e70}, 0x1, 0xc0000dc8c0)
2026-02-03T19:00:16.685514035Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:238 +0x12c
2026-02-03T19:00:16.685530565Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc0004f7ee0, 0x77359400, 0x0, 0x1, 0xc0000dc8c0)
2026-02-03T19:00:16.685539245Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.685543545Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.685551675Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.685563475Z stderr F k8s.io/client-go/tools/leaderelection.(*LeaderElector).renew(0xc0007192c0, {0x240c908?, 0xc0003ce4b0?})
2026-02-03T19:00:16.685575535Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/leaderelection/leaderelection.go:282 +0xf4
2026-02-03T19:00:16.685587345Z stderr F k8s.io/client-go/tools/leaderelection.(*LeaderElector).Run(0xc0007192c0, {0x240c908, 0xc000448000})
2026-02-03T19:00:16.685595745Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/leaderelection/leaderelection.go:221 +0xfa
2026-02-03T19:00:16.685603926Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*controllerManager).Start.func3()
2026-02-03T19:00:16.685611936Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/internal.go:449 +0x32
2026-02-03T19:00:16.685643776Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*controllerManager).Start in goroutine 1
2026-02-03T19:00:16.685653376Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/internal.go:448 +0x9f4
2026-02-03T19:00:16.685657346Z stderr F 
2026-02-03T19:00:16.685661476Z stderr F goroutine 136 [chan receive]:
2026-02-03T19:00:16.685669646Z stderr F k8s.io/client-go/util/workqueue.(*Typed[...]).updateUnfinishedWorkLoop(0x241eba0)
2026-02-03T19:00:16.685677876Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:355 +0x97
2026-02-03T19:00:16.685681966Z stderr F created by k8s.io/client-go/util/workqueue.newQueue[...] in goroutine 134
2026-02-03T19:00:16.685690356Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:176 +0x1e7
2026-02-03T19:00:16.685694127Z stderr F 
2026-02-03T19:00:16.685702207Z stderr F goroutine 137 [select]:
2026-02-03T19:00:16.685710397Z stderr F k8s.io/client-go/util/workqueue.(*delayingType[...]).waitingLoop(0x241b7c0)
2026-02-03T19:00:16.685718667Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/delaying_queue.go:311 +0x334
2026-02-03T19:00:16.685727017Z stderr F created by k8s.io/client-go/util/workqueue.newDelayingQueue[...] in goroutine 134
2026-02-03T19:00:16.685735227Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/delaying_queue.go:148 +0x245
2026-02-03T19:00:16.685743057Z stderr F 
2026-02-03T19:00:16.685751427Z stderr F goroutine 138 [chan receive, 2 minutes]:
2026-02-03T19:00:16.685761957Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1()
2026-02-03T19:00:16.685784748Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:162 +0x2c
2026-02-03T19:00:16.685789618Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start in goroutine 134
2026-02-03T19:00:16.685798458Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:161 +0x156
2026-02-03T19:00:16.685802608Z stderr F 
2026-02-03T19:00:16.685811418Z stderr F goroutine 192 [sync.Cond.Wait, 2 minutes]:
2026-02-03T19:00:16.685820088Z stderr F sync.runtime_notifyListWait(0xc0005ee690, 0x0)
2026-02-03T19:00:16.685828998Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.685841738Z stderr F sync.(*Cond).Wait(0x16d45d9?)
2026-02-03T19:00:16.685850168Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.685860738Z stderr F k8s.io/client-go/util/workqueue.(*Typed[...]).Get(0x241eba0)
2026-02-03T19:00:16.685872638Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:277 +0xb2
2026-02-03T19:00:16.685883959Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem(0x242b540, {0x240c908, 0xc0003e9bd0})
2026-02-03T19:00:16.685894879Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:271 +0x5e
2026-02-03T19:00:16.685911099Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2()
2026-02-03T19:00:16.685922909Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:249 +0x85
2026-02-03T19:00:16.685931729Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2 in goroutine 134
2026-02-03T19:00:16.685943459Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:245 +0x6b8
2026-02-03T19:00:16.685947589Z stderr F 
2026-02-03T19:00:16.685960119Z stderr F goroutine 244 [select, 2 minutes]:
2026-02-03T19:00:16.68596819Z stderr F k8s.io/client-go/tools/cache.(*processorListener).pop(0xc0001443f0)
2026-02-03T19:00:16.68597604Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:943 +0xf5
2026-02-03T19:00:16.68598417Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.68600409Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.68600833Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 48
2026-02-03T19:00:16.68601983Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.68602376Z stderr F 
2026-02-03T19:00:16.68602768Z stderr F goroutine 267 [chan receive]:
2026-02-03T19:00:16.68603836Z stderr F k8s.io/client-go/util/workqueue.(*Typed[...]).updateUnfinishedWorkLoop(0x241eba0)
2026-02-03T19:00:16.68605312Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:355 +0x97
2026-02-03T19:00:16.686067421Z stderr F created by k8s.io/client-go/util/workqueue.newQueue[...] in goroutine 265
2026-02-03T19:00:16.686095661Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:176 +0x1e7
2026-02-03T19:00:16.686099211Z stderr F 
2026-02-03T19:00:16.686109781Z stderr F goroutine 268 [select]:
2026-02-03T19:00:16.686178892Z stderr F k8s.io/client-go/util/workqueue.(*delayingType[...]).waitingLoop(0x241b7c0)
2026-02-03T19:00:16.686184792Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/delaying_queue.go:311 +0x334
2026-02-03T19:00:16.686197382Z stderr F created by k8s.io/client-go/util/workqueue.newDelayingQueue[...] in goroutine 265
2026-02-03T19:00:16.686205622Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/delaying_queue.go:148 +0x245
2026-02-03T19:00:16.686209782Z stderr F 
2026-02-03T19:00:16.686263413Z stderr F goroutine 190 [chan receive]:
2026-02-03T19:00:16.686272603Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run.func1()
2026-02-03T19:00:16.686276633Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:973 +0x45
2026-02-03T19:00:16.686280513Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.686284263Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.686293073Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0000d5f70, {0x23eab40, 0xc0001500c0}, 0x1, 0xc0000dc000)
2026-02-03T19:00:16.686300753Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.686304433Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc000120f70, 0x3b9aca00, 0x0, 0x1, 0xc0000dc000)
2026-02-03T19:00:16.686327073Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.686337324Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.686341984Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.686345974Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run(0xc0008a4000)
2026-02-03T19:00:16.686350014Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:972 +0x5a
2026-02-03T19:00:16.686358644Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.686365384Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.686368744Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 161
2026-02-03T19:00:16.686371934Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.686375024Z stderr F 
2026-02-03T19:00:16.686384604Z stderr F goroutine 150 [select, 2 minutes]:
2026-02-03T19:00:16.686394184Z stderr F reflect.rselect({0xc0000daf00, 0x3, 0xc00011ef30?})
2026-02-03T19:00:16.686404284Z stderr F 	/usr/local/go/src/runtime/select.go:600 +0x2c5
2026-02-03T19:00:16.686429145Z stderr F reflect.Select({0xc00037a000?, 0x3, 0xc00011efd0?})
2026-02-03T19:00:16.686444595Z stderr F 	/usr/local/go/src/reflect/value.go:3176 +0x5ca
2026-02-03T19:00:16.686449415Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...].func2()
2026-02-03T19:00:16.686461145Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:34 +0x4f
2026-02-03T19:00:16.686473395Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...] in goroutine 121
2026-02-03T19:00:16.686485835Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:32 +0x438
2026-02-03T19:00:16.686489965Z stderr F 
2026-02-03T19:00:16.686494035Z stderr F goroutine 123 [chan receive, 2 minutes]:
2026-02-03T19:00:16.686505955Z stderr F k8s.io/apimachinery/pkg/watch.(*Broadcaster).loop(0xc0003ce3c0)
2026-02-03T19:00:16.686510245Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/mux.go:268 +0x66
2026-02-03T19:00:16.686522436Z stderr F created by k8s.io/apimachinery/pkg/watch.NewLongQueueBroadcaster in goroutine 145
2026-02-03T19:00:16.686526796Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/mux.go:93 +0x125
2026-02-03T19:00:16.686530416Z stderr F 
2026-02-03T19:00:16.686542186Z stderr F goroutine 243 [chan receive, 2 minutes]:
2026-02-03T19:00:16.686546376Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run.func1()
2026-02-03T19:00:16.686558346Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:973 +0x45
2026-02-03T19:00:16.686566736Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.686574876Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.686586996Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc000a91f70, {0x23eab40, 0xc0007ce7e0}, 0x1, 0xc0009a28c0)
2026-02-03T19:00:16.686600206Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.686621117Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc00011f770, 0x3b9aca00, 0x0, 0x1, 0xc0009a28c0)
2026-02-03T19:00:16.686629467Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.686639297Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.686646987Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.686651837Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run(0xc0001443f0)
2026-02-03T19:00:16.686661587Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:972 +0x5a
2026-02-03T19:00:16.686665957Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.686675877Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.686683077Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 48
2026-02-03T19:00:16.686692167Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.686696508Z stderr F 
2026-02-03T19:00:16.686700408Z stderr F goroutine 144 [select, 2 minutes]:
2026-02-03T19:00:16.686713288Z stderr F reflect.rselect({0xc000a94f00, 0x3, 0xc000099f68?})
2026-02-03T19:00:16.686722248Z stderr F 	/usr/local/go/src/runtime/select.go:600 +0x2c5
2026-02-03T19:00:16.686741458Z stderr F reflect.Select({0xc0009a4000?, 0x3, 0x1b626a0?})
2026-02-03T19:00:16.686776258Z stderr F 	/usr/local/go/src/reflect/value.go:3176 +0x5ca
2026-02-03T19:00:16.686785058Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...].func2()
2026-02-03T19:00:16.686789659Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:34 +0x4f
2026-02-03T19:00:16.686793679Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...] in goroutine 178
2026-02-03T19:00:16.686797539Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:32 +0x438
2026-02-03T19:00:16.686806399Z stderr F 
2026-02-03T19:00:16.686810879Z stderr F goroutine 124 [select, 2 minutes]:
2026-02-03T19:00:16.686819469Z stderr F k8s.io/client-go/tools/record.(*eventBroadcasterImpl).StartEventWatcher.func1()
2026-02-03T19:00:16.686823929Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/record/event.go:407 +0xfe
2026-02-03T19:00:16.686843429Z stderr F created by k8s.io/client-go/tools/record.(*eventBroadcasterImpl).StartEventWatcher in goroutine 145
2026-02-03T19:00:16.686847279Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/record/event.go:404 +0xb5
2026-02-03T19:00:16.686850339Z stderr F 
2026-02-03T19:00:16.686856999Z stderr F goroutine 152 [chan receive, 2 minutes]:
2026-02-03T19:00:16.686860449Z stderr F k8s.io/client-go/tools/cache.(*sharedProcessor).run(0xc0003ce190, 0xc0004f8fc0)
2026-02-03T19:00:16.686867649Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:807 +0x4d
2026-02-03T19:00:16.68688304Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run.(*Group).StartWithChannel.func4()
2026-02-03T19:00:16.68689582Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.68690017Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.68690949Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.686918Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 121
2026-02-03T19:00:16.68692646Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.68693052Z stderr F 
2026-02-03T19:00:16.68694293Z stderr F goroutine 153 [chan receive, 2 minutes]:
2026-02-03T19:00:16.68694731Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.func1()
2026-02-03T19:00:16.68695609Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:138 +0x25
2026-02-03T19:00:16.68696428Z stderr F created by k8s.io/client-go/tools/cache.(*controller).Run in goroutine 121
2026-02-03T19:00:16.686972921Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:137 +0xab
2026-02-03T19:00:16.687010771Z stderr F 
2026-02-03T19:00:16.687038901Z stderr F goroutine 194 [chan receive, 2 minutes]:
2026-02-03T19:00:16.687049841Z stderr F k8s.io/client-go/tools/cache.(*sharedProcessor).run(0xc0003eb130, 0xc000a982a0)
2026-02-03T19:00:16.687054361Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:807 +0x4d
2026-02-03T19:00:16.687058501Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run.(*Group).StartWithChannel.func4()
2026-02-03T19:00:16.687062702Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.687066732Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.687093502Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.687099492Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 178
2026-02-03T19:00:16.687109642Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.687118162Z stderr F 
2026-02-03T19:00:16.687137872Z stderr F goroutine 195 [chan receive, 2 minutes]:
2026-02-03T19:00:16.687142882Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.func1()
2026-02-03T19:00:16.687146782Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:138 +0x25
2026-02-03T19:00:16.687150453Z stderr F created by k8s.io/client-go/tools/cache.(*controller).Run in goroutine 178
2026-02-03T19:00:16.687154793Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:137 +0xab
2026-02-03T19:00:16.687158653Z stderr F 
2026-02-03T19:00:16.687163183Z stderr F goroutine 154 [select]:
2026-02-03T19:00:16.687177623Z stderr F k8s.io/client-go/tools/cache.handleAnyWatch({0xc00070e95a?, 0x3?, 0x35b55e0?}, {0x23f6d30, 0xc00074a7c0}, {0x7f4e846c7260, 0xc00037b130}, {0x2437500, 0x20770c0}, 0x0, ...)
2026-02-03T19:00:16.687182433Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:802 +0x230
2026-02-03T19:00:16.687213923Z stderr F k8s.io/client-go/tools/cache.handleWatch({0x3?, 0x0?, 0x35b55e0?}, {0x23f6d30?, 0xc00074a7c0?}, {0x7f4e846c7260?, 0xc00037b130?}, {0x2437500?, 0x20770c0?}, 0x0, ...)
2026-02-03T19:00:16.687234463Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:768 +0xdd
2026-02-03T19:00:16.687254474Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watch(0xc000216f00, {0x0?, 0x0?}, 0xc0004f8ee0, 0xc0002d31f0)
2026-02-03T19:00:16.687268034Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:466 +0x556
2026-02-03T19:00:16.687279994Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watchWithResync(0xc000216f00, {0x0, 0x0}, 0xc0004f8ee0)
2026-02-03T19:00:16.687292384Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:414 +0x12c
2026-02-03T19:00:16.687300734Z stderr F k8s.io/client-go/tools/cache.(*Reflector).ListAndWatch(0xc000216f00, 0xc0004f8ee0)
2026-02-03T19:00:16.687308944Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:377 +0x3c5
2026-02-03T19:00:16.687317204Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run.func1()
2026-02-03T19:00:16.687325124Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:315 +0x25
2026-02-03T19:00:16.687333195Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x10?)
2026-02-03T19:00:16.687341115Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.687356735Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0004f5f50, {0x23eab60, 0xc000448190}, 0x1, 0xc0004f8ee0)
2026-02-03T19:00:16.687378435Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.687383495Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run(0xc000216f00, 0xc0004f8ee0)
2026-02-03T19:00:16.687395915Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:314 +0x1af
2026-02-03T19:00:16.687400575Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.(*Group).StartWithChannel.func2()
2026-02-03T19:00:16.687408555Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.687417395Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.687426116Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.687434886Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 121
2026-02-03T19:00:16.687443086Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.687449786Z stderr F 
2026-02-03T19:00:16.687460486Z stderr F goroutine 196 [select]:
2026-02-03T19:00:16.687513906Z stderr F k8s.io/client-go/tools/cache.handleAnyWatch({0xc0001952b8?, 0x3?, 0x35b55e0?}, {0x23f6d30, 0xc000892180}, {0x7f4e846c7260, 0xc0009a40b0}, {0x2437500, 0x20981c0}, 0xc00099c6c0, ...)
2026-02-03T19:00:16.687526417Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:802 +0x230
2026-02-03T19:00:16.687578567Z stderr F k8s.io/client-go/tools/cache.handleWatch({0x3?, 0x0?, 0x35b55e0?}, {0x23f6d30?, 0xc000892180?}, {0x7f4e846c7260?, 0xc0009a40b0?}, {0x2437500?, 0x20981c0?}, 0xc00099c6c0, ...)
2026-02-03T19:00:16.687594437Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:768 +0xdd
2026-02-03T19:00:16.687614488Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watch(0xc0007a6870, {0x0?, 0x0?}, 0xc000a981c0, 0xc0004224d0)
2026-02-03T19:00:16.687628158Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:466 +0x556
2026-02-03T19:00:16.687640398Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watchWithResync(0xc0007a6870, {0x0, 0x0}, 0xc000a981c0)
2026-02-03T19:00:16.687651158Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:414 +0x12c
2026-02-03T19:00:16.687660428Z stderr F k8s.io/client-go/tools/cache.(*Reflector).ListAndWatch(0xc0007a6870, 0xc000a981c0)
2026-02-03T19:00:16.687672738Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:377 +0x3c5
2026-02-03T19:00:16.687682398Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run.func1()
2026-02-03T19:00:16.687690898Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:315 +0x25
2026-02-03T19:00:16.687701679Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x10?)
2026-02-03T19:00:16.687710649Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.687722839Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc000807f50, {0x23eab60, 0xc00013c140}, 0x1, 0xc000a981c0)
2026-02-03T19:00:16.687744219Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.687767299Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run(0xc0007a6870, 0xc000a981c0)
2026-02-03T19:00:16.687774759Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:314 +0x1af
2026-02-03T19:00:16.687778779Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.(*Group).StartWithChannel.func2()
2026-02-03T19:00:16.68779075Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.68779549Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.68783976Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.68784621Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 178
2026-02-03T19:00:16.68785024Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.6878538Z stderr F 
2026-02-03T19:00:16.68785772Z stderr F goroutine 225 [select, 2 minutes]:
2026-02-03T19:00:16.68786183Z stderr F k8s.io/client-go/tools/cache.(*Reflector).startResync(0xc000216f00, 0xc0004f8ee0, 0xc0000dd5e0, 0xc0002d31f0)
2026-02-03T19:00:16.68787172Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:389 +0x106
2026-02-03T19:00:16.68787607Z stderr F created by k8s.io/client-go/tools/cache.(*Reflector).watchWithResync in goroutine 154
2026-02-03T19:00:16.687880051Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:413 +0x105
2026-02-03T19:00:16.687883731Z stderr F 
2026-02-03T19:00:16.687895931Z stderr F goroutine 210 [select, 2 minutes]:
2026-02-03T19:00:16.687900261Z stderr F k8s.io/client-go/tools/cache.(*Reflector).startResync(0xc0007a6870, 0xc000a981c0, 0xc000946230, 0xc0004224d0)
2026-02-03T19:00:16.687912271Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:389 +0x106
2026-02-03T19:00:16.687916441Z stderr F created by k8s.io/client-go/tools/cache.(*Reflector).watchWithResync in goroutine 196
2026-02-03T19:00:16.687928101Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:413 +0x105
2026-02-03T19:00:16.687932111Z stderr F 
2026-02-03T19:00:16.687936191Z stderr F goroutine 180 [sync.Cond.Wait]:
2026-02-03T19:00:16.687947921Z stderr F sync.runtime_notifyListWait(0xc000698868, 0xc)
2026-02-03T19:00:16.687956771Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.687971982Z stderr F sync.(*Cond).Wait(0xc0001bc500?)
2026-02-03T19:00:16.687980252Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.687988252Z stderr F k8s.io/client-go/tools/cache.(*DeltaFIFO).Pop(0xc000698840, 0xc0003d7260)
2026-02-03T19:00:16.687996002Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/delta_fifo.go:588 +0x231
2026-02-03T19:00:16.688003622Z stderr F k8s.io/client-go/tools/cache.(*controller).processLoop(0xc0006988f0)
2026-02-03T19:00:16.688015912Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:195 +0x30
2026-02-03T19:00:16.688028142Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.688036352Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.688055732Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0007a1de8, {0x23eab40, 0xc0005b5050}, 0x1, 0xc0009a2700)
2026-02-03T19:00:16.688069223Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.688092963Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc0007a1de8, 0x3b9aca00, 0x0, 0x1, 0xc0009a2700)
2026-02-03T19:00:16.688103453Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.688121703Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.688154634Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.688163264Z stderr F k8s.io/client-go/tools/cache.(*controller).Run(0xc0006988f0, 0xc0009a2700)
2026-02-03T19:00:16.688167154Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:166 +0x375
2026-02-03T19:00:16.688170904Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run(0xc0006986e0, 0xc0009a2700)
2026-02-03T19:00:16.688174654Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:508 +0x2a9
2026-02-03T19:00:16.688182114Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Cache).Start(0xc0000e4f50, 0x0?)
2026-02-03T19:00:16.688189014Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:108 +0x72
2026-02-03T19:00:16.688200214Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked.func1()
2026-02-03T19:00:16.688204394Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:242 +0x75
2026-02-03T19:00:16.688208124Z stderr F created by sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked in goroutine 161
2026-02-03T19:00:16.688216484Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:240 +0x87
2026-02-03T19:00:16.688220384Z stderr F 
2026-02-03T19:00:16.688229294Z stderr F goroutine 103 [chan receive]:
2026-02-03T19:00:16.688233504Z stderr F k8s.io/client-go/util/workqueue.(*Typed[...]).updateUnfinishedWorkLoop(0x241eba0)
2026-02-03T19:00:16.688241724Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:355 +0x97
2026-02-03T19:00:16.688250005Z stderr F created by k8s.io/client-go/util/workqueue.newQueue[...] in goroutine 264
2026-02-03T19:00:16.688258415Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:176 +0x1e7
2026-02-03T19:00:16.688262505Z stderr F 
2026-02-03T19:00:16.688270755Z stderr F goroutine 182 [select, 2 minutes]:
2026-02-03T19:00:16.688283085Z stderr F reflect.rselect({0xc00088ef00, 0x3, 0x0?})
2026-02-03T19:00:16.688295285Z stderr F 	/usr/local/go/src/runtime/select.go:600 +0x2c5
2026-02-03T19:00:16.688316505Z stderr F reflect.Select({0xc000698790?, 0x3, 0x0?})
2026-02-03T19:00:16.688327315Z stderr F 	/usr/local/go/src/reflect/value.go:3176 +0x5ca
2026-02-03T19:00:16.688335376Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...].func2()
2026-02-03T19:00:16.688343056Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:34 +0x4f
2026-02-03T19:00:16.688350546Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...] in goroutine 180
2026-02-03T19:00:16.688358186Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:32 +0x438
2026-02-03T19:00:16.688361816Z stderr F 
2026-02-03T19:00:16.688369696Z stderr F goroutine 101 [sync.Cond.Wait]:
2026-02-03T19:00:16.688377616Z stderr F sync.runtime_notifyListWait(0xc0008864c8, 0x9)
2026-02-03T19:00:16.688385766Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.688422096Z stderr F sync.(*Cond).Wait(0xc0008a2118?)
2026-02-03T19:00:16.688426457Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.688434087Z stderr F golang.org/x/net/http2.(*pipe).Read(0xc0008864b0, {0xc000d36001, 0xfdff, 0xfdff})
2026-02-03T19:00:16.688441687Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/pipe.go:76 +0xd6
2026-02-03T19:00:16.688463077Z stderr F golang.org/x/net/http2.transportResponseBody.Read({0x46fe5d?}, {0xc000d36001?, 0x21d8500?, 0x21d8508?})
2026-02-03T19:00:16.688473037Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:2560 +0x65
2026-02-03T19:00:16.688509827Z stderr F encoding/json.(*Decoder).refill(0xc000412000)
2026-02-03T19:00:16.688514577Z stderr F 	/usr/local/go/src/encoding/json/stream.go:165 +0x188
2026-02-03T19:00:16.688518348Z stderr F encoding/json.(*Decoder).readValue(0xc000412000)
2026-02-03T19:00:16.688522278Z stderr F 	/usr/local/go/src/encoding/json/stream.go:140 +0x85
2026-02-03T19:00:16.688531988Z stderr F encoding/json.(*Decoder).Decode(0xc000412000, {0x1dc8100, 0xc000c1d1d0})
2026-02-03T19:00:16.688547078Z stderr F 	/usr/local/go/src/encoding/json/stream.go:63 +0x75
2026-02-03T19:00:16.688559118Z stderr F k8s.io/apimachinery/pkg/util/framer.(*jsonFrameReader).Read(0xc0007ce390, {0xc000d5c000, 0x10000, 0x14000})
2026-02-03T19:00:16.688567338Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/framer/framer.go:151 +0x15c
2026-02-03T19:00:16.688586848Z stderr F k8s.io/apimachinery/pkg/runtime/serializer/streaming.(*decoder).Decode(0xc00040a000, 0x0, {0x23f31a0, 0xc0005ad8c0})
2026-02-03T19:00:16.688599388Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/runtime/serializer/streaming/streaming.go:77 +0xa3
2026-02-03T19:00:16.688607479Z stderr F k8s.io/client-go/rest/watch.(*Decoder).Decode(0xc00064a120)
2026-02-03T19:00:16.688622939Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/rest/watch/decoder.go:49 +0x4b
2026-02-03T19:00:16.688634439Z stderr F k8s.io/apimachinery/pkg/watch.(*StreamWatcher).receive(0xc000892180)
2026-02-03T19:00:16.688645619Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:105 +0xc7
2026-02-03T19:00:16.688653779Z stderr F created by k8s.io/apimachinery/pkg/watch.NewStreamWatcher in goroutine 196
2026-02-03T19:00:16.688661959Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:76 +0x105
2026-02-03T19:00:16.688665869Z stderr F 
2026-02-03T19:00:16.688674419Z stderr F goroutine 184 [chan receive, 2 minutes]:
2026-02-03T19:00:16.688682539Z stderr F k8s.io/client-go/tools/cache.(*sharedProcessor).run(0xc0003eb540, 0xc0009a27e0)
2026-02-03T19:00:16.688694519Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:807 +0x4d
2026-02-03T19:00:16.68870328Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run.(*Group).StartWithChannel.func4()
2026-02-03T19:00:16.68871143Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.68871957Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.68872985Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.68874071Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 180
2026-02-03T19:00:16.6887486Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.68875236Z stderr F 
2026-02-03T19:00:16.68876055Z stderr F goroutine 185 [chan receive, 2 minutes]:
2026-02-03T19:00:16.68876891Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.func1()
2026-02-03T19:00:16.68877698Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:138 +0x25
2026-02-03T19:00:16.68878504Z stderr F created by k8s.io/client-go/tools/cache.(*controller).Run in goroutine 180
2026-02-03T19:00:16.688796821Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:137 +0xab
2026-02-03T19:00:16.688804821Z stderr F 
2026-02-03T19:00:16.688813111Z stderr F goroutine 186 [select]:
2026-02-03T19:00:16.688868521Z stderr F k8s.io/client-go/tools/cache.handleAnyWatch({0xc00070ebb0?, 0x3?, 0x35b55e0?}, {0x23f6d30, 0xc000882700}, {0x7f4e846c7260, 0xc000698840}, {0x2437500, 0x20981c0}, 0xc0005b5020, ...)
2026-02-03T19:00:16.688879901Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:802 +0x230
2026-02-03T19:00:16.688934492Z stderr F k8s.io/client-go/tools/cache.handleWatch({0x3?, 0x0?, 0x35b55e0?}, {0x23f6d30?, 0xc000882700?}, {0x7f4e846c7260?, 0xc000698840?}, {0x2437500?, 0x20981c0?}, 0xc0005b5020, ...)
2026-02-03T19:00:16.688952122Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:768 +0xdd
2026-02-03T19:00:16.688971823Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watch(0xc000b001e0, {0x0?, 0x0?}, 0xc0009a2700, 0xc0002d33b0)
2026-02-03T19:00:16.688983323Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:466 +0x556
2026-02-03T19:00:16.688999023Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watchWithResync(0xc000b001e0, {0x0, 0x0}, 0xc0009a2700)
2026-02-03T19:00:16.689010613Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:414 +0x12c
2026-02-03T19:00:16.689022023Z stderr F k8s.io/client-go/tools/cache.(*Reflector).ListAndWatch(0xc000b001e0, 0xc0009a2700)
2026-02-03T19:00:16.689033143Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:377 +0x3c5
2026-02-03T19:00:16.689037113Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run.func1()
2026-02-03T19:00:16.689047303Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:315 +0x25
2026-02-03T19:00:16.689059073Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x10?)
2026-02-03T19:00:16.689067474Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.689078684Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc00069ff50, {0x23eab60, 0xc0003eb5e0}, 0x1, 0xc0009a2700)
2026-02-03T19:00:16.689089954Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.689102574Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run(0xc000b001e0, 0xc0009a2700)
2026-02-03T19:00:16.689115174Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:314 +0x1af
2026-02-03T19:00:16.689119364Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.(*Group).StartWithChannel.func2()
2026-02-03T19:00:16.689130454Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.689134354Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.689145284Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.689149414Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 180
2026-02-03T19:00:16.689172895Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.689180555Z stderr F 
2026-02-03T19:00:16.689200495Z stderr F goroutine 227 [select, 2 minutes]:
2026-02-03T19:00:16.689204965Z stderr F k8s.io/client-go/tools/cache.(*Reflector).startResync(0xc000b001e0, 0xc0009a2700, 0xc0000dd810, 0xc0002d33b0)
2026-02-03T19:00:16.689212885Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:389 +0x106
2026-02-03T19:00:16.689221095Z stderr F created by k8s.io/client-go/tools/cache.(*Reflector).watchWithResync in goroutine 186
2026-02-03T19:00:16.689229165Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:413 +0x105
2026-02-03T19:00:16.689233015Z stderr F 
2026-02-03T19:00:16.689240875Z stderr F goroutine 212 [sync.Cond.Wait]:
2026-02-03T19:00:16.689248766Z stderr F sync.runtime_notifyListWait(0xc00076c648, 0xe)
2026-02-03T19:00:16.689256876Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.689268436Z stderr F sync.(*Cond).Wait(0xc0008a2100?)
2026-02-03T19:00:16.689280376Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.689299506Z stderr F golang.org/x/net/http2.(*pipe).Read(0xc00076c630, {0xc000ce6001, 0xfdff, 0xfdff})
2026-02-03T19:00:16.689349727Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/pipe.go:76 +0xd6
2026-02-03T19:00:16.689363537Z stderr F golang.org/x/net/http2.transportResponseBody.Read({0x46fe5d?}, {0xc000ce6001?, 0x21d8500?, 0x21d8508?})
2026-02-03T19:00:16.689368437Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:2560 +0x65
2026-02-03T19:00:16.689377187Z stderr F encoding/json.(*Decoder).refill(0xc0001f9400)
2026-02-03T19:00:16.689381267Z stderr F 	/usr/local/go/src/encoding/json/stream.go:165 +0x188
2026-02-03T19:00:16.689395857Z stderr F encoding/json.(*Decoder).readValue(0xc0001f9400)
2026-02-03T19:00:16.689400207Z stderr F 	/usr/local/go/src/encoding/json/stream.go:140 +0x85
2026-02-03T19:00:16.689438768Z stderr F encoding/json.(*Decoder).Decode(0xc0001f9400, {0x1dc8100, 0xc000c1d110})
2026-02-03T19:00:16.689449668Z stderr F 	/usr/local/go/src/encoding/json/stream.go:63 +0x75
2026-02-03T19:00:16.689458178Z stderr F k8s.io/apimachinery/pkg/util/framer.(*jsonFrameReader).Read(0xc00094e210, {0xc000e90000, 0x10000, 0x14000})
2026-02-03T19:00:16.689462578Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/framer/framer.go:151 +0x15c
2026-02-03T19:00:16.689471298Z stderr F k8s.io/apimachinery/pkg/runtime/serializer/streaming.(*decoder).Decode(0xc0003e8410, 0x0, {0x23f31a0, 0xc0005ad840})
2026-02-03T19:00:16.689480358Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/runtime/serializer/streaming/streaming.go:77 +0xa3
2026-02-03T19:00:16.689487118Z stderr F k8s.io/client-go/rest/watch.(*Decoder).Decode(0xc000794560)
2026-02-03T19:00:16.689500588Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/rest/watch/decoder.go:49 +0x4b
2026-02-03T19:00:16.689505108Z stderr F k8s.io/apimachinery/pkg/watch.(*StreamWatcher).receive(0xc000882700)
2026-02-03T19:00:16.689513798Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:105 +0xc7
2026-02-03T19:00:16.689521299Z stderr F created by k8s.io/apimachinery/pkg/watch.NewStreamWatcher in goroutine 186
2026-02-03T19:00:16.689527889Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:76 +0x105
2026-02-03T19:00:16.689531079Z stderr F 
2026-02-03T19:00:16.689537899Z stderr F goroutine 228 [select, 2 minutes]:
2026-02-03T19:00:16.6896348Z stderr F golang.org/x/net/http2.(*clientStream).writeRequest(0xc00076c600, 0xc00037d2c0, 0x0)
2026-02-03T19:00:16.68964237Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1570 +0xc85
2026-02-03T19:00:16.6896464Z stderr F golang.org/x/net/http2.(*clientStream).doRequest(0xc00076c600, 0x16c5b44?, 0xc0008020c0?)
2026-02-03T19:00:16.68965032Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1431 +0x56
2026-02-03T19:00:16.68965421Z stderr F created by golang.org/x/net/http2.(*ClientConn).roundTrip in goroutine 186
2026-02-03T19:00:16.68965813Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1336 +0x44b
2026-02-03T19:00:16.68966765Z stderr F 
2026-02-03T19:00:16.689672Z stderr F goroutine 211 [select, 2 minutes]:
2026-02-03T19:00:16.68967601Z stderr F golang.org/x/net/http2.(*clientStream).writeRequest(0xc000886480, 0xc0001f8f00, 0x0)
2026-02-03T19:00:16.68968006Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1570 +0xc85
2026-02-03T19:00:16.689689Z stderr F golang.org/x/net/http2.(*clientStream).doRequest(0xc000886480, 0x0?, 0x21da0a8?)
2026-02-03T19:00:16.68969328Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1431 +0x56
2026-02-03T19:00:16.68969714Z stderr F created by golang.org/x/net/http2.(*ClientConn).roundTrip in goroutine 196
2026-02-03T19:00:16.689706241Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1336 +0x44b
2026-02-03T19:00:16.689709931Z stderr F 
2026-02-03T19:00:16.689716481Z stderr F goroutine 125 [select, 2 minutes]:
2026-02-03T19:00:16.689719831Z stderr F k8s.io/client-go/tools/record.(*eventBroadcasterImpl).StartEventWatcher.func1()
2026-02-03T19:00:16.689726261Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/record/event.go:407 +0xfe
2026-02-03T19:00:16.689732781Z stderr F created by k8s.io/client-go/tools/record.(*eventBroadcasterImpl).StartEventWatcher in goroutine 145
2026-02-03T19:00:16.689739321Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/record/event.go:404 +0xb5
2026-02-03T19:00:16.689742461Z stderr F 
2026-02-03T19:00:16.689750571Z stderr F goroutine 265 [chan receive, 2 minutes]:
2026-02-03T19:00:16.689789331Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start(0x242b540, {0x240c908, 0xc0003e9b80})
2026-02-03T19:00:16.689801692Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:261 +0x1a9
2026-02-03T19:00:16.689812282Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc00042c5c0)
2026-02-03T19:00:16.689816002Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.689822712Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 199
2026-02-03T19:00:16.689829212Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.689832382Z stderr F 
2026-02-03T19:00:16.689841882Z stderr F goroutine 199 [chan receive, 2 minutes]:
2026-02-03T19:00:16.689852922Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile(0xc0007b2d80)
2026-02-03T19:00:16.689865472Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:186 +0x45
2026-02-03T19:00:16.689870262Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).Start.func1 in goroutine 126
2026-02-03T19:00:16.689882593Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:139 +0xbf
2026-02-03T19:00:16.689886813Z stderr F 
2026-02-03T19:00:16.689890973Z stderr F goroutine 326 [select]:
2026-02-03T19:00:16.689899393Z stderr F k8s.io/client-go/tools/cache.(*processorListener).pop(0xc000de23f0)
2026-02-03T19:00:16.689908593Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:943 +0xf5
2026-02-03T19:00:16.689912963Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.689921063Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.689952213Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 276
2026-02-03T19:00:16.689957653Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.689961323Z stderr F 
2026-02-03T19:00:16.689965363Z stderr F goroutine 104 [select]:
2026-02-03T19:00:16.689969583Z stderr F k8s.io/client-go/util/workqueue.(*delayingType[...]).waitingLoop(0x241b7c0)
2026-02-03T19:00:16.689979034Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/delaying_queue.go:311 +0x334
2026-02-03T19:00:16.689983604Z stderr F created by k8s.io/client-go/util/workqueue.newDelayingQueue[...] in goroutine 264
2026-02-03T19:00:16.689987584Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/delaying_queue.go:148 +0x245
2026-02-03T19:00:16.689991404Z stderr F 
2026-02-03T19:00:16.690000734Z stderr F goroutine 226 [select, 2 minutes]:
2026-02-03T19:00:16.690007584Z stderr F golang.org/x/net/http2.(*clientStream).writeRequest(0xc00076c300, 0xc00037cc80, 0x0)
2026-02-03T19:00:16.690014014Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1570 +0xc85
2026-02-03T19:00:16.690029224Z stderr F golang.org/x/net/http2.(*clientStream).doRequest(0xc00076c300, 0x0?, 0x0?)
2026-02-03T19:00:16.690035894Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1431 +0x56
2026-02-03T19:00:16.690045204Z stderr F created by golang.org/x/net/http2.(*ClientConn).roundTrip in goroutine 154
2026-02-03T19:00:16.690054844Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1336 +0x44b
2026-02-03T19:00:16.690061284Z stderr F 
2026-02-03T19:00:16.690064775Z stderr F goroutine 229 [sync.Cond.Wait]:
2026-02-03T19:00:16.690084695Z stderr F sync.runtime_notifyListWait(0xc00076c348, 0x3)
2026-02-03T19:00:16.690092105Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.690095575Z stderr F sync.(*Cond).Wait(0x2?)
2026-02-03T19:00:16.690102315Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.690120245Z stderr F golang.org/x/net/http2.(*pipe).Read(0xc00076c330, {0xc000c6e70c, 0x4, 0x4})
2026-02-03T19:00:16.690129805Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/pipe.go:76 +0xd6
2026-02-03T19:00:16.690152475Z stderr F golang.org/x/net/http2.transportResponseBody.Read({0x0?}, {0xc000c6e70c?, 0xc00079bce0?, 0x410725?})
2026-02-03T19:00:16.690170396Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:2560 +0x65
2026-02-03T19:00:16.690195746Z stderr F io.ReadAtLeast({0x7f4e848d5e48, 0xc00076c300}, {0xc000c6e70c, 0x4, 0x4}, 0x4)
2026-02-03T19:00:16.690207426Z stderr F 	/usr/local/go/src/io/io.go:335 +0x90
2026-02-03T19:00:16.690229596Z stderr F k8s.io/apimachinery/pkg/util/framer.(*lengthDelimitedFrameReader).Read(0xc000011698, {0xc000b9e000, 0x2000, 0x2500})
2026-02-03T19:00:16.690238396Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/framer/framer.go:76 +0x88
2026-02-03T19:00:16.690260787Z stderr F k8s.io/apimachinery/pkg/runtime/serializer/streaming.(*decoder).Decode(0xc0003cea00, 0x0, {0x23f31a0, 0xc000882380})
2026-02-03T19:00:16.690274077Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/runtime/serializer/streaming/streaming.go:77 +0xa3
2026-02-03T19:00:16.690285847Z stderr F k8s.io/client-go/rest/watch.(*Decoder).Decode(0xc00042c6c0)
2026-02-03T19:00:16.690298087Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/rest/watch/decoder.go:49 +0x4b
2026-02-03T19:00:16.690306537Z stderr F k8s.io/apimachinery/pkg/watch.(*StreamWatcher).receive(0xc00074a7c0)
2026-02-03T19:00:16.690314567Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:105 +0xc7
2026-02-03T19:00:16.690322637Z stderr F created by k8s.io/apimachinery/pkg/watch.NewStreamWatcher in goroutine 154
2026-02-03T19:00:16.690334227Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:76 +0x105
2026-02-03T19:00:16.690338368Z stderr F 
2026-02-03T19:00:16.690342498Z stderr F goroutine 241 [chan receive]:
2026-02-03T19:00:16.690352568Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run.func1()
2026-02-03T19:00:16.690358708Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:973 +0x45
2026-02-03T19:00:16.690366898Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.690378658Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.690395638Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc00079ff70, {0x23eab40, 0xc0007ce660}, 0x1, 0xc0009a2380)
2026-02-03T19:00:16.690404688Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.690422938Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc000a86f70, 0x3b9aca00, 0x0, 0x1, 0xc0009a2380)
2026-02-03T19:00:16.690433079Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.690442929Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.690451039Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.690460679Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run(0xc000144120)
2026-02-03T19:00:16.690470649Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:972 +0x5a
2026-02-03T19:00:16.690475909Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.690488749Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.690499049Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 143
2026-02-03T19:00:16.690512099Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.690517869Z stderr F 
2026-02-03T19:00:16.69052854Z stderr F goroutine 242 [select]:
2026-02-03T19:00:16.69053979Z stderr F k8s.io/client-go/tools/cache.(*processorListener).pop(0xc000144120)
2026-02-03T19:00:16.69055042Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:943 +0xf5
2026-02-03T19:00:16.69056165Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.69057847Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.69058373Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 143
2026-02-03T19:00:16.69058798Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.69059262Z stderr F 
2026-02-03T19:00:16.69060223Z stderr F goroutine 191 [select]:
2026-02-03T19:00:16.69060851Z stderr F k8s.io/client-go/tools/cache.(*processorListener).pop(0xc0008a4000)
2026-02-03T19:00:16.690620031Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:943 +0xf5
2026-02-03T19:00:16.690628411Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.690632671Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.690636661Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 161
2026-02-03T19:00:16.690645751Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.690649621Z stderr F 
2026-02-03T19:00:16.690653991Z stderr F goroutine 314 [IO wait]:
2026-02-03T19:00:16.690662351Z stderr F internal/poll.runtime_pollWait(0x7f4e849ef560, 0x72)
2026-02-03T19:00:16.690666391Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.690677811Z stderr F internal/poll.(*pollDesc).wait(0xc000dfb280?, 0xc0002bd000?, 0x0)
2026-02-03T19:00:16.690689041Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.690701982Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.690711712Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.690727962Z stderr F internal/poll.(*FD).Read(0xc000dfb280, {0xc0002bd000, 0xc00, 0xc00})
2026-02-03T19:00:16.690740792Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:165 +0x27a
2026-02-03T19:00:16.690758192Z stderr F net.(*netFD).Read(0xc000dfb280, {0xc0002bd000?, 0xc000869b88?, 0x65ca62?})
2026-02-03T19:00:16.690767592Z stderr F 	/usr/local/go/src/net/fd_posix.go:55 +0x25
2026-02-03T19:00:16.690792092Z stderr F net.(*conn).Read(0xc0008a2670, {0xc0002bd000?, 0x240c8d0?, 0xc00060b290?})
2026-02-03T19:00:16.690801503Z stderr F 	/usr/local/go/src/net/net.go:189 +0x45
2026-02-03T19:00:16.690824653Z stderr F crypto/tls.(*atLeastReader).Read(0xc0002967f8, {0xc0002bd000?, 0x0?, 0xc0002967f8?})
2026-02-03T19:00:16.690833623Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:809 +0x3b
2026-02-03T19:00:16.690849093Z stderr F bytes.(*Buffer).ReadFrom(0xc000705b38, {0x23e8220, 0xc0002967f8})
2026-02-03T19:00:16.690861003Z stderr F 	/usr/local/go/src/bytes/buffer.go:211 +0x98
2026-02-03T19:00:16.690880603Z stderr F crypto/tls.(*Conn).readFromUntil(0xc000705888, {0x23e9a00, 0xc0008a2670}, 0xc000869cf8?)
2026-02-03T19:00:16.690895274Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:831 +0xde
2026-02-03T19:00:16.690906604Z stderr F crypto/tls.(*Conn).readRecordOrCCS(0xc000705888, 0x0)
2026-02-03T19:00:16.690919574Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:629 +0x3cf
2026-02-03T19:00:16.690936174Z stderr F crypto/tls.(*Conn).readRecord(...)
2026-02-03T19:00:16.690940804Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:591
2026-02-03T19:00:16.690953834Z stderr F crypto/tls.(*Conn).Read(0xc000705888, {0xc000151091, 0x1, 0xc0008fb110?})
2026-02-03T19:00:16.690963384Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:1385 +0x150
2026-02-03T19:00:16.690994825Z stderr F net/http.(*connReader).backgroundRead(0xc000151080)
2026-02-03T19:00:16.691000705Z stderr F 	/usr/local/go/src/net/http/server.go:690 +0x37
2026-02-03T19:00:16.691004825Z stderr F created by net/http.(*connReader).startBackgroundRead in goroutine 557
2026-02-03T19:00:16.691016645Z stderr F 	/usr/local/go/src/net/http/server.go:686 +0xb6
2026-02-03T19:00:16.691026655Z stderr F 
2026-02-03T19:00:16.691037335Z stderr F goroutine 279 [select, 2 minutes]:
2026-02-03T19:00:16.691047115Z stderr F reflect.rselect({0xc00079cf00, 0x3, 0x7f4ecb661108?})
2026-02-03T19:00:16.691061375Z stderr F 	/usr/local/go/src/runtime/select.go:600 +0x2c5
2026-02-03T19:00:16.691072946Z stderr F reflect.Select({0xc000186420?, 0x3, 0xc00080dfd0?})
2026-02-03T19:00:16.691084256Z stderr F 	/usr/local/go/src/reflect/value.go:3176 +0x5ca
2026-02-03T19:00:16.691095506Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...].func2()
2026-02-03T19:00:16.691108236Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:34 +0x4f
2026-02-03T19:00:16.691117256Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...] in goroutine 277
2026-02-03T19:00:16.691126076Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:32 +0x438
2026-02-03T19:00:16.691130106Z stderr F 
2026-02-03T19:00:16.691143186Z stderr F goroutine 264 [chan receive, 2 minutes]:
2026-02-03T19:00:16.691156146Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start(0x242b540, {0x240c908, 0xc0003e9b80})
2026-02-03T19:00:16.691169147Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:261 +0x1a9
2026-02-03T19:00:16.691181497Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc0005a9f60)
2026-02-03T19:00:16.691188397Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.691201417Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 199
2026-02-03T19:00:16.691204987Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.691208077Z stderr F 
2026-02-03T19:00:16.691217597Z stderr F goroutine 203 [IO wait]:
2026-02-03T19:00:16.691224967Z stderr F internal/poll.runtime_pollWait(0x7f4e849ef9c0, 0x72)
2026-02-03T19:00:16.691237337Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.691249848Z stderr F internal/poll.(*pollDesc).wait(0xc000940680?, 0x900000036?, 0x0)
2026-02-03T19:00:16.691262628Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.691272898Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.691276758Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.691286748Z stderr F internal/poll.(*FD).Accept(0xc000940680)
2026-02-03T19:00:16.691293448Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:620 +0x295
2026-02-03T19:00:16.691299908Z stderr F net.(*netFD).accept(0xc000940680)
2026-02-03T19:00:16.691306598Z stderr F 	/usr/local/go/src/net/fd_unix.go:172 +0x29
2026-02-03T19:00:16.691316538Z stderr F net.(*TCPListener).accept(0xc000892380)
2026-02-03T19:00:16.691332468Z stderr F 	/usr/local/go/src/net/tcpsock_posix.go:159 +0x1e
2026-02-03T19:00:16.691336788Z stderr F net.(*TCPListener).Accept(0xc000892380)
2026-02-03T19:00:16.691344849Z stderr F 	/usr/local/go/src/net/tcpsock.go:372 +0x30
2026-02-03T19:00:16.691352679Z stderr F crypto/tls.(*listener).Accept(0xc000011230)
2026-02-03T19:00:16.691360629Z stderr F 	/usr/local/go/src/crypto/tls/tls.go:67 +0x27
2026-02-03T19:00:16.691379259Z stderr F net/http.(*Server).Serve(0xc0007a64b0, {0x23fb548, 0xc000011230})
2026-02-03T19:00:16.691390969Z stderr F 	/usr/local/go/src/net/http/server.go:3330 +0x30c
2026-02-03T19:00:16.691413579Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook.(*DefaultServer).Start(0xc000568280, {0x240c908, 0xc0003e9ae0})
2026-02-03T19:00:16.691422239Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/server.go:263 +0x872
2026-02-03T19:00:16.69143355Z stderr F sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile.func1(0xc0005a9ae0)
2026-02-03T19:00:16.69144548Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:226 +0xc2
2026-02-03T19:00:16.69145494Z stderr F created by sigs.k8s.io/controller-runtime/pkg/manager.(*runnableGroup).reconcile in goroutine 115
2026-02-03T19:00:16.69148702Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/manager/runnable_group.go:210 +0x19d
2026-02-03T19:00:16.69149651Z stderr F 
2026-02-03T19:00:16.69150568Z stderr F goroutine 275 [select, 2 minutes]:
2026-02-03T19:00:16.69151393Z stderr F sigs.k8s.io/controller-runtime/pkg/certwatcher.(*CertWatcher).Watch(0xc0002d2700)
2026-02-03T19:00:16.691523131Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/certwatcher/certwatcher.go:149 +0xc5
2026-02-03T19:00:16.691532001Z stderr F created by sigs.k8s.io/controller-runtime/pkg/certwatcher.(*CertWatcher).Start in goroutine 206
2026-02-03T19:00:16.691543211Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/certwatcher/certwatcher.go:128 +0x26d
2026-02-03T19:00:16.691547521Z stderr F 
2026-02-03T19:00:16.691556431Z stderr F goroutine 269 [chan receive, 2 minutes]:
2026-02-03T19:00:16.691564401Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1()
2026-02-03T19:00:16.691578881Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:162 +0x2c
2026-02-03T19:00:16.691587541Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start in goroutine 265
2026-02-03T19:00:16.691595501Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:161 +0x156
2026-02-03T19:00:16.691599541Z stderr F 
2026-02-03T19:00:16.691611231Z stderr F goroutine 205 [IO wait, 2 minutes]:
2026-02-03T19:00:16.691625282Z stderr F internal/poll.runtime_pollWait(0x7f4e849efad8, 0x72)
2026-02-03T19:00:16.691637092Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.691649042Z stderr F internal/poll.(*pollDesc).wait(0xc0005f1c20?, 0xc000841cdf?, 0x1)
2026-02-03T19:00:16.691661112Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.691690082Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.691695332Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.691710253Z stderr F internal/poll.(*FD).Read(0xc0005f1c20, {0xc000841cdf, 0x10000, 0x10000})
2026-02-03T19:00:16.691715243Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:165 +0x27a
2026-02-03T19:00:16.691724063Z stderr F os.(*File).read(...)
2026-02-03T19:00:16.691732063Z stderr F 	/usr/local/go/src/os/file_posix.go:29
2026-02-03T19:00:16.691741813Z stderr F os.(*File).Read(0xc0001a8720, {0xc000841cdf?, 0x813c66ce60929e97?, 0x9fd13b30218fb724?})
2026-02-03T19:00:16.691751323Z stderr F 	/usr/local/go/src/os/file.go:124 +0x52
2026-02-03T19:00:16.691761463Z stderr F github.com/fsnotify/fsnotify.(*inotify).readEvents(0xc0005b0a00)
2026-02-03T19:00:16.691771713Z stderr F 	/go/pkg/mod/github.com/fsnotify/fsnotify@v1.8.0/backend_inotify.go:431 +0xc5
2026-02-03T19:00:16.691781223Z stderr F created by github.com/fsnotify/fsnotify.newBufferedBackend in goroutine 203
2026-02-03T19:00:16.691793243Z stderr F 	/go/pkg/mod/github.com/fsnotify/fsnotify@v1.8.0/backend_inotify.go:195 +0x196
2026-02-03T19:00:16.691797704Z stderr F 
2026-02-03T19:00:16.691809744Z stderr F goroutine 206 [select]:
2026-02-03T19:00:16.691822074Z stderr F sigs.k8s.io/controller-runtime/pkg/certwatcher.(*CertWatcher).Start(0xc0002d2700, {0x240c908, 0xc0003e9ae0})
2026-02-03T19:00:16.691830694Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/certwatcher/certwatcher.go:135 +0x3b2
2026-02-03T19:00:16.691837304Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook.(*DefaultServer).Start.func1()
2026-02-03T19:00:16.691844004Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/server.go:214 +0x1f
2026-02-03T19:00:16.691850774Z stderr F created by sigs.k8s.io/controller-runtime/pkg/webhook.(*DefaultServer).Start in goroutine 203
2026-02-03T19:00:16.691868724Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/server.go:213 +0x31f
2026-02-03T19:00:16.691872914Z stderr F 
2026-02-03T19:00:16.691888875Z stderr F goroutine 270 [sync.Cond.Wait, 2 minutes]:
2026-02-03T19:00:16.691893405Z stderr F sync.runtime_notifyListWait(0xc000459090, 0x0)
2026-02-03T19:00:16.691901425Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.691909265Z stderr F sync.(*Cond).Wait(0x0?)
2026-02-03T19:00:16.691917315Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.691925905Z stderr F k8s.io/client-go/util/workqueue.(*Typed[...]).Get(0x241eba0)
2026-02-03T19:00:16.691937495Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:277 +0xb2
2026-02-03T19:00:16.691957815Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem(0x242b540, {0x240c908, 0xc0003e9b80})
2026-02-03T19:00:16.691971635Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:271 +0x5e
2026-02-03T19:00:16.691994946Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2()
2026-02-03T19:00:16.692003416Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:249 +0x85
2026-02-03T19:00:16.692012976Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2 in goroutine 265
2026-02-03T19:00:16.692022216Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:245 +0x6b8
2026-02-03T19:00:16.692026656Z stderr F 
2026-02-03T19:00:16.692036316Z stderr F goroutine 105 [chan receive, 2 minutes]:
2026-02-03T19:00:16.692048086Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1()
2026-02-03T19:00:16.692052216Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:162 +0x2c
2026-02-03T19:00:16.692063876Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start in goroutine 264
2026-02-03T19:00:16.692077497Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:161 +0x156
2026-02-03T19:00:16.692084627Z stderr F 
2026-02-03T19:00:16.692096647Z stderr F goroutine 207 [chan receive, 2 minutes]:
2026-02-03T19:00:16.692101257Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook.(*DefaultServer).Start.func2()
2026-02-03T19:00:16.692109577Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/server.go:248 +0x45
2026-02-03T19:00:16.692125187Z stderr F created by sigs.k8s.io/controller-runtime/pkg/webhook.(*DefaultServer).Start in goroutine 203
2026-02-03T19:00:16.692133367Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/server.go:247 +0x7eb
2026-02-03T19:00:16.692137217Z stderr F 
2026-02-03T19:00:16.692141607Z stderr F goroutine 286 [sync.Cond.Wait]:
2026-02-03T19:00:16.692149357Z stderr F sync.runtime_notifyListWait(0xc0003ad710, 0x8)
2026-02-03T19:00:16.692157397Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.692165318Z stderr F sync.(*Cond).Wait(0x16d45d9?)
2026-02-03T19:00:16.692176698Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.692188998Z stderr F k8s.io/client-go/util/workqueue.(*Typed[...]).Get(0x241eba0)
2026-02-03T19:00:16.692200888Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/util/workqueue/queue.go:277 +0xb2
2026-02-03T19:00:16.692219768Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem(0x242b540, {0x240c908, 0xc0003e9b80})
2026-02-03T19:00:16.692231598Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:271 +0x5e
2026-02-03T19:00:16.692239458Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2()
2026-02-03T19:00:16.692250799Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:249 +0x85
2026-02-03T19:00:16.692262519Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2 in goroutine 264
2026-02-03T19:00:16.692284789Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/controller/controller.go:245 +0x6b8
2026-02-03T19:00:16.692293099Z stderr F 
2026-02-03T19:00:16.692300379Z stderr F goroutine 231 [sync.Cond.Wait, 2 minutes]:
2026-02-03T19:00:16.692308969Z stderr F sync.runtime_notifyListWait(0xc00037b368, 0x0)
2026-02-03T19:00:16.692322479Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.692330779Z stderr F sync.(*Cond).Wait(0x7f4ecb658f18?)
2026-02-03T19:00:16.69234388Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.69235279Z stderr F k8s.io/client-go/tools/cache.(*DeltaFIFO).Pop(0xc00037b340, 0xc00005ec80)
2026-02-03T19:00:16.69236161Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/delta_fifo.go:588 +0x231
2026-02-03T19:00:16.69237057Z stderr F k8s.io/client-go/tools/cache.(*controller).processLoop(0xc00037b3f0)
2026-02-03T19:00:16.6923797Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:195 +0x30
2026-02-03T19:00:16.69238849Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.69239709Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.69241255Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc00088dde8, {0x23eab40, 0xc00060aa50}, 0x1, 0xc0009461c0)
2026-02-03T19:00:16.69242734Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.692442921Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc00088dde8, 0x3b9aca00, 0x0, 0x1, 0xc0009461c0)
2026-02-03T19:00:16.692454771Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.692466301Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.692477631Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.692489121Z stderr F k8s.io/client-go/tools/cache.(*controller).Run(0xc00037b3f0, 0xc0009461c0)
2026-02-03T19:00:16.692500451Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:166 +0x375
2026-02-03T19:00:16.692508641Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run(0xc00037ab00, 0xc0009461c0)
2026-02-03T19:00:16.692519981Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:508 +0x2a9
2026-02-03T19:00:16.692531582Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Cache).Start(0xc0004c89a0, 0x0?)
2026-02-03T19:00:16.692542992Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:108 +0x72
2026-02-03T19:00:16.692550952Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked.func1()
2026-02-03T19:00:16.692562442Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:242 +0x75
2026-02-03T19:00:16.692570322Z stderr F created by sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked in goroutine 230
2026-02-03T19:00:16.692582972Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:240 +0x87
2026-02-03T19:00:16.692591632Z stderr F 
2026-02-03T19:00:16.692624653Z stderr F goroutine 325 [chan receive]:
2026-02-03T19:00:16.692630673Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run.func1()
2026-02-03T19:00:16.692635113Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:973 +0x45
2026-02-03T19:00:16.692639253Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.692648843Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.692657653Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc00088ff70, {0x23eab40, 0xc00060b6e0}, 0x1, 0xc000946d20)
2026-02-03T19:00:16.692666223Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.692685713Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc00062ff70, 0x3b9aca00, 0x0, 0x1, 0xc000946d20)
2026-02-03T19:00:16.692690453Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.692703253Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.692707924Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.692716704Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run(0xc000de23f0)
2026-02-03T19:00:16.692725504Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:972 +0x5a
2026-02-03T19:00:16.692729874Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.692742694Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.692747434Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 276
2026-02-03T19:00:16.692755914Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.692759834Z stderr F 
2026-02-03T19:00:16.692768154Z stderr F goroutine 233 [select, 2 minutes]:
2026-02-03T19:00:16.692781364Z stderr F reflect.rselect({0xc0007a0f00, 0x3, 0x0?})
2026-02-03T19:00:16.692793844Z stderr F 	/usr/local/go/src/runtime/select.go:600 +0x2c5
2026-02-03T19:00:16.692809245Z stderr F reflect.Select({0xc00037b290?, 0x3, 0x0?})
2026-02-03T19:00:16.692821915Z stderr F 	/usr/local/go/src/reflect/value.go:3176 +0x5ca
2026-02-03T19:00:16.692830915Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...].func2()
2026-02-03T19:00:16.692843815Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:34 +0x4f
2026-02-03T19:00:16.692854335Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...] in goroutine 231
2026-02-03T19:00:16.692880215Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:32 +0x438
2026-02-03T19:00:16.692887195Z stderr F 
2026-02-03T19:00:16.692890636Z stderr F goroutine 604 [IO wait]:
2026-02-03T19:00:16.692894056Z stderr F internal/poll.runtime_pollWait(0x7f4e849ef678, 0x72)
2026-02-03T19:00:16.692904506Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.692908066Z stderr F internal/poll.(*pollDesc).wait(0xc0008aa880?, 0xc0008dd500?, 0x0)
2026-02-03T19:00:16.692917506Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.692924446Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.692931336Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.692946416Z stderr F internal/poll.(*FD).Read(0xc0008aa880, {0xc0008dd500, 0xa80, 0xa80})
2026-02-03T19:00:16.692961006Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:165 +0x27a
2026-02-03T19:00:16.692986627Z stderr F net.(*netFD).Read(0xc0008aa880, {0xc0008dd500?, 0x52cb85?, 0xc0008aa880?})
2026-02-03T19:00:16.692999127Z stderr F 	/usr/local/go/src/net/fd_posix.go:55 +0x25
2026-02-03T19:00:16.693024867Z stderr F net.(*conn).Read(0xc000432428, {0xc0008dd500?, 0xc000cd18d0?, 0x65e064?})
2026-02-03T19:00:16.693035457Z stderr F 	/usr/local/go/src/net/net.go:189 +0x45
2026-02-03T19:00:16.693055887Z stderr F crypto/tls.(*atLeastReader).Read(0xc000bb65a0, {0xc0008dd500?, 0x0?, 0xc000bb65a0?})
2026-02-03T19:00:16.693064397Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:809 +0x3b
2026-02-03T19:00:16.693080338Z stderr F bytes.(*Buffer).ReadFrom(0xc000734638, {0x23e8220, 0xc000bb65a0})
2026-02-03T19:00:16.693087058Z stderr F 	/usr/local/go/src/bytes/buffer.go:211 +0x98
2026-02-03T19:00:16.693108378Z stderr F crypto/tls.(*Conn).readFromUntil(0xc000734388, {0x23e9a00, 0xc000432428}, 0xc000cd1868?)
2026-02-03T19:00:16.693117918Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:831 +0xde
2026-02-03T19:00:16.693130518Z stderr F crypto/tls.(*Conn).readRecordOrCCS(0xc000734388, 0x0)
2026-02-03T19:00:16.693142768Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:629 +0x3cf
2026-02-03T19:00:16.693152318Z stderr F crypto/tls.(*Conn).readRecord(...)
2026-02-03T19:00:16.693158928Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:591
2026-02-03T19:00:16.693173689Z stderr F crypto/tls.(*Conn).Read(0xc000734388, {0xc0003bf000, 0x1000, 0x35b55e0?})
2026-02-03T19:00:16.693183189Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:1385 +0x150
2026-02-03T19:00:16.693207329Z stderr F net/http.(*connReader).Read(0xc000831230, {0xc0003bf000, 0x1000, 0x1000})
2026-02-03T19:00:16.693219949Z stderr F 	/usr/local/go/src/net/http/server.go:798 +0x14b
2026-02-03T19:00:16.693229119Z stderr F bufio.(*Reader).fill(0xc000ac8600)
2026-02-03T19:00:16.693237899Z stderr F 	/usr/local/go/src/bufio/bufio.go:110 +0x103
2026-02-03T19:00:16.693247089Z stderr F bufio.(*Reader).Peek(0xc000ac8600, 0x4)
2026-02-03T19:00:16.6932558Z stderr F 	/usr/local/go/src/bufio/bufio.go:148 +0x53
2026-02-03T19:00:16.69326847Z stderr F net/http.(*conn).serve(0xc0008eb3b0, {0x240c8d0, 0xc00099d380})
2026-02-03T19:00:16.69327742Z stderr F 	/usr/local/go/src/net/http/server.go:2127 +0x738
2026-02-03T19:00:16.6932861Z stderr F created by net/http.(*Server).Serve in goroutine 203
2026-02-03T19:00:16.6932987Z stderr F 	/usr/local/go/src/net/http/server.go:3360 +0x485
2026-02-03T19:00:16.6933084Z stderr F 
2026-02-03T19:00:16.69332072Z stderr F goroutine 235 [chan receive, 2 minutes]:
2026-02-03T19:00:16.6933293Z stderr F k8s.io/client-go/tools/cache.(*sharedProcessor).run(0xc000796140, 0xc0009465b0)
2026-02-03T19:00:16.69334127Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:807 +0x4d
2026-02-03T19:00:16.693349211Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run.(*Group).StartWithChannel.func4()
2026-02-03T19:00:16.693357251Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.693365501Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.693373821Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.693381571Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 231
2026-02-03T19:00:16.693396851Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.693400801Z stderr F 
2026-02-03T19:00:16.693408921Z stderr F goroutine 236 [chan receive, 2 minutes]:
2026-02-03T19:00:16.693424661Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.func1()
2026-02-03T19:00:16.693428901Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:138 +0x25
2026-02-03T19:00:16.693436832Z stderr F created by k8s.io/client-go/tools/cache.(*controller).Run in goroutine 231
2026-02-03T19:00:16.693447962Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:137 +0xab
2026-02-03T19:00:16.693460392Z stderr F 
2026-02-03T19:00:16.693465332Z stderr F goroutine 237 [select]:
2026-02-03T19:00:16.693514192Z stderr F k8s.io/client-go/tools/cache.handleAnyWatch({0xc0002f593d?, 0x3?, 0x35b55e0?}, {0x23f6d30, 0xc000892b00}, {0x7f4e846c7260, 0xc00037b340}, {0x2437500, 0x20533e0}, 0x0, ...)
2026-02-03T19:00:16.693528263Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:802 +0x230
2026-02-03T19:00:16.693586523Z stderr F k8s.io/client-go/tools/cache.handleWatch({0x3?, 0x0?, 0x35b55e0?}, {0x23f6d30?, 0xc000892b00?}, {0x7f4e846c7260?, 0xc00037b340?}, {0x2437500?, 0x20533e0?}, 0x0, ...)
2026-02-03T19:00:16.693599793Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:768 +0xdd
2026-02-03T19:00:16.693620274Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watch(0xc00060e0f0, {0x0?, 0x0?}, 0xc0009461c0, 0xc0002d29a0)
2026-02-03T19:00:16.693630834Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:466 +0x556
2026-02-03T19:00:16.693646374Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watchWithResync(0xc00060e0f0, {0x0, 0x0}, 0xc0009461c0)
2026-02-03T19:00:16.693679544Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:414 +0x12c
2026-02-03T19:00:16.693686304Z stderr F k8s.io/client-go/tools/cache.(*Reflector).ListAndWatch(0xc00060e0f0, 0xc0009461c0)
2026-02-03T19:00:16.693689834Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:377 +0x3c5
2026-02-03T19:00:16.693697554Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run.func1()
2026-02-03T19:00:16.693700974Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:315 +0x25
2026-02-03T19:00:16.693704314Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x10?)
2026-02-03T19:00:16.693724455Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.693731945Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc00080bf50, {0x23eab60, 0xc0007961e0}, 0x1, 0xc0009461c0)
2026-02-03T19:00:16.693738555Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.693748445Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run(0xc00060e0f0, 0xc0009461c0)
2026-02-03T19:00:16.693758085Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:314 +0x1af
2026-02-03T19:00:16.693764665Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.(*Group).StartWithChannel.func2()
2026-02-03T19:00:16.693771045Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.693777565Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.693784145Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.693793325Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 231
2026-02-03T19:00:16.693807256Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.693811256Z stderr F 
2026-02-03T19:00:16.693819146Z stderr F goroutine 208 [select, 2 minutes]:
2026-02-03T19:00:16.693841536Z stderr F k8s.io/client-go/tools/cache.(*Reflector).startResync(0xc00060e0f0, 0xc0009461c0, 0xc0004f8d90, 0xc0002d29a0)
2026-02-03T19:00:16.693853356Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:389 +0x106
2026-02-03T19:00:16.693861416Z stderr F created by k8s.io/client-go/tools/cache.(*Reflector).watchWithResync in goroutine 237
2026-02-03T19:00:16.693873166Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:413 +0x105
2026-02-03T19:00:16.693880876Z stderr F 
2026-02-03T19:00:16.693887816Z stderr F goroutine 322 [sync.Cond.Wait]:
2026-02-03T19:00:16.693898657Z stderr F sync.runtime_notifyListWait(0xc00076c7c8, 0x2)
2026-02-03T19:00:16.693908177Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.693918167Z stderr F sync.(*Cond).Wait(0xc000417420?)
2026-02-03T19:00:16.693927877Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.693944197Z stderr F golang.org/x/net/http2.(*pipe).Read(0xc00076c7b0, {0xc000bc2c01, 0x5ff, 0x5ff})
2026-02-03T19:00:16.693951107Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/pipe.go:76 +0xd6
2026-02-03T19:00:16.693977287Z stderr F golang.org/x/net/http2.transportResponseBody.Read({0x46fe5d?}, {0xc000bc2c01?, 0x0?, 0x0?})
2026-02-03T19:00:16.693989958Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:2560 +0x65
2026-02-03T19:00:16.693996578Z stderr F encoding/json.(*Decoder).refill(0xc0005b17c0)
2026-02-03T19:00:16.694005948Z stderr F 	/usr/local/go/src/encoding/json/stream.go:165 +0x188
2026-02-03T19:00:16.694012508Z stderr F encoding/json.(*Decoder).readValue(0xc0005b17c0)
2026-02-03T19:00:16.694021958Z stderr F 	/usr/local/go/src/encoding/json/stream.go:140 +0x85
2026-02-03T19:00:16.694034038Z stderr F encoding/json.(*Decoder).Decode(0xc0005b17c0, {0x1dc8100, 0xc000c1d3f8})
2026-02-03T19:00:16.694044478Z stderr F 	/usr/local/go/src/encoding/json/stream.go:63 +0x75
2026-02-03T19:00:16.694075539Z stderr F k8s.io/apimachinery/pkg/util/framer.(*jsonFrameReader).Read(0xc000de0630, {0xc00057d000, 0x400, 0x400})
2026-02-03T19:00:16.694084079Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/framer/framer.go:151 +0x15c
2026-02-03T19:00:16.694104029Z stderr F k8s.io/apimachinery/pkg/runtime/serializer/streaming.(*decoder).Decode(0xc00040a3c0, 0x0, {0x23f31a0, 0xc0005ad9c0})
2026-02-03T19:00:16.694114709Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/runtime/serializer/streaming/streaming.go:77 +0xa3
2026-02-03T19:00:16.694122629Z stderr F k8s.io/client-go/rest/watch.(*Decoder).Decode(0xc00064ad00)
2026-02-03T19:00:16.694132449Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/rest/watch/decoder.go:49 +0x4b
2026-02-03T19:00:16.694139129Z stderr F k8s.io/apimachinery/pkg/watch.(*StreamWatcher).receive(0xc000892b00)
2026-02-03T19:00:16.694148639Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:105 +0xc7
2026-02-03T19:00:16.694158149Z stderr F created by k8s.io/apimachinery/pkg/watch.NewStreamWatcher in goroutine 237
2026-02-03T19:00:16.69416764Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:76 +0x105
2026-02-03T19:00:16.69417093Z stderr F 
2026-02-03T19:00:16.69418115Z stderr F goroutine 281 [chan receive, 2 minutes]:
2026-02-03T19:00:16.69420408Z stderr F k8s.io/client-go/tools/cache.(*sharedProcessor).run(0xc0003cf7c0, 0xc000a18b60)
2026-02-03T19:00:16.69420915Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:807 +0x4d
2026-02-03T19:00:16.69421753Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run.(*Group).StartWithChannel.func4()
2026-02-03T19:00:16.69423166Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.69423589Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.69424381Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.69425176Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 277
2026-02-03T19:00:16.694259651Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.694263551Z stderr F 
2026-02-03T19:00:16.694271371Z stderr F goroutine 282 [chan receive, 2 minutes]:
2026-02-03T19:00:16.694279811Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.func1()
2026-02-03T19:00:16.694287731Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:138 +0x25
2026-02-03T19:00:16.694295611Z stderr F created by k8s.io/client-go/tools/cache.(*controller).Run in goroutine 277
2026-02-03T19:00:16.694306871Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:137 +0xab
2026-02-03T19:00:16.694310941Z stderr F 
2026-02-03T19:00:16.694322951Z stderr F goroutine 283 [select]:
2026-02-03T19:00:16.694370502Z stderr F k8s.io/client-go/tools/cache.handleAnyWatch({0xc000195329?, 0x3?, 0x35b55e0?}, {0x23f6d30, 0xc0008a0d00}, {0x7f4e846c7260, 0xc0001864d0}, {0x2437500, 0x2075b00}, 0x0, ...)
2026-02-03T19:00:16.694402212Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:802 +0x230
2026-02-03T19:00:16.694440703Z stderr F k8s.io/client-go/tools/cache.handleWatch({0x3?, 0x0?, 0x35b55e0?}, {0x23f6d30?, 0xc0008a0d00?}, {0x7f4e846c7260?, 0xc0001864d0?}, {0x2437500?, 0x2075b00?}, 0x0, ...)
2026-02-03T19:00:16.694450683Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:768 +0xdd
2026-02-03T19:00:16.694474343Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watch(0xc000217a40, {0x0?, 0x0?}, 0xc000a18a80, 0xc000706e00)
2026-02-03T19:00:16.694487013Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:466 +0x556
2026-02-03T19:00:16.694509753Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watchWithResync(0xc000217a40, {0x0, 0x0}, 0xc000a18a80)
2026-02-03T19:00:16.694516493Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:414 +0x12c
2026-02-03T19:00:16.694527554Z stderr F k8s.io/client-go/tools/cache.(*Reflector).ListAndWatch(0xc000217a40, 0xc000a18a80)
2026-02-03T19:00:16.694548114Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:377 +0x3c5
2026-02-03T19:00:16.694553344Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run.func1()
2026-02-03T19:00:16.694557514Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:315 +0x25
2026-02-03T19:00:16.694568784Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x10?)
2026-02-03T19:00:16.694581934Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.694594234Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0006cff50, {0x23eab60, 0xc0003cf860}, 0x1, 0xc000a18a80)
2026-02-03T19:00:16.694602264Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.694614864Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run(0xc000217a40, 0xc000a18a80)
2026-02-03T19:00:16.694627925Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:314 +0x1af
2026-02-03T19:00:16.694634745Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.(*Group).StartWithChannel.func2()
2026-02-03T19:00:16.694644215Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.694651155Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.694663895Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.694670435Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 277
2026-02-03T19:00:16.694677355Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.694680715Z stderr F 
2026-02-03T19:00:16.694690255Z stderr F goroutine 293 [select, 2 minutes]:
2026-02-03T19:00:16.694716676Z stderr F k8s.io/client-go/tools/cache.(*Reflector).startResync(0xc000217a40, 0xc000a18a80, 0xc000a987e0, 0xc000706e00)
2026-02-03T19:00:16.694731646Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:389 +0x106
2026-02-03T19:00:16.694736096Z stderr F created by k8s.io/client-go/tools/cache.(*Reflector).watchWithResync in goroutine 283
2026-02-03T19:00:16.694743846Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:413 +0x105
2026-02-03T19:00:16.694751316Z stderr F 
2026-02-03T19:00:16.694759986Z stderr F goroutine 156 [sync.Cond.Wait]:
2026-02-03T19:00:16.694769016Z stderr F sync.runtime_notifyListWait(0xc0009a4398, 0x9)
2026-02-03T19:00:16.694777186Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.694785056Z stderr F sync.(*Cond).Wait(0xc000051460?)
2026-02-03T19:00:16.694793126Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.694804637Z stderr F k8s.io/client-go/tools/cache.(*DeltaFIFO).Pop(0xc0009a4370, 0xc0004240b0)
2026-02-03T19:00:16.694816257Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/delta_fifo.go:588 +0x231
2026-02-03T19:00:16.694824347Z stderr F k8s.io/client-go/tools/cache.(*controller).processLoop(0xc0009a4420)
2026-02-03T19:00:16.694835687Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:195 +0x30
2026-02-03T19:00:16.694847817Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.694855867Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.694872247Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc000a93de8, {0x23eab40, 0xc000738a50}, 0x1, 0xc000a983f0)
2026-02-03T19:00:16.694902648Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.694916198Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc000a93de8, 0x3b9aca00, 0x0, 0x1, 0xc000a983f0)
2026-02-03T19:00:16.694920938Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.694933798Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.694938418Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.694952618Z stderr F k8s.io/client-go/tools/cache.(*controller).Run(0xc0009a4420, 0xc000a983f0)
2026-02-03T19:00:16.694962468Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:166 +0x375
2026-02-03T19:00:16.694972828Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run(0xc0009a4210, 0xc000a983f0)
2026-02-03T19:00:16.694977318Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:508 +0x2a9
2026-02-03T19:00:16.694993139Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Cache).Start(0xc0004229a0, 0x0?)
2026-02-03T19:00:16.694999849Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:108 +0x72
2026-02-03T19:00:16.695011899Z stderr F sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked.func1()
2026-02-03T19:00:16.695017209Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:242 +0x75
2026-02-03T19:00:16.695028709Z stderr F created by sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).startInformerLocked in goroutine 272
2026-02-03T19:00:16.695032909Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/cache/internal/informers.go:240 +0x87
2026-02-03T19:00:16.695040919Z stderr F 
2026-02-03T19:00:16.695048809Z stderr F goroutine 297 [select]:
2026-02-03T19:00:16.695057069Z stderr F k8s.io/client-go/tools/cache.(*processorListener).pop(0xc0008fef30)
2026-02-03T19:00:16.695064989Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:943 +0xf5
2026-02-03T19:00:16.695072899Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.69508093Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.6950892Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 272
2026-02-03T19:00:16.69510077Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.69510469Z stderr F 
2026-02-03T19:00:16.69511599Z stderr F goroutine 296 [chan receive]:
2026-02-03T19:00:16.69512017Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run.func1()
2026-02-03T19:00:16.69513151Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:973 +0x45
2026-02-03T19:00:16.69513879Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.69514823Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.695166241Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc000b0df70, {0x23eab40, 0xc000948bd0}, 0x1, 0xc000a98c40)
2026-02-03T19:00:16.695175981Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.695195181Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc00062c770, 0x3b9aca00, 0x0, 0x1, 0xc000a98c40)
2026-02-03T19:00:16.695207581Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.695216511Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.695221001Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.695229611Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run(0xc0008fef30)
2026-02-03T19:00:16.695238321Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:972 +0x5a
2026-02-03T19:00:16.695247051Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.695255661Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.695264092Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 272
2026-02-03T19:00:16.695272962Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.695277082Z stderr F 
2026-02-03T19:00:16.695285872Z stderr F goroutine 158 [select, 2 minutes]:
2026-02-03T19:00:16.695300122Z stderr F reflect.rselect({0xc00088af00, 0x3, 0x569135ed4d8765b1?})
2026-02-03T19:00:16.695314342Z stderr F 	/usr/local/go/src/runtime/select.go:600 +0x2c5
2026-02-03T19:00:16.695335792Z stderr F reflect.Select({0xc0009a42c0?, 0x3, 0x0?})
2026-02-03T19:00:16.695347062Z stderr F 	/usr/local/go/src/reflect/value.go:3176 +0x5ca
2026-02-03T19:00:16.695356383Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...].func2()
2026-02-03T19:00:16.695365943Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:34 +0x4f
2026-02-03T19:00:16.695375523Z stderr F created by sigs.k8s.io/controller-runtime/pkg/internal/syncs.MergeChans[...] in goroutine 156
2026-02-03T19:00:16.695387813Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/internal/syncs/syncs.go:32 +0x438
2026-02-03T19:00:16.695391223Z stderr F 
2026-02-03T19:00:16.695397563Z stderr F goroutine 160 [chan receive, 2 minutes]:
2026-02-03T19:00:16.695409933Z stderr F k8s.io/client-go/tools/cache.(*sharedProcessor).run(0xc0003e8230, 0xc000a984d0)
2026-02-03T19:00:16.695419253Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:807 +0x4d
2026-02-03T19:00:16.695425923Z stderr F k8s.io/client-go/tools/cache.(*sharedIndexInformer).Run.(*Group).StartWithChannel.func4()
2026-02-03T19:00:16.695435473Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.695442084Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.695454294Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.695462464Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 156
2026-02-03T19:00:16.695481114Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.695484604Z stderr F 
2026-02-03T19:00:16.695494144Z stderr F goroutine 289 [chan receive, 2 minutes]:
2026-02-03T19:00:16.695501224Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.func1()
2026-02-03T19:00:16.695524354Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:138 +0x25
2026-02-03T19:00:16.695531575Z stderr F created by k8s.io/client-go/tools/cache.(*controller).Run in goroutine 156
2026-02-03T19:00:16.695539875Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/controller.go:137 +0xab
2026-02-03T19:00:16.695545335Z stderr F 
2026-02-03T19:00:16.695552285Z stderr F goroutine 290 [select]:
2026-02-03T19:00:16.695595945Z stderr F k8s.io/client-go/tools/cache.handleAnyWatch({0xc0006301b8?, 0x3?, 0x35b55e0?}, {0x23f6d30, 0xc00081c800}, {0x7f4e846c7260, 0xc0009a4370}, {0x2437500, 0x2075020}, 0x0, ...)
2026-02-03T19:00:16.695602775Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:802 +0x230
2026-02-03T19:00:16.695668946Z stderr F k8s.io/client-go/tools/cache.handleWatch({0x3?, 0x0?, 0x35b55e0?}, {0x23f6d30?, 0xc00081c800?}, {0x7f4e846c7260?, 0xc0009a4370?}, {0x2437500?, 0x2075020?}, 0x0, ...)
2026-02-03T19:00:16.695678786Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:768 +0xdd
2026-02-03T19:00:16.695705786Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watch(0xc000768000, {0x0?, 0x0?}, 0xc000a983f0, 0xc0004c90a0)
2026-02-03T19:00:16.695712767Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:466 +0x556
2026-02-03T19:00:16.695730587Z stderr F k8s.io/client-go/tools/cache.(*Reflector).watchWithResync(0xc000768000, {0x0, 0x0}, 0xc000a983f0)
2026-02-03T19:00:16.695737217Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:414 +0x12c
2026-02-03T19:00:16.695749327Z stderr F k8s.io/client-go/tools/cache.(*Reflector).ListAndWatch(0xc000768000, 0xc000a983f0)
2026-02-03T19:00:16.695761687Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:377 +0x3c5
2026-02-03T19:00:16.695768557Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run.func1()
2026-02-03T19:00:16.695780267Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:315 +0x25
2026-02-03T19:00:16.695786917Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x10?)
2026-02-03T19:00:16.695796607Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.695814588Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc000d97f50, {0x23eab60, 0xc0003e82d0}, 0x1, 0xc000a983f0)
2026-02-03T19:00:16.695824008Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.695833828Z stderr F k8s.io/client-go/tools/cache.(*Reflector).Run(0xc000768000, 0xc000a983f0)
2026-02-03T19:00:16.695846338Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:314 +0x1af
2026-02-03T19:00:16.695853358Z stderr F k8s.io/client-go/tools/cache.(*controller).Run.(*Group).StartWithChannel.func2()
2026-02-03T19:00:16.695859938Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:55 +0x1b
2026-02-03T19:00:16.695866528Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.695883798Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.695892368Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 156
2026-02-03T19:00:16.695902159Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.695906589Z stderr F 
2026-02-03T19:00:16.695915779Z stderr F goroutine 240 [select, 2 minutes]:
2026-02-03T19:00:16.695925119Z stderr F k8s.io/client-go/tools/cache.(*Reflector).startResync(0xc000768000, 0xc000a983f0, 0xc0009469a0, 0xc0004c90a0)
2026-02-03T19:00:16.695939419Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:389 +0x106
2026-02-03T19:00:16.695950529Z stderr F created by k8s.io/client-go/tools/cache.(*Reflector).watchWithResync in goroutine 290
2026-02-03T19:00:16.695958779Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/reflector.go:413 +0x105
2026-02-03T19:00:16.695962529Z stderr F 
2026-02-03T19:00:16.695975649Z stderr F goroutine 321 [select, 2 minutes]:
2026-02-03T19:00:16.69600132Z stderr F golang.org/x/net/http2.(*clientStream).writeRequest(0xc00076c780, 0xc0005b1540, 0x0)
2026-02-03T19:00:16.69600557Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1570 +0xc85
2026-02-03T19:00:16.69601687Z stderr F golang.org/x/net/http2.(*clientStream).doRequest(0xc00076c780, 0x0?, 0x0?)
2026-02-03T19:00:16.69602756Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1431 +0x56
2026-02-03T19:00:16.69604474Z stderr F created by golang.org/x/net/http2.(*ClientConn).roundTrip in goroutine 237
2026-02-03T19:00:16.69605419Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1336 +0x44b
2026-02-03T19:00:16.69605811Z stderr F 
2026-02-03T19:00:16.69606615Z stderr F goroutine 305 [select, 2 minutes]:
2026-02-03T19:00:16.696266703Z stderr F golang.org/x/net/http2.(*clientStream).writeRequest(0xc000820180, 0xc0001f8c80, 0x0)
2026-02-03T19:00:16.696285363Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1570 +0xc85
2026-02-03T19:00:16.696289403Z stderr F golang.org/x/net/http2.(*clientStream).doRequest(0xc000820180, 0x0?, 0x0?)
2026-02-03T19:00:16.696293253Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1431 +0x56
2026-02-03T19:00:16.696313593Z stderr F created by golang.org/x/net/http2.(*ClientConn).roundTrip in goroutine 290
2026-02-03T19:00:16.696322793Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1336 +0x44b
2026-02-03T19:00:16.696326933Z stderr F 
2026-02-03T19:00:16.696331683Z stderr F goroutine 306 [sync.Cond.Wait]:
2026-02-03T19:00:16.696335873Z stderr F sync.runtime_notifyListWait(0xc0008201c8, 0xc)
2026-02-03T19:00:16.696339963Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.696344043Z stderr F sync.(*Cond).Wait(0x2?)
2026-02-03T19:00:16.696354224Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.696367364Z stderr F golang.org/x/net/http2.(*pipe).Read(0xc0008201b0, {0xc000a7a88c, 0x4, 0x4})
2026-02-03T19:00:16.696371704Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/pipe.go:76 +0xd6
2026-02-03T19:00:16.696380694Z stderr F golang.org/x/net/http2.transportResponseBody.Read({0x0?}, {0xc000a7a88c?, 0xc00086cce0?, 0x410725?})
2026-02-03T19:00:16.696389424Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:2560 +0x65
2026-02-03T19:00:16.696414034Z stderr F io.ReadAtLeast({0x7f4e848d5e48, 0xc000820180}, {0xc000a7a88c, 0x4, 0x4}, 0x4)
2026-02-03T19:00:16.696424884Z stderr F 	/usr/local/go/src/io/io.go:335 +0x90
2026-02-03T19:00:16.696440455Z stderr F k8s.io/apimachinery/pkg/util/framer.(*lengthDelimitedFrameReader).Read(0xc0001b9ab8, {0xc000ba0500, 0x2000, 0x2500})
2026-02-03T19:00:16.696450265Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/framer/framer.go:76 +0x88
2026-02-03T19:00:16.696471195Z stderr F k8s.io/apimachinery/pkg/runtime/serializer/streaming.(*decoder).Decode(0xc0007963c0, 0x0, {0x23f31a0, 0xc0005ad940})
2026-02-03T19:00:16.696483045Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/runtime/serializer/streaming/streaming.go:77 +0xa3
2026-02-03T19:00:16.696495105Z stderr F k8s.io/client-go/rest/watch.(*Decoder).Decode(0xc000794fc0)
2026-02-03T19:00:16.696505295Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/rest/watch/decoder.go:49 +0x4b
2026-02-03T19:00:16.696517435Z stderr F k8s.io/apimachinery/pkg/watch.(*StreamWatcher).receive(0xc00081c800)
2026-02-03T19:00:16.696521435Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:105 +0xc7
2026-02-03T19:00:16.696529415Z stderr F created by k8s.io/apimachinery/pkg/watch.NewStreamWatcher in goroutine 290
2026-02-03T19:00:16.696537666Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:76 +0x105
2026-02-03T19:00:16.696541466Z stderr F 
2026-02-03T19:00:16.696553526Z stderr F goroutine 294 [select, 2 minutes]:
2026-02-03T19:00:16.696624777Z stderr F golang.org/x/net/http2.(*clientStream).writeRequest(0xc00097e000, 0xc0000ec640, 0x0)
2026-02-03T19:00:16.696630767Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1570 +0xc85
2026-02-03T19:00:16.696634187Z stderr F golang.org/x/net/http2.(*clientStream).doRequest(0xc00097e000, 0x8baeaefc653c9d92?, 0xd8c7ba51aae755ef?)
2026-02-03T19:00:16.696641527Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1431 +0x56
2026-02-03T19:00:16.696644917Z stderr F created by golang.org/x/net/http2.(*ClientConn).roundTrip in goroutine 283
2026-02-03T19:00:16.696648277Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:1336 +0x44b
2026-02-03T19:00:16.696651337Z stderr F 
2026-02-03T19:00:16.696658027Z stderr F goroutine 295 [sync.Cond.Wait]:
2026-02-03T19:00:16.696664757Z stderr F sync.runtime_notifyListWait(0xc00097e048, 0x35)
2026-02-03T19:00:16.696671257Z stderr F 	/usr/local/go/src/runtime/sema.go:587 +0x159
2026-02-03T19:00:16.696680847Z stderr F sync.(*Cond).Wait(0x2?)
2026-02-03T19:00:16.696690347Z stderr F 	/usr/local/go/src/sync/cond.go:71 +0x85
2026-02-03T19:00:16.696705477Z stderr F golang.org/x/net/http2.(*pipe).Read(0xc00097e030, {0xc000a7a8a4, 0x4, 0x4})
2026-02-03T19:00:16.696715068Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/pipe.go:76 +0xd6
2026-02-03T19:00:16.696753438Z stderr F golang.org/x/net/http2.transportResponseBody.Read({0x0?}, {0xc000a7a8a4?, 0xc0006cbce0?, 0x410725?})
2026-02-03T19:00:16.696757368Z stderr F 	/go/pkg/mod/golang.org/x/net@v0.37.0/http2/transport.go:2560 +0x65
2026-02-03T19:00:16.696784278Z stderr F io.ReadAtLeast({0x7f4e848d5e48, 0xc00097e000}, {0xc000a7a8a4, 0x4, 0x4}, 0x4)
2026-02-03T19:00:16.696791018Z stderr F 	/usr/local/go/src/io/io.go:335 +0x90
2026-02-03T19:00:16.696806089Z stderr F k8s.io/apimachinery/pkg/util/framer.(*lengthDelimitedFrameReader).Read(0xc000915290, {0xc0009b6000, 0x2000, 0x2500})
2026-02-03T19:00:16.696819989Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/framer/framer.go:76 +0x88
2026-02-03T19:00:16.696848509Z stderr F k8s.io/apimachinery/pkg/runtime/serializer/streaming.(*decoder).Decode(0xc00013c320, 0x0, {0x23f31a0, 0xc0005ad980})
2026-02-03T19:00:16.696853589Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/runtime/serializer/streaming/streaming.go:77 +0xa3
2026-02-03T19:00:16.696862149Z stderr F k8s.io/client-go/rest/watch.(*Decoder).Decode(0xc0005e80c0)
2026-02-03T19:00:16.696870779Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/rest/watch/decoder.go:49 +0x4b
2026-02-03T19:00:16.696878599Z stderr F k8s.io/apimachinery/pkg/watch.(*StreamWatcher).receive(0xc0008a0d00)
2026-02-03T19:00:16.696886129Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:105 +0xc7
2026-02-03T19:00:16.696893769Z stderr F created by k8s.io/apimachinery/pkg/watch.NewStreamWatcher in goroutine 283
2026-02-03T19:00:16.69690194Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/watch/streamwatcher.go:76 +0x105
2026-02-03T19:00:16.69690753Z stderr F 
2026-02-03T19:00:16.69691908Z stderr F goroutine 323 [chan receive, 2 minutes]:
2026-02-03T19:00:16.69692578Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run.func1()
2026-02-03T19:00:16.69693603Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:973 +0x45
2026-02-03T19:00:16.69694551Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0x30?)
2026-02-03T19:00:16.69695513Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:226 +0x33
2026-02-03T19:00:16.69697337Z stderr F k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc000480f70, {0x23eab40, 0xc000de06c0}, 0x1, 0xc0004f92d0)
2026-02-03T19:00:16.69698319Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:227 +0xaf
2026-02-03T19:00:16.696998751Z stderr F k8s.io/apimachinery/pkg/util/wait.JitterUntil(0xc000480f70, 0x3b9aca00, 0x0, 0x1, 0xc0004f92d0)
2026-02-03T19:00:16.697008341Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:204 +0x7f
2026-02-03T19:00:16.697014871Z stderr F k8s.io/apimachinery/pkg/util/wait.Until(...)
2026-02-03T19:00:16.697038151Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/backoff.go:161
2026-02-03T19:00:16.697041871Z stderr F k8s.io/client-go/tools/cache.(*processorListener).run(0xc000de2360)
2026-02-03T19:00:16.697045101Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:972 +0x5a
2026-02-03T19:00:16.697048461Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.697056361Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.697059901Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 230
2026-02-03T19:00:16.697070311Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.697083812Z stderr F 
2026-02-03T19:00:16.697092022Z stderr F goroutine 324 [select, 2 minutes]:
2026-02-03T19:00:16.697104122Z stderr F k8s.io/client-go/tools/cache.(*processorListener).pop(0xc000de2360)
2026-02-03T19:00:16.697112522Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/tools/cache/shared_informer.go:943 +0xf5
2026-02-03T19:00:16.697120902Z stderr F k8s.io/apimachinery/pkg/util/wait.(*Group).Start.func1()
2026-02-03T19:00:16.697128972Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:72 +0x4c
2026-02-03T19:00:16.697137132Z stderr F created by k8s.io/apimachinery/pkg/util/wait.(*Group).Start in goroutine 230
2026-02-03T19:00:16.697148662Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/util/wait/wait.go:70 +0x73
2026-02-03T19:00:16.697152572Z stderr F 
2026-02-03T19:00:16.697163622Z stderr F goroutine 557 [runnable]:
2026-02-03T19:00:16.697224663Z stderr F reflect.deepValueEqual({0x1cb0140?, 0x35dbf20?, 0x98?}, {0x1cb0140?, 0xc0006d1630?, 0x98?}, 0xc000b45bb8)
2026-02-03T19:00:16.697235413Z stderr F 	/usr/local/go/src/reflect/deepequal.go:27 +0x1747
2026-02-03T19:00:16.697268684Z stderr F reflect.DeepEqual({0x1cb0140?, 0x35dbf20?}, {0x1cb0140?, 0xc0006d1630?})
2026-02-03T19:00:16.697285044Z stderr F 	/usr/local/go/src/reflect/deepequal.go:238 +0x25a
2026-02-03T19:00:16.697303734Z stderr F k8s.io/apimachinery/pkg/conversion/queryparams.zeroValue({0x1cb0140?, 0xc000ac87c8?, 0x19?})
2026-02-03T19:00:16.697319204Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/conversion/queryparams/convert.go:78 +0x9d
2026-02-03T19:00:16.697359385Z stderr F k8s.io/apimachinery/pkg/conversion/queryparams.addParam(0xc000831800, {0x1da7479, 0xf}, 0x0?, {0x1cb0140?, 0xc000ac87c8?, 0x1da7473?})
2026-02-03T19:00:16.697367855Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/conversion/queryparams/convert.go:114 +0x65
2026-02-03T19:00:16.697408095Z stderr F k8s.io/apimachinery/pkg/conversion/queryparams.convertStruct(0xc000831800, {0x2437500, 0x1f20c60}, {0x1f20c60?, 0xc000ac8780?, 0x1f20c60?})
2026-02-03T19:00:16.697417275Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/conversion/queryparams/convert.go:181 +0x512
2026-02-03T19:00:16.697435665Z stderr F k8s.io/apimachinery/pkg/conversion/queryparams.Convert({0x2009b00, 0xc000ac8780})
2026-02-03T19:00:16.697447396Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/conversion/queryparams/convert.go:153 +0x152
2026-02-03T19:00:16.697486956Z stderr F k8s.io/apimachinery/pkg/runtime.(*parameterCodec).EncodeParameters(0x358e820, {0x23f3010, 0xc000ac8720}, {{0x20c5bf2, 0x14}, {0x20ab923, 0x2}})
2026-02-03T19:00:16.697496856Z stderr F 	/go/pkg/mod/k8s.io/apimachinery@v0.32.3/pkg/runtime/codec.go:202 +0x17c
2026-02-03T19:00:16.697555437Z stderr F k8s.io/client-go/rest.(*Request).SpecificallyVersionedParams(0xc000886f00, {0x23f3010?, 0xc000ac8720?}, {0x23f3290?, 0x358e820?}, {{0x20c5bf2?, 0x7f4e84748d68?}, {0x20ab923?, 0x23de318?}})
2026-02-03T19:00:16.697562707Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/rest/request.go:412 +0x75
2026-02-03T19:00:16.697579107Z stderr F k8s.io/client-go/rest.(*Request).VersionedParams(...)
2026-02-03T19:00:16.697587097Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/rest/request.go:405
2026-02-03T19:00:16.697637398Z stderr F k8s.io/client-go/gentype.(*Client[...]).Create(0x2429460, {0x240c8d0, 0xc00060b920}, 0xc000886a80, {{{0x0, 0x0}, {0x0, 0x0}}, {0x0, 0x0, ...}, ...})
2026-02-03T19:00:16.697651348Z stderr F 	/go/pkg/mod/k8s.io/client-go@v0.32.3/gentype/type.go:250 +0x165
2026-02-03T19:00:16.697709648Z stderr F github.com/project-codeflare/appwrapper/internal/webhook.(*appWrapperWebhook).validateAppWrapperCreate(0xc00052e540, {0x240c8d0, 0xc00060b920}, 0xc000c22600)
2026-02-03T19:00:16.697716119Z stderr F 	/workspace/internal/webhook/appwrapper_webhook.go:188 +0xe2c
2026-02-03T19:00:16.697728359Z stderr F github.com/project-codeflare/appwrapper/internal/webhook.(*appWrapperWebhook).ValidateCreate(0xc00052e540, {0x240c8d0, 0xc00060b920}, {0x23f3640?, 0xc000c22600})
2026-02-03T19:00:16.697752819Z stderr F 	/workspace/internal/webhook/appwrapper_webhook.go:108 +0x130
2026-02-03T19:00:16.69780807Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*validatorForType).Handle(_, {_, _}, {{{0xc0004c5380, 0x24}, {{0xc000e0c8e8, 0x16}, {0xc00094ad40, 0x7}, {0xc00094ad50, ...}}, ...}})
2026-02-03T19:00:16.69782009Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/admission/validator_custom.go:94 +0x2b6
2026-02-03T19:00:16.69788979Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*Webhook).Handle(_, {_, _}, {{{0xc0004c5380, 0x24}, {{0xc000e0c8e8, 0x16}, {0xc00094ad40, 0x7}, {0xc00094ad50, ...}}, ...}})
2026-02-03T19:00:16.697905731Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/admission/webhook.go:181 +0x224
2026-02-03T19:00:16.697936801Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook/admission.(*Webhook).ServeHTTP(0xc000448410, {0x7f4e849d7d50, 0xc000448870}, 0xc000b1b540)
2026-02-03T19:00:16.697941151Z stderr F 	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.20.3/pkg/webhook/admission/http.go:119 +0xaf0
2026-02-03T19:00:16.697966191Z stderr F sigs.k8s.io/controller-runtime/pkg/webhook/internal/metrics.InstrumentedHook.InstrumentHandlerInFlight.func1({0x7f4e849d7d50, 0xc000448870}, 0xc000b1b540)
2026-02-03T19:00:16.697979921Z stderr F 	/go/pkg/mod/github.com/prometheus/client_golang@v1.21.1/prometheus/promhttp/instrument_server.go:60 +0xbc
2026-02-03T19:00:16.697996932Z stderr F net/http.HandlerFunc.ServeHTTP(0x3572240?, {0x7f4e849d7d50?, 0xc000448870?}, 0xc000b478d8?)
2026-02-03T19:00:16.698005062Z stderr F 	/usr/local/go/src/net/http/server.go:2220 +0x29
2026-02-03T19:00:16.698020712Z stderr F github.com/prometheus/client_golang/prometheus/promhttp.InstrumentHandlerCounter.func1({0x23ff350?, 0xc000c160e0?}, 0xc000b1b540)
2026-02-03T19:00:16.698047782Z stderr F 	/go/pkg/mod/github.com/prometheus/client_golang@v1.21.1/prometheus/promhttp/instrument_server.go:147 +0xc3
2026-02-03T19:00:16.698056922Z stderr F net/http.HandlerFunc.ServeHTTP(0x1f66cc0?, {0x23ff350?, 0xc000c160e0?}, 0xc000b47a20?)
2026-02-03T19:00:16.698072602Z stderr F 	/usr/local/go/src/net/http/server.go:2220 +0x29
2026-02-03T19:00:16.698085733Z stderr F github.com/prometheus/client_golang/prometheus/promhttp.InstrumentHandlerDuration.func2({0x23ff350, 0xc000c160e0}, 0xc000b1b540)
2026-02-03T19:00:16.698094533Z stderr F 	/go/pkg/mod/github.com/prometheus/client_golang@v1.21.1/prometheus/promhttp/instrument_server.go:109 +0xc2
2026-02-03T19:00:16.698120123Z stderr F net/http.HandlerFunc.ServeHTTP(0xc0002f8c40?, {0x23ff350?, 0xc000c160e0?}, 0x3?)
2026-02-03T19:00:16.698131873Z stderr F 	/usr/local/go/src/net/http/server.go:2220 +0x29
2026-02-03T19:00:16.698155393Z stderr F net/http.(*ServeMux).ServeHTTP(0x410725?, {0x23ff350, 0xc000c160e0}, 0xc000b1b540)
2026-02-03T19:00:16.698163623Z stderr F 	/usr/local/go/src/net/http/server.go:2747 +0x1ca
2026-02-03T19:00:16.698200564Z stderr F net/http.serverHandler.ServeHTTP({0x23f3cd8?}, {0x23ff350?, 0xc000c160e0?}, 0x6?)
2026-02-03T19:00:16.698209474Z stderr F 	/usr/local/go/src/net/http/server.go:3210 +0x8e
2026-02-03T19:00:16.698224234Z stderr F net/http.(*conn).serve(0xc000bd0990, {0x240c8d0, 0xc00099d380})
2026-02-03T19:00:16.698236004Z stderr F 	/usr/local/go/src/net/http/server.go:2092 +0x5d0
2026-02-03T19:00:16.698244294Z stderr F created by net/http.(*Server).Serve in goroutine 203
2026-02-03T19:00:16.698255664Z stderr F 	/usr/local/go/src/net/http/server.go:3360 +0x485
2026-02-03T19:00:16.698263455Z stderr F 
2026-02-03T19:00:16.698271825Z stderr F goroutine 605 [IO wait]:
2026-02-03T19:00:16.698294505Z stderr F internal/poll.runtime_pollWait(0x7f4e849ef790, 0x72)
2026-02-03T19:00:16.698302035Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.698312105Z stderr F internal/poll.(*pollDesc).wait(0xc0008aa900?, 0xc0002bb800?, 0x0)
2026-02-03T19:00:16.698322745Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.698331845Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.698342315Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.698358516Z stderr F internal/poll.(*FD).Read(0xc0008aa900, {0xc0002bb800, 0xc00, 0xc00})
2026-02-03T19:00:16.698368666Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:165 +0x27a
2026-02-03T19:00:16.698391846Z stderr F net.(*netFD).Read(0xc0008aa900, {0xc0002bb800?, 0x52cb85?, 0xc0008aa900?})
2026-02-03T19:00:16.698401756Z stderr F 	/usr/local/go/src/net/fd_posix.go:55 +0x25
2026-02-03T19:00:16.698440126Z stderr F net.(*conn).Read(0xc000432448, {0xc0002bb800?, 0xc000c438d0?, 0x65e064?})
2026-02-03T19:00:16.698448317Z stderr F 	/usr/local/go/src/net/net.go:189 +0x45
2026-02-03T19:00:16.698464277Z stderr F crypto/tls.(*atLeastReader).Read(0xc000a828b8, {0xc0002bb800?, 0x0?, 0xc000a828b8?})
2026-02-03T19:00:16.698474757Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:809 +0x3b
2026-02-03T19:00:16.698487237Z stderr F bytes.(*Buffer).ReadFrom(0xc0007349b8, {0x23e8220, 0xc000a828b8})
2026-02-03T19:00:16.698494027Z stderr F 	/usr/local/go/src/bytes/buffer.go:211 +0x98
2026-02-03T19:00:16.698537658Z stderr F crypto/tls.(*Conn).readFromUntil(0xc000734708, {0x23e9a00, 0xc000432448}, 0xc000c43868?)
2026-02-03T19:00:16.698551738Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:831 +0xde
2026-02-03T19:00:16.698556288Z stderr F crypto/tls.(*Conn).readRecordOrCCS(0xc000734708, 0x0)
2026-02-03T19:00:16.698566668Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:629 +0x3cf
2026-02-03T19:00:16.698571438Z stderr F crypto/tls.(*Conn).readRecord(...)
2026-02-03T19:00:16.698575728Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:591
2026-02-03T19:00:16.698588988Z stderr F crypto/tls.(*Conn).Read(0xc000734708, {0xc0006d6000, 0x1000, 0x35b55e0?})
2026-02-03T19:00:16.698594038Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:1385 +0x150
2026-02-03T19:00:16.698606678Z stderr F net/http.(*connReader).Read(0xc000831200, {0xc0006d6000, 0x1000, 0x1000})
2026-02-03T19:00:16.698619868Z stderr F 	/usr/local/go/src/net/http/server.go:798 +0x14b
2026-02-03T19:00:16.698627809Z stderr F bufio.(*Reader).fill(0xc000a7c960)
2026-02-03T19:00:16.698634729Z stderr F 	/usr/local/go/src/bufio/bufio.go:110 +0x103
2026-02-03T19:00:16.698641379Z stderr F bufio.(*Reader).Peek(0xc000a7c960, 0x4)
2026-02-03T19:00:16.698651019Z stderr F 	/usr/local/go/src/bufio/bufio.go:148 +0x53
2026-02-03T19:00:16.698664679Z stderr F net/http.(*conn).serve(0xc0008eb440, {0x240c8d0, 0xc00099d380})
2026-02-03T19:00:16.698677919Z stderr F 	/usr/local/go/src/net/http/server.go:2127 +0x738
2026-02-03T19:00:16.698689459Z stderr F created by net/http.(*Server).Serve in goroutine 203
2026-02-03T19:00:16.698698269Z stderr F 	/usr/local/go/src/net/http/server.go:3360 +0x485
2026-02-03T19:00:16.698706219Z stderr F 
2026-02-03T19:00:16.698709839Z stderr F goroutine 558 [IO wait]:
2026-02-03T19:00:16.6987194Z stderr F internal/poll.runtime_pollWait(0x7f4e849ef8a8, 0x72)
2026-02-03T19:00:16.69872292Z stderr F 	/usr/local/go/src/runtime/netpoll.go:351 +0x85
2026-02-03T19:00:16.69873242Z stderr F internal/poll.(*pollDesc).wait(0xc0001f5780?, 0xc000b9aa80?, 0x0)
2026-02-03T19:00:16.69874511Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:84 +0x27
2026-02-03T19:00:16.69875472Z stderr F internal/poll.(*pollDesc).waitRead(...)
2026-02-03T19:00:16.69875817Z stderr F 	/usr/local/go/src/internal/poll/fd_poll_runtime.go:89
2026-02-03T19:00:16.69877896Z stderr F internal/poll.(*FD).Read(0xc0001f5780, {0xc000b9aa80, 0xa80, 0xa80})
2026-02-03T19:00:16.69879041Z stderr F 	/usr/local/go/src/internal/poll/fd_unix.go:165 +0x27a
2026-02-03T19:00:16.69880664Z stderr F net.(*netFD).Read(0xc0001f5780, {0xc000b9aa80?, 0x0?, 0xc00044e000?})
2026-02-03T19:00:16.698816761Z stderr F 	/usr/local/go/src/net/fd_posix.go:55 +0x25
2026-02-03T19:00:16.698832561Z stderr F net.(*conn).Read(0xc00009e4e0, {0xc000b9aa80?, 0x23e8100?, 0x23f3cb0?})
2026-02-03T19:00:16.698842121Z stderr F 	/usr/local/go/src/net/net.go:189 +0x45
2026-02-03T19:00:16.698858551Z stderr F crypto/tls.(*atLeastReader).Read(0xc000a82930, {0xc000b9aa80?, 0x0?, 0xc000a82930?})
2026-02-03T19:00:16.698868171Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:809 +0x3b
2026-02-03T19:00:16.698884581Z stderr F bytes.(*Buffer).ReadFrom(0xc0007122b8, {0x23e8220, 0xc000a82930})
2026-02-03T19:00:16.698892411Z stderr F 	/usr/local/go/src/bytes/buffer.go:211 +0x98
2026-02-03T19:00:16.698907512Z stderr F crypto/tls.(*Conn).readFromUntil(0xc000712008, {0x23e9a00, 0xc00009e4e0}, 0xc000b0fcf8?)
2026-02-03T19:00:16.698917482Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:831 +0xde
2026-02-03T19:00:16.698928092Z stderr F crypto/tls.(*Conn).readRecordOrCCS(0xc000712008, 0x0)
2026-02-03T19:00:16.698936542Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:629 +0x3cf
2026-02-03T19:00:16.698944982Z stderr F crypto/tls.(*Conn).readRecord(...)
2026-02-03T19:00:16.698953622Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:591
2026-02-03T19:00:16.698968942Z stderr F crypto/tls.(*Conn).Read(0xc000712008, {0xc000bee911, 0x1, 0x0?})
2026-02-03T19:00:16.698977762Z stderr F 	/usr/local/go/src/crypto/tls/conn.go:1385 +0x150
2026-02-03T19:00:16.698986392Z stderr F net/http.(*connReader).backgroundRead(0xc000bee900)
2026-02-03T19:00:16.698998743Z stderr F 	/usr/local/go/src/net/http/server.go:690 +0x37
2026-02-03T19:00:16.699002293Z stderr F created by net/http.(*connReader).startBackgroundRead in goroutine 313
2026-02-03T19:00:16.699012603Z stderr F 	/usr/local/go/src/net/http/server.go:686 +0xb6
```
Opened the issue there: https://github.com/project-codeflare/appwrapper/issues/384

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2026-02-08T18:51:36Z

Should be fixed by #9049

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T07:30:30Z

/close
Thank you 👍

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-09T07:30:36Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8970#issuecomment-3869840328):

>/close
>Thank you 👍 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
