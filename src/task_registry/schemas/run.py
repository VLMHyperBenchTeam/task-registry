from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel
from .base import BaseRegistryModel, DependencySource

class PackageManagerType(str, Enum):
    PIP = "pip"
    UV = "uv"
    CONDA = "conda"

class ModelConfig(BaseModel):
    """
    Model configuration.
    """
    name: str
    framework: str = "vllm"
    docker_image: Optional[str] = None
    package_manager: PackageManagerType = PackageManagerType.PIP
    params: Dict[str, Any] = {}

class RunTaskSchema(BaseRegistryModel):
    """
    Single run definition schema.
    
    Attributes:
        ml_task: Name of the MLTask to execute.
        model: Model configuration.
        dataset: Name of the dataset instance.
        metrics: List of metric instance names to calculate.
        reports: List of report instance names to generate.
    """
    ml_task: str
    model: ModelConfig
    dataset: str
    metrics: List[str] = []
    reports: List[str] = []