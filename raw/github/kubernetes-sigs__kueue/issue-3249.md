# Issue #3249: Questions on creating external AC controller for Kueue

**Summary**: Questions on creating external AC controller for Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3249

**Last updated**: 2024-10-25T21:39:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@leipanhz](https://github.com/leipanhz)
- **Created**: 2024-10-17T01:09:12Z
- **Updated**: 2024-10-25T21:39:11Z
- **Closed**: 2024-10-25T21:39:11Z
- **Labels**: `kind/support`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 19

## Description

<!--
STOP -- PLEASE READ!

GitHub is not the right place for support requests.

If you're looking for help, check the [troubleshooting guide](https://kubernetes.io/docs/tasks/debug-application-cluster/troubleshooting/)
or our [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-scheduling)

If the matter is security related, please disclose it privately via https://kubernetes.io/security/.
-->

In the doc and repo, there is an example for additional AdmissionCheck: ProvisioningRequest, but it's part of Kueue source code. It seems the implementation of admissin check controller has high dependencies with Kueue. Are there examples and documentations for a separate external AdmissionCheck controller that works with Kueue

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-10-17T12:32:43Z

Hi @leipanhz,

The dependencies ,I think, you are referring to are just built-time dependencies, meaning the admission check controllers are using some public packages of Kueue as utilities (e.g.  ` !workload.HasQuotaReservation(wl)` to check if the given workload has quota reservation instead of checking the workload's `status.conditions` for the presence and Status of `kueue.WorkloadQuotaReserved` ), but there is no dependencies at runtime, the ACCs can run in a different controller-manager deployment with no functional differences.

### Comment by [@trasc](https://github.com/trasc) — 2024-10-17T12:55:36Z

/assign

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-17T16:37:51Z

@trasc I am new to Kubernetes, I have some detailed questions: 

1. To perform checks, the admission check controller needs to exam workload created by Kueue during reconcile. This is done by setting up its controller in main() and pass client of kueue to the controller: https://github.com/kubernetes-sigs/kueue/blob/main/cmd/kueue/main.go#L238-L262. How can external admission check set up controller with Kueue? 

2. I see both provisioningchecks and multikueue have indexer.go. I didn't find docs about it. How is it needed in admission check process

If you can explain steps needed for implementing  external admission check to integrate with Kueue, that will be very helpful. Thank you.

### Comment by [@trasc](https://github.com/trasc) — 2024-10-18T13:21:16Z

@leipanhz 

1. The external controller-manager should start its own AdmissionCheckController from it's own main() with it's own controller-runtime manager.
2. Those indexes are specific to provisioning and multikueue AdmissionCheckControllers. 

I am working a simplified `demo-acc` #3265, It's still work in progress but feel free to have an early look. (cmd/experimental/demo-acc/STEP-BY-STEP.md describes the steps I took to develop and test it).

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-19T03:28:16Z

> @leipanhz
> 
> 1. The external controller-manager should start its own AdmissionCheckController from it's own main() with it's own controller-runtime manager.
> 2. Those indexes are specific to provisioning and multikueue AdmissionCheckControllers.
> 
> I am working a simplified `demo-acc` #3265, It's still work in progress but feel free to have an early look. (cmd/experimental/demo-acc/STEP-BY-STEP.md describes the steps I took to develop and test it).

@trasc Thank you for providing example of demo-acc! I hit an error during compilation: 
`# sigs.k8s.io/kueue/pkg/features
../../../../go/pkg/mod/sigs.k8s.io/kueue@v0.8.1/pkg/features/kube_features.go:126:9: featuregatetesting.SetFeatureGateDuringTest(tb, utilfeature.DefaultFeatureGate, f, value) (no value) used as value
make: *** [vet] Error 1`
FYI, the controller is on a separate repo with different domain and group names.

### Comment by [@trasc](https://github.com/trasc) — 2024-10-19T15:55:14Z

`featuregatetesting.SetFeatureGateDuringTest` was changed lately in `k8s.io/component-base`, please try to use an older component-base or a newer kueue version

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-19T22:53:40Z

> `featuregatetesting.SetFeatureGateDuringTest` was changed lately in `k8s.io/component-base`, please try to use an older component-base or a newer kueue version

The v0.8.1 version I used seems to be the latest stable release: https://github.com/kubernetes-sigs/kueue/releases/tag/v0.8.1. I found v0.9.0-devel is the only higher version than v0.8.1. After trying, still seeing the same issue (with other errors):

\# sigs.k8s.io/kueue/pkg/features
../../../../go/pkg/mod/sigs.k8s.io/kueue@v0.9.0-devel/pkg/features/kube_features.go:126:9: featuregatetesting.SetFeatureGateDuringTest(tb, utilfeature.DefaultFeatureGate, f, value) (no value) used as value
\# sigs.k8s.io/controller-runtime/pkg/metrics
../../../../go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/metrics/leaderelection.go:26:71: undefined: leaderelection.SwitchMetric
\# k8s.io/apiserver/pkg/cel/library
../../../../go/pkg/mod/k8s.io/apiserver@v0.29.6/pkg/cel/library/cost.go:182:28: args[1].Expr().GetConstExpr undefined (type "github.com/google/cel-go/common/ast".Expr has no field or method GetConstExpr)
../../../../go/pkg/mod/k8s.io/apiserver@v0.29.6/pkg/cel/library/cost.go:259:11: cannot use &itemsNode{…} (value of type *itemsNode) as checker.AstNode value in return statement: *itemsNode does not implement checker.AstNode (wrong type for method Expr)
		have Expr() *expr.Expr
		want Expr() "github.com/google/cel-go/common/ast".Expr
../../../../go/pkg/mod/k8s.io/apiserver@v0.29.6/pkg/cel/library/cost.go:262:11: cannot use &itemsNode{…} (value of type *itemsNode) as checker.AstNode value in return statement: *itemsNode does not implement checker.AstNode (wrong type for method Expr)
		have Expr() *expr.Expr
		want Expr() "github.com/google/cel-go/common/ast".Expr

If I need to downgrade k8s.io/component-base, can you please recommend a version number?

### Comment by [@trasc](https://github.com/trasc) — 2024-10-20T05:53:10Z

> If I need to downgrade k8s.io/component-base, can you please recommend a version number?

Check the version kueue 0.8.1 is using (in kueue's go.mod)

You can also use kueue@main, temporarily, we will release v0.9.0 shortly.

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-21T05:15:42Z

> > If I need to downgrade k8s.io/component-base, can you please recommend a version number?
> 
> Check the version kueue 0.8.1 is using (in kueue's go.mod)
> 
> You can also use kueue@main, temporarily, we will release v0.9.0 shortly.

I downgraded versions of a few packages to be compatible with kueue 0.8.1. I am able to run makefile and build image. However, when I deployed the image, the controller-manager is crashing with the following error: 
2024-10-21T04:47:10Z	ERROR	setup	unable to create controller	{"controller": "AdmissionCheck", "error": "no kind is registered for the type v1beta1.AdmissionCheck in scheme \"pkg/runtime/scheme.go:100\""}
main.main
	/workspace/cmd/main.go:151
runtime.main
	/usr/local/go/src/runtime/proc.go:271
The above error is from the external customer controller. I noticed the version of k8s.io/apimachinery where has scheme.go is older than the one in main, however, upgrading it triggers other compilation issues. 

Then in the kueu repo, I pulled demo-acc, built and deployed for comparison. The kueue controller manager crashes too, but for a different error (I don't have this issue with mainline code before 9/6): 
{"level":"error","ts":"2024-10-21T04:50:11.346596132Z","logger":"setup","caller":"kueue/main.go:208","msg":"Provisioning Requests are not supported, skipped admission check controller setup","stacktrace":"main.setupIndexes\n\t/workspace/cmd/kueue/main.go:208\nmain.main\n\t/workspace/cmd/kueue/main.go:169\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:272"}
{"level":"error","ts":"2024-10-21T04:50:11.347161923Z","logger":"setup","caller":"kueue/main.go:217","msg":"Could not setup multikueue indexer","error":"setting index on clusters using kubeconfig: no matches for kind \"MultiKueueCluster\" in version \"kueue.x-k8s.io/v1beta1\"","stacktrace":"main.setupIndexes\n\t/workspace/cmd/kueue/main.go:217\nmain.main\n\t/workspace/cmd/kueue/main.go:169\nruntime.main\n\t/usr/local/go/src/runtime/proc.go:272"}

Do you have any suggestions for me to move forward? Happy to schedule an online troubleshooting session at your convenient time if that works for you. Btw, attached is the go.mod file used in my controller. Thank you for your time. 
[gomod.txt](https://github.com/user-attachments/files/17455179/gomod.txt)

### Comment by [@trasc](https://github.com/trasc) — 2024-10-21T05:55:01Z

Hi, 

For the first part:
> I downgraded versions of a few packages to be compatible with kueue 0.8.1. I am able to run makefile and build image. However, when.....................

I likely because the Kueue's API is not registered in the scheme, you'll need to do something like 

```diff
@@ -34,6 +34,7 @@ import (
 	"sigs.k8s.io/controller-runtime/pkg/metrics/filters"
 	metricsserver "sigs.k8s.io/controller-runtime/pkg/metrics/server"
 	"sigs.k8s.io/controller-runtime/pkg/webhook"
+	kueueapi "sigs.k8s.io/kueue/apis/kueue/v1beta1"

 	"sigs.k8s.io/kueue/cmd/experimental/demo-acc/internal/controller"
 	// +kubebuilder:scaffold:imports
@@ -46,6 +47,7 @@ var (

 func init() {
 	utilruntime.Must(clientgoscheme.AddToScheme(scheme))
+	utilruntime.Must(kueueapi.AddToScheme(scheme))

 	// +kubebuilder:scaffold:scheme
 }
```
I  your controller's `main.go`


The second part:

> Then in the kueu repo, I pulled demo-acc, built and deployed for comparison. The kueue controller manager crashes too, but for a different error (I don't have this issue with mainline code before 9/6):.......

It's likely because the manifests in your cluster are out of sync with the kueue's controller-manager. Not long ago, we've moved the MultiKueue APIs from `v1alpha1` to `v1beta1`. This should not happen if you run `make install` and `make deploy`, for Kueue, from the same source tree (and version).

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-21T22:42:51Z

@trasc, I followed your comments and was able to resolve most issues, thank you! For the multikueue issue: after removing some previously defined CRDs related to multikueue,  and recompile with all cache cleaned, the error is gone. 

Note that, there are other errors related to webhook when running "make deploy", for example: 
`failed calling webhook "mdeployment.kb.io"... the server could not find the requested resource. ` For now I deleted "mdeployment.kb.io" and "rdeployment.kb.io" in the webhook, deployment went through but that may not be desired actions. 

For the first part (with my external controller), there is a mistakes in imports. After fixing that, the admission check registration issue was resolved. I encountered different errors, but that is probably related to my system setup and implementation. I am looking into them, and will reach out if I have additional questions about Kueue integration. Appreciate your knowledge sharing.

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-23T21:47:02Z

@trasc I noticed there is always an error message when an Admissioncheck is created, from kueue/vendor/k8s.io/apiserver/pkg/registry/generic/registry/store.go, and the log information is not printed in the controller log,  although admissioncheck is up running:

2024-10-23T20:57:16Z	INFO	Starting Controller	{"controller": "admissioncheck", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "AdmissionCheck"}
2024-10-23T20:57:17Z	INFO	Starting workers	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "worker count": 1}
2024-10-23T20:57:17Z	INFO	Starting workers	{"controller": "admissioncheck", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "AdmissionCheck", "worker count": 1}
2024-10-23T21:36:14Z	ERROR	Reconciler error	{"controller": "admissioncheck", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "AdmissionCheck", "AdmissionCheck": {"name":"demo-ac"}, "namespace": "", "name": "demo-ac", "reconcileID": "fca955c2-a0d1-4675-a883-259ce9855c5b", "error": "Operation cannot be fulfilled on admissionchecks.kueue.x-k8s.io \"demo-ac\": the object has been modified; please apply your changes to the latest version and try again"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.19.0/pkg/internal/controller/controller.go:316
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.19.0/pkg/internal/controller/controller.go:263
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2
	/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.19.0/pkg/internal/controller/controller.go:224

Is this related to the package version or something else? I am using kueue v0.8.1 image.

### Comment by [@trasc](https://github.com/trasc) — 2024-10-24T12:39:40Z

No, this happens because there are two controllers trying to update the same  resource at the same time, one of them will get the conflict, however, when this happens controller-runtime will queue another reconcile request for that object and eventually will succeed.

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-24T13:58:23Z

> No, this happens because there are two controllers trying to update the same resource at the same time, one of them will get the conflict, however, when this happens controller-runtime will queue another reconcile request for that object and eventually will succeed.

I don't see any logs from the other reconciler (the custom controller) after the error. Do you have any suggestions?

### Comment by [@trasc](https://github.com/trasc) — 2024-10-24T14:51:47Z

> > No, this happens because there are two controllers trying to update the same resource at the same time, one of them will get the conflict, however, when this happens controller-runtime will queue another reconcile request for that object and eventually will succeed.
> 
> I don't see any logs from the other reconciler (the custom controller) after the error. Do you have any suggestions?

No error is an indication that nothing went wrong :). In the demo-acc, the AC reconciler has only one job, to set the `Active` condition to true for the ACs managed by it. 

The testing step: 

---
It should get marked as `Active`

```bash
kubectl get admissionchecks.kueue.x-k8s.io demo-ac -o=jsonpath='{.status.conditions[?(@.type=="Active")].status}{" -> "}{.status.conditions[?(@.type=="Active")].message}{"\n"}'
```
---

Checks if that in fact happening.

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-24T15:38:06Z

> No error is an indication that nothing went wrong :). 

Sorry, I meant the info level logs added in the reconcile code didn't show as expected, after the above error message was printed. I tested on demo-ac and my controller, in both cases there are no logs printed even though the reconcile requests seems working. Is there anything I missed?

> Checks if that in fact happening.

Yes this works

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-25T01:55:40Z

> Sorry, I meant the info level logs added in the reconcile code didn't show as expected, after the above error message was printed. 

I realized this is related to log level setting. I thought V(2) would enable printing logs by default, but it isn't. Feel free to resolve the issue. Thanks!

### Comment by [@trasc](https://github.com/trasc) — 2024-10-25T07:20:49Z

You can add `--zap-log-level=2` in the managers args, to increase its log level.

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-10-25T21:39:11Z

Thanks for your support @trasc
