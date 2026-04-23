# Issue #8848: Add support for OTLP metrics export

**Summary**: Add support for OTLP metrics export

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8848

**Last updated**: 2026-04-21T10:17:39Z

---

## Metadata

- **State**: open
- **Author**: [@kimminw00](https://github.com/kimminw00)
- **Created**: 2026-01-28T07:04:25Z
- **Updated**: 2026-04-21T10:17:39Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@yashnib](https://github.com/yashnib)
- **Comments**: 5

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
