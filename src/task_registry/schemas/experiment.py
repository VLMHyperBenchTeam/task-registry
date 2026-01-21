from typing import List, Union
from .base import BaseRegistryModel
from .run import RunTaskSchema

class ExperimentPlanSchema(BaseRegistryModel):
    """
    Experiment plan grouping multiple runs.
    
    Attributes:
        parallelism: Number of parallel tasks.
        tasks: List of RunTask names or inline RunTaskSchema definitions.
    """
    parallelism: int = 1
    tasks: List[Union[str, RunTaskSchema]] = []