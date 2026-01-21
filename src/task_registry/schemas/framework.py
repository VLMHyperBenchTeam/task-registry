from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from .base import BaseRegistryModel

class SpecializedAdapter(BaseModel):
    """Rule for selecting a specialized adapter for specific models."""
    match_models: List[str]
    package: str
    backend_class: str

class FrameworkDefinition(BaseRegistryModel):
    """
    Framework definition in registries/frameworks/*.yaml.
    """
    default_adapter_package: str
    default_backend_class: str
    specialized_adapters: List[SpecializedAdapter] = []