# Issue #9751: LeaderWorkerSet integration when LeaderWorkerSet created with Restart Policy should recreate pods when policy is set to RecreateGroupOnPodRestart

**Summary**: LeaderWorkerSet integration when LeaderWorkerSet created with Restart Policy should recreate pods when policy is set to RecreateGroupOnPodRestart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9751

**Last updated**: 2026-03-25T13:50:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-09T08:55:24Z
- **Updated**: 2026-03-25T13:50:19Z
- **Closed**: 2026-03-25T13:50:19Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 1

## Description



**Which test is flaking?**:
LeaderWorkerSet integration when LeaderWorkerSet created with Restart Policy should recreate pods when policy is set to RecreateGroupOnPodRestart
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-16-1-34/2030157647042318336
**Failure message or logs**:
```
End To End Suite: kindest/node:v1.34.3: [It] LeaderWorkerSet integration when LeaderWorkerSet created with Restart Policy should recreate pods when policy is set to RecreateGroupOnPodRestart [area:singlecluster, feature:leaderworkerset] expand_less	1m2s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:253 with:
Expected
    <[]v1.Pod | len:3, cap:4>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0",
                GenerateName: "lws-",
                Namespace: "lws-e2e-vtlbk",
                SelfLink: "",
                UID: "489f5a31-d188-40c6-892e-76631d241c2b",
                ResourceVersion: "8512",
                Generation: 3,
                CreationTimestamp: {
                    Time: 2026-03-07T06:02:38Z,
                },
                DeletionTimestamp: {
                    Time: 2026-03-07T06:02:44Z,
                },
                DeletionGracePeriodSeconds: 1,
                Labels: {
                    "apps.kubernetes.io/pod-index": "0",
                    "controller-revision-hash": "lws-6f75ccb9f8",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-ca73b",
                    "kueue.x-k8s.io/queue-name": "lws-lq-lws-e2e-vtlbk",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/group-key": "ff2552bf4f4223f2f2e5fa9db5e23e0cead953c4",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/worker-index": "0",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-ca73b",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "794ccff98",
                    "statefulset.kubernetes.io/pod-name": "lws-0",
                },
                Annotations: {
                    "leaderworkerset.sigs.k8s.io/size": "3",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-ca73b",
                    "kueue.x-k8s.io/workload-slice-name": "leaderworkerset-lws-0-ca73b",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws",
                        UID: "5471cd2f-6fff-4e37-93e9-aa9a2db10580",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:38Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/worker-index\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"5471cd2f-6fff-4e37-93e9-aa9a2db10580\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomain\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:38Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\"f:kueue.x-k8s.io/pod-group-total-count\":{},\"f:kueue.x-k8s.io/role-hash\":{},\"f:kueue.x-k8s.io/workload\":{},\"f:kueue.x-k8s.io/workload-slice-name\":{}},\"f:labels\":{\"f:kueue.x-k8s.io/managed\":{},\"f:kueue.x-k8s.io/pod-group-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/prebuilt-workload-name\":{},\"f:kueue.x-k8s.io/queue-name\":{}}},\"f:spec\":{\"f:nodeSelector\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:44Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodScheduled\\\"}\":{\"f:observedGeneration\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}}},\"f:containerStatuses\":{},\"f:hostIP\":{},\"f:hostIPs\":{},\"f:observedGeneration\":{},\"f:phase\":{},\"f:podIP\":{},\"f:podIPs\":{\".\":{},\"k:{\\\"ip\\\":\\\"10.244.2.99\\\"}\":{\".\":{},\"f:ip\":{}}},\"f:startTime\":{}}}",
                        },
                        Subresource: "status",
                    },
                ],
            },
            Spec: {
                Volumes: [
                    {
                        Name: "kube-api-access-szgm7",
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
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.62.0",
                        Command: nil,
                        Args: ["netexec"],
                        WorkingDir: "",
                        Ports: nil,
                        EnvFrom: nil,
                        Env: [
                            {
                                Name: "LWS_LEADER_ADDRESS",
                                Value: "lws-0.lws.lws-e2e-vtlbk",
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
                                Name: "kube-api-access-szgm7",
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
                Hostname: "lws-0",
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
                ObservedGeneration: 3,
                Phase: "Running",
                Conditions: [
                    {
                        Type: "PodReadyToStartContainers",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:41Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Initialized",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:38Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Ready",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:41Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "ContainersReady",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:41Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "PodScheduled",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:38Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                ],
                Message: "",
                Reason: "",
                NominatedNodeName: "",
                HostIP: "172.18.0.2",
                HostIPs: [{IP: "172.18.0.2"}],
                PodIP: "10.244.2.99",
                PodIPs: [{IP: "10.244.2.99"}],
                StartTime: {
                    Time: 2026-03-07T06:02:38Z,
                },
                InitContainerStatuses: nil,
                ContainerStatuses: [
                    {
                        Name: "c",
                        State: {
                            Waiting: nil,
                            Running: {
                                StartedAt: {
                                    Time: 2026-03-07T06:02:41Z,
                                },
                            },
                            Terminated: nil,
                        },
                        LastTerminationState: {Waiting: nil, Running: nil, Terminated: nil},
                        Ready: true,
                        RestartCount: 0,
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.62.0",
                        ImageID: "sha256:e222f54944ebc598ea5e517ba12609a25d24398addecc0ccb93bbd897ae4b8c1",
                        ContainerID: "containerd://f0df9a81f736ca6a974088814bf032a49ed423443ec846665365e99cede0c83e",
                        Started: true,
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
                                Name: "kube-api-access-szgm7",
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
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0-1",
                GenerateName: "lws-0-",
                Namespace: "lws-e2e-vtlbk",
                SelfLink: "",
                UID: "5b912a71-9d36-4aa1-9ef0-44614866d698",
                ResourceVersion: "8520",
                Generation: 3,
                CreationTimestamp: {
                    Time: 2026-03-07T06:02:38Z,
                },
                DeletionTimestamp: {
                    Time: 2026-03-07T06:02:44Z,
                },
                DeletionGracePeriodSeconds: 1,
                Labels: {
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "leaderworkerset.sigs.k8s.io/worker-index": "1",
                    "controller-revision-hash": "lws-0-544c695d64",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-ca73b",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-ca73b",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "794ccff98",
                    "statefulset.kubernetes.io/pod-name": "lws-0-1",
                    "apps.kubernetes.io/pod-index": "1",
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/queue-name": "lws-lq-lws-e2e-vtlbk",
                    "leaderworkerset.sigs.k8s.io/group-key": "ff2552bf4f4223f2f2e5fa9db5e23e0cead953c4",
                },
                Annotations: {
                    "leaderworkerset.sigs.k8s.io/size": "3",
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-ca73b",
                    "kueue.x-k8s.io/workload-slice-name": "leaderworkerset-lws-0-ca73b",
                    "leaderworkerset.sigs.k8s.io/leader-name": "lws-0",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws-0",
                        UID: "c4bcf0a7-85fe-42fa-b47c-3a4682987e49",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:38Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/leader-name\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/group-index\":{},\"f:leaderworkerset.sigs.k8s.io/group-key\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"c4bcf0a7-85fe-42fa-b47c-3a4682987e49\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomain\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:39Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\"f:kueue.x-k8s.io/pod-group-total-count\":{},\"f:kueue.x-k8s.io/role-hash\":{},\"f:kueue.x-k8s.io/workload\":{},\"f:kueue.x-k8s.io/workload-slice-name\":{}},\"f:labels\":{\"f:kueue.x-k8s.io/managed\":{},\"f:kueue.x-k8s.io/pod-group-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/prebuilt-workload-name\":{},\"f:kueue.x-k8s.io/queue-name\":{}}},\"f:spec\":{\"f:nodeSelector\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:45Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodScheduled\\\"}\":{\"f:observedGeneration\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}}},\"f:containerStatuses\":{},\"f:hostIP\":{},\"f:hostIPs\":{},\"f:observedGeneration\":{},\"f:phase\":{},\"f:podIP\":{},\"f:podIPs\":{\".\":{},\"k:{\\\"ip\\\":\\\"10.244.2.100\\\"}\":{\".\":{},\"f:ip\":{}}},\"f:startTime\":{}}}",
                        },
                        Subresource: "status",
                    },
                ],
            },
            Spec: {
                Volumes: [
                    {
                        Name: "kube-api-access-tfh5j",
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
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.62.0",
                        Command: nil,
                        Args: ["netexec"],
                        WorkingDir: "",
                        Ports: nil,
                        EnvFrom: nil,
                        Env: [
                            {
                                Name: "LWS_LEADER_ADDRESS",
                                Value: "lws-0.lws.lws-e2e-vtlbk",
                                ValueFrom: nil,
                            },
                            {
                                Name: "LWS_GROUP_SIZE",
                                Value: "3",
                                ValueFrom: nil,
                            },
                            {
                                Name: "LWS_WORKER_INDEX",
                                Value: "1",
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
                                Name: "kube-api-access-tfh5j",
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
                Hostname: "lws-0-1",
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
                ObservedGeneration: 3,
                Phase: "Running",
                Conditions: [
                    {
                        Type: "PodReadyToStartContainers",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:43Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Initialized",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:39Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Ready",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:43Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "ContainersReady",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:43Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "PodScheduled",
                        ObservedGeneration: 3,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-03-07T06:02:39Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                ],
                Message: "",
                Reason: "",
                NominatedNodeName: "",
                HostIP: "172.18.0.2",
                HostIPs: [{IP: "172.18.0.2"}],
                PodIP: "10.244.2.100",
                PodIPs: [{IP: "10.244.2.100"}],
                StartTime: {
                    Time: 2026-03-07T06:02:39Z,
                },
                InitContainerStatuses: nil,
                ContainerStatuses: [
                    {
                        Name: "c",
                        State: {
                            Waiting: nil,
                            Running: {
                                StartedAt: {
                                    Time: 2026-03-07T06:02:42Z,
                                },
                            },
                            Terminated: nil,
                        },
                        LastTerminationState: {Waiting: nil, Running: nil, Terminated: nil},
                        Ready: true,
                        RestartCount: 0,
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.62.0",
                        ImageID: "sha256:e222f54944ebc598ea5e517ba12609a25d24398addecc0ccb93bbd897ae4b8c1",
                        ContainerID: "containerd://5400c331488d03fbecc89a639cc755ab56df90e6512be6f91e5bf89f0a9a4d98",
                        Started: true,
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
                                Name: "kube-api-access-tfh5j",
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
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "lws-0-2",
                GenerateName: "lws-0-",
                Namespace: "lws-e2e-vtlbk",
                SelfLink: "",
                UID: "164e5148-c71b-40a1-b5a6-e9433bf5105a",
                ResourceVersion: "8521",
                Generation: 3,
                CreationTimestamp: {
                    Time: 2026-03-07T06:02:38Z,
                },
                DeletionTimestamp: {
                    Time: 2026-03-07T06:02:44Z,
                },
                DeletionGracePeriodSeconds: 1,
                Labels: {
                    "kueue.x-k8s.io/managed": "true",
                    "kueue.x-k8s.io/queue-name": "lws-lq-lws-e2e-vtlbk",
                    "leaderworkerset.sigs.k8s.io/template-revision-hash": "794ccff98",
                    "leaderworkerset.sigs.k8s.io/worker-index": "2",
                    "kueue.x-k8s.io/pod-group-name": "leaderworkerset-lws-0-ca73b",
                    "kueue.x-k8s.io/podset": "main",
                    "kueue.x-k8s.io/prebuilt-workload-name": "leaderworkerset-lws-0-ca73b",
                    "leaderworkerset.sigs.k8s.io/group-index": "0",
                    "leaderworkerset.sigs.k8s.io/group-key": "ff2552bf4f4223f2f2e5fa9db5e23e0cead953c4",
                    "leaderworkerset.sigs.k8s.io/name": "lws",
                    "statefulset.kubernetes.io/pod-name": "lws-0-2",
                    "apps.kubernetes.io/pod-index": "2",
                    "controller-revision-hash": "lws-0-544c695d64",
                },
                Annotations: {
                    "kueue.x-k8s.io/pod-group-serving": "true",
                    "kueue.x-k8s.io/pod-group-total-count": "3",
                    "kueue.x-k8s.io/pod-suspending-parent": "leaderworkerset.x-k8s.io/leaderworkerset",
                    "kueue.x-k8s.io/role-hash": "main",
                    "kueue.x-k8s.io/workload": "leaderworkerset-lws-0-ca73b",
                    "kueue.x-k8s.io/workload-slice-name": "leaderworkerset-lws-0-ca73b",
                    "leaderworkerset.sigs.k8s.io/leader-name": "lws-0",
                    "leaderworkerset.sigs.k8s.io/size": "3",
                },
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "lws-0",
                        UID: "c4bcf0a7-85fe-42fa-b47c-3a4682987e49",
                        Controller: true,
                        BlockOwnerDeletion: true,
                    },
                ],
                Finalizers: nil,
                ManagedFields: [
                    {
                        Manager: "kube-controller-manager",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:38Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/pod-group-serving\":{},\"f:kueue.x-k8s.io/pod-suspending-parent\":{},\"f:leaderworkerset.sigs.k8s.io/leader-name\":{},\"f:leaderworkerset.sigs.k8s.io/size\":{}},\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:leaderworkerset.sigs.k8s.io/group-index\":{},\"f:leaderworkerset.sigs.k8s.io/group-key\":{},\"f:leaderworkerset.sigs.k8s.io/name\":{},\"f:leaderworkerset.sigs.k8s.io/template-revision-hash\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"c4bcf0a7-85fe-42fa-b47c-3a4682987e49\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:subdomain\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:39Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\"f:kueue.x-k8s.io/pod-group-total-count\":{},\"f:kueue.x-k8s.io/role-hash\":{},\"f:kueue.x-k8s.io/workload\":{},\"f:kueue.x-k8s.io/workload-slice-name\":{}},\"f:labels\":{\"f:kueue.x-k8s.io/managed\":{},\"f:kueue.x-k8s.io/pod-group-name\":{},\"f:kueue.x-k8s.io/podset\":{},\"f:kueue.x-k8s.io/prebuilt-workload-name\":{},\"f:kueue.x-k8s.io/queue-name\":{}}},\"f:spec\":{\"f:nodeSelector\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-03-07T06:02:45Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodScheduled\\\"}\":{\"f:observedGeneration\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}}},\"f:containerStatuses\":{},\"f:hostIP\":{},\"f:hostIPs\":{},\"f:observedGeneration\":{},\"f:phase\":{},\"f:podIP\":{},\"f:podIPs\":{\".\":{},\"k:{\\\"ip\\\":\\\"10.244.2.101\\\"}\":{\".\":{},\"f:ip\":{}}},\"f:startTime\":{}}}",
                        },
                        Subresource: "status",
                    },
                ],
            },
            Spec: {
                Volumes: [
                    {
                        Name: "kube-api-access-wcfw4",
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
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.62.0",
                        Command: nil,
                        Args: ["netexec"],
                        WorkingDir: "",
                        Ports: nil,

   // cut to fit into the chars limit
            },
        },
    ]
to be empty
In [AfterEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:85 @ 03/07/26 06:03:29.374
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-09T10:46:14Z

/assign
