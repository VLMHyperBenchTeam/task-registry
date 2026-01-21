from enum import Enum
from typing import Optional, Union, Literal, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict

class SourceType(str, Enum):
    LOCAL = "local"
    GIT = "git"
    PYPI = "pypi"

class LocalSource(BaseModel):
    type: Literal[SourceType.LOCAL] = SourceType.LOCAL
    path: str
    editable: bool = True

class GitSource(BaseModel):
    type: Literal[SourceType.GIT] = SourceType.GIT
    url: str
    ref: Optional[str] = None  # tag, branch, or commit hash

class PyPISource(BaseModel):
    type: Literal[SourceType.PYPI] = SourceType.PYPI
    name: str
    version: Optional[str] = None

DependencySource = Union[LocalSource, GitSource, PyPISource]

class RuntimeManifest(BaseModel):
    """
    SBOM-ready manifest of used packages and their resolved sources.
    """
    model_config = ConfigDict(frozen=True)
    
    timestamp: str
    run_mode: str
    packages: Dict[str, DependencySource]
    environment_info: Dict[str, str] = Field(default_factory=dict)

class BaseRegistryModel(BaseModel):
    """
    Base class for all registry items.
    """
    name: str
    version: str = "1.0.0"
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)