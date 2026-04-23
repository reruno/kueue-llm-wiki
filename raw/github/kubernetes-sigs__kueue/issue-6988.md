# Issue #6988: [Doc] Automate updating metrics page

**Summary**: [Doc] Automate updating metrics page

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6988

**Last updated**: 2025-11-25T12:30:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-09-24T10:22:04Z
- **Updated**: 2025-11-25T12:30:41Z
- **Closed**: 2025-11-25T10:42:44Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Currently there is no updating/synchornization mechanism between what's really in the codebase and the documentation regarding metrics. E.g. there is a new metrics called `pods_ready_to_evicted_time_seconds` in the codebase but it's not documented on the website

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-24T10:32:26Z

cc @mimowo

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-01T23:15:47Z

I can try to implement that, since I was the last one who synced new labels for metrics with the docs

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-04T16:17:39Z

### Overview
- Problem: The metrics documentation in `site/content/en/docs/reference/metrics.md` can drift from the actual metrics defined in `pkg/metrics/metrics.go`. Example: `pods_ready_to_evicted_time_seconds` exists in code but is missing in docs.
- Solution: Add an automated generator that updates only the metrics tables in-place in the English documentation, bounded by explicit comment markers, sourced from the code’s metric definitions.

### Goals
- Automatically generate and update only the metrics tables in `site/content/en/docs/reference/metrics.md`.
- Preserve all non-table content and formatting in the doc.
- Keep table structure identical (columns and styling); extend content where available (multi-line descriptions via line breaks).
- Minimal integration friction: a single make target and inclusion in the existing `generate` flow.
- Provide an option to target other locales in the future (i18n-capable output path).

### Non-goals
- Do not generate the entire Markdown page; only tables.
- Do not localize or translate content automatically (English only for now).
- Do not introspect runtime metrics from external registries; only parse Kueue’s source code.

### User Experience
- Editors add comment markers in `site/content/en/docs/reference/metrics.md`. Generator replaces only the content between markers:
  - `<!-- BEGIN GENERATED TABLE: health --> ... <!-- END GENERATED TABLE: health -->`
  - `<!-- BEGIN GENERATED TABLE: clusterqueue --> ... <!-- END GENERATED TABLE: clusterqueue -->`
  - `<!-- BEGIN GENERATED TABLE: localqueue --> ... <!-- END GENERATED TABLE: localqueue -->`
  - `<!-- BEGIN GENERATED TABLE: cohort --> ... <!-- END GENERATED TABLE: cohort -->`
  - `<!-- BEGIN GENERATED TABLE: optional_clusterqueue_resources --> ... <!-- END GENERATED TABLE: optional_clusterqueue_resources -->`
  - `<!-- BEGIN GENERATED TABLE: optional_wait_for_pods_ready --> ... <!-- END GENERATED TABLE: optional_wait_for_pods_ready -->`
- Running the generator updates just these blocks; everything else remains unchanged.
- Columns preserved: Metric name | Type | Description | Labels.
- Multi-line descriptions rendered in a single cell using `<br>` for line breaks.
- Labels rendered as backticked, comma-separated names (e.g., `cluster_queue`, `reason`).

### Functional Requirements
- Parse metrics from `pkg/metrics/metrics.go`, detecting:
  - `prometheus.NewCounterVec`, `prometheus.NewGaugeVec`, `prometheus.NewHistogramVec`.
  - `Name`, `Help`, and label vector values (as defined in code).
- Generated metric name must include subsystem prefix `kueue_` (derived from code).
- Grouping into tables:
  - health: metrics with label `result` and name containing `admission_attempt`.
  - clusterqueue: default group (includes CQ status and scheduling metrics).
  - localqueue: metrics with labels containing both `name` and `namespace`.
  - cohort: metrics with `cohort` label.
  - optional_clusterqueue_resources: names starting with `cluster_queue_resource_` or equal to `cluster_queue_nominal_quota`, `cluster_queue_borrowing_limit`, `cluster_queue_lending_limit`, `cluster_queue_weighted_share`.
  - optional_wait_for_pods_ready: names `ready_wait_time_seconds`, `admitted_until_ready_wait_time_seconds`, `local_queue_ready_wait_time_seconds`, `local_queue_admitted_until_ready_wait_time_seconds`.
- Sorting: metrics listed alphabetically by full metric name within each table.
- Replacement semantics:
  - If marker blocks exist, replace contents between them.
  - If markers are missing, do nothing (no accidental overwrite).
- CLI:
  - `--metrics-file` default `pkg/metrics/metrics.go`.
  - `--out` default `site/content/en/docs/reference/metrics.md`.
- Make integration:
  - `make generate-metrics-tables` runs the tool.
  - Include in `make generate` so tables stay fresh during regular generation.
- Idempotency: running generator twice yields no diff if no code changes.

### Technical Approach
- Implement a small Go tool at `hack/metricsdoc/main.go` using `go/ast`:
  - Walk const/var specs to find metric declarations created via `prometheus.New*Vec`.
  - Extract `Name`, `Help`, and label list from `HistogramOpts`/`CounterOpts`/`GaugeOpts` and the label vector argument.
  - Handle string literals and concatenations (raw strings and `+`).
- Rendering:
  - Build groups per rules above.
  - Generate Markdown tables with four columns; convert newlines in `Help` to `<br>`; backtick labels.
- In-place file update:
  - Find each marker block by regex; replace block with newly rendered table.
- Makefile:
  - Add `generate-metrics-tables` target invoking `go run ./hack/metricsdoc --metrics-file=pkg/metrics/metrics.go --out=site/content/en/docs/reference/metrics.md`.
  - Append target to existing `generate` aggregate.
- CI (optional initial scope):
  - Verify step can run generator and fail if diffs exist to ensure sync.

### Documentation Changes
- Insert the six marker pairs at the appropriate locations in `site/content/en/docs/reference/metrics.md` (directly around the current tables).
- Add a note for maintainers: “Do not edit between BEGIN/END GENERATED TABLE markers; generated by `make generate-metrics-tables`.”
- Optionally, add a brief note in `CONTRIBUTING.md` about updating metrics docs.

### Acceptance Criteria
- After running `make generate-metrics-tables`, `site/content/en/docs/reference/metrics.md` includes current metrics:
  - `kueue_pods_ready_to_evicted_time_seconds` appears with correct type, description, and labels.
- Only the content between marker comments is modified; headings and prose are preserved.
- Removing or renaming a metric in `pkg/metrics/metrics.go` updates the corresponding table accordingly.
- Re-running the generator without code changes produces no diff (idempotent).
- English docs only are modified; other locales remain untouched.

### Edge Cases and Constraints
- Multi-line `Help` strings and concatenations are supported.
- If metrics are split across files in the future, the tool supports overriding `--metrics-file`; multi-file parsing is a future enhancement.
- If a metric doesn’t match any grouping rule, it falls back to `clusterqueue`.

### Risks and Mitigations
- Parsing assumptions may break if metrics stop using `prometheus.NewVec` or move to dynamic constructs.
  - Mitigation: keep Kueue metrics defined via literal opts and label slices; adjust parser if structure changes.
- Editors might accidentally delete markers.
  - Mitigation: generator is no-op without markers; verify in CI.

### Future Enhancements
- Multi-file support (discover all metrics definitions in `pkg/metrics`).
- Emit per-locale tables by running with different `--out` and translation workflows.
- Optional columns: metric stability, feature gate flags, buckets (not required now).

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-06T08:37:16Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-08T20:26:33Z

That's how it's done in core kubernetes: https://github.com/kubernetes/kubernetes/blob/ddc2c5d192275207b7ebb43b066fd0b0e94fc011/test/instrumentation/documentation/main.go#L4

But since they wrap every metric in their custom struct, we cannot use this app

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T17:25:31Z

> But since they wrap every metric in their custom struct, we cannot use this app

can you elaborate what it means "custom struct", and where is the wrapping?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-13T17:54:38Z

For example, this is what's used for histogram: https://github.com/kubernetes/kubernetes/blob/095b9d6045cc2d3f1a2ae9ae23b9644c55aaf594/staging/src/k8s.io/component-base/metrics/opts.go#L171
This is the usage: https://github.com/kubernetes/kubernetes/blob/095b9d6045cc2d3f1a2ae9ae23b9644c55aaf594/pkg/volume/util/metrics.go#L47

[This script](https://github.com/kubernetes/kubernetes/blob/095b9d6045cc2d3f1a2ae9ae23b9644c55aaf594/test/instrumentation/stability-utils.sh#L150) is used to look for [histograms](https://github.com/kubernetes/kubernetes/blob/095b9d6045cc2d3f1a2ae9ae23b9644c55aaf594/staging/src/k8s.io/component-base/metrics/opts.go#L171) (from the first reference), and other types and store them to yaml file, from which docs are then generated

So the script is looking for metric components which are defined in https://github.com/kubernetes/kubernetes/blob/095b9d6045cc2d3f1a2ae9ae23b9644c55aaf594/staging/src/k8s.io/component-base/metrics/opts.go which we don't use

By wrapping, I mean that they convert these structs to prometheus https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/component-base/metrics/opts.go#L203

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T18:02:01Z

Thank you for the summary, so IIUC the reason is that the script is used specifically used in the core k8s core to define metrics, and in Kueue we use different types. 

So, my follow up question, could we refactor the types used by Kueue to define metrics so that we can use the same script from them? Yes, this can generate extra effort for refactoring, but maybe worth to align. PTAL.

> This script is used to look for histograms (from the first reference), and other types and store them to yaml file, from which docs are then generated

So, IIUC there are two steps:
1. generate the yaml file from the *go files with the metrics specifications
2. load the yaml file and generate documentation

As you mentioned above doing (1.) with the script is tricky as different types are used, but maybe we could use it at least for the (2.) ?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-10-13T18:13:56Z

> So, my follow up question, could we refactor the types used by Kueue to define metrics so that we can use the same script from them?

I'm not sure that we want to group metrics as they do (stable, alpha, beta), we probably want our own groups

> As you mentioned above doing (1.) with the script is tricky as different types are used, but maybe we could use it at least for the (2.) ?

[Here's the script that generated the markdown file](https://github.com/kubernetes/kubernetes/blob/095b9d6045cc2d3f1a2ae9ae23b9644c55aaf594/test/instrumentation/documentation/main.go#L4). It has a hard-coded template, which we also want to adjust (with our groups and additional information). So that's why we also cannot use option 2

What we can still do is to refactor the app to add our groups to each metric, maybe some other info as well. Here I'm not sure if it's worth the cost, or it's better to maintain the grouping in the app which generates documentation

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T18:16:18Z

> I'm not sure that we want to group metrics as they do (stable, alpha, beta), we probably want our own groups

Using the same grouping seems reasonable to me, I wouldn't consider this as a blocker.

@tenzen-y do you maybe remember why in Kueue we use different API to define metrics than in the core k8s?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T07:13:54Z

In any case I'm ok with the approach approach implemented in https://github.com/kubernetes-sigs/kueue/pull/7211#issuecomment-3404909907. I would like to have another pair of eyes on the decision, and if all conclude reusing k8s scripting is not feasible then I ok to move forward the PR.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-25T12:30:41Z

> > I'm not sure that we want to group metrics as they do (stable, alpha, beta), we probably want our own groups
> 
> Using the same grouping seems reasonable to me, I wouldn't consider this as a blocker.
> 
> [@tenzen-y](https://github.com/tenzen-y) do you maybe remember why in Kueue we use different API to define metrics than in the core k8s?

Uhmm... Unfortunatelly, I didn't remember that...
