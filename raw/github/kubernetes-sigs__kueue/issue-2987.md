# Issue #2987: deployment webhook is broken

**Summary**: deployment webhook is broken

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2987

**Last updated**: 2024-09-05T18:33:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alaypatel07](https://github.com/alaypatel07)
- **Created**: 2024-09-04T18:57:43Z
- **Updated**: 2024-09-05T18:33:00Z
- **Closed**: 2024-09-05T18:33:00Z
- **Labels**: `kind/bug`
- **Assignees**: [@alaypatel07](https://github.com/alaypatel07)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
1. Installed kueue using the following commands:
```
IMAGE_REGISTRY=<registry> make  image-local-push deploy
```
2. Ran patch command to try out the visibility api
```
 kubectl patch -n kueue-system deployment kueue-controller-manager --type='json' -p='[

  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--feature-gates=VisibilityOnDemand=true"
  }
]'
```

The error failed with 
```
Error from server (InternalError): Internal error occurred: failed calling webhook "vdeployment.kb.io": failed to call webhook: the server could not find the requested resource
```
3. Tried to create busybox deployment, failed with the same error

**What you expected to happen**:
Create and update calls to deployment should work.

**How to reproduce it (as minimally and precisely as possible)**:
1. checkout main
2. run `IMAGE_REGISTRY=<registry> make  image-local-push deploy`
3. create or update deployment as noted above

**Anything else we need to know?**:
This PR #2813 added a validating and mutating webhook for deployments, but it is not registered by default

**Environment**:
- Kubernetes version (use `kubectl version`): tested in 1.30.3 and 1.31.0
- Kueue version (use `git describe --tags --dirty --always`): main at commit  0bcde8c82e6a769bf75e3d195b65d18dbb6e2bf6
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2024-09-04T18:57:55Z

/assign

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2024-09-04T19:32:56Z

It seems like importing deployment https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/jobs.go#L28 should solve the issue.

Trying it out in local environment

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2024-09-04T19:53:45Z

```
diff --git a/config/components/manager/controller_manager_config.yaml b/config/components/manager/controller_manager_config.yaml
index c0a9f597..9850c3fa 100644
--- a/config/components/manager/controller_manager_config.yaml
+++ b/config/components/manager/controller_manager_config.yaml
@@ -48,15 +48,16 @@ integrations:
   - "kubeflow.org/pytorchjob"
   - "kubeflow.org/tfjob"
   - "kubeflow.org/xgboostjob"
-#  - "pod"
+  - "pod"
+  - "deployment"
 #  externalFrameworks:
 #  - "Foo.v1.example.com"
-#  podOptions:
-#    namespaceSelector:
-#      matchExpressions:
-#        - key: kubernetes.io/metadata.name
-#          operator: NotIn
-#          values: [ kube-system, kueue-system ]
+  podOptions:
+    namespaceSelector:
+      matchExpressions:
+        - key: kubernetes.io/metadata.name
+          operator: NotIn
+          values: [ kube-system, kueue-system ]
```

enabling the above configuration made it work for me.

```
# kubectl patch -n kueue-system deployment kueue-controller-manager --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--feature-gates=VisibilityOnDemand=true"
  }
]'
deployment.apps/kueue-controller-manager patched
```

So either the pod framework should be enabled or webhook configuration should be disable, one or the other should solve this issue in main branch.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-04T20:57:09Z

/cc @vladikkuzn

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-05T06:51:50Z

The original intention was to enforce that the pod integration is enabled. From https://github.com/kubernetes-sigs/kueue/issues/2717#issue-2435374397: "introduce a dedicated Deployment integration, and validate that it can only be enabled when pod integration is enabled".

Here was the preparatory PR: https://github.com/kubernetes-sigs/kueue/pull/2768. However, I'm not sure if the mechanism was eventually used. Do you know @vladikkuzn @trasc ?

@alaypatel07 would enforcing the dependency solve this issue for you?

EDIT: ah I see the dependency is already there: https://github.com/kubernetes-sigs/kueue/blob/afb49468223ca81419b13e45923f752f803dd80e/pkg/controller/jobs/deployment/deployment_controller.go#L46. Let's fix the remaining issue in https://github.com/kubernetes-sigs/kueue/pull/2988
