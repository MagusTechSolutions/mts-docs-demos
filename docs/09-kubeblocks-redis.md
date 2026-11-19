# ⚡ Redis with KubeBlocks

Add a small standalone Redis instance for caching and short-lived application state.

> **Open the starter in a browser IDE:** [KubeBlocks source browser](code-browser/kubeblocks.md). You can expand, copy, and save the Redis Cluster and Service files.

## 1. Create the cluster

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: demo-redis
  namespace: demo
spec:
  clusterDef: redis
  topology: standalone
  terminationPolicy: DoNotTerminate
  componentSpecs:
    - name: redis
      componentDef: redis
      replicas: 1
      resources:
        requests:
          cpu: 25m
          memory: 128Mi
        limits:
          cpu: 100m
          memory: 256Mi
      volumeClaimTemplates:
        - name: data
          spec:
            storageClassName: truenas-nfs
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 1Gi
```

## 2. Create an internal Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-redis
  namespace: demo
spec:
  type: NodePort
  selector:
    app.kubernetes.io/instance: demo-redis
    apps.kubeblocks.io/component-name: redis
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
```

## 3. Verify the workload

```bash
kubectl -n demo get cluster demo-redis
kubectl -n demo get pods -l app.kubernetes.io/instance=demo-redis
kubectl -n demo get svc,pvc | grep demo-redis
kubectl -n demo describe cluster demo-redis
```

## 4. Test without exposing Redis publicly

Start a temporary Redis client:

```bash
kubectl -n demo run redis-check --rm -it --restart=Never \
  --image=redis:7-alpine -- redis-cli -h demo-redis
```

Then:

```text
PING
SET demo:message "hello MTS"
GET demo:message
```

## 5. Configure an application

```yaml
env:
  - name: REDIS_HOST
    value: demo-redis
  - name: REDIS_PORT
    value: "6379"
  - name: REDIS_PASSWORD
    valueFrom:
      secretKeyRef:
        name: REPLACE_WITH_REDIS_SECRET
        key: password
```

For an application outside MKP, use the shared MTS database hostname rather than hard-coding `192.168.1.241`:

```text
mts-db.magus.lab:<redis-nodeport>
```

Find the allocated port:

```bash
kubectl -n demo get service demo-redis \
  -o jsonpath='{.spec.ports[?(@.name=="redis")].nodePort}{"\n"}'
```

Existing MTS workloads use Redis NodePorts such as `32306`, `32307`, and `30606`. Each KubeBlocks Redis Service can have a different assigned port.

## Topic Q&A

### 1. Is Redis a source-of-truth database?
Usually no. Use it intentionally for cache or transient data with expiry.

### 2. What does standalone topology mean?
The demo creates one Redis instance rather than a replication/sentinel topology.

### 3. Does persistent storage guarantee durability?
No. Retention, backup, application semantics, and failure mode still matter.

### 4. Should keys have TTLs?
Use TTLs for cache entries unless data-lifetime requirements say otherwise.

### 5. Should Redis be publicly exposed?
No. Prefer cluster-internal access unless a specific approved network need exists.

## MTS Labs Q&A

### 1. Which StorageClass does the demo use?
`truenas-nfs`.

### 2. Which external hostname is used by MTS?
`mts-db.magus.lab`, backed by the current internal address `192.168.1.241`.

### 3. Are MTS Redis ports fixed?
No. Existing examples use different NodePorts; read the Service's actual port.

### 4. Which labels select KubeBlocks Redis pods?
`app.kubernetes.io/instance` and `apps.kubeblocks.io/component-name: redis`.

### 5. Where should the application get its password?
From the generated MTS/KubeBlocks Secret, through `secretKeyRef`.

## Troubleshooting questions

### Why does Redis remain unavailable?
Check the KubeBlocks Cluster status, pod events, PVC, and generated Service endpoints.

### Why can the temporary pod not resolve `demo-redis`?
Confirm it runs in namespace `demo` and the Service exists there.

### Why does `AUTH` fail?
Verify the installed component's generated credential Secret and key names.

### Why does external connection to `mts-db.magus.lab` fail?
Verify the VPN, firewall path, NodePort assigned to this Redis Service, and Service type.

