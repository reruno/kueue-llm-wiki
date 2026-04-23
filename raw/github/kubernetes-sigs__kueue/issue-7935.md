# Issue #7935: [flaky test] SchedulerWithExcludeResourcePrefixes should use exact prefix matching

**Summary**: [flaky test] SchedulerWithExcludeResourcePrefixes should use exact prefix matching

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7935

**Last updated**: 2025-11-27T10:00:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-27T08:15:15Z
- **Updated**: 2025-11-27T10:00:24Z
- **Closed**: 2025-11-27T10:00:24Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo), [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

**What happened**:

failure: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7933/pull-kueue-test-integration-baseline-main/1993948535971647488

**What you expected to happen**:

no flake

**How to reproduce it (as minimally and precisely as possible)**:

ci
**Anything else we need to know?**:
```
Scheduler with Exclude Resource Prefixes Suite: [It] SchedulerWithExcludeResourcePrefixes should use exact prefix matching expand_less	1s
{failed to run manager
Unexpected error:
    <*net.OpError | 0xc0006c1ea0>: 
    listen tcp 127.0.0.1:33465: bind: address already in use
    {
        Op: "listen",
        Net: "tcp",
        Source: nil,
        Addr: <*net.TCPAddr | 0xc0014127e0>{
            IP: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 127, 0, 0, 1],
            Port: 33465,
            Zone: "",
        },
        Err: <*os.SyscallError | 0xc0013288a0>{
            Syscall: "bind",
            Err: <syscall.Errno>0x62,
        },
    }
occurred failed [FAILED] failed to run manager
Unexpected error:
    <*net.OpError | 0xc0006c1ea0>: 
    listen tcp 127.0.0.1:33465: bind: address already in use
    {
        Op: "listen",
        Net: "tcp",
        Source: nil,
        Addr: <*net.TCPAddr | 0xc0014127e0>{
            IP: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 127, 0, 0, 1],
            Port: 33465,
            Zone: "",
        },
        Err: <*os.SyscallError | 0xc0013288a0>{
            Syscall: "bind",
            Err: <syscall.Errno>0x62,
        },
    }
occurred
In [It] at: /usr/local/go/src/runtime/asm_amd64.s:1693 @ 11/27/25 08:00:00.616
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T08:15:35Z

cc @kannon92 
/assign @mbobrovskyi 
tentatively

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T08:26:56Z

http://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1993936402559012864

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T08:57:21Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T09:34:53Z

/assign
I have a bit of time, and confirmed with @mbobrovskyi to take it
