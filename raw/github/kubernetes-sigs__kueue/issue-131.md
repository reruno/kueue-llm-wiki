# Issue #131: Failed to watch *v1.PriorityClass

**Summary**: Failed to watch *v1.PriorityClass

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/131

**Last updated**: 2022-03-19T16:51:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Created**: 2022-03-18T20:50:13Z
- **Updated**: 2022-03-19T16:51:08Z
- **Closed**: 2022-03-19T16:51:08Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
After deploying and applying the sample objects this error is repeating on the logs 
```bash
E0318 20:46:22.352756       1 reflector.go:138] pkg/mod/k8s.io/client-go@v0.23.4/tools/cache/reflector.go:167: Failed to watch *v1.PriorityClass: unknown (get priorityclasses.scheduling.k8s.io)
```
**What you expected to happen**:
Not to see that error
**How to reproduce it (as minimally and precisely as possible)**:
```bash
make image-build image-push deploy
kubectl logs -f $(kubectl get pods -n kueue-system --no-headers -o name) manager -n kueue-system
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
```bash
kubectl version
Client Version: version.Info{Major:"1", Minor:"23", GitVersion:"v0.23.0", GitCommit:"f93da179fe606775f8249fed96e0b9903d9188ed", GitTreeState:"clean", BuildDate:"2022-03-09T05:14:42Z", GoVersion:"go1.17.5", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"23+", GitVersion:"v1.23.4-rc.0", GitCommit:"72506a8439cb4465d176af044e4404439135c915", GitTreeState:"clean", BuildDate:"2022-01-25T21:44:57Z", GoVersion:"go1.17.6", Compiler:"gc", Platform:"linux/amd64"}
```
- Kueue version (use `git describe --tags --dirty --always`): main branch
- Cloud provider or hardware configuration: minikube
- OS (e.g: `cat /etc/os-release`): minikube
- Kernel (e.g. `uname -a`): minikube latest
- Install tools: 
- Others:
