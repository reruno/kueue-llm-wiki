# Issue #2148: Kueue integration tests are marked failed consistently in the testgrid

**Summary**: Kueue integration tests are marked failed consistently in the testgrid

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2148

**Last updated**: 2024-05-07T11:22:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-05-07T10:04:43Z
- **Updated**: 2024-05-07T11:22:07Z
- **Closed**: 2024-05-07T11:21:44Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

The integration tests (both periodic and pull) are marked failed:

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main

![image](https://github.com/kubernetes-sigs/kueue/assets/10359181/80df3ef2-94cb-45c7-9e32-32bba19d7ac9)

https://testgrid.k8s.io/sig-scheduling#pull-kueue-test-integration-main:

![image](https://github.com/kubernetes-sigs/kueue/assets/10359181/d2683c2e-0b8f-4620-94f8-8d6d55e89b58)

Even though all tests are reported as succeeded inside.

**What you expected to happen**:

The tests are reported as successful (green)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-07T10:04:54Z

/cc @tenzen-y @alculquicondor

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-05-07T11:14:42Z

duplicate of https://github.com/kubernetes-sigs/kueue/issues/2097

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-07T11:21:52Z

@gabesaba Great call.
@mimowo Let us keep track of this issue in #2097
/close
