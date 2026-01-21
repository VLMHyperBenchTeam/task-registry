# Task Registry

**English** | [Русский](README.ru.md)

A universal configuration and registry management system for ML projects, built on Pydantic v2 and principles of dynamic composition.

## Features
- **Strict Validation**: Leveraging Pydantic v2 for type checking and logical data consistency.
- **Dynamic Composition**: Support for various code sources (Local, Git, PyPI) via the `DependencySource` schema.
- **Execution Modes (RUN_MODE)**: Seamless switching between `dev` (local development with overlays) and `prod` (stable releases).
- **Atomicity**: Each component (task, dataset, metric) is described by a separate YAML file.
- **LEGO-style Architecture**: The package is fully autonomous and can be used in any project independently of VLMHyperBench.

## Installation
Requires Python 3.13+ and [uv](https://github.com/astral-sh/uv).

```bash
uv pip install git+https://github.com/VLMHyperBenchTeam/task-registry.git
```

## Quick Start
Example of using `RegistryManager`:

```python
from task_registry.manager import RegistryManager

# Initialize the manager (point to your YAML registries)
manager = RegistryManager(root_dir="path/to/registries", run_mode="dev")

# Load and validate a task
task = manager.get_task("VQA")
print(f"Loaded task: {task.name}, entry point: {task.entry_point}")
```

## Registry Structure
Recommended directory structure:
```text
registries/
├── packages/    # Package source definitions
├── tasks/       # ML Task types
├── metrics/     # Metric instances
├── datasets/    # Data descriptions
└── runs/        # Specific run configurations
```

## License
MIT