# 💻 Browser IDE: Node.js

Welcome to the copyable source browser for the [Node.js tutorial](../12-jenkins-node.md). Expand a file to read it. Select the code block's copy action, then save it using the displayed path.

> [!NOTE]
> This page requires no JavaScript. If Outline removes HTML details elements, the file contents remain visible as ordinary Markdown code blocks.

## Explorer

```text
📁 node
│   └── 📄 Dockerfile
│   └── 📄 Jenkinsfile
│   └── 📄 package.json
│   └── 📄 pipeline.yml
│   ├── 📁 src
│   │   └── 📄 app.js
│   │   └── 📄 server.js
│   ├── 📁 test
│   │   └── 📄 app.test.js
```

## Save the complete starter

1. Create a local folder named `node`.
2. Expand each file below.
3. Copy its code block into a file at the exact displayed path.
4. Commit the copied folder as the root of a new application repository.

A separate whole-folder ZIP/download link can be added later without changing any of the source shown on this page.

## Files

<details>
<summary><strong>📄 Dockerfile</strong></summary>

**Save as:** `Dockerfile`

```dockerfile
FROM node:20-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY src ./src
USER node
EXPOSE 3000
CMD ["npm", "start"]
```

</details>

<details>
<summary><strong>📄 Jenkinsfile</strong></summary>

**Save as:** `Jenkinsfile`

```groovy
library identifier: 'buildPipeline@master',
  retriever: modernSCM([
    $class: 'GitSCMSource',
    credentialsId: 'github-repo-token',
    remote: 'https://github.com/MagusTechSolutions/mts-jenkins-lib.git'
  ])

buildPipeline(configFile: 'pipeline.yml')
```

</details>

<details>
<summary><strong>📄 package.json</strong></summary>

**Save as:** `package.json`

```json
{
  "name": "demo-node",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "start": "node src/server.js",
    "test": "node --test"
  },
  "engines": {
    "node": ">=20"
  }
}
```

</details>

<details>
<summary><strong>📄 pipeline.yml</strong></summary>

**Save as:** `pipeline.yml`

```yaml
app: demo-node
stack: nodejs
project: demo
artifacts:
  - 'imageRef.properties'
  - 'pipeline.properties'

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

</details>

<details>
<summary><strong>📄 src/app.js</strong></summary>

**Save as:** `src/app.js`

```javascript
import http from "node:http";

export function createServer() {
  return http.createServer((request, response) => {
    response.setHeader("Content-Type", "application/json");

    if (request.url === "/health") {
      response.end(JSON.stringify({ status: "ok" }));
      return;
    }

    response.end(JSON.stringify({ message: "Hello from MTS Node.js" }));
  });
}
```

</details>

<details>
<summary><strong>📄 src/server.js</strong></summary>

**Save as:** `src/server.js`

```javascript
import { createServer } from "./app.js";

const port = Number.parseInt(process.env.PORT ?? "3000", 10);
const server = createServer();

server.listen(port, "0.0.0.0", () => {
  console.log(`MTS Node demo listening on ${port}`);
});
```

</details>

<details>
<summary><strong>📄 test/app.test.js</strong></summary>

**Save as:** `test/app.test.js`

```javascript
import assert from "node:assert/strict";
import test from "node:test";
import { once } from "node:events";
import { createServer } from "../src/app.js";

test("GET / returns the demo message", async (t) => {
  const server = createServer();
  server.listen(0);
  await once(server, "listening");
  t.after(() => server.close());

  const address = server.address();
  const response = await fetch(`http://127.0.0.1:${address.port}/`);

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { message: "Hello from MTS Node.js" });
});

test("GET /health reports ready", async (t) => {
  const server = createServer();
  server.listen(0);
  await once(server, "listening");
  t.after(() => server.close());

  const address = server.address();
  const response = await fetch(`http://127.0.0.1:${address.port}/health`);

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { status: "ok" });
});
```

</details>
