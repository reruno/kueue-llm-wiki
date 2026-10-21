# Performance tests

**Summary**: Kueue has scheduler-focused performance benchmarks under `test/performance/scheduler/`. They measure admission-loop throughput, not correctness, and are driven by a generator/runner that replays synthetic Workload traffic against a minimal Kueue controller. This page covers how to run them locally and which make targets wrap them.

**Sources**: `raw/kueue/hack/make/test.mk` (formerly `Makefile-test.mk`), `raw/kueue/test/performance/scheduler/`, `raw/kueue/hack/testing/performance-test.sh`, `raw/kueue/hack/testing/compare-performance.sh`; pr-16652.md, pr-16923.md.

**Last updated**: 2026-10-21

---

## What exists

Under `test/performance/`:

```
test/performance/
├── scheduler/
│   ├── checker/         # assertions over a run's summary/cmd-stats
│   ├── configs/
│   │   ├── baseline/    # default generator + range spec
│   │   ├── large-scale/ # 10 cohorts x 100 CQs, 50,000 single-pod workloads
│   │   ├── tas/         # TAS generator + range spec
│   │   └── tas-dra/     # same topology/workloads as tas/, every pod also claims DRA devices
│   ├── minimalkueue/    # a stripped-down controller binary used as the runner target
│   └── runner/          # drives the scenario, collects metrics
└── e2e/                 # (separate; exercises perf in a Kind cluster)
```

Two binaries are built from this tree by `hack/make/test.mk` (the former `Makefile-test.mk`, split up in #14127):

- `bin/performance-scheduler-runner` — the scenario driver (`make performance-scheduler-runner`).
- `bin/minimalkueue` — a reduced Kueue that the runner targets (`make minimalkueue`).

## Make targets

### Scheduler perf (baseline config)

```shell
make run-performance-scheduler          # runs the scenario, writes results under $ARTIFACTS/run-performance-scheduler/
make test-performance-scheduler-once    # run + validate against configs/baseline/rangespec.yaml
make test-performance-scheduler         # same, but wrapped by hack/testing/performance-test.sh with retries (PERFORMANCE_RETRY_COUNT, default 2)
make run-performance-scheduler-in-cluster   # variant used inside a cluster: no minimalkueue, higher QPS/burst, 15m timeout
```

Controls (`Makefile-test.mk`):

- `SCALABILITY_GENERATOR_CONFIG` (default `test/performance/scheduler/configs/baseline/generator.yaml`).
- `SCALABILITY_CPU_PROFILE` — set (truthy) to enable CPU profiling (`--withCPUProfile=true`).
- `SCALABILITY_MEM_PROFILE` — same for memory.
- `SCALABILITY_SCRAPE_URL` — point scraping at a specific metrics URL.
- `SCALABILITY_SCRAPE_INTERVAL` (default `5s`).
- `NO_SCALABILITY_KUEUE_LOGS` — unset by default; when set, suppresses `--withLogs --logToFile` flags.
- `NO_SCALABILITY_SCRAPE` — same, suppresses metrics scraping.
- `PERFORMANCE_RETRY_COUNT` (default `2`) — retries for the wrapped perf test.

### Scheduler perf with TAS

```shell
make run-tas-performance-scheduler
make test-tas-performance-scheduler-once
make test-tas-performance-scheduler
make run-tas-performance-scheduler-in-cluster
```

Controls:

- `SCALABILITY_TAS_GENERATOR_CONFIG` (default `test/performance/scheduler/configs/tas/generator.yaml`).
- `SCALABILITY_TAS_RANGE_FILE` (default `test/performance/scheduler/configs/tas/rangespec.yaml`).

TAS runs pass `--enableTAS=true` and a 20-min or 25-min timeout depending on mode.

### Scheduler perf with TAS + DRA

```shell
make run-tas-dra-performance-scheduler
make test-tas-dra-performance-scheduler-once
make test-tas-dra-performance-scheduler
```

Controls: `SCALABILITY_TAS_DRA_GENERATOR_CONFIG`, `SCALABILITY_TAS_DRA_RANGE_FILE` (defaults under `configs/tas-dra/`). Runs pass `--enableTAS=true --enableDRA=true` with a 20-min timeout. The generator uses the same 640-node topology and 15,000 workloads as `configs/tas`, so the two runs compare directly. Each node publishes 8 devices; small and medium pods claim 1 and large pods 2. Device quota is twice the CPU quota, so CPU stays the binding quota. There is no kube-scheduler, so devices are never allocated: the run measures the cost of the per-node **device feasibility check** in each scheduling cycle, not device contention. Devices carry no attributes, so each is cheaper to evaluate than a real GPU with attribute selectors.

The `rangespec.yaml` thresholds were set from **10 CI runs**: wall time and per-class average time-to-admission use mean + 20%, rounded up to 1000 ms (for example `maxWallMs: 436_000`; `small-required-rack` 288 s); ClusterQueue minimum usage uses mean − 7% (`cq: 49.7`%) (source: pr-16652.md, fixes #16352). The same method (mean ± a margin from repeated CI runs, with mean/stddev/CV recorded as comments) is the pattern to follow when adjusting any rangespec.

### Large-scale config

`run-large-scale-performance-scheduler` / `test-large-scale-performance-scheduler[-once]` (and an `-in-cluster` variant with `--qps=1000 --burst=2000`) use `configs/large-scale`: 10 cohorts × 100 ClusterQueues = 1,000 CQs, with 50 single-pod Workloads per queue (50,000 total) and a 30-min timeout (source: `hack/make/test.mk`, `configs/large-scale/generator.yaml`).

## CI

The unit tests of the performance tooling itself (for example the MultiKueue performance tool) now run in the regular unit-test shards, with race detection, JUnit and coverage. They no longer run as a separate race-test step in `make verify` (source: pr-16923.md). CI job names for the scheduler perf benchmarks are not individually attested in the raw issue/PR corpus. The make targets above are what contributors invoke locally; corresponding Prow jobs wrap them.

## Comparing runs

`hack/testing/compare-performance.sh` compares two runs' output directories to surface regressions. Pair it with CPU/memory profiles written to `$ARTIFACTS/run-*-scheduler/` when profiling is enabled.

## What to watch

Primary signals (emitted by the running Kueue controller and collected by the runner via Prometheus scrape):

- `kueue_admission_attempt_duration_seconds` — scheduling loop latency.
- `kueue_admission_attempts_total` — attempt rate.

See [[metrics]] for the full surface and [[performance-and-scale]] for what rising numbers mean in each regime.

## When to run these

You generally don't, during a feature PR. Reach for the perf targets when:

- A change touches the hot path: `pkg/cache/`, `pkg/scheduler/`, cohort-hierarchy walks, TAS per-domain accounting.
- A reviewer asks for a before/after on a specific generator config.
- You are investigating a regression reported against a release.

For all other work, the normal integration and e2e tiers are sufficient.

## Related pages

- [[performance-and-scale]] — what the perf benchmarks are designed to prove out, and where the hotspots live.
- [[metrics]] — the instrumentation these benchmarks read.
- [[topology-aware-scheduling]] — subject of the TAS-specific perf config.
- [[architecture]] — the cache and queue whose cost these benchmarks measure.
- [[testing]] — the developer-workflow landing page.
