# Issue #2226: Visibility API & pprof endpoint are both 8082

**Summary**: Visibility API & pprof endpoint are both 8082

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2226

**Last updated**: 2024-05-20T07:41:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2024-05-17T21:00:32Z
- **Updated**: 2024-05-20T07:41:28Z
- **Closed**: 2024-05-20T07:41:28Z
- **Labels**: `kind/bug`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
It looks like the recommended config for both pprof and visibility api use port 8082. The version I encountered this was `v0.6.2`. This causes the error `{"level":"error","ts":"2024-05-17T20:12:46.493819819Z","logger":"visibility-server","caller":"visibility/server.go:52","msg":"Unable to apply VisibilityServerOptions","error":"failed to create listener: failed to listen on 0.0.0.0:8082: listen tcp 0.0.0.0:8082: bind: address already in use","stacktrace":"sigs.k8s.io/kueue/pkg/visibility.CreateAndStartVisibilityServer\n\t/workspace/pkg/visibility/server.go:52"}
`
Should update the config to change either pprof or visibility port. 

Also see: https://github.com/kubernetes-sigs/kueue/issues/2205#issuecomment-2118319404

## Discussion

### Comment by [@amy](https://github.com/amy) — 2024-05-17T21:07:14Z

/assign

I'll change references for pprof 8082 to 8083?
