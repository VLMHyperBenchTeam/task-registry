import os
import yaml
from typing import Dict, Any, Optional, List, Type, TypeVar
from pathlib import Path
from .schemas import (
    PackageDefinition, MLTaskSchema, DatasetSchema, 
    MetricSchema, ReportSchema, RunTaskSchema, ExperimentPlanSchema,
    BaseRegistryModel
)

T = TypeVar("T", bound=BaseRegistryModel)

class RegistryManager:
    """
    Manager for loading and validating registry items with RUN_MODE support.
    
    This manager handles hierarchical YAML configuration files and applies
    environment-specific overrides based on RUN_MODE.
    """
    
    def __init__(self, root_dir: str, run_mode: str = "prod"):
        """
        Initialize the RegistryManager.
        
        Args:
            root_dir (str): Root directory of the registries (e.g., vlmhyperbench/registries).
            run_mode (str): Execution mode ('dev' or 'prod'). Defaults to 'prod'.
        """
        self.root_dir = Path(root_dir)
        self.run_mode = run_mode
        self._cache: Dict[str, Dict[str, Any]] = {
            "packages": {},
            "tasks": {},
            "datasets": {},
            "metrics": {},
            "reports": {},
            "runs": {},
            "experiments": {}
        }

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """
        Load and parse a YAML file.
        
        Args:
            path (Path): Path to the YAML file.
            
        Returns:
            Dict[str, Any]: Parsed YAML content.
        """
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _get_item_path(self, category: str, name: str, dev: bool = False) -> Path:
        """
        Get the path to a registry item.
        
        Args:
            category (str): Registry category folder name.
            name (str): Item name (without extension).
            dev (bool): Whether to look for a dev override file.
            
        Returns:
            Path: Path to the YAML file.
        """
        ext = ".dev.yaml" if dev else ".yaml"
        return self.root_dir / category / f"{name}{ext}"

    def _load_and_merge(self, category: str, name: str) -> Dict[str, Any]:
        """
        Load base and dev YAMLs and merge them if in dev mode.
        
        Args:
            category (str): Registry category folder name.
            name (str): Item name.
            
        Returns:
            Dict[str, Any]: Merged configuration data.
            
        Raises:
            FileNotFoundError: If the base configuration file does not exist.
        """
        base_path = self._get_item_path(category, name)
        if not base_path.exists():
            raise FileNotFoundError(f"Base config not found: {base_path}")
        
        data = self._load_yaml(base_path)
        
        if self.run_mode == "dev":
            dev_path = self._get_item_path(category, name, dev=True)
            if dev_path.exists():
                dev_data = self._load_yaml(dev_path)
                # Simple shallow merge for now
                data.update(dev_data)
        
        return data

    def get_package(self, name: str) -> PackageDefinition:
        """
        Get a package definition from registry.
        
        Args:
            name (str): Package name.
            
        Returns:
            PackageDefinition: Validated package definition.
        """
        if name not in self._cache["packages"]:
            data = self._load_and_merge("packages", name)
            self._cache["packages"][name] = PackageDefinition(**data)
        return self._cache["packages"][name]

    def get_task(self, name: str) -> MLTaskSchema:
        """
        Get an ML task definition from registry.
        
        Args:
            name (str): Task name.
            
        Returns:
            MLTaskSchema: Validated task definition.
        """
        if name not in self._cache["tasks"]:
            data = self._load_and_merge("tasks", name)
            self._cache["tasks"][name] = MLTaskSchema(**data)
        return self._cache["tasks"][name]

    def get_dataset(self, name: str) -> DatasetSchema:
        """
        Get a dataset definition from registry.
        
        Args:
            name (str): Dataset name.
            
        Returns:
            DatasetSchema: Validated dataset definition.
        """
        if name not in self._cache["datasets"]:
            data = self._load_and_merge("datasets", name)
            self._cache["datasets"][name] = DatasetSchema(**data)
        return self._cache["datasets"][name]

    def get_metric(self, name: str) -> MetricSchema:
        """
        Get a metric definition from registry.
        
        Args:
            name (str): Metric name.
            
        Returns:
            MetricSchema: Validated metric definition.
        """
        if name not in self._cache["metrics"]:
            data = self._load_and_merge("metrics", name)
            self._cache["metrics"][name] = MetricSchema(**data)
        return self._cache["metrics"][name]

    def get_report(self, name: str) -> ReportSchema:
        """
        Get a report definition from registry.
        
        Args:
            name (str): Report name.
            
        Returns:
            ReportSchema: Validated report definition.
        """
        if name not in self._cache["reports"]:
            data = self._load_and_merge("reports", name)
            self._cache["reports"][name] = ReportSchema(**data)
        return self._cache["reports"][name]

    def get_run(self, name: str) -> RunTaskSchema:
        """
        Get a run task definition from registry.
        
        Args:
            name (str): Run name.
            
        Returns:
            RunTaskSchema: Validated run task definition.
        """
        if name not in self._cache["runs"]:
            data = self._load_and_merge("runs", name)
            self._cache["runs"][name] = RunTaskSchema(**data)
        return self._cache["runs"][name]

    def get_experiment(self, name: str) -> ExperimentPlanSchema:
        """
        Get an experiment plan from registry.
        
        Args:
            name (str): Experiment name.
            
        Returns:
            ExperimentPlanSchema: Validated experiment plan.
        """
        if name not in self._cache["experiments"]:
            data = self._load_and_merge("experiments", name)
            self._cache["experiments"][name] = ExperimentPlanSchema(**data)
        return self._cache["experiments"][name]

    def validate_run(self, run: RunTaskSchema):
        """
        Perform cross-validation for a RunTask.
        
        Checks if metrics and reports requested in the run are supported
         by the associated MLTask.
        
        Args:
            run (RunTaskSchema): The run configuration to validate.
            
        Raises:
            ValueError: If an unsupported metric or report is found.
        """
        task = self.get_task(run.ml_task)
        
        # Validate metrics
        for m_name in run.metrics:
            if m_name not in task.supported_metrics:
                raise ValueError(
                    f"Metric '{m_name}' is not supported by task '{task.name}'. "
                    f"Supported metrics: {task.supported_metrics}"
                )
        
        # Validate reports
        for r_name in run.reports:
            if r_name not in task.supported_reports:
                raise ValueError(
                    f"Report '{r_name}' is not supported by task '{task.name}'. "
                    f"Supported reports: {task.supported_reports}"
                )