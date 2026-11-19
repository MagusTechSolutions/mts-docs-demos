# 💻 Browser IDE: Python FastAPI

Welcome to the copyable source browser for the [Python FastAPI tutorial](../05-jenkins-python-fastapi.md). Expand a file to read it. Select the code block's copy action, then save it using the displayed path.

> [!NOTE]
> This page requires no JavaScript. If Outline removes HTML details elements, the file contents remain visible as ordinary Markdown code blocks.

## Explorer

```text
📁 python-fastapi
│   ├── 📁 app
│   │   └── 📄 __init__.py
│   │   └── 📄 main.py
│   └── 📄 Dockerfile
│   └── 📄 Jenkinsfile
│   └── 📄 pipeline.yml
│   └── 📄 pyproject.toml
│   └── 📄 requirements.txt
│   └── 📄 test_main.py
```

## Save the complete starter

1. Create a local folder named `python-fastapi`.
2. Expand each file below.
3. Copy its code block into a file at the exact displayed path.
4. Commit the copied folder as the root of a new application repository.

A separate whole-folder ZIP/download link can be added later without changing any of the source shown on this page.

## Files

<details>
<summary><strong>📄 app/__init__.py</strong></summary>

**Save as:** `app/__init__.py`

```python
"""MTS FastAPI demo package."""
```

</details>

<details>
<summary><strong>📄 app/main.py</strong></summary>

**Save as:** `app/main.py`

```python
from fastapi import FastAPI

app = FastAPI(title="MTS FastAPI Demo")


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello from MTS FastAPI"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

</details>

<details>
<summary><strong>📄 Dockerfile</strong></summary>

**Save as:** `Dockerfile`

```dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt pyproject.toml ./
COPY app ./app
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
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
<summary><strong>📄 pipeline.yml</strong></summary>

**Save as:** `pipeline.yml`

```yaml
app: demo-fastapi
stack: python311
project: demo
artifacts:
  - 'coverage.xml'
  - 'imageRef.properties'
  - 'pipeline.properties'

spinnaker_app: demo-fastapi
environments:
  - name: develop
    deploy: true
    spinnaker:
      pipeline: deploy-dev
      parameters:
        namespace: demo
        appname: demo-fastapi
  - name: master
    deploy: true
    spinnaker:
      pipeline: deploy-prod
      parameters:
        namespace: demo
        appname: demo-fastapi
```

</details>

<details>
<summary><strong>📄 pyproject.toml</strong></summary>

**Save as:** `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "demo-fastapi"
version = "0.1.0"
requires-python = ">=3.11"

[tool.setuptools]
packages = ["app"]
```

</details>

<details>
<summary><strong>📄 requirements.txt</strong></summary>

**Save as:** `requirements.txt`

```text
fastapi==0.121.2
uvicorn[standard]==0.38.0
httpx==0.28.1
pytest==8.4.2
pytest-cov==7.0.0
```

</details>

<details>
<summary><strong>📄 test_main.py</strong></summary>

**Save as:** `test_main.py`

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from MTS FastAPI"}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

</details>
