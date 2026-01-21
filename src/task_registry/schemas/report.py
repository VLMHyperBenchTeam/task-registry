from typing import Optional, Dict, Any
from .base import BaseRegistryModel

class ReportSchema(BaseRegistryModel):
    """
    Report generator definition schema.
    
    Attributes:
        class_path: Python path to the report generator implementation class.
        params: Configuration parameters for the report generator.
        package: Optional name of the atomic package providing this report.
    """
    class_path: str
    params: Dict[str, Any] = {}
    package: Optional[str] = None