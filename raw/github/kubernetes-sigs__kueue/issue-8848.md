# Issue #8848: Add support for OTLP metrics export

**Summary**: Add support for OTLP metrics export

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8848

**Last updated**: 2026-05-02T14:36:56Z

---

## Metadata

- **State**: open
- **Author**: [@kimminw00](https://github.com/kimminw00)
- **Created**: 2026-01-28T07:04:25Z
- **Updated**: 2026-05-02T14:36:56Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@yashnib](https://github.com/yashnib)
- **Comments**: 15

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to request support for exporting Kueue metrics via the **OpenTelemetry Protocol (OTLP)**.

Currently, Kueue only supports exposing metrics via the Prometheus format (pull model). I propose adding an option to configure an OTLP exporter so that Kueue can directly **push** metrics to an OpenTelemetry Collector or other OTLP-compatible backends.

**Why is this needed**:

While Prometheus is widely used, relying solely on the pull-based model has limitations in certain environments. OTLP support is needed for the following reasons:

1.  **Push-based Architecture**: In environments with strict network policies (e.g., firewalls preventing inbound scraping) or complex mesh setups, pushing metrics via OTLP is often easier to manage than configuring Prometheus scrapers.
2.  **Ecosystem Compatibility**: OpenTelemetry is the de-facto standard for observability. OTLP support allows users to integrate Kueue with a wide range of tools and OTel Collectors.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [X] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T14:43:45Z

This sounds great @kimminw00 ! Do you know if there are some projects in the k8s ecosystem which already support OTLP we could use for guiding the decisions for implementation? For example what libraries to use, what are the useful config params etc.

### Comment by [@yashnib](https://github.com/yashnib) — 2026-02-09T04:07:43Z

@mimowo One Kubernetes-native prior art we can use is **Kubernetes system component tracing**. K8s components emit telemetry via **OTLP over gRPC** and recommend routing through an **OpenTelemetry Collector** (Collector as the aggregation point, rather than pushing directly to arbitrary vendor backends). This is traces rather than metrics, but it’s a strong reference for the *shape* of configuration we could follow in Kueue: specify an OTLP endpoint and choose secure transport (TLS vs insecure). 

From an implementation standpoint, this aligns well with using the standard OpenTelemetry Go exporters. For traces, the OTLP gRPC exporter is `go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc` (and K8s has its own wrappers under `k8s.io/component-base/...` for tracing setup). For Kueue *metrics* export, the analogous library would be the OTLP metrics gRPC exporter: `go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc` (or the HTTP/protobuf exporter if we choose HTTP).

### Comment by [@yashnib](https://github.com/yashnib) — 2026-02-12T03:08:05Z

I can think of adding OTLP metrics export in two ways: (1) **bridge the existing Prometheus registry** (lowest-churn, since Kueue/controller-runtime already registers metrics there) or (2) **migrate to OTel-native instruments** (cleaner long-term, but a larger change). For an MVP, I’d suggest the bridging approach to minimize risk and review surface, while keeping the door open to a native OTel metrics path later.

I’d be happy to put together a KEP to discuss the design, API/config surface, and failure-mode semantics.

### Comment by [@yashnib](https://github.com/yashnib) — 2026-02-16T03:00:34Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-21T06:44:00Z

@yashnib @kimminw00 any progress here? I think the starting point should be KEP, probably with some prototype. 

Do you also know if using the new strategy is more performant when it comes to high cardinality metrics? I'm wondering if this could be used for metrics per workload or per pod (200k+ rows in the standard fomat), wdyt?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-30T17:05:48Z

x-referncing a PR which seems to go in that direction: https://github.com/kubernetes-sigs/kueue/pull/10818

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-04-30T19:01:29Z

> Do you also know if using the new strategy is more performant when it comes to high cardinality metrics

@mimowo Push vs pull doesn’t inherently solve high cardinality performance issues. The bottleneck is usually cardinality itself, not the transport model.

When OpenTelemetry can feel more performant
It’s not the push model—it’s that you typically:
- Use a collector
- Pre-aggregate or filter metrics
- Control export frequency

That pipeline makes high-cardinality workloads more manageable.

### Comment by [@kimminw00](https://github.com/kimminw00) — 2026-05-01T04:03:16Z

> Do you also know if using the new strategy is more performant when it comes to high cardinality metrics? I'm wondering if this could be used for metrics per workload or per pod (200k+ rows in the standard fomat), wdyt?

@mimowo Using OTLP with OTel Collector is much more performant for high-cardinality metrics (200k+ series).

Prometheus forces clients to keep full state for every unique label combination, quickly leading to high memory usage and OOM risk with per-workload or per-pod metrics.

OTel handles this far better:

- Delta temporality: Clients only send changes and can immediately forget state → dramatically lower memory footprint.
- Intelligent edge processing: With `k8sattributes` processor, we can attach stable context (namespace, workload) while dropping or aggregating noisy high-cardinality labels (pod.name, pod.uid, etc.) before export.

Reference: [High Cardinality with OpenTelemetry](https://last9.io/guides/high-cardinality/opentelemetry-and-modern-tooling-for-high-cardinality/#high-cardinality-without-compromise)

### Comment by [@kimminw00](https://github.com/kimminw00) — 2026-05-01T04:35:26Z

@yashnib, would it be okay if I draft the KEP instead?

I think the KEP should focus on Kueue-specific **metrics and traces** for OpenTelemetry support.

[Zero-code instrumentation](https://opentelemetry.io/docs/zero-code/) is useful for generic application telemetry, but it cannot fully describe Kueue-specific semantics such as queueing, admission decisions, quota reservation, resource flavor usage, or Workload lifecycle transitions.

So the KEP should define the explicit implementation needed in Kueue, especially OTLP export for Kueue **metrics and traces** around reconciliation, scheduling, admission, and Workload state changes.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-05-01T04:51:18Z

> So the KEP should define the explicit implementation needed in Kueue, especially OTLP export for Kueue metrics and semantic traces around reconciliation, scheduling, admission, and Workload state changes.

Does this mean that we can support all Kueue Prometheus metrics by OTel?

### Comment by [@kimminw00](https://github.com/kimminw00) — 2026-05-01T06:47:01Z

Yes, we can support all existing Kueue Prometheus metrics with OTEL.

In my opinion, we should support both Prometheus and OpenTelemetry as selectable options, so users can choose one depending on their needs.

Prometheus mode: Keep the existing metric names unchanged for full backward compatibility. (kueue_admission_attempts_total, kueue_pending_workloads, etc.)
OTEL mode: Provide the same metrics using [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/general/metrics/) (kueue.admission.attempts.total, kueue.workload.pending, etc.).

This approach gives users flexibility while protecting existing monitoring setups.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-05-01T07:09:02Z

> Yes, we can support all existing Kueue Prometheus metrics with OTEL.
> 
> In my opinion, we should support both Prometheus and OpenTelemetry as selectable options, so users can choose one or both depending on their needs.
> 
> Prometheus mode: Keep the existing metric names unchanged for full backward compatibility. (kueue_admission_attempts_total, kueue_pending_workloads, etc.) OTEL mode: Provide the same metrics using [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/general/metrics/) (kueue.admission.attempts.total, kueue.workload.pending, etc.).
> 
> This approach gives users flexibility while protecting existing monitoring setups.

Thank you for letting us know! Yes, I fully agree with providing both metrics, and they can select a comfortable way.
I imagine that we have a knob for metrics type in https://github.com/kubernetes-sigs/kueue/blob/04ca5992887eef596352c852eff9c6ff36204313/apis/config/v1beta2/configuration_types.go#L174.

An additional question is how to propagate controller-runtime provided metrics via OTel. Because Kueue dedicated metrics easily migrate to OTel format, but controller-runtime and client-go provided ones are not managed by this repository.

Any plan?

### Comment by [@kimminw00](https://github.com/kimminw00) — 2026-05-01T09:36:29Z

For dependency-provided metrics such as controller-runtime and client-go metrics, I think the safer approach is to keep the existing Prometheus endpoint and convert them through the OpenTelemetry Collector.

Users can configure a `PrometheusReceiver` to scrape the existing /metrics endpoint and an `OTLPExporter` to forward those metrics in OTLP format.

I also considered the in-process bridge approach, but I prefer the Collector-based approach so that Kueue does not need to manage dependency-provided metrics directly.

If these dependencies support direct OTLP export in the future, we can revisit this and simplify the pipeline.

Does this approach sound reasonable?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-05-01T18:18:19Z

> In my opinion, we should support both Prometheus and OpenTelemetry as selectable options, so users can choose one depending on their needs.
Prometheus mode: Keep the existing metric names unchanged for full backward compatibility. (kueue_admission_attempts_total, kueue_pending_workloads, etc.)

I think there should even be a possibility to convert all existing metrics to OTEL ones, then just configure the OTEL metric exporter (on code level) the way it's compatible with current Prometheus set up, so there's no need to support both libs, and this way we can work on each individual metric standalone

### Comment by [@kimminw00](https://github.com/kimminw00) — 2026-05-02T00:26:31Z

> I think there should even be a possibility to convert all existing metrics to OTEL ones, then just configure the OTEL metric exporter (on code level) the way it's compatible with current Prometheus set up, so there's no need to support both libs, and this way we can work on each individual metric standalone

I understand the suggestion as making OpenTelemetry metrics the primary implementation, and then using the [OTel Prometheus exporter](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/) to keep compatibility with the current Prometheus setup.

That sounds like a good direction especially for Kueue-owned metrics, because it could avoid maintaining both Prometheus and OTel instrumentation.

We could also make the exporter configurable, so users can choose either the [Prometheus exporter](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/) or the [OTLP exporter](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/otlp/) depending on their observability setup.
