# Issue #8733: [Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale down LeaderReadyStartupPolicy

**Summary**: [Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale down LeaderReadyStartupPolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8733

**Last updated**: 2026-01-30T08:26:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-22T05:01:03Z
- **Updated**: 2026-01-30T08:26:00Z
- **Closed**: 2026-01-30T08:25:59Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

End To End Suite: kindest/node:v1.33.7: [It] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale down LeaderReadyStartupPolicy [area:singlecluster, feature:leaderworkerset]

```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:401 with:
Expected
    <[]v1.Pod | len:1, cap:1>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-1",
                GenerateName: "lws-",
                Namespace: "lws-e2e-kxs58",
                SelfLink: "",
                UID: "2e00ca28-c0a8-4163-b2eb-401eb3e28ada",
                ResourceVersion: "7408",
                Generation: 3,
                CreationTimestamp: {
                    Time: 2026-01-22T04:44:12Z,
                },
                DeletionTimestamp: {
                    Time: 2026-01-22T04:44:16Z,
                },
                DeletionGracePeriodSeconds: 0,
                Labels: {
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/queue-name": "lws-lq-lws-e2e-kxs58",
                    "leaderworkerset.sigs.k8s.io/group-index": "1",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "statefulset.kubernetes.io/pod-name": "lws-1",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-1-617bf",
                    "leaderworkerset.sigs.k8s.io/group-key": "ab78cb5390af86053cda5b5fbad00c73773216e3",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "855d744646",
                    "apps.kubernetes.io/pod-index": "1",
                    "controller-revision-hash": "lws-99c4ff976",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-1-617bf",
                },
                Annotations: {
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-1-617bf",
                    "leaderworkerset.sigs.k8s.io/size": "3",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "fa42f1dd-d424-4851-941b-ff313b6985ec",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: ["foregroundDeletion"],
                ManagedFields: [
                    {
                        Manager: "kueue",
                        Operation: "Apply",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-01-22T04:44:14Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"TerminationTarget\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:message\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}}}}}",
                        },
                        Subresource: "status",
                    },
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-01-22T04:44:12Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"fa42f1dd-d424-4851-941b-ff313b6985ec\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomain\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-01-22T04:44:12Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\"f:kueue.x-k8s.io/pod-group-total-count\":{},\"f:kueue.x-k8s.io/role-hash\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:labels\":{\"f:kueue.x-k8s.io/managed\":{},\"f:kueue.x-k8s.io/pod-group-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/prebuilt-workload-name\":{},\"f:kueue.x-k8s.io/queue-name\":{}}},\"f:spec\":{\"f:nodeSelector\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-01-22T04:44:15Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}}},\"f:containerStatuses\":{},\"f:hostIP\":{},\"f:hostIPs\":{},\"f:phase\":{},\"f:podIP\":{},\"f:podIPs\":{\".\":{},\"k:{\\\"ip\\\":\\\"10.244.2.80\\\"}\":{\".\":{},\"f:ip\":{}}},\"f:startTime\":{}}}",
                        },
                        Subresource: "status",
                    },
                ],
            },
            Spec: {
                Volumes: [
                    {
                        Name: "kube-api-access-wb522",
                        VolumeSource: {
                            HostPath: nil,
                            EmptyDir: nil,
                            GCEPersistentDisk: nil,
                            AWSElasticBlockStore: nil,
                            GitRepo: nil,
                            Secret: nil,
                            NFS: nil,
                            ISCSI: nil,
                            Glusterfs: nil,
                            PersistentVolumeClaim: nil,
                            RBD: nil,
                            FlexVolume: nil,
                            Cinder: nil,
                            CephFS: nil,
                            Flocker: nil,
                            DownwardAPI: nil,
                            FC: nil,
                            AzureFile: nil,
                            ConfigMap: nil,
                            VsphereVolume: nil,
                            Quobyte: nil,
                            AzureDisk: nil,
                            PhotonPersistentDisk: nil,
                            Projected: {
                                Sources: [
                                    {
                                        Secret: nil,
                                        DownwardAPI: nil,
                                        ConfigMap: nil,
                                        ServiceAccountToken: {
                                            Audience: ...,
                                            ExpirationSeconds: ...,
                                            Path: ...,
                                        },
                                        ClusterTrustBundle: nil,
                                        PodCertificate: nil,
                                    },
                                    {
                                        Secret: nil,
                                        DownwardAPI: nil,
                                        ConfigMap: {
                                            LocalObjectReference: ...,
                                            Items: ...,
                                            Optional: ...,
                                        },
                                        ServiceAccountToken: nil,
                                        ClusterTrustBundle: nil,
                                        PodCertificate: nil,
                                    },
                                    {
                                        Secret: nil,
                                        DownwardAPI: {Items: ...},
                                        ConfigMap: nil,
                                        ServiceAccountToken: nil,
                                        ClusterTrustBundle: nil,
                                        PodCertificate: nil,
                                    },
                                ],
                                DefaultMode: 420,
                            },
                            PortworxVolume: nil,
                            ScaleIO: nil,
                            StorageOS: nil,
                            CSI: nil,
                            Ephemeral: nil,
                            Image: nil,
                        },
                    },
                ],
                InitContainers: nil,
                Containers: [
                    {
                        Name: "c",
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.60",
                        Command: nil,
                        Args: ["netexec"],
                        WorkingDir: "",
                        Ports: nil,
                        EnvFrom: nil,
                        Env: [
                            {
                                Name: "LWS_LEADER_ADDRESS",
                                Value: "lws-1.lws.lws-e2e-kxs58",
                                ValueFrom: nil,
                            },
                            {
                                Name: "LWS_GROUP_SIZE",
                                Value: "3",
                                ValueFrom: nil,
                            },
                            {
                                Name: "LWS_WORKER_INDEX",
                                Value: "0",
                                ValueFrom: nil,
                            },
                        ],
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 200, scale: -3},
                                    d: {Dec: nil},
                                    s: "200m",
                                    Format: "DecimalSI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 200, scale: -3},
                                    d: {Dec: nil},
                                    s: "200m",
                                    Format: "DecimalSI",
                                },
                            },
                            Claims: nil,
                        },
                        ResizePolicy: nil,
                        RestartPolicy: nil,
                        RestartPolicyRules: nil,
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-wb522",
                                ReadOnly: true,
                                RecursiveReadOnly: nil,
                                MountPath: "/var/run/secrets/kubernetes.io/serviceaccount",
                                SubPath: "",
                                MountPropagation: nil,
                                SubPathExpr: "",
                            },
                        ],
                        VolumeDevices: nil,
                        LivenessProbe: nil,
                        ReadinessProbe: nil,
                        StartupProbe: nil,
                        Lifecycle: nil,
                        TerminationMessagePath: "/dev/termination-log",
                        TerminationMessagePolicy: "File",
                        ImagePullPolicy: "IfNotPresent",
                        SecurityContext: nil,
                        Stdin: false,
                        StdinOnce: false,
                        TTY: false,
                    },
                ],
                EphemeralContainers: nil,
                RestartPolicy: "Always",
                TerminationGracePeriodSeconds: 1,
                ActiveDeadlineSeconds: nil,
                DNSPolicy: "ClusterFirst",
                NodeSelector: {
                    "instance-type": "on-demand",
                },
                ServiceAccountName: "default",
                DeprecatedServiceAccount: "default",
                AutomountServiceAccountToken: nil,
                NodeName: "kind-worker",
                HostNetwork: false,
                HostPID: false,
                HostIPC: false,
                ShareProcessNamespace: nil,
                SecurityContext: {
                    SELinuxOptions: nil,
                    WindowsOptions: nil,
                    RunAsUser: nil,
                    RunAsGroup: nil,
                    RunAsNonRoot: nil,
                    SupplementalGroups: nil,
                    SupplementalGroupsPolicy: nil,
                    FSGroup: nil,
                    Sysctls: nil,
                    FSGroupChangePolicy: nil,
                    SeccompProfile: nil,
                    AppArmorProfile: nil,
                    SELinuxChangePolicy: nil,
                },
                ImagePullSecrets: nil,
                Hostname: "lws-1",
                Subdomain: "lws",
                Affinity: nil,
                SchedulerName: "default-scheduler",
                Tolerations: [
                    {
                        Key: "node.kubernetes.io/not-ready",
                        Operator: "Exists",
                        Value: "",
                        Effect: "NoExecute",
                        TolerationSeconds: 300,
                    },
                    {
                        Key: "node.kubernetes.io/unreachable",
                        Operator: "Exists",
                        Value: "",
                        Effect: "NoExecute",
                        TolerationSeconds: 300,
                    },
                ],
                HostAliases: nil,
                PriorityClassName: "",
                Priority: 0,
                DNSConfig: nil,
                ReadinessGates: nil,
                RuntimeClassName: nil,
                EnableServiceLinks: true,
                PreemptionPolicy: "PreemptLowerPriority",
                Overhead: nil,
                TopologySpreadConstraints: nil,
                SetHostnameAsFQDN: nil,
                OS: nil,
                HostUsers: nil,
                SchedulingGates: nil,
                ResourceClaims: nil,
                Resources: nil,
                HostnameOverride: nil,
                WorkloadRef: nil,
            },
            Status: {
                ObservedGeneration: 0,
                Phase: "Succeeded",
                Conditions: [
                    {
                        Type: "TerminationTarget",
                        ObservedGeneration: 0,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:14Z,
                        },
                        Reason: "NoMatchingWorkload",
                        Message: "missing workload",
                    },
                    {
                        Type: "PodReadyToStartContainers",
                        ObservedGeneration: 0,
                        Status: "False",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:15Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Initialized",
                        ObservedGeneration: 0,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:12Z,
                        },
                        Reason: "PodCompleted",
                        Message: "",
                    },
                    {
                        Type: "Ready",
                        ObservedGeneration: 0,
                        Status: "False",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:15Z,
                        },
                        Reason: "PodCompleted",
                        Message: "",
                    },
                    {
                        Type: "ContainersReady",
                        ObservedGeneration: 0,
                        Status: "False",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:15Z,
                        },
                        Reason: "PodCompleted",
                        Message: "",
                    },
                    {
                        Type: "PodScheduled",
                        ObservedGeneration: 0,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:12Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                ],
                Message: "",
                Reason: "",
                NominatedNodeName: "",
                HostIP: "172.18.0.3",
                HostIPs: [{IP: "172.18.0.3"}],
                PodIP: "10.244.2.80",
                PodIPs: [{IP: "10.244.2.80"}],
                StartTime: {
                    Time: 2026-01-22T04:44:12Z,
                },
                InitContainerStatuses: nil,
                ContainerStatuses: [
                    {
                        Name: "c",
                        State: {
                            Waiting: nil,
                            Running: nil,
                            Terminated: {
                                ExitCode: 0,
                                Signal: 0,
                                Reason: "Completed",
                                Message: "",
                                StartedAt: {
                                    Time: 2026-01-22T04:44:13Z,
                                },
                                FinishedAt: {
                                    Time: 2026-01-22T04:44:15Z,
                                },
                                ContainerID: "containerd://2f779c4800f5e708da239f009065e03a992b9c6baa4027684d0a2124514bb8d2",
                            },
                        },
                        LastTerminationState: {Waiting: nil, Running: nil, Terminated: nil},
                        Ready: false,
                        RestartCount: 0,
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.60",
                        ImageID: "sha256:d9b1f93401bfcf4303c130dca0890f18667239f8daf633d211f718a230604147",
                        ContainerID: "containerd://2f779c4800f5e708da239f009065e03a992b9c6baa4027684d0a2124514bb8d2",
                        Started: false,
                        AllocatedResources: {
                            "cpu": {
                                i: {value: 200, scale: -3},
                                d: {Dec: nil},
                                s: "200m",
                                Format: "DecimalSI",
                            },
                        },
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 200, scale: -3},
                                    d: {Dec: nil},
                                    s: "200m",
                                    Format: "DecimalSI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 200, scale: -3},
                                    d: {Dec: nil},
                                    s: "200m",
                                    Format: "DecimalSI",
                                },
                            },
                            Claims: nil,
                        },
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-wb522",
                                MountPath: "/var/run/secrets/kubernetes.io/serviceaccount",
                                ReadOnly: true,
                                RecursiveReadOnly: "Disabled",
                            },
                        ],
                        User: {
                            Linux: {
                                UID: 0,
                                GID: 0,
                                SupplementalGroups: [0, 1, 2, 3, 4, 6, 10, 11, 20, 26, 27],
                            },
                        },
                        AllocatedResourcesStatus: nil,
                        StopSignal: nil,
                    },
                ],
                QOSClass: "Burstable",
                EphemeralContainerStatuses: nil,
                Resize: "",
                ResourceClaimStatuses: nil,
                ExtendedResourceClaimStatus: nil,
                AllocatedResources: nil,
                Resources: nil,
            },
        },
    ]
to be empty failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:401 with:
Expected
    <[]v1.Pod | len:1, cap:1>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-1",
                GenerateName: "lws-",
                Namespace: "lws-e2e-kxs58",
                SelfLink: "",
                UID: "2e00ca28-c0a8-4163-b2eb-401eb3e28ada",
                ResourceVersion: "7408",
                Generation: 3,
                CreationTimestamp: {
                    Time: 2026-01-22T04:44:12Z,
                },
                DeletionTimestamp: {
                    Time: 2026-01-22T04:44:16Z,
                },
                DeletionGracePeriodSeconds: 0,
                Labels: {
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/queue-name": "lws-lq-lws-e2e-kxs58",
                    "leaderworkerset.sigs.k8s.io/group-index": "1",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "statefulset.kubernetes.io/pod-name": "lws-1",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-1-617bf",
                    "leaderworkerset.sigs.k8s.io/group-key": "ab78cb5390af86053cda5b5fbad00c73773216e3",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "855d744646",
                    "apps.kubernetes.io/pod-index": "1",
                    "controller-revision-hash": "lws-99c4ff976",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-1-617bf",
                },
                Annotations: {
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-1-617bf",
                    "leaderworkerset.sigs.k8s.io/size": "3",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "fa42f1dd-d424-4851-941b-ff313b6985ec",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: ["foregroundDeletion"],
                ManagedFields: [
                    {
                        Manager: "kueue",
                        Operation: "Apply",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-01-22T04:44:14Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"TerminationTarget\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:message\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}}}}}",
                        },
                        Subresource: "status",
                    },
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-01-22T04:44:12Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"fa42f1dd-d424-4851-941b-ff313b6985ec\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomain\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-01-22T04:44:12Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\"f:kueue.x-k8s.io/pod-group-total-count\":{},\"f:kueue.x-k8s.io/role-hash\":{},\"f:kueue.x-k8s.io/workload\":{}},\"f:labels\":{\"f:kueue.x-k8s.io/managed\":{},\"f:kueue.x-k8s.io/pod-group-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/prebuilt-workload-name\":{},\"f:kueue.x-k8s.io/queue-name\":{}}},\"f:spec\":{\"f:nodeSelector\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-01-22T04:44:15Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}}},\"f:containerStatuses\":{},\"f:hostIP\":{},\"f:hostIPs\":{},\"f:phase\":{},\"f:podIP\":{},\"f:podIPs\":{\".\":{},\"k:{\\\"ip\\\":\\\"10.244.2.80\\\"}\":{\".\":{},\"f:ip\":{}}},\"f:startTime\":{}}}",
                        },
                        Subresource: "status",
                    },
                ],
            },
            Spec: {
                Volumes: [
                    {
                        Name: "kube-api-access-wb522",
                        VolumeSource: {
                            HostPath: nil,
                            EmptyDir: nil,
                            GCEPersistentDisk: nil,
                            AWSElasticBlockStore: nil,
                            GitRepo: nil,
                            Secret: nil,
                            NFS: nil,
                            ISCSI: nil,
                            Glusterfs: nil,
                            PersistentVolumeClaim: nil,
                            RBD: nil,
                            FlexVolume: nil,
                            Cinder: nil,
                            CephFS: nil,
                            Flocker: nil,
                            DownwardAPI: nil,
                            FC: nil,
                            AzureFile: nil,
                            ConfigMap: nil,
                            VsphereVolume: nil,
                            Quobyte: nil,
                            AzureDisk: nil,
                            PhotonPersistentDisk: nil,
                            Projected: {
                                Sources: [
                                    {
                                        Secret: nil,
                                        DownwardAPI: nil,
                                        ConfigMap: nil,
                                        ServiceAccountToken: {
                                            Audience: ...,
                                            ExpirationSeconds: ...,
                                            Path: ...,
                                        },
                                        ClusterTrustBundle: nil,
                                        PodCertificate: nil,
                                    },
                                    {
                                        Secret: nil,
                                        DownwardAPI: nil,
                                        ConfigMap: {
                                            LocalObjectReference: ...,
                                            Items: ...,
                                            Optional: ...,
                                        },
                                        ServiceAccountToken: nil,
                                        ClusterTrustBundle: nil,
                                        PodCertificate: nil,
                                    },
                                    {
                                        Secret: nil,
                                        DownwardAPI: {Items: ...},
                                        ConfigMap: nil,
                                        ServiceAccountToken: nil,
                                        ClusterTrustBundle: nil,
                                        PodCertificate: nil,
                                    },
                                ],
                                DefaultMode: 420,
                            },
                            PortworxVolume: nil,
                            ScaleIO: nil,
                            StorageOS: nil,
                            CSI: nil,
                            Ephemeral: nil,
                            Image: nil,
                        },
                    },
                ],
                InitContainers: nil,
                Containers: [
                    {
                        Name: "c",
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.60",
                        Command: nil,
                        Args: ["netexec"],
                        WorkingDir: "",
                        Ports: nil,
                        EnvFrom: nil,
                        Env: [
                            {
                                Name: "LWS_LEADER_ADDRESS",
                                Value: "lws-1.lws.lws-e2e-kxs58",
                                ValueFrom: nil,
                            },
                            {
                                Name: "LWS_GROUP_SIZE",
                                Value: "3",
                                ValueFrom: nil,
                            },
                            {
                                Name: "LWS_WORKER_INDEX",
                                Value: "0",
                                ValueFrom: nil,
                            },
                        ],
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 200, scale: -3},
                                    d: {Dec: nil},
                                    s: "200m",
                                    Format: "DecimalSI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 200, scale: -3},
                                    d: {Dec: nil},
                                    s: "200m",
                                    Format: "DecimalSI",
                                },
                            },
                            Claims: nil,
                        },
                        ResizePolicy: nil,
                        RestartPolicy: nil,
                        RestartPolicyRules: nil,
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-wb522",
                                ReadOnly: true,
                                RecursiveReadOnly: nil,
                                MountPath: "/var/run/secrets/kubernetes.io/serviceaccount",
                                SubPath: "",
                                MountPropagation: nil,
                                SubPathExpr: "",
                            },
                        ],
                        VolumeDevices: nil,
                        LivenessProbe: nil,
                        ReadinessProbe: nil,
                        StartupProbe: nil,
                        Lifecycle: nil,
                        TerminationMessagePath: "/dev/termination-log",
                        TerminationMessagePolicy: "File",
                        ImagePullPolicy: "IfNotPresent",
                        SecurityContext: nil,
                        Stdin: false,
                        StdinOnce: false,
                        TTY: false,
                    },
                ],
                EphemeralContainers: nil,
                RestartPolicy: "Always",
                TerminationGracePeriodSeconds: 1,
                ActiveDeadlineSeconds: nil,
                DNSPolicy: "ClusterFirst",
                NodeSelector: {
                    "instance-type": "on-demand",
                },
                ServiceAccountName: "default",
                DeprecatedServiceAccount: "default",
                AutomountServiceAccountToken: nil,
                NodeName: "kind-worker",
                HostNetwork: false,
                HostPID: false,
                HostIPC: false,
                ShareProcessNamespace: nil,
                SecurityContext: {
                    SELinuxOptions: nil,
                    WindowsOptions: nil,
                    RunAsUser: nil,
                    RunAsGroup: nil,
                    RunAsNonRoot: nil,
                    SupplementalGroups: nil,
                    SupplementalGroupsPolicy: nil,
                    FSGroup: nil,
                    Sysctls: nil,
                    FSGroupChangePolicy: nil,
                    SeccompProfile: nil,
                    AppArmorProfile: nil,
                    SELinuxChangePolicy: nil,
                },
                ImagePullSecrets: nil,
                Hostname: "lws-1",
                Subdomain: "lws",
                Affinity: nil,
                SchedulerName: "default-scheduler",
                Tolerations: [
                    {
                        Key: "node.kubernetes.io/not-ready",
                        Operator: "Exists",
                        Value: "",
                        Effect: "NoExecute",
                        TolerationSeconds: 300,
                    },
                    {
                        Key: "node.kubernetes.io/unreachable",
                        Operator: "Exists",
                        Value: "",
                        Effect: "NoExecute",
                        TolerationSeconds: 300,
                    },
                ],
                HostAliases: nil,
                PriorityClassName: "",
                Priority: 0,
                DNSConfig: nil,
                ReadinessGates: nil,
                RuntimeClassName: nil,
                EnableServiceLinks: true,
                PreemptionPolicy: "PreemptLowerPriority",
                Overhead: nil,
                TopologySpreadConstraints: nil,
                SetHostnameAsFQDN: nil,
                OS: nil,
                HostUsers: nil,
                SchedulingGates: nil,
                ResourceClaims: nil,
                Resources: nil,
                HostnameOverride: nil,
                WorkloadRef: nil,
            },
            Status: {
                ObservedGeneration: 0,
                Phase: "Succeeded",
                Conditions: [
                    {
                        Type: "TerminationTarget",
                        ObservedGeneration: 0,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:14Z,
                        },
                        Reason: "NoMatchingWorkload",
                        Message: "missing workload",
                    },
                    {
                        Type: "PodReadyToStartContainers",
                        ObservedGeneration: 0,
                        Status: "False",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:15Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Initialized",
                        ObservedGeneration: 0,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:12Z,
                        },
                        Reason: "PodCompleted",
                        Message: "",
                    },
                    {
                        Type: "Ready",
                        ObservedGeneration: 0,
                        Status: "False",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:15Z,
                        },
                        Reason: "PodCompleted",
                        Message: "",
                    },
                    {
                        Type: "ContainersReady",
                        ObservedGeneration: 0,
                        Status: "False",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:15Z,
                        },
                        Reason: "PodCompleted",
                        Message: "",
                    },
                    {
                        Type: "PodScheduled",
                        ObservedGeneration: 0,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-01-22T04:44:12Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                ],
                Message: "",
                Reason: "",
                NominatedNodeName: "",
                HostIP: "172.18.0.3",
                HostIPs: [{IP: "172.18.0.3"}],
                PodIP: "10.244.2.80",
                PodIPs: [{IP: "10.244.2.80"}],
                StartTime: {
                    Time: 2026-01-22T04:44:12Z,
                },
                InitContainerStatuses: nil,
                ContainerStatuses: [
                    {
                        Name: "c",
                        State: {
                            Waiting: nil,
                            Running: nil,
                            Terminated: {
                                ExitCode: 0,
                                Signal: 0,
                                Reason: "Completed",
                                Message: "",
                                StartedAt: {
                                    Time: 2026-01-22T04:44:13Z,
                                },
                                FinishedAt: {
                                    Time: 2026-01-22T04:44:15Z,
                                },
                                ContainerID: "containerd://2f779c4800f5e708da239f009065e03a992b9c6baa4027684d0a2124514bb8d2",
                            },
                        },
                        LastTerminationState: {Waiting: nil, Running: nil, Terminated: nil},
                        Ready: false,
                        RestartCount: 0,
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.60",
                        ImageID: "sha256:d9b1f93401bfcf4303c130dca0890f18667239f8daf633d211f718a230604147",
                        ContainerID: "containerd://2f779c4800f5e708da239f009065e03a992b9c6baa4027684d0a2124514bb8d2",
                        Started: false,
                        AllocatedResources: {
                            "cpu": {
                                i: {value: 200, scale: -3},
                                d: {Dec: nil},
                                s: "200m",
                                Format: "DecimalSI",
                            },
                        },
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 200, scale: -3},
                                    d: {Dec: nil},
                                    s: "200m",
                                    Format: "DecimalSI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 200, scale: -3},
                                    d: {Dec: nil},
                                    s: "200m",
                                    Format: "DecimalSI",
                                },
                            },
                            Claims: nil,
                        },
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-wb522",
                                MountPath: "/var/run/secrets/kubernetes.io/serviceaccount",
                                ReadOnly: true,
                                RecursiveReadOnly: "Disabled",
                            },
                        ],
                        User: {
                            Linux: {
                                UID: 0,
                                GID: 0,
                                SupplementalGroups: [0, 1, 2, 3, 4, 6, 10, 11, 20, 26, 27],
                            },
                        },
                        AllocatedResourcesStatus: nil,
                        StopSignal: nil,
                    },
                ],
                QOSClass: "Burstable",
                EphemeralContainerStatuses: nil,
                Resize: "",
                ResourceClaimStatuses: nil,
                ExtendedResourceClaimStatus: nil,
                AllocatedResources: nil,
                Resources: nil,
            },
        },
    ]
to be empty
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:402 @ 01/22/26 04:45:00.661
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8732/pull-kueue-test-e2e-main-1-33/2014193502698606592

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-22T09:51:26Z

/assign @mykysha

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T14:56:46Z

Interesting so the deletion of the leader Pod `lws-e2e-kxs58/lws-1` (UID: `2e00ca28-c0a8-4163-b2eb-401eb3e28ada") is stuck due to the finalizer: `foregroundDeletion` - this is the core finalizer indicating the k8s GC is waiting for the children to be deleted fist. 

In this case the child is StatefulSet for leaders, and it matches the LWS code propagation policy, see [here](https://github.com/kubernetes-sigs/lws/blob/d450679bd16bab7156ae2b9962068776964ea971/pkg/controllers/pod_controller.go#L2454-L250). We can confirm that request in [LWS logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8732/pull-kueue-test-e2e-main-1-33/2014193502698606592/artifacts/run-test-e2e-singlecluster-1.33.7/kind-worker2/pods/lws-system_lws-controller-manager-8cf8bfb5d-4zln6_b223c871-5af1-42be-9eaf-a4e390f10284/manager/0.log), see:
```
2026-01-22T04:44:14.399736918Z stderr F 2026-01-22T04:44:14Z	DEBUG	events	Worker pod lws-1-2 failed, deleted leader pod lws-1 to recreate group 1	{"type": "Normal", "object": {"kind":"LeaderWorkerSet","namespace":"lws-e2e-kxs58","name":"lws","uid":"940d0e08-7f9a-4a61-8eb6-c20b265bb984","apiVersion":"leaderworkerset.x-k8s.io/v1","resourceVersion":"7299"}, "reason": "RecreateGroupOnPodRestart"}
```
so now the question is why the StatefulSet couldn't get deleted.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T14:59:08Z

Why thing which stands out is this log in the [kube-controller-manager](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8732/pull-kueue-test-e2e-main-1-33/2014193502698606592/artifacts/run-test-e2e-singlecluster-1.33.7/kind-control-plane/pods/kube-system_kube-controller-manager-kind-control-plane_8a1398db1ff4f808bf4f65fdd17efddf/kube-controller-manager/0.log) logs:

```
2026-01-22T04:45:05.786241049Z stderr F E0122 04:45:05.786032       1 garbagecollector.go:360] "Unhandled Error" err="error syncing item &garbagecollector.node{identity:garbagecollector.objectReference{OwnerReference:v1.OwnerReference{APIVersion:\"apps/v1\", Kind:\"StatefulSet\", Name:\"lws-1\", UID:\"299406b0-694d-4f0d-bb42-f4af834b3f69\", Controller:(*bool)(nil), BlockOwnerDeletion:(*bool)(nil)}, Namespace:\"lws-e2e-kxs58\"}, dependentsLock:sync.RWMutex{w:sync.Mutex{_:sync.noCopy{}, mu:sync.Mutex{state:0, sema:0x0}}, writerSem:0x0, readerSem:0x0, readerCount:atomic.Int32{_:atomic.noCopy{}, v:1}, readerWait:atomic.Int32{_:atomic.noCopy{}, v:0}}, dependents:map[*garbagecollector.node]struct {}{}, deletingDependents:true, deletingDependentsLock:sync.RWMutex{w:sync.Mutex{_:sync.noCopy{}, mu:sync.Mutex{state:0, sema:0x0}}, writerSem:0x0, readerSem:0x0, readerCount:atomic.Int32{_:atomic.noCopy{}, v:0}, readerWait:atomic.Int32{_:atomic.noCopy{}, v:0}}, beingDeleted:true, beingDeletedLock:sync.RWMutex{w:sync.Mutex{_:sync.noCopy{}, mu:sync.Mutex{state:0, sema:0x0}}, writerSem:0x0, readerSem:0x0, readerCount:atomic.Int32{_:atomic.noCopy{}, v:0}, readerWait:atomic.Int32{_:atomic.noCopy{}, v:0}}, virtual:false, virtualLock:sync.RWMutex{w:sync.Mutex{_:sync.noCopy{}, mu:sync.Mutex{state:0, sema:0x0}}, writerSem:0x0, readerSem:0x0, readerCount:atomic.Int32{_:atomic.noCopy{}, v:0}, readerWait:atomic.Int32{_:atomic.noCopy{}, v:0}}, owners:[]v1.OwnerReference{v1.OwnerReference{APIVersion:\"v1\", Kind:\"Pod\", Name:\"lws-1\", UID:\"2e00ca28-c0a8-4163-b2eb-401eb3e28ada\", Controller:(*bool)(0xc003a50efa), BlockOwnerDeletion:(*bool)(0xc003a50efb)}}}: admission webhook \"mstatefulset.kb.io\" denied the request: Pod \"lws-1\" not found" logger="UnhandledError"
```
This suggests there might be a bug in our statefulset_webhook when we call owner traversal. If the owner is already deleted this would return error. I think we should call the owner traversal only on the first attempts.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T14:59:23Z

cc @mbobrovskyi @sohankunkerkar who may have some ideas here

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-26T18:00:30Z

I spent some time tracing through the code to understand what’s happening here. When GC tries to delete the `StatefulSet`, Kubernetes first updates it to set a `DeletionTimestamp`, and that update gets intercepted by Kueue’s mutating webhook. The webhook ends up calling `WorkloadShouldBeSuspended()`, which walks the owner chain via `FindAncestorJobManagedByKueue()`. At that point, the parent Pod has already been deleted, so the GET fails with a NotFound error and the webhook blocks GC.

One thought is to short-circuit this earlier: if an object already has a `DeletionTimestamp`, we could simply skip the suspend/owner-traversal logic altogether. We don’t really need to reason about suspension for resources that are already being deleted.

It might also be worth making the owner traversal a bit more defensive by handling `NotFound` gracefully and stopping the walk if an owner is already gone. That wouldn’t change the core behavior here, but could help avoid similar edge cases in other call paths.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T18:09:44Z

> It might also be worth making the owner traversal a bit more defensive by handling NotFound gracefully and stopping the walk if an owner is already gone. That wouldn’t change the core behavior here, but could help avoid similar edge cases in other call paths

I was thinking about it, but I think it could actually generate wrong results in case th3 informer in Kueue learns about the child earlier than about the parent. This is possible because k8s does not provide any guarantee about the order of event propagation for differrnt types. So I think is is unlikely but possible Kueue would see parent JobSet as not found even if it already observes the child Job.

Also skipping suspend on deleteTimestamp might be tricky. A terminating Hob may stilll be creating Pods. I know this is unlikely. so it might be pragmati. fix.


Stilll I think short circuit if the SuspendedByParent annotation is already present sounds reasonable to me.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-26T18:17:52Z

> > It might also be worth making the owner traversal a bit more defensive by handling NotFound gracefully and stopping the walk if an owner is already gone. That wouldn’t change the core behavior here, but could help avoid similar edge cases in other call paths
> 
> I was thinking about it, but I think it could actually generate wrong results in case th3 informer in Kueue learns about the child earlier than about the parent. This is possible because k8s does not provide any guarantee about the order of event propagation for differrnt types. So I think is is unlikely but possible Kueue would see parent JobSet as not found even if it already observes the child Job.
> 
> Also skipping suspend on deleteTimestamp might be tricky. A terminating Hob may stilll be creating Pods. I know this is unlikely. so it might be pragmati. fix.
> 
> Stilll I think short circuit if the SuspendedByParent annotation is already present sounds reasonable to me.

Thanks for the inputs. The informer ordering issue with `NotFound` handling makes sense and good point about terminating Jobs still creating Pods, which makes the `DeletionTimestamp` check tricky.               
                                                                                                                                                                             
 So, the `SuspendedByParentAnnotation` check seems like the cleanest approach since it only skips objects that were definitely already processed.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-27T16:12:56Z

I’m wondering: is there a race condition here? 

https://github.com/kubernetes-sigs/kueue/blob/4888792ce5767d9a2ffba71dec79126d5e707d82/pkg/controller/jobs/pod/pod_controller.go#L560-L565

@mykysha could you please take a look at it and maybe create some experiment PR to confirm.

If yes, I think https://github.com/kubernetes-sigs/kueue/pull/3912 should fix it.

### Comment by [@mykysha](https://github.com/mykysha) — 2026-01-27T16:15:27Z

Taking a look at the moment, if focus is used in tests, the problem is easily replicated locally, so no need for an experiment PR. Let me try to test with and without the featuregate.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T08:25:53Z

/close

Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/8862.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-30T08:25:59Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8733#issuecomment-3822484768):

>/close
>
>Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/8862.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
