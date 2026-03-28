#!/usr/bin/env python3
"""
Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config.json at runtime,
then launches `nanobot gateway`.
"""

import json
import os
import re
from pathlib import Path


def resolve_env_vars(obj):
    """Recursively resolve ${VAR} placeholders in config values."""
    if isinstance(obj, dict):
        return {k: resolve_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_env_vars(item) for item in obj]
    elif isinstance(obj, str):
        # Match ${VAR} pattern
        pattern = r"\$\{([^}]+)\}"
        match = re.fullmatch(pattern, obj)
        if match:
            # Entire value is a single ${VAR}
            var_name = match.group(1)
            return os.environ.get(var_name, obj)
        else:
            # Replace all ${VAR} occurrences in the string
            def replacer(m):
                return os.environ.get(m.group(1), m.group(0))

            return re.sub(pattern, replacer, obj)
    else:
        return obj


def main():
    # Paths
    app_dir = Path(__file__).parent
    config_path = app_dir / "config.json"
    workspace_dir = app_dir / "workspace"
    resolved_path = app_dir / "config.resolved.json"

    # Load original config
    with open(config_path, "r") as f:
        config = json.load(f)

    # Resolve all ${VAR} placeholders
    config = resolve_env_vars(config)

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    # Launch nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            str(workspace_dir),
        ],
    )


if __name__ == "__main__":
    main()
