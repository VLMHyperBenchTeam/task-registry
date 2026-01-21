import pytest
import yaml
import os
from pathlib import Path
from task_registry.manager import RegistryManager
from task_registry.schemas import SourceType, RunTaskSchema, ModelConfig

@pytest.fixture
def registry_setup(tmp_path):
    """
    Setup a temporary registry structure for testing.
    
    Args:
        tmp_path (Path): Pytest temporary directory fixture.
        
    Returns:
        Path: Path to the root registry directory.
    """
    reg_dir = tmp_path / "registries"
    (reg_dir / "packages").mkdir(parents=True)
    (reg_dir / "tasks").mkdir(parents=True)
    (reg_dir / "metrics").mkdir(parents=True)
    
    # Create a package
    pkg_data = {
        "name": "vqa_dataset",
        "source": {"type": "git", "url": "http://github.com/vqa"}
    }
    with open(reg_dir / "packages" / "vqa_dataset.yaml", "w") as f:
        yaml.dump(pkg_data, f)
        
    # Create a dev override
    pkg_dev_data = {
        "source": {"type": "local", "path": "./local/vqa"}
    }
    with open(reg_dir / "packages" / "vqa_dataset.dev.yaml", "w") as f:
        yaml.dump(pkg_dev_data, f)
        
    # Create a task
    task_data = {
        "name": "VQA",
        "entry_point": "vqa.main",
        "supported_metrics": ["anls"]
    }
    with open(reg_dir / "tasks" / "VQA.yaml", "w") as f:
        yaml.dump(task_data, f)
        
    return reg_dir

def test_manager_prod_mode(registry_setup):
    """
    Test that the manager correctly loads base configs in prod mode.
    """
    manager = RegistryManager(registry_setup, run_mode="prod")
    pkg = manager.get_package("vqa_dataset")
    assert pkg.source.type == SourceType.GIT
    assert pkg.source.url == "http://github.com/vqa"

def test_manager_dev_mode(registry_setup):
    """
    Test that the manager correctly applies dev overrides in dev mode.
    """
    manager = RegistryManager(registry_setup, run_mode="dev")
    pkg = manager.get_package("vqa_dataset")
    assert pkg.source.type == SourceType.LOCAL
    assert pkg.source.path == "./local/vqa"

def test_cross_validation(registry_setup):
    """
    Test that cross-validation between RunTask and MLTask works correctly.
    """
    manager = RegistryManager(registry_setup, run_mode="prod")
    
    run = RunTaskSchema(
        name="test_run",
        ml_task="VQA",
        model=ModelConfig(name="qwen"),
        dataset="some_ds",
        metrics=["anls"]
    )
    
    # Should not raise
    manager.validate_run(run)
    
    # Should raise for unsupported metric
    run.metrics = ["unsupported"]
    with pytest.raises(ValueError, match="not supported"):
        manager.validate_run(run)