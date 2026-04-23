# Issue #5304: [flaky multikueue integration tests]  Ginkgo timed out waiting for all parallel procs to report back

**Summary**: [flaky multikueue integration tests]  Ginkgo timed out waiting for all parallel procs to report back

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5304

**Last updated**: 2025-05-28T08:27:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-20T15:48:28Z
- **Updated**: 2025-05-28T08:27:36Z
- **Closed**: 2025-05-28T08:27:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What happened**:

failure on periodic job: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-multikueue-main/1924199703738585088

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```

Will run 23 of 23 specs
Running in parallel across 3 processes
Ginkgo timed out waiting for all parallel procs to report back
Test suite: multikueue (./test/integration/multikueue)
This occurs if a parallel process exits before it reports its results to the
Ginkgo CLI.  The CLI will now print out all the stdout/stderr output it's
collected from the running processes.  However you may not see anything useful
in these logs because the individual test processes usually intercept output to
stdout/stderr in order to capture it in the spec reports.
You may want to try rerunning your test suite with
--output-interceptor-mode=none to see additional output here and debug your
suite.
  
Output from proc 1:
Output from proc 2:
Output from proc 3:
** End **Could not open /logs/artifacts/test_integration_multikueue_multikueue-integration.json:
open /logs/artifacts/test_integration_multikueue_multikueue-integration.json: no such file or directory
Could not open /logs/artifacts/test_integration_multikueue_multikueue-junit.xml:
open /logs/artifacts/test_integration_multikueue_multikueue-junit.xml: no such file or directory

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-20T15:48:34Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-23T08:09:57Z

I think what is likely is that there is a rare panic, but it does not get printed due to the bug: https://github.com/kubernetes-sigs/kueue/issues/5315

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-23T08:10:21Z

cc @mszadkow @IrvingMg @mykysha @vladikkuzn

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-26T14:42:57Z

another recent occurence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-multikueue-main/1926917691281510400

pity before we merged https://github.com/kubernetes-sigs/kueue/pull/5327

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-28T08:11:15Z

I think we could close this one, cuz it will be hard to link it to anything that will show up later as flaky.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-28T08:27:30Z

/close
Yes, let's reopen with more details when this re-occurs.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-28T08:27:35Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5304#issuecomment-2915433322):

>/close
>Yes, let's reopen with more details when this re-occurs.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
