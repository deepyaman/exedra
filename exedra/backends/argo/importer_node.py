from argo_workflows.model.container import Container
from argo_workflows.model.io_argoproj_workflow_v1alpha1_artifact import (
    IoArgoprojWorkflowV1alpha1Artifact,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_inputs import (
    IoArgoprojWorkflowV1alpha1Inputs,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_outputs import (
    IoArgoprojWorkflowV1alpha1Outputs,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_template import (
    IoArgoprojWorkflowV1alpha1Template,
)

from exedra.backends.argo import component, pipeline_task

INPUT_KEY = "uri"
OUTPUT_KEY = "artifact"

# it explicitly or by the image (as the minimal "hello-world" does). See

# Argo Workflows requires that `command` be specified for containers, be
# it explicitly or by the image. See the docs for the emissary executor:
# https://argoproj.github.io/argo-workflows/workflow-executors/#emissary-emissary
_IMPORTER_IMAGE = "hello-world"  # Choose a minimal image with a command

importer_component = component.Component(
    template=IoArgoprojWorkflowV1alpha1Template(
        name="importer",
        inputs=IoArgoprojWorkflowV1alpha1Inputs(
            artifacts=[
                IoArgoprojWorkflowV1alpha1Artifact(name=INPUT_KEY, path="/tmp/data")
            ]
        ),
        outputs=IoArgoprojWorkflowV1alpha1Outputs(
            artifacts=[
                IoArgoprojWorkflowV1alpha1Artifact(name=OUTPUT_KEY, path="/tmp/data")
            ]
        ),
        container=Container(image=_IMPORTER_IMAGE),
    )
)


def importer(artifact_uri: str) -> pipeline_task.PipelineTask:
    return importer_component(uri=artifact_uri)
