from typing import Optional, Dict, Any
from .base import BaseRegistryModel, DependencySource

class PackageDefinition(BaseRegistryModel):
    """
    Atomic package definition in registries/packages/*.yaml.
    """
    source: DependencySource
    # Metadata for the package installer
    install_args: Dict[str, Any] = {}