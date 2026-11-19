# Spinnaker Kubernetes starter

This template follows the MTS Kustomize and `bakeManifest` to `deployManifest` pattern.

Replace:

- `REPLACE_WITH_GIT_ARTIFACT_ACCOUNT`
- `REPLACE_WITH_KUBERNETES_ACCOUNT`
- the deployment repository URL and version in `pipeline.json`

Jenkins should provide `image`, `namespace`, and `appname` as pipeline parameters. The deployment base uses `app-image`; the dev overlay replaces it with `${image}`.

Import `pipeline.json` through the Spinnaker pipeline configuration workflow supported by your MTS environment, then generate a fresh expected-artifact ID through Spinnaker rather than reusing the placeholder.

