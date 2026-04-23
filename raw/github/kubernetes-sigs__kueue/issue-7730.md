# Issue #7730: pull-kueue-verify-main and pull-kueue-test-e2e-kueueviz-main are failing due to cypress download

**Summary**: pull-kueue-verify-main and pull-kueue-test-e2e-kueueviz-main are failing due to cypress download

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7730

**Last updated**: 2025-11-18T19:11:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-18T16:22:09Z
- **Updated**: 2025-11-18T19:11:41Z
- **Closed**: 2025-11-18T19:11:41Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 5

## Description

**What happened**:

failures: https://github.com/kubernetes-sigs/kueue/pull/7707#issuecomment-3548206256

**What you expected to happen**:
no such failures
**How to reproduce it (as minimally and precisely as possible)**:
build on ci
**Anything else we need to know?**:
```
#8 9.922 npm error [FAILED] Failed downloading the Cypress binary.
#8 9.922 npm error [FAILED] Response code: 500
#8 9.922 npm error [FAILED] Response message: Internal Server Error
#8 9.925 npm error A complete log of this run can be found in: /root/.npm/_logs/2025-11-18T15_32_27_911Z-debug-0.log
#8 ERROR: process "/bin/sh -c npm install" did not complete successfully: exit code: 1
------
 > [4/5] RUN npm install:
9.922 npm error Installing Cypress (version: 15.6.0)
9.922 npm error
9.922 npm error [STARTED] Task without title.
9.922 npm error Failed downloading the Cypress binary.
9.922 npm error Response code: 500
9.922 npm error Response message: Internal Server Error
9.922 npm error [FAILED] Failed downloading the Cypress binary.
9.922 npm error [FAILED] Response code: 500
9.922 npm error [FAILED] Response message: Internal Server Error
9.925 npm error A complete log of this run can be found in: /root/.npm/_logs/2025-11-18T15_32_27_911Z-debug-0.log
------
Dockerfile:10
--------------------
   8 |     
   9 |     # Install ALL dependencies (including dev dependencies needed for build)
  10 | >>> RUN npm install
  11 |     
  12 |     # Copy source files
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c npm install" did not complete successfully: exit code: 1
make: *** [Makefile:270: npm-depcheck] Error 1
+ EXIT_VALUE=2
+ set +o xtrace
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T16:22:45Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T16:30:17Z

Many of the failed jobs are due to this 

<img width="998" height="514" alt="Image" src="https://github.com/user-attachments/assets/0c7ec982-fe1e-4812-afcb-f02ff26746a4" />

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T16:30:54Z

Opened https://github.com/kubernetes-sigs/kueue/pull/7731 to temporarily mitigate the problem

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T16:44:48Z

<img width="1076" height="447" alt="Image" src="https://github.com/user-attachments/assets/1e9e5ae1-b426-4656-b391-9d12719a68b6" />

from https://www.cypressstatus.com/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T17:59:22Z

<img width="1049" height="179" alt="Image" src="https://github.com/user-attachments/assets/44b09588-7997-4c60-9d2b-9b1437865eb0" />
looks healthy now
