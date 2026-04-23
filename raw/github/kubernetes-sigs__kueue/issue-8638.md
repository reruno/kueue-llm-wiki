# Issue #8638: Kueue: e2e tests hang on macOS due to incompatible Bash parameter

**Summary**: Kueue: e2e tests hang on macOS due to incompatible Bash parameter

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8638

**Last updated**: 2026-01-16T16:13:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@anahas-redhat](https://github.com/anahas-redhat)
- **Created**: 2026-01-16T15:17:19Z
- **Updated**: 2026-01-16T16:13:19Z
- **Closed**: 2026-01-16T16:13:19Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When trying to run e2e tests on MacOS, execution gets stuck.

**What you expected to happen**:
Execution should end successfully.

**How to reproduce it (as minimally and precisely as possible)**:
I'm following the steps provided [here](https://kueue.sigs.k8s.io/docs/contribution_guidelines/testing/#running-e2e-tests-using-custom-build).
1. Run `make kind-image-build`
2. Run `make test-e2e`

**Actual behavior:**
After running step 2, execution gets stuck on step "_namespace/kueue-system serverside-applied_". It keeps in this state for hours, until user manually stops it. 

**Anything else we need to know?**:
After debugging, it was discovered that execution stops at this code point: https://github.com/kubernetes-sigs/kueue/blob/main/hack/e2e-common.sh#L360

On local tests, if we change this line from:
`build_output=${build_output//kueue-system/$KUEUE_NAMESPACE}`
to:
`build_output=$(echo "$build_output" | sed "s/kueue-system/$KUEUE_NAMESPACE/g")`
an execute the steps again, execution finishes successfully.

Looking at a PR from last year, it was checked that in the past the command used to be `build_output=$(echo "$build_output" | sed "s/kueue-system/$KUEUE_NAMESPACE/g")`. I'm not sure why it changed but, it would be good if we could add it back so execution on MacOS passes again.

[log.txt](https://github.com/user-attachments/files/24674760/log.txt)

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`): 
ProductName:            macOS (m1)
ProductVersion:         26.2
BuildVersion:           25C56
- Kernel (e.g. `uname -a`): 
Darwin Kernel Version 25.2.0
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-16T15:28:05Z

Hmm, we already fixed this with @mykysha in #5838.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-16T15:29:23Z

I see. It was reverted by this PR #7772. Actually, I don't know why.

cc: @sohankunkerkar

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-16T15:40:09Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-16T15:40:31Z

@anahas-redhat Thanks for catching that!

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-16T15:47:39Z

>I see. It was reverted by this PR https://github.com/kubernetes-sigs/kueue/pull/7772. Actually, I don't know why.

Actually, I didn’t realize that since my local machine uses Linux, but yeah, that should be reverted.
