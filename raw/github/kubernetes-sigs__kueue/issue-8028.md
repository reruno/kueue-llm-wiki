# Issue #8028: Default `KUEUEVIZ_ALLOWED_ORIGINS` is invalid

**Summary**: Default `KUEUEVIZ_ALLOWED_ORIGINS` is invalid

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8028

**Last updated**: 2025-12-12T16:35:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tjcuddihy](https://github.com/tjcuddihy)
- **Created**: 2025-12-02T03:37:01Z
- **Updated**: 2025-12-12T16:35:54Z
- **Closed**: 2025-12-12T16:35:54Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

**What happened**:
The [default values](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml) for KueueViz offer `frontend.kueueviz.local` as the `KUEUEVIZ_ALLOWED_ORIGIN`.

However, the origins are validated [here](https://github.com/kubernetes-sigs/kueue/blob/1f6804fc5ea95f17e868b8a603689f49ac666eff/cmd/kueueviz/backend/middleware/cors.go#L33) which has a [specific check](https://github.com/kubernetes-sigs/kueue/blob/1f6804fc5ea95f17e868b8a603689f49ac666eff/cmd/kueueviz/backend/middleware/cors.go#L45) to ensure that the url has a scheme of either HTTP or HTTPS. I.e. the provided default value is invalid.


**Environment**:
- Kubernetes version (use `kubectl version`):
```
Client Version: v1.30.1
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.32.9-eks-3cfe0ce
```
- Kueue version (use `git describe --tags --dirty --always`): `v0.14.1`
- KueueViz Version: `v0.14.1`
