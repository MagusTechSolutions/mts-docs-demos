# KubeBlocks demo manifests

These manifests use the shared MTS KubeBlocks StorageClass:

```text
truenas-nfs
```

For external MTS clients, use `mts-db.magus.lab` rather than hard-coding its current address (`192.168.1.241`). PostgreSQL, Redis, and MinIO have separate NodePorts; read each port from its Service before connecting.

Apply only after confirming the KubeBlocks `Cluster`, PostgreSQL, Redis, and MinIO component definitions installed in the cluster.

```bash
kubectl -n demo apply -f postgres-cluster.yml
kubectl -n demo apply -f postgres-service.yml
kubectl -n demo apply -f redis-cluster.yml
kubectl -n demo apply -f redis-service.yml
kubectl -n demo apply -f minio-cluster.yml
kubectl -n demo apply -f minio-service.yml
kubectl -n demo apply -f minio-bucket-job.yml
```

