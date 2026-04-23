# Issue #392: kueue manager does not work on clusters with OwnerReferencesPermissionEnforcement admission control validation enabled

**Summary**: kueue manager does not work on clusters with OwnerReferencesPermissionEnforcement admission control validation enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/392

**Last updated**: 2022-09-15T15:25:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kincl](https://github.com/kincl)
- **Created**: 2022-09-15T01:02:44Z
- **Updated**: 2022-09-15T15:25:24Z
- **Closed**: 2022-09-15T15:25:24Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When a Job is created, the controller-manager attempts to set an ownerReference on the corresponding Workload that references the Job but the OwnerReferencesPermissionEnforcement admission controller does not allow that to be set because the manager does not have permissions to access the jobs/finalizer resource.

controller-manager logs:
```
manager {"level":"Level(-2)","ts":"2022-09-15T00:40:36.953047876Z","caller":"job/job_controller.go:140","msg":"Reconciling Job","controller":"job","controllerGroup":"batch","controllerKind":"Job","job":{"name":"sample-job-qvqxz","namespace":"default"},"namespace":"default","name":"sample-job-qvqxz","reconcileID":"fcabfef2-ed3d-49e1-b660-9312c0d61a54","job":{"name":"sample-job-qvqxz","namespace":"default"}}
manager {"level":"debug","ts":"2022-09-15T00:40:36.956372565Z","logger":"controller-runtime.webhook.webhooks","caller":"admission/http.go:96","msg":"received request","webhook":"/mutate-kueue-x-k8s-io-v1alpha2-workload","UID":"1ca4afbf-4426-409c-b985-0630caef3f75","kind":"kueue.x-k8s.io/v1alpha2, Kind=Workload","resource":{"group":"kueue.x-k8s.io","version":"v1alpha2","resource":"workloads"}}
manager {"level":"debug","ts":"2022-09-15T00:40:36.956690404Z","logger":"controller-runtime.webhook.webhooks","caller":"admission/http.go:143","msg":"wrote response","webhook":"/mutate-kueue-x-k8s-io-v1alpha2-workload","code":200,"reason":"","UID":"1ca4afbf-4426-409c-b985-0630caef3f75","allowed":true}
manager {"level":"error","ts":"2022-09-15T00:40:36.959084919Z","caller":"job/job_controller.go:165","msg":"Handling job with no workload","controller":"job","controllerGroup":"batch","controllerKind":"Job","job":{"name":"sample-job-qvqxz","namespace":"default"},"namespace":"default","name":"sample-job-qvqxz","reconcileID":"fcabfef2-ed3d-49e1-b660-9312c0d61a54","job":{"name":"sample-job-qvqxz","namespace":"default"},"error":"workloads.kueue.x-k8s.io \"sample-job-qvqxz\" is forbidden: cannot set blockOwnerDeletion if an ownerReference refers to a resource you can't set finalizers on: , <nil>","stacktrace":"sigs.k8s.io/kueue/pkg/controller/workload/job.(*JobReconciler).Reconcile\n\t/workspace/pkg/controller/workload/job/job_controller.go:165\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:121\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:320\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:273\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:234"}
manager {"level":"error","ts":"2022-09-15T00:40:36.959140793Z","caller":"controller/controller.go:326","msg":"Reconciler error","controller":"job","controllerGroup":"batch","controllerKind":"Job","job":{"name":"sample-job-qvqxz","namespace":"default"},"namespace":"default","name":"sample-job-qvqxz","reconcileID":"fcabfef2-ed3d-49e1-b660-9312c0d61a54","error":"workloads.kueue.x-k8s.io \"sample-job-qvqxz\" is forbidden: cannot set blockOwnerDeletion if an ownerReference refers to a resource you can't set finalizers on: , <nil>","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:326\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:273\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.12.3/pkg/internal/controller/controller.go:234"}
```

**What you expected to happen**:

Upon creating a Job, the controller-manager correctly creates a Workload object and processes the queued jobs.

**How to reproduce it (as minimally and precisely as possible)**:

- Enable [OwnerReferencesPermissionEnforcement](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#ownerreferencespermissionenforcement) admission controller validation on Kubernetes API server
- Deploy kueue controller-manager
- Run in-repo samples
- Check manager logs 

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.24.0+b62823b
- Kueue version (use `git describe --tags --dirty --always`): v0.2.1
- OS (e.g: `cat /etc/os-release`): OpenShift 4.11.2
