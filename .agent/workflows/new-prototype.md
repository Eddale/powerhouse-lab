---
description: Create a new Powerhouse Lab prototype with proper configuration
---

Use this workflow when the user asks to "start a new prototype" or "create a new project".

1.  **Ask for the Prototype Name**
    - If not provided, ask the user for a "kebab-case" name (e.g., `marketing-agent`).

2.  **Git Preparation**
    - `git checkout main`
    - `git pull`
    - `git checkout -b prototype/<name>` (Creates a clean isolated branch)

3.  **Folder Setup**
    - `mkdir prototypes/<name>`
    
4.  **Template Injection**
    - `cp powerhouse-lab/CLAUDE.md prototypes/<name>/` (Copies Iron Rules)
    - `cp -r powerhouse-lab/_templates/tool-template/* prototypes/<name>/` (Copies structure)
    
5.  **Workspace Configuration**
    - Create `prototypes/<name>/<name>.code-workspace`:
    ```json
    {
        "folders": [
            { "path": "." }
        ],
        "settings": {
            "git.autofetch": true
        }
    }
    ```

6.  **Task Initialization**
    - Update `prototypes/<name>/tasks/todo.md` with the specific project goals.

7.  **Final Commit**
    - `git add prototypes/<name>`
    - `git commit -m "feat: Initialize <name> prototype"`
    - Notify user that the environment is ready.
