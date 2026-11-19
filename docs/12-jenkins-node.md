# 🟢 Jenkins demo: Node.js

This demo creates a tiny Node HTTP service, tests it with Node's built-in test runner, and builds an image with the MTS Node pipeline.

Use [examples/node](../examples/node/) as the complete starter.

> **Open the starter in a browser IDE:** [Node.js source browser](code-browser/node.md). You can expand, copy, and save every file.

## 1. Run locally

```bash
npm install
npm test
npm start
```

Verify:

```bash
curl http://localhost:3000/
curl http://localhost:3000/health
```

## 2. Configure `pipeline.yml`

```yaml
app: demo-node
stack: nodejs
project: demo
artifacts:
  - 'imageRef.properties'
  - 'pipeline.properties'
```

The Node pipeline's default build sequence is:

```bash
npm install
npm test
npm run build --if-present
```

Therefore `npm test` must be real and must exit non-zero when a test fails.

## 3. Build the image

```bash
docker build -t demo-node:local .
docker run --rm -p 3000:3000 demo-node:local
```

## 4. Attach a Spinnaker contract

```yaml
spinnaker_app: demo-node
environments:
  - name: feature/
    deploy: true
    spinnaker:
      pipeline: deploy-dev
      parameters:
        namespace: demo
        appname: demo-node
  - name: develop
    deploy: true
    spinnaker:
      pipeline: deploy-dev
      parameters:
        namespace: demo
        appname: demo-node
  - name: master
    deploy: true
    spinnaker:
      pipeline: deploy-prod
      parameters:
        namespace: demo
        appname: demo-node
```

## Topic Q&A

### 1. Which package install command does the default pipeline use?
`npm install`, followed by `npm test` and `npm run build --if-present`.

### 2. Can I use `npm ci`?
Yes with a custom build command and a committed lockfile.

### 3. Does `npm test` need to be meaningful?
Yes. It must exit non-zero when the application contract is broken.

### 4. Should frontend and API repositories use different apps?
Yes. Each independently deployable artifact needs an unambiguous app and image name.

### 5. How should the container stop?
Handle termination signals when stateful work or graceful shutdown matters.

## MTS Labs Q&A

### 1. Which MTS agent runs Node?
`stack: nodejs` maps to the `node20` agent.

### 2. What image name does the demo produce?
`mts-sandbox/demo/demo-node` or `mts-release/demo/demo-node`, based on branch.

### 3. Which health path should MKP probes target?
This starter exposes `/health` on port `3000`.

### 4. Where does Jenkins publish the digest?
In `imageRef.properties` and `pipeline.properties`.

### 5. Which Spinnaker pipeline is used for development?
The demo maps `feature/` and `develop` to `deploy-dev`.

## Troubleshooting questions

### Why does Jenkins report that no test script exists?
Commit a `test` script in `package.json` that exits successfully only when tests pass.

### Why does the image start locally but fail in MKP?
Compare port, environment variables, read-only filesystem assumptions, health path, and image pull permissions.

### Why is `npm install` inconsistent?
Commit a lockfile and consider a custom `npm ci` command.

### Why did the Deployment probe fail?
Confirm the Service and container both use port `3000` and `/health`.

