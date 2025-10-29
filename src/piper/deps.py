import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: str | None = None):
    """
    executes a shell command with error checking.

    A wrapper around subprocess.run that will automatically check for success
    and raises an exception if the command fails.

    Args:
        cmd: list of command and arguments to execute
        cwd: working directory for command execution
    """
    subprocess.run(cmd, cwd=cwd, check=True)


def install_for(detection: dict, cwd: str = "."):
    """
    install the dependencies for detected project types.

    analyzes detection results and runs appropriate package manager
    commands to install dependencies for each detected technology stack.

    Args:
        detection: dictionary containing detected project types and signals
        cwd: working directory for installation commands
    """
    types = detection.get("types", [])

    # python dependency installation
    if "python" in types:
        requirements_file = Path(cwd) / "requirements.txt"
        if requirements_file.exists():
            # upgrade core packaging tools and install from requirements
            run([sys.executable, "-m", "pip", "install", "-U", "pip", "setuptools", "wheel"])
            run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=cwd)
        else:
            # install default Python testing tools if no requirements file
            run([sys.executable, "-m", "pip", "install", "-U", "pip", "setuptools", "wheel"])
            run([sys.executable, "-m", "pip", "install", "pytest"], cwd=cwd)

    # Node.js dependency installation with package manager detection
    if "node" in types:
        # detect package manager based on lock file presence
        lock_file = (
            "pnpm-lock.yaml"
            if Path(cwd, "pnpm-lock.yaml").exists()
            else (
                "yarn.lock"
                if Path(cwd, "yarn.lock").exists()
                else "package-lock.json" if Path(cwd, "package-lock.json").exists() else None
            )
        )

        if lock_file and lock_file.endswith("pnpm-lock.yaml"):
            run(["pnpm", "install", "--frozen-lockfile"], cwd=cwd)
        elif lock_file and lock_file.endswith("yarn.lock"):
            run(["yarn", "install", "--frozen-lockfile"], cwd=cwd)
        else:
            # using npm with ci for exact reproduction or install for flexibility
            run(["npm", "ci" if lock_file else "install"], cwd=cwd)

    # rust dependency updates
    if "rust" in types:
        run(["cargo", "update"], cwd=cwd)

    # Go module dependency download
    if "go" in types:
        run(["go", "mod", "download"], cwd=cwd)
