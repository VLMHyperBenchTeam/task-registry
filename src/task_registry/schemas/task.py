from typing import List, Optional
from .base import BaseRegistryModel

class MLTaskSchema(BaseRegistryModel):
    """
    ML Task definition schema (e.g., VQA, OCR).
    
    Attributes:
        entry_point: Python module path to run the task (python -m ...).
        required_packages: List of atomic package names required for this task.
        supported_metrics: List of metric instance names allowed for this task.
        supported_reports: List of report instance names allowed for this task.
    """
    entry_point: str
    required_packages: List[str] = []
    supported_metrics: List[str] = []
    supported_reports: List[str] = []
    supported_frameworks: List[str] = ["vllm", "huggingface", "sglang"]