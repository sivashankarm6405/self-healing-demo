# Self-Healing CI/CD Pipeline

A Jenkins CI/CD pipeline that automatically analyzes and fixes build failures using a **local AI model**, without sending source code to the cloud.

## How It Works

```text
Developer
   ↓
GitHub
   ↓
Jenkins
   ↓
Maven Build
   ↓
Build Fails
   ↓
healing_script.py
   ↓
Ollama (localhost:11434)
   ↓
qwen2.5-coder:3b
   ↓
Generated Fix
   ↓
New Git Branch + Commit
   ↓
GitHub Pull Request
   ↓
Human Review & Merge
   ↓
Jenkins Build Again
```

## Components

| Component             | Purpose                                       |
| --------------------- | --------------------------------------------- |
| **Jenkins**           | Runs the CI/CD pipeline and triggers builds   |
| **Maven**             | Builds the Java project                       |
| **Python**            | Handles the healing workflow                  |
| **Ollama**            | Runs the AI model locally                     |
| **qwen2.5-coder:3b**  | Analyzes failures and generates fixes         |
| **Git**               | Creates branches, commits, and pushes changes |
| **GitHub CLI (`gh`)** | Creates Pull Requests automatically           |

## Why Local AI?

* 🔒 Source code stays on the local machine
* ☁️ No cloud AI API required
* 💰 No API costs or rate limits
* 🌐 Works without internet after the model is downloaded
* ⚡ Suitable for small and straightforward build fixes

The tradeoff is that `qwen2.5-coder:3b` is a small model and is better suited for simple fixes rather than complex bugs or architectural changes.

## Requirements

* Jenkins
* JDK 17+
* Maven
* Python 3
* Git
* GitHub CLI (`gh`)
* Ollama
* `qwen2.5-coder:3b`

## Setup

### Ollama

Pull the model:

```bash
ollama pull qwen2.5-coder:3b
```

Ollama runs locally at:

```text
http://localhost:11434
```

It can also be started manually with:

```bash
ollama serve
```

### Python

Install the required package:

```bash
pip install requests
```

### Jenkins

Create a Jenkins **Pipeline** job and configure it to use the `Jenkinsfile` from the repository.

Configure:

* JDK and Maven through Jenkins Global Tool Configuration
* GitHub credentials through Jenkins Credentials
* Required Git/GitHub CLI access for the pipeline

> **Windows Note:** Jenkins commonly runs as a Windows service under a different account than your normal user. Therefore, your personal `PATH`, Git configuration, and `gh auth login` session may not be available to Jenkins. Configure tools and credentials explicitly inside Jenkins.

## Project Structure

```text
self-healing-cicd/
│
├── Jenkinsfile
├── healing_script.py
├── pom.xml
├── src/
│   └── ...
└── README.md
```

## Key Files

**`Jenkinsfile`**
Defines the CI/CD workflow and handles build failures.

**`healing_script.py`**
Reads the build failure, communicates with Ollama, applies the generated fix, and handles Git operations.

**`pom.xml`**
Contains the Maven project configuration.

## Workflow

When a build fails:

1. Jenkins captures the failure.
2. `healing_script.py` reads the build error.
3. The error is sent to the local Ollama instance.
4. `qwen2.5-coder:3b` analyzes the problem and generates a fix.
5. The script applies the fix.
6. A new Git branch is created.
7. The fix is committed and pushed.
8. GitHub CLI creates a Pull Request.
9. A developer reviews and merges the change.
10. Jenkins runs the build again.

**The AI proposes the fix; the developer makes the final decision.**
