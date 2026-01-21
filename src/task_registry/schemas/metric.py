from typing import Optional, Dict, Any, List
from .base import BaseRegistryModel

class MetricSchema(BaseRegistryModel):
    """
    Metric definition schema.
    
    Attributes:
        name: Unique identifier of the metric instance.
        class_path: Python path to the metric implementation class.
        params: Configuration parameters for the metric.
        package: Optional name of the atomic package providing this metric.
    """
    class_path: str
    params: Dict[str, Any] = {}
    package: Optional[str] = None