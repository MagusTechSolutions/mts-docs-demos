# ✅ MKP release readiness checklist

Use this checklist before moving from a local or Jenkins-tested build to an MKP deployment.

## Access and destination

- [ ] MTS Lab VPN is connected.
- [ ] `kubectl oidc-login` authenticates through Authentik.
- [ ] The selected context matches the environment.
- [ ] `kubectl auth whoami` shows the intended identity.
- [ ] `kubectl auth can-i` confirms required namespace actions.

## Source and build

- [ ] The branch is intentional and protected as required.
- [ ] Tests pass and evidence is archived.
- [ ] `pipeline.yml` uses the intended app, project, and stack.
- [ ] Docker builds from the repository root.
- [ ] The built image was pushed and resolved to a digest.

## Deployment contract

- [ ] `IMAGE_NAME` is digest-pinned.
- [ ] `namespace` and `appname` match the Spinnaker pipeline.
- [ ] The Spinnaker application and pipeline exist.
- [ ] The Git artifact and Kubernetes accounts are configured by MTS.
- [ ] Development and production use approved overlays/gates.

## Runtime contract

- [ ] Container port matches Service target port.
- [ ] Readiness and liveness paths work.
- [ ] Resource requests and limits are appropriate.
- [ ] Required Secrets and ConfigMaps exist.
- [ ] No sensitive values are embedded in manifests.
- [ ] Persistent data has an approved backup/restore plan.

## Network and exposure

- [ ] Internal applications use cluster Service DNS.
- [ ] External NodePorts are documented and approved.
- [ ] Ingress hostname follows the selected MKP environment.
- [ ] Certificate/CA expectations are verified.
- [ ] DNS resolves over the MTS VPN or intended client network.

## Verification record

```text
Git commit:
Jenkins build:
Image digest:
Spinnaker execution:
MKP context:
Namespace:
Deployment:
Service:
Ingress/NodePort:
Verified by:
Date:
```

## Rollout verification

```bash
kubectl config current-context
kubectl -n demo rollout status deployment/demo-node
kubectl -n demo get deploy,pod,svc,ingress
kubectl -n demo get endpoints demo-node
kubectl -n demo get events --sort-by=.lastTimestamp
```

## Topic Q&A

### 1. Why use a checklist?
It makes cross-team release assumptions visible and repeatable.

### 2. Which artifact should be approved?
The immutable image digest and matching manifest/configuration.

### 3. Is a green Jenkins build enough?
No. Runtime contracts, RBAC, networking, data, and rollout must also be verified.

### 4. When should production gates be tested?
Before the release window, using the same or equivalent deployment path.

### 5. Who owns the verification record?
The release/service owner, with platform and operations evidence attached.

## MTS Labs Q&A

### 1. How do developers authenticate to MKP?
Through the MTS VPN and supplied Authentik OIDC kubeconfig.

### 2. Which tool publishes the image?
Jenkins through `mts-jenkins-lib` and the MTS registry path.

### 3. Which tool deploys to MKP?
Spinnaker with a Kubernetes account and Kustomize bake stage.

### 4. Which context must be verified for production?
An approved `mkp-p1-*` context; normal developer access may be intentionally limited.

### 5. Which storage policy is required for persistent demos?
Use `truenas-nfs` for the MTS examples and an explicit backup/restore plan.

## Troubleshooting questions

### Why does the checklist fail before build?
Confirm account, VPN, repository, and Jenkins credentials first.

### Why is the image approved but not running?
Trace the digest through Spinnaker, bake output, Deployment spec, and pod events.

### Why can the app run internally but not through ingress?
Check DNS, ingress host/class, TLS, Service selector, and endpoints.

### Why is production blocked after development succeeds?
Production uses separate context, account, RBAC, pipeline gate, and approval requirements.
