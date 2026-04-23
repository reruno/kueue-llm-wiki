# Issue #8586: Logging: some logging does not conform to JSON lines format

**Summary**: Logging: some logging does not conform to JSON lines format

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8586

**Last updated**: 2026-04-01T11:29:22Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-14T12:54:29Z
- **Updated**: 2026-04-01T11:29:22Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 10

## Description

**What happened**:

Some logging does not conform to JSON format. 

**What you expected to happen**:

I would like all the logging, at least down to V6, to be consistent with JSON formatting.

This is so that we can use standard JSON tooling for parsing. 

**How to reproduce it (as minimally and precisely as possible)**:

What I did I looked at the logs from integration tests at v3, eg: https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/2011334372992487424/build-log.txt

Then I found with some scripting problematic lines, examples:

```
2026-01-14T07:18:19.675323116Z	DEBUG	events	recorder/recorder.go:104	Quota reserved in ClusterQueue prod-cq, wait time since queued was 1s; Flavors considered: main: spot-tainted(NoFit;untolerated taint {cloud.provider.com/instance spot-tainted NoSchedule <nil>} in flavor spot-tainted)	{"type": "Normal", "object": {"kind":"Workload","namespace":"core-tl7wn","name":"job-prod-job1-e9458","uid":"61f0e5dc-2adc-43a4-a37b-ab4eaad0d455","apiVersion":"kueue.x-k8s.io/v1beta2","resourceVersion":"831"}, "reason": "QuotaReserved"}
```
However, this is just for v3, we should repeat this experiment for v6.

**Anything else we need to know?**:

This is the python script I used to process the log:

```python
import sys
import re

def process_logs():
    # ^\s* allows for any amount of leading whitespace
    # \d{4}-\d{2}-\d{2} matches the YYYY-MM-DD date format
    date_pattern = re.compile(r"^\s*\d{4}-\d{2}-\d{2}")
    for line in sys.stdin:
        clean_line = line.rstrip()      
        if not clean_line:
            continue
        if not date_pattern.match(clean_line):
            continue
        index = clean_line.find('{')
        
        if index != -1:
            json_payload = clean_line[index:]
            print(json_payload)

if __name__ == "__main__":
    try:
        process_logs()
    except (KeyboardInterrupt, BrokenPipeError):
        sys.stderr.close()
        sys.exit(0)
```
Then I used https://jsonlines.org/validator/ to find examples of invalid JSON lines.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T12:54:52Z

cc @mwielgus @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:30:20Z

/priority important-soon

### Comment by [@Piyushkhobragade](https://github.com/Piyushkhobragade) — 2026-01-15T16:00:41Z

Hi @mimowo,

Thanks for the detailed report and examples.

I’d like to work on this issue. I’ll start by identifying log statements that mix free text with structured fields and fix them to ensure JSON-lines compliant logging (at least up to v6), based on the CI log examples you shared.

I’ll update here with findings or questions.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T16:04:12Z

Awwsome, thank you, please assign yourself to the issue

### Comment by [@Piyushkhobragade](https://github.com/Piyushkhobragade) — 2026-01-15T16:49:48Z

I found a concrete instance of non-JSON logging in pkg/scheduler/fair_sharing_iterator.go, specifically in logDrsValuesWhenVerbose, where fmt.Sprintf is used to serialize DRS values into strings.

I’m working on fixing this by switching to structured logging fields so the output conforms to JSON lines. I’ll follow the same logging conventions used elsewhere in the project.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T17:46:05Z

To get the more or less complete list of such values you may open a PR with logging level at V6, probably here: https://github.com/kubernetes-sigs/kueue/blob/8269991262613c39d6ad96aaeeb182129ee3b4d6/Makefile-test.mk#L24

Then grab the logs from artifacts and analyze similarly as I did

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T13:30:27Z

@Piyushkhobragade what is the status for the issue? Were you able to identify more of the problematic logs using v6? I think one idea is to just create PR with increased logs, and look at the artifacts.

### Comment by [@Piyushkhobragade](https://github.com/Piyushkhobragade) — 2026-01-30T02:27:56Z

Hi @mimowo,

Thanks for the follow-up.

I’ve opened an initial PR fixing one concrete instance of non–JSON-lines logging in the scheduler path (cohort-less ClusterQueue case):
https://github.com/kubernetes-sigs/kueue/pull/8880

I’m taking an incremental approach: converting individual problematic log statements to structured logging based on what shows up with V6 verbosity, keeping each PR small and focused.

Next, I’ll continue analyzing V6 integration test artifacts to identify additional cases and follow up with more targeted PRs. Please let me know if you’d prefer a different scope or grouping.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-01T10:36:00Z

@Piyushkhobragad any progress on that?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-01T11:29:21Z

@Piyushkhobragade , sorry I made a typo in the GH handle, so sending another message
cc @mwielgus who I think may be interested in the issue
