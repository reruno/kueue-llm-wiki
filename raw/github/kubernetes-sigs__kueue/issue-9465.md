# Issue #9465: Flaky test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should not suspend the pods created by a StatefulSet in the kube-system namespace

**Summary**: Flaky test: ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should not suspend the pods created by a StatefulSet in the kube-system namespace

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9465

**Last updated**: 2026-02-27T06:07:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-25T07:48:15Z
- **Updated**: 2026-02-27T06:07:57Z
- **Closed**: 2026-02-27T06:07:57Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 2

## Description

**Which test is flaking?**:

ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should not suspend the pods created by a StatefulSet in the kube-system namespace 

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-release-0-16/2026533170517643264

**Failure message or logs**:
```
End To End Custom Configs handling Suite: kindest/node:v1.35.0: [It] ManageJobsWithoutQueueName when manageJobsWithoutQueueName=true should not suspend the pods created by a StatefulSet in the kube-system namespace expand_less	50s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:778 with:
Expected
    <[]v1.Pod | len:2, cap:2>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "test-sts-0",
                GenerateName: "test-sts-",
                Namespace: "kube-system",
                SelfLink: "",
                UID: "aa4d3628-c133-4c8a-95b3-374307823c73",
                ResourceVersion: "5740",
                Generation: 2,
                CreationTimestamp: {
                    Time: 2026-02-25T06:01:42Z,
                },
                DeletionTimestamp: {
                    Time: 2026-02-25T06:02:16Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "app": "test-sts-pod",
                    "apps.kubernetes.io/pod-index": "0",
                    "controller-revision-hash": "test-sts-858f6d997f",
                    "statefulset.kubernetes.io/pod-name": "test-sts-0",
                },
                Annotations: nil,
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "test-sts",
                        UID: "0e7778fa-15ef-4732-821d-4488680720d5",
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
                            Time: 2026-02-25T06:01:42Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0e7778fa-15ef-4732-821d-4488680720d5\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{},\"f:memory\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{},\"f:memory\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-02-25T06:01:46Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodScheduled\\\"}\":{\"f:observedGeneration\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}}},\"f:containerStatuses\":{},\"f:hostIP\":{},\"f:hostIPs\":{},\"f:observedGeneration\":{},\"f:phase\":{},\"f:podIP\":{},\"f:podIPs\":{\".\":{},\"k:{\\\"ip\\\":\\\"10.244.2.29\\\"}\":{\".\":{},\"f:ip\":{}}},\"f:startTime\":{}}}",
                        },
                        Subresource: "status",
                    },
                ],
            },
            Spec: {
                Volumes: [
                    {
                        Name: "kube-api-access-8jhd4",
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
                        Env: nil,
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Claims: nil,
                        },
                        ResizePolicy: nil,
                        RestartPolicy: nil,
                        RestartPolicyRules: nil,
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-8jhd4",
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
                TerminationGracePeriodSeconds: 30,
                ActiveDeadlineSeconds: nil,
                DNSPolicy: "ClusterFirst",
                NodeSelector: nil,
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
                Hostname: "test-sts-0",
                Subdomain: "",
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
                ObservedGeneration: 2,
                Phase: "Running",
                Conditions: [
                    {
                        Type: "PodReadyToStartContainers",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:44Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Initialized",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:42Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Ready",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:44Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "ContainersReady",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:44Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "PodScheduled",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:42Z,
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
                PodIP: "10.244.2.29",
                PodIPs: [{IP: "10.244.2.29"}],
                StartTime: {
                    Time: 2026-02-25T06:01:42Z,
                },
                InitContainerStatuses: nil,
                ContainerStatuses: [
                    {
                        Name: "c",
                        State: {
                            Waiting: nil,
                            Running: {
                                StartedAt: {
                                    Time: 2026-02-25T06:01:44Z,
                                },
                            },
                            Terminated: nil,
                        },
                        LastTerminationState: {Waiting: nil, Running: nil, Terminated: nil},
                        Ready: true,
                        RestartCount: 0,
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.62.0",
                        ImageID: "sha256:e222f54944ebc598ea5e517ba12609a25d24398addecc0ccb93bbd897ae4b8c1",
                        ContainerID: "containerd://b48992a24b93e94ebdfb8ecbca869672ff80acbd45c2b6d2fc6433dcd1798ac7",
                        Started: true,
                        AllocatedResources: {
                            "cpu": {
                                i: {value: 1, scale: 0},
                                d: {Dec: nil},
                                s: "1",
                                Format: "DecimalSI",
                            },
                            "memory": {
                                i: {value: 2147483648, scale: 0},
                                d: {Dec: nil},
                                s: "2Gi",
                                Format: "BinarySI",
                            },
                        },
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Claims: nil,
                        },
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-8jhd4",
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
                QOSClass: "Guaranteed",
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
                Name: "test-sts-1",
                GenerateName: "test-sts-",
                Namespace: "kube-system",
                SelfLink: "",
                UID: "210c9ec9-92f6-4fd5-bd28-263312b144c8",
                ResourceVersion: "5745",
                Generation: 2,
                CreationTimestamp: {
                    Time: 2026-02-25T06:01:44Z,
                },
                DeletionTimestamp: {
                    Time: 2026-02-25T06:02:16Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "controller-revision-hash": "test-sts-858f6d997f",
                    "statefulset.kubernetes.io/pod-name": "test-sts-1",
                    "app": "test-sts-pod",
                    "apps.kubernetes.io/pod-index": "1",
                },
                Annotations: nil,
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "test-sts",
                        UID: "0e7778fa-15ef-4732-821d-4488680720d5",
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
                            Time: 2026-02-25T06:01:44Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0e7778fa-15ef-4732-821d-4488680720d5\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{},\"f:memory\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{},\"f:memory\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-02-25T06:01:47Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodScheduled\\\"}\":{\"f:observedGeneration\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}}},\"f:containerStatuses\":{},\"f:hostIP\":{},\"f:hostIPs\":{},\"f:observedGeneration\":{},\"f:phase\":{},\"f:podIP\":{},\"f:podIPs\":{\".\":{},\"k:{\\\"ip\\\":\\\"10.244.1.22\\\"}\":{\".\":{},\"f:ip\":{}}},\"f:startTime\":{}}}",
                        },
                        Subresource: "status",
                    },
                ],
            },
            Spec: {
                Volumes: [
                    {
                        Name: "kube-api-access-jcn9z",
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
                        Env: nil,
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Claims: nil,
                        },
                        ResizePolicy: nil,
                        RestartPolicy: nil,
                        RestartPolicyRules: nil,
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-jcn9z",
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
                TerminationGracePeriodSeconds: 30,
                ActiveDeadlineSeconds: nil,
                DNSPolicy: "ClusterFirst",
                NodeSelector: nil,
                ServiceAccountName: "default",
                DeprecatedServiceAccount: "default",
                AutomountServiceAccountToken: nil,
                NodeName: "kind-worker2",
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
                Hostname: "test-sts-1",
                Subdomain: "",
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
                ObservedGeneration: 2,
                Phase: "Running",
                Conditions: [
                    {
                        Type: "PodReadyToStartContainers",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:46Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Initialized",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:44Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Ready",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:46Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "ContainersReady",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:46Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "PodScheduled",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:44Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                ],
                Message: "",
                Reason: "",
                NominatedNodeName: "",
                HostIP: "172.18.0.4",
                HostIPs: [{IP: "172.18.0.4"}],
                PodIP: "10.244.1.22",
                PodIPs: [{IP: "10.244.1.22"}],
                StartTime: {
                    Time: 2026-02-25T06:01:44Z,
                },
                InitContainerStatuses: nil,
                ContainerStatuses: [
                    {
                        Name: "c",
                        State: {
                            Waiting: nil,
                            Running: {
                                StartedAt: {
                                    Time: 2026-02-25T06:01:46Z,
                                },
                            },
                            Terminated: nil,
                        },
                        LastTerminationState: {Waiting: nil, Running: nil, Terminated: nil},
                        Ready: true,
                        RestartCount: 0,
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.62.0",
                        ImageID: "sha256:e222f54944ebc598ea5e517ba12609a25d24398addecc0ccb93bbd897ae4b8c1",
                        ContainerID: "containerd://b0553f810594a1d8c7db9df62520bcc984792ce08bdd788ad98350dec089c5b3",
                        Started: true,
                        AllocatedResources: {
                            "cpu": {
                                i: {value: 1, scale: 0},
                                d: {Dec: nil},
                                s: "1",
                                Format: "DecimalSI",
                            },
                            "memory": {
                                i: {value: 2147483648, scale: 0},
                                d: {Dec: nil},
                                s: "2Gi",
                                Format: "BinarySI",
                            },
                        },
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Claims: nil,
                        },
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-jcn9z",
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
                QOSClass: "Guaranteed",
                EphemeralContainerStatuses: nil,
                Resize: "",
                ResourceClaimStatuses: nil,
                ExtendedResourceClaimStatus: nil,
                AllocatedResources: nil,
                Resources: nil,
            },
        },
    ]
to be empty failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:778 with:
Expected
    <[]v1.Pod | len:2, cap:2>: [
        {
            TypeMeta: {Kind: "", APIVersion: ""},
            ObjectMeta: {
                Name: "test-sts-0",
                GenerateName: "test-sts-",
                Namespace: "kube-system",
                SelfLink: "",
                UID: "aa4d3628-c133-4c8a-95b3-374307823c73",
                ResourceVersion: "5740",
                Generation: 2,
                CreationTimestamp: {
                    Time: 2026-02-25T06:01:42Z,
                },
                DeletionTimestamp: {
                    Time: 2026-02-25T06:02:16Z,
                },
                DeletionGracePeriodSeconds: 30,
                Labels: {
                    "app": "test-sts-pod",
                    "apps.kubernetes.io/pod-index": "0",
                    "controller-revision-hash": "test-sts-858f6d997f",
                    "statefulset.kubernetes.io/pod-name": "test-sts-0",
                },
                Annotations: nil,
                OwnerReferences: [
                    {
                        APIVersion: "apps/v1",
                        Kind: "StatefulSet",
                        Name: "test-sts",
                        UID: "0e7778fa-15ef-4732-821d-4488680720d5",
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
                            Time: 2026-02-25T06:01:42Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:generateName\":{},\"f:labels\":{\".\":{},\"f:app\":{},\"f:apps.kubernetes.io/pod-index\":{},\"f:controller-revision-hash\":{},\"f:statefulset.kubernetes.io/pod-name\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"0e7778fa-15ef-4732-821d-4488680720d5\\\"}\":{}}},\"f:spec\":{\"f:containers\":{\"k:{\\\"name\\\":\\\"c\\\"}\":{\".\":{},\"f:args\":{},\"f:image\":{},\"f:imagePullPolicy\":{},\"f:name\":{},\"f:resources\":{\".\":{},\"f:limits\":{\".\":{},\"f:cpu\":{},\"f:memory\":{}},\"f:requests\":{\".\":{},\"f:cpu\":{},\"f:memory\":{}}},\"f:terminationMessagePath\":{},\"f:terminationMessagePolicy\":{}}},\"f:dnsPolicy\":{},\"f:enableServiceLinks\":{},\"f:hostname\":{},\"f:restartPolicy\":{},\"f:schedulerName\":{},\"f:securityContext\":{},\"f:terminationGracePeriodSeconds\":{}}}",
                        },
                        Subresource: "",
                    },
                    {
                        Manager: "kubelet",
                        Operation: "Update",
                        APIVersion: "v1",
                        Time: {
                            Time: 2026-02-25T06:01:46Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:status\":{\"f:conditions\":{\"k:{\\\"type\\\":\\\"ContainersReady\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"Initialized\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodReadyToStartContainers\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"PodScheduled\\\"}\":{\"f:observedGeneration\":{}},\"k:{\\\"type\\\":\\\"Ready\\\"}\":{\".\":{},\"f:lastProbeTime\":{},\"f:lastTransitionTime\":{},\"f:observedGeneration\":{},\"f:status\":{},\"f:type\":{}}},\"f:containerStatuses\":{},\"f:hostIP\":{},\"f:hostIPs\":{},\"f:observedGeneration\":{},\"f:phase\":{},\"f:podIP\":{},\"f:podIPs\":{\".\":{},\"k:{\\\"ip\\\":\\\"10.244.2.29\\\"}\":{\".\":{},\"f:ip\":{}}},\"f:startTime\":{}}}",
                        },
                        Subresource: "status",
                    },
                ],
            },
            Spec: {
                Volumes: [
                    {
                        Name: "kube-api-access-8jhd4",
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
                        Env: nil,
                        Resources: {
                            Limits: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Requests: {
                                "cpu": {
                                    i: {value: 1, scale: 0},
                                    d: {Dec: nil},
                                    s: "1",
                                    Format: "DecimalSI",
                                },
                                "memory": {
                                    i: {value: 2147483648, scale: 0},
                                    d: {Dec: nil},
                                    s: "2Gi",
                                    Format: "BinarySI",
                                },
                            },
                            Claims: nil,
                        },
                        ResizePolicy: nil,
                        RestartPolicy: nil,
                        RestartPolicyRules: nil,
                        VolumeMounts: [
                            {
                                Name: "kube-api-access-8jhd4",
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
                TerminationGracePeriodSeconds: 30,
                ActiveDeadlineSeconds: nil,
                DNSPolicy: "ClusterFirst",
                NodeSelector: nil,
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
                Hostname: "test-sts-0",
                Subdomain: "",
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
                ObservedGeneration: 2,
                Phase: "Running",
                Conditions: [
                    {
                        Type: "PodReadyToStartContainers",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:44Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Initialized",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:42Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "Ready",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:44Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "ContainersReady",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:44Z,
                        },
                        Reason: "",
                        Message: "",
                    },
                    {
                        Type: "PodScheduled",
                        ObservedGeneration: 2,
                        Status: "True",
                        LastProbeTime: {
                            Time: 0001-01-01T00:00:00Z,
                        },
                        LastTransitionTime: {
                            Time: 2026-02-25T06:01:42Z,
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
                PodIP: "10.244.2.29",
                PodIPs: [{IP: "10.244.2.29"}],
                StartTime: {
                    Time: 2026-02-25T06:01:42Z,
                },
                InitContainerStatuses: nil,
                ContainerStatuses: [
                    {
                        Name: "c",
                        State: {
                            Waiting: nil,
                            Running: {
                                StartedAt: {
                                    Time: 2026-02-25T06:01:44Z,
                                },
                            },
                            Terminated: nil,
                        },
                        LastTerminationState: {Waiting: nil, Running: nil, Terminated: nil},
                        Ready: true,
                        RestartCount: 0,
                        Image: "registry.k8s.io/e2e-test-images/agnhost:2.62.0",
                        ImageID: "sha256:e222f54944ebc598ea5e517ba12609a25d24398addecc0ccb93bbd897ae4b8c1",
                        ContainerID: "containerd://b48992a24b93e94ebdfb8ecbca869672ff80acbd45c2b6d2fc6433dcd1798ac7",
                        Started: true,
                        AllocatedResources: {
                            "cpu": {
                                i: {value: 1, scale: 0},
                                d: {Dec: nil},
                                s: "1",
                                Format: "DecimalSI",
                            },
                            "memory": {
                                i: {value: 2147483648, scale: 0},
                                d: {Dec: nil},
                                s: "2Gi",
                                Format: "BinarySI",
                            },
                        },
  // <-  cut to make it fit in the chars limit
            },
        },
    ]
to be empty
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:779 @ 02/25/26 06:02:31.593
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T07:59:53Z

The Pods are in Running phase: `Phase: "Running"` while with deletionTimestamp, so Kubelet is working on their termination.

I think we should do two things here:
1. wait for Pods to be ready rather than running. Running does not imply the agnhost already registered the endpoint handler, I think most likely the SIGTERM was received between Running and Ready. 
2. reduce the TerminationGracePeriodSeconds to 1s, currently 30s a safety mechanism when the SIGTERM is missed
 `TerminationGracePeriodSeconds: 30,` so probably this takes mo

FYI the agnhost code: https://github.com/kubernetes/kubernetes/blob/master/test/images/agnhost/netexec/netexec.go

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-02-25T08:16:16Z

/assign

I can have a look at this one 🙂
