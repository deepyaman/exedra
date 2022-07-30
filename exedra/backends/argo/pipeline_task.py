from __future__ import annotations

from argo_workflows.model.io_argoproj_workflow_v1alpha1_artifact import (
    IoArgoprojWorkflowV1alpha1Artifact,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_template import (
    IoArgoprojWorkflowV1alpha1Template,
)


class PipelineTask:
    def __init__(
        self,
        template: IoArgoprojWorkflowV1alpha1Template,
        input_mapping: dict[str, IoArgoprojWorkflowV1alpha1Artifact],
    ):
        self.template = template
        self.input_mapping = input_mapping
