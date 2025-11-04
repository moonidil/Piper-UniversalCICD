from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

__all__ = ["run", "install_for"]


def run(cmd: list[str], cwd: str | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def install_for(detection: Dict[str, Any], cwd: str = ".") -> None:
    types = detection.get("types", [])
    root = Path(cwd)

    if "python" in types:
        req = root / "requirements.txt"
        if req.exists():
            run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
                cwd=cwd,
            )
            run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=cwd)
        else:
            pyproject = root / "pyproject.toml"
            if pyproject.exists():
                run([sys.executable, "-m", "pip", "install", "."], cwd=cwd)

    if "node" in types:
        npm_lock = root / "package-lock.json"
        pnpm_lock = root / "pnpm-lock.yaml"
        yarn_lock = root / "yarn.lock"

        if npm_lock.exists():
            run(["npm", "ci"], cwd=cwd)
        elif pnpm_lock.exists():
            run(["pnpm", "install", "--frozen-lockfile"], cwd=cwd)
        elif yarn_lock.exists():
            run(["yarn", "install", "--frozen-lockfile"], cwd=cwd)
        else:
            pkg = root / "package.json"
            if pkg.exists():
                run(["npm", "install"], cwd=cwd)

    if "rust" in types:
        cargo_toml = root / "Cargo.toml"
        if cargo_toml.exists():
            run(["cargo", "fetch"], cwd=cwd)

    if "go" in types:
        go_mod = root / "go.mod"
        if go_mod.exists():
            run(["go", "mod", "download"], cwd=cwd)
