# Issue #5420: [YAML Processor] Does not exist warnings

**Summary**: [YAML Processor] Does not exist warnings

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5420

**Last updated**: 2025-05-30T16:28:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-05-30T08:01:53Z
- **Updated**: 2025-05-30T16:28:20Z
- **Closed**: 2025-05-30T16:28:20Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We get a lot of warnings when running `make update-helm`.

```
2025-05-30T06:21:10.609Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/batch_admin_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.609Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/batch_admin_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.610Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/batch_admin_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.610Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/batch_admin_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.610Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/batch_admin_role.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.613Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/batch_user_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.614Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/batch_user_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.614Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/batch_user_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.615Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/batch_user_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.615Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/batch_user_role.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.618Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/clusterqueue_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.618Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/clusterqueue_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.619Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/clusterqueue_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.619Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/clusterqueue_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.620Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/clusterqueue_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.627Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/clusterqueue_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.628Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/clusterqueue_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.628Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/clusterqueue_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.628Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/clusterqueue_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.629Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/clusterqueue_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.633Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/jaxjob_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.633Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/jaxjob_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.634Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/jaxjob_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.634Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/jaxjob_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.635Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/jaxjob_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.641Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/jaxjob_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.641Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/jaxjob_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.642Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/jaxjob_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.642Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/jaxjob_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.643Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/jaxjob_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.648Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/job_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.649Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/job_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.650Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/job_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.650Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/job_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.651Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/job_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.654Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/job_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.656Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/job_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.657Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/job_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.657Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/job_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.658Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/job_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.669Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/jobset_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.670Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/jobset_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.671Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/jobset_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.671Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/jobset_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.672Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/jobset_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.687Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/jobset_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.687Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/jobset_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.688Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/jobset_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.688Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/jobset_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.689Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/jobset_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.725Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/leader_election_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.726Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/leader_election_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.727Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/leader_election_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.727Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/leader_election_role.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.741Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/leader_election_role_binding.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.743Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/localqueue_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.744Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/localqueue_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.744Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/localqueue_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.746Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/localqueue_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.747Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/localqueue_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.750Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/localqueue_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.750Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/localqueue_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.751Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/localqueue_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.752Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/localqueue_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.753Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/localqueue_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.756Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/metrics_auth_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.756Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/metrics_auth_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.757Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/metrics_auth_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.757Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/metrics_auth_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.757Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/metrics_auth_role.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.762Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/metrics_auth_role_binding.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.767Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/metrics_auth_role_binding.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.770Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/metrics_reader_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.770Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/metrics_reader_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.771Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/metrics_reader_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.771Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/metrics_reader_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.771Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/metrics_reader_role.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.774Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/mpijob_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.775Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/mpijob_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.775Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/mpijob_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.776Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/mpijob_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.777Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/mpijob_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.784Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/mpijob_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.785Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/mpijob_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.785Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/mpijob_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.786Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/mpijob_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.786Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/mpijob_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.789Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/paddlejob_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.790Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/paddlejob_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.791Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/paddlejob_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.791Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/paddlejob_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.792Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/paddlejob_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.796Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/paddlejob_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.797Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/paddlejob_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.798Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/paddlejob_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.798Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/paddlejob_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.799Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/paddlejob_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.801Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/pending_workloads_cq_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.802Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/pending_workloads_cq_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.802Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/pending_workloads_cq_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.803Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/pending_workloads_cq_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.803Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/pending_workloads_cq_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.807Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/pending_workloads_lq_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.807Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/pending_workloads_lq_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.809Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/pending_workloads_lq_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.809Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/pending_workloads_lq_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.810Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/pending_workloads_lq_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.815Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/pytorchjob_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.816Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/pytorchjob_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.817Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/pytorchjob_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.818Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/pytorchjob_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.819Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/pytorchjob_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.823Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/pytorchjob_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.823Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/pytorchjob_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.824Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/pytorchjob_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.824Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/pytorchjob_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.825Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/pytorchjob_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.834Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/raycluster_editor_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.835Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/raycluster_editor_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.836Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/raycluster_editor_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.836Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/raycluster_editor_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.837Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/raycluster_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.840Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/raycluster_viewer_role.yaml", "error": "key '.metadata.namespace' does not exist"}
2025-05-30T06:21:10.842Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/raycluster_viewer_role.yaml", "error": "key '.roleRef.name' does not exist"}
2025-05-30T06:21:10.842Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/rbac/raycluster_viewer_role.yaml", "error": "key '.subjects.[].name' does not exist"}
2025-05-30T06:21:10.843Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/rbac/raycluster_viewer_role.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:10.844Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/raycluster_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.849Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/rayjob_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.854Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/rayjob_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.860Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/resourceflavor_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.864Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/resourceflavor_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.886Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/role.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.899Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/role_binding.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.902Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/service_account.yaml", "error": "condition '.metadata.labels != null' not met"}
2025-05-30T06:21:10.908Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/tfjob_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.912Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/tfjob_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.918Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/topology_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.925Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/topology_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.930Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/workload_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.935Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/workload_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.939Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/xgboostjob_editor_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.948Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/rbac/xgboostjob_viewer_role.yaml", "error": "condition '.metadata.labels == null' not met"}
2025-05-30T06:21:10.953Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/visibility/apiservice_v1beta1.yaml", "error": "condition '.kind == \"Service\"' not met"}
2025-05-30T06:21:10.961Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "config/components/visibility/role_binding.yaml", "error": "condition '.kind == \"Service\"' not met"}
2025-05-30T06:21:11.105Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.118Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.122Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.125Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.128Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.131Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.133Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.135Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.140Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.143Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.145Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.147Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.150Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.153Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.183Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"ValidatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.494Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.496Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.501Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.506Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.543Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.545Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.548Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.550Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.555Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.557Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.560Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.562Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.564Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.567Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.569Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.571Z	warn	yamlproc/processor.go:232	Skipping post operation	{"operation": "INSERT_TEXT", "file": "./config/components/webhook/manifests.yaml", "error": "condition '.kind == \"MutatingWebhookConfiguration\"' not met"}
2025-05-30T06:21:11.817Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/backend-deployment.yaml", "error": "condition '.metadata.name == \"kueueviz-frontend\"' not met"}
2025-05-30T06:21:11.819Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/backend-deployment.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.820Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/backend-deployment.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.820Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/backend-deployment.yaml", "error": "condition '.kind == \"ClusterRoleBinding\"' not met"}
2025-05-30T06:21:11.821Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/backend-deployment.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:11.824Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/backend-ingress.yaml", "error": "condition '.metadata.name == \"kueueviz-backend\"' not met"}
2025-05-30T06:21:11.825Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/backend-ingress.yaml", "error": "condition '.metadata.name == \"kueueviz-frontend\"' not met"}
2025-05-30T06:21:11.829Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/backend-ingress.yaml", "error": "condition '.kind == \"ClusterRoleBinding\"' not met"}
2025-05-30T06:21:11.830Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/backend-ingress.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:11.832Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/backend-service.yaml", "error": "key '.spec.template.spec.containers[0].image' does not exist"}
2025-05-30T06:21:11.833Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/backend-service.yaml", "error": "condition '.metadata.name == \"kueueviz-frontend\"' not met"}
2025-05-30T06:21:11.834Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/backend-service.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.835Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/backend-service.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.840Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/backend-service.yaml", "error": "condition '.kind == \"ClusterRoleBinding\"' not met"}
2025-05-30T06:21:11.840Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/backend-service.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:11.842Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/cluster-role-binding.yaml", "error": "condition '.metadata.name == \"kueueviz-backend\"' not met"}
2025-05-30T06:21:11.842Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/cluster-role-binding.yaml", "error": "condition '.metadata.name == \"kueueviz-frontend\"' not met"}
2025-05-30T06:21:11.844Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/cluster-role-binding.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.844Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/cluster-role-binding.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.848Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/clusterrole.yaml", "error": "condition '.metadata.name == \"kueueviz-backend\"' not met"}
2025-05-30T06:21:11.850Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/clusterrole.yaml", "error": "condition '.metadata.name == \"kueueviz-frontend\"' not met"}
2025-05-30T06:21:11.852Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/clusterrole.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.853Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/clusterrole.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.853Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/clusterrole.yaml", "error": "condition '.kind == \"ClusterRoleBinding\"' not met"}
2025-05-30T06:21:11.854Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/clusterrole.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:11.856Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/frontend-deployment.yaml", "error": "condition '.metadata.name == \"kueueviz-backend\"' not met"}
2025-05-30T06:21:11.860Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/frontend-deployment.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.861Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/frontend-deployment.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.861Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/frontend-deployment.yaml", "error": "condition '.kind == \"ClusterRoleBinding\"' not met"}
2025-05-30T06:21:11.862Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/frontend-deployment.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:11.866Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/frontend-ingress.yaml", "error": "condition '.metadata.name == \"kueueviz-backend\"' not met"}
2025-05-30T06:21:11.866Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/frontend-ingress.yaml", "error": "condition '.metadata.name == \"kueueviz-frontend\"' not met"}
2025-05-30T06:21:11.871Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/frontend-ingress.yaml", "error": "condition '.kind == \"ClusterRoleBinding\"' not met"}
2025-05-30T06:21:11.872Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/frontend-ingress.yaml", "error": "key '.subjects.[].namespace' does not exist"}
2025-05-30T06:21:11.874Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/frontend-service.yaml", "error": "condition '.metadata.name == \"kueueviz-backend\"' not met"}
2025-05-30T06:21:11.875Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/frontend-service.yaml", "error": "key '.spec.template.spec.containers[0].image' does not exist"}
2025-05-30T06:21:11.876Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/frontend-service.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.876Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/frontend-service.yaml", "error": "condition '.kind == \"Ingress\"' not met"}
2025-05-30T06:21:11.877Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "APPEND", "file": "config/components/kueueviz/frontend-service.yaml", "error": "condition '.kind == \"ClusterRoleBinding\"' not met"}
2025-05-30T06:21:11.878Z	warn	yamlproc/processor.go:195	Skipping operation	{"operation": "UPDATE", "file": "config/components/kueueviz/frontend-service.yaml", "error": "key '.subjects.[].namespace' does not exist"}
```

**Why is this needed**:

Avoid showing unnecessary warnings.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-30T08:02:10Z

cc @IrvingMg

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-30T10:52:42Z

/assign
