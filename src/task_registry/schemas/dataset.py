from typing import Optional, Dict, Any
from .base import BaseRegistryModel

class DatasetSchema(BaseRegistryModel):
    """
    Dataset definition schema.
    
    Attributes:
        type: Python path to the dataset iterator class.
        path: Data source path (local, s3, etc.).
        params: Specific parameters for the iterator.
        package: Optional name of the atomic package providing this dataset.
    """
    type: str
    path: str
    params: Dict[str, Any] = {}
    package: Optional[str] = None