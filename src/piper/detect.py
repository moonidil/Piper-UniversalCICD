from pathlib import Path
import json
from typing import Dict, List, Optional, TypedDict


class Detection(TypedDict):
    types: List[str]
    framework: Optional[str]
    deploy: Optional[str]
    signals: Dict[str, List[str]]


# mapping of technology types to their identifying configuration files
SIGNALS: Dict[str, List[str]] = {
    "node": ["package.json", "pnpm-lock.yaml", "yarn.lock"],
    "python": ["requirements.txt", "pyproject.toml", "tox.ini"],
    "rust": ["Cargo.toml"],
    "go": ["go.mod"],
    "docker": ["Dockerfile", "docker-compose.yml"],
    "next": ["next.config.js", "next.config.mjs"],
    "vue": ["vue.config.js", "vite.config.ts", "vite.config.js"],
    "vercel": ["vercel.json"],
    "netlify": ["netlify.toml"],
    "heroku": ["Procfile"],
    "railway": ["railway.json", "railway.toml"],
}


def scan(root: str = ".") -> Detection:
    """
    scan directory for technology indicators and detect project configuration

    Returns:
        dict: detected project types, framework, deployment targets and signal files
    """
    p = Path(root)
    found: Dict[str, List[str]] = {k: [] for k in SIGNALS.keys()}

    # check for each signal file in the target directory
    for tech_type, files in SIGNALS.items():
        for file in files:
            if (p / file).exists():
                found[tech_type].append(file)

    # determine primary technology types
    types_list: List[str] = []
    if found["node"]:
        types_list.append("node")
    if found["python"]:
        types_list.append("python")
    if found["rust"]:
        types_list.append("rust")
    if found["go"]:
        types_list.append("go")

    # detect framework with priority order
    framework: Optional[str] = "next" if found["next"] else ("vue" if found["vue"] else None)

    # detect deployment platform with fallback to docker
    deploy: Optional[str] = None
    if found["vercel"]:
        deploy = "vercel"
    elif found["netlify"]:
        deploy = "netlify"
    elif found["heroku"]:
        deploy = "heroku"
    elif found["railway"]:
        deploy = "railway"
    elif found["docker"]:
        deploy = "docker"

    return {"types": types_list, "framework": framework, "deploy": deploy, "signals": found}


def write_report(data: Detection, path: str = ".pipeline/detection.json") -> str:
    """
    Write detection results as JSON report to specified path

    creates parent directories if needed and then returns the output path
    """
    # ensure output directory exists
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    # write formatted JSON data
    Path(path).write_text(json.dumps(data, indent=2))
    return path
