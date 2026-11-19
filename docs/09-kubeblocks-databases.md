# 🗄️ PostgreSQL with KubeBlocks

Welcome to managed databases on MKP. KubeBlocks represents a database cluster as a Kubernetes custom resource and keeps operational details behind a consistent `Cluster` interface.

> **Open the starter in a browser IDE:** [KubeBlocks source browser](code-browser/kubeblocks.md). It contains the PostgreSQL, Redis, and MinIO files together.

## 1. Confirm prerequisites

```bash
kubectl api-resources | grep -i kubeblocks
kubectl get crd | grep kubeblocks
kubectl get storageclass
```

Confirm with your administrator:

- the installed KubeBlocks version;
- `clusterDef: postgresql`;
- `componentDef: postgresql`;
- which namespaces may create database clusters.

The MTS KubeBlocks StorageClass is:

```text
truenas-nfs
```

## 2. Deploy the cluster

Adapt this MTS pattern:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: demo-db
  namespace: demo
spec:
  clusterDef: postgresql
  topology: replication
  terminationPolicy: DoNotTerminate
  componentSpecs:
    - name: postgresql
      componentDef: postgresql
      replicas: 1
      resources:
        requests:
          cpu: 100m
          memory: 512Mi
        limits:
          cpu: 500m
          memory: 1Gi
      volumeClaimTemplates:
        - name: data
          spec:
            storageClassName: truenas-nfs
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 5Gi
```

## 3. Expose the primary

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-db
  namespace: demo
spec:
  type: NodePort
  selector:
    app.kubernetes.io/instance: demo-db
    apps.kubeblocks.io/component-name: postgresql
    kubeblocks.io/role: primary
  ports:
    - name: postgres
      port: 5432
      targetPort: 5432
```

For applications inside Kubernetes, prefer `ClusterIP`. MTS applications that are outside the cluster can use the shared host:

```text
mts-db.magus.lab
```

The production configurations map that hostname to `192.168.1.241`. Use the DNS hostname so an infrastructure address can change without changing every application.

The hostname is shared, but each Service gets a different port. Query the actual assigned port:

```bash
kubectl -n demo get service demo-db \
  -o jsonpath='{.spec.ports[?(@.name=="postgres")].nodePort}{"\n"}'
```

Existing MTS production examples include PostgreSQL NodePorts such as `31446`, `31447`, and `32486`; do not assume one port belongs to every database.

## 4. Check readiness

```bash
kubectl -n demo get cluster demo-db
kubectl -n demo get pods -l app.kubernetes.io/instance=demo-db
kubectl -n demo get pvc -l app.kubernetes.io/instance=demo-db
kubectl -n demo describe cluster demo-db
kubectl -n demo get events --sort-by=.lastTimestamp
```

## 5. Find generated credentials

```bash
kubectl -n demo get secrets | grep demo-db
```

MTS initialization jobs reference a generated PostgreSQL account secret pattern:

```text
demo-db-postgresql-account-postgres
```

List keys rather than printing values:

```bash
kubectl -n demo get secret demo-db-postgresql-account-postgres \
  -o jsonpath='{.data}' | jq 'keys'
```

> [!CAUTION]
> Do not use `kubectl get secret -o yaml` in a shared terminal, screen share, or CI log.

## 6. Connect from an application

Inject only the required values:

```yaml
env:
  - name: DATABASE_URL
    value: jdbc:postgresql://demo-db:5432/REPLACE_WITH_DATABASE
  - name: DATABASE_USERNAME
    valueFrom:
      secretKeyRef:
        name: demo-db-postgresql-account-postgres
        key: username
  - name: DATABASE_PASSWORD
    valueFrom:
      secretKeyRef:
        name: demo-db-postgresql-account-postgres
        key: password
```

For an application connecting from outside MKP:

```text
jdbc:postgresql://mts-db.magus.lab:<demo-db-nodeport>/<database>
```

## Topic Q&A

### 1. What is a KubeBlocks `Cluster`?
A Kubernetes custom resource representing a managed database topology.

### 2. Does `DoNotTerminate` replace backups?
No. It protects against ordinary deletion but does not provide recovery.

### 3. What is a topology?
The database arrangement, such as single-instance or replication.

### 4. Why mount persistent storage?
It preserves database files across pod replacement.

### 5. When is `NodePort` useful?
When approved clients outside the cluster must reach the Service.

## MTS Labs Q&A

### 1. Which StorageClass is used by MTS KubeBlocks examples?
`truenas-nfs`.

### 2. Which shared hostname reaches MTS database ports externally?
`mts-db.magus.lab`, currently mapped in production configuration to `192.168.1.241`.

### 3. Is the port identical for every PostgreSQL database?
No. Each NodePort is independently allocated.

### 4. Which component definition does this example expect?
`postgresql`, matching the installed MTS KubeBlocks addon.

### 5. How do MTS applications obtain database credentials?
From generated account Secrets referenced through `secretKeyRef`, not embedded in YAML.

## Troubleshooting questions

### Why is the Cluster not progressing?
Describe it and inspect KubeBlocks events, CR status, component definition, and StorageClass.

### Why is the PVC `Pending`?
Verify `truenas-nfs` exists and has enough permitted capacity.

### Why is the primary selector empty?
Check KubeBlocks labels and the `kubeblocks.io/role: primary` label on the generated pods.

### Why does `mts-db.magus.lab` connect to the wrong service?
Read the actual NodePort assigned to this Service; the hostname is shared across services.

