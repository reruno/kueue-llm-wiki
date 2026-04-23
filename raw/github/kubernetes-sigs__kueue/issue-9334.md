# Issue #9334: `readOnlyRootFilesystem:true` or `runAsUser!=0` causes silent misconfiguration in kueueviz frontend

**Summary**: `readOnlyRootFilesystem:true` or `runAsUser!=0` causes silent misconfiguration in kueueviz frontend

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9334

**Last updated**: 2026-03-19T18:06:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ziadmoubayed](https://github.com/ziadmoubayed)
- **Created**: 2026-02-18T09:06:34Z
- **Updated**: 2026-03-19T18:06:35Z
- **Closed**: 2026-03-19T18:06:35Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 6

## Description

**What happened**:

When deploying kueueviz with `containerSecurityContext.readOnlyRootFilesystem: true` (which is the default in values.yaml) or setting `runAsUser!=0`, the frontend container fails to generate build/env.js at startup. 
1. The build directory is owned by root incompatible with `runAsUser!=0`
2. `readOnlyRootFilesystem` is not compatible with start.sh logic.

The failure is silent and npx serve starts, but the frontend loads the baked-in default env.js from the image (ws://localhost:8080), causing the dashboard to be unable to connect to the backend regardless of what REACT_APP_WEBSOCKET_URL is set to.

**What you expected to happen**:
Frontend would respect `REACT_APP_WEBSOCKET_URL` configuration

**How to reproduce it (as minimally and precisely as possible)**:

Set `readOnlyRootFilesystem: true` or `runAsUser: 1000` when deploying kueueviz frontend

**Anything else we need to know?**:
kueue values.yaml chart defaults to `readOnlyRootFilesystem: true` so i am afraid this might hurt users when released.

**Environment**:
- Kubernetes version (use `kubectl version`): `v1.32.11`
- Kueue version (use `git describe --tags --dirty --always`): `v1.16.0`

## Discussion

### Comment by [@ziadmoubayed](https://github.com/ziadmoubayed) — 2026-02-18T09:08:58Z

Happy to pick this up. I feel a clean solution would be to mount env.js via config map. Unfortunately this would introduce a small _breaking change_ (currently frontend backend config is defined with env).
Curious what you think

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-18T10:46:44Z

Thank you for the reporting!

@ziadmoubayed so you are saying this PR https://github.com/kubernetes-sigs/kueue/pull/9311 is a regression? Should we change the defaults then in this PR?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-18T10:52:20Z

I see, so we could move forward "mounting env.js via configMap", I think I'm ok with that, but we should mention in the release notes the upgrade steps.

### Comment by [@ziadmoubayed](https://github.com/ziadmoubayed) — 2026-02-18T11:52:04Z

> Thank you for the reporting!
> 
> [@ziadmoubayed](https://github.com/ziadmoubayed) so you are saying this PR [#9311](https://github.com/kubernetes-sigs/kueue/pull/9311) is a regression? Should we change the defaults then in this PR?

Unfortunately my previous PR introduces a regression. Updating the default values here: https://github.com/kubernetes-sigs/kueue/pull/9339

### Comment by [@ziadmoubayed](https://github.com/ziadmoubayed) — 2026-02-18T11:52:25Z

> I see, so we could move forward "mounting env.js via configMap", I think I'm ok with that, but we should mention in the release notes the upgrade steps.

Thanks, will pick this up

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-18T12:04:52Z

ok and then we will change the default values and fix it properly in 0.17+
