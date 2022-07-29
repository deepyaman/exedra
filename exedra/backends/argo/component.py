from argo_workflows.model.io_argoproj_workflow_v1alpha1_artifact import (
    IoArgoprojWorkflowV1alpha1Artifact,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_http_artifact import (
    IoArgoprojWorkflowV1alpha1HTTPArtifact,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_template import (
    IoArgoprojWorkflowV1alpha1Template,
)

from exedra.backends.argo import pipeline_task


class Component:
    def __init__(self, template: IoArgoprojWorkflowV1alpha1Template):
        self.template = template
        self.name = template.name

    def __call__(self, *args, **kwargs) -> pipeline_task.PipelineTask:
        if args:
            nargs = len(args)
            if kwargs:
                raise TypeError(
                    f"{self.name}() takes 0 positional arguments but {nargs} "
                    f"positional arguments (and {len(kwargs)} keyword-only "
                    f"argument{'' if len(kwargs) == 1 else 's'}) were given"
                )
            else:
                raise TypeError(
                    f"{self.name}() takes 0 positional arguments but {nargs} were given"
                )

        input_mapping = {}  # TODO(deepyaman): Handle optional arguments
        for k, v in kwargs.items():
            if k not in self.inputs:
                raise TypeError(
                    f"{self.name}() got an unexpected keyword argument {repr(k)}"
                )
            input_mapping[k] = IoArgoprojWorkflowV1alpha1Artifact(
                name=k, http=IoArgoprojWorkflowV1alpha1HTTPArtifact(url=v)
            )

        missing_inputs = [repr(x) for x in self.inputs if x not in input_mapping]
        if len(missing_inputs) == 1:
            raise TypeError(
                f"{self.name}() missing 1 required keyword-only argument: "
                f"{missing_inputs[0]}"
            )
        elif len(missing_inputs) == 2:
            raise TypeError(
                f"{self.name}() missing 2 required keyword-only arguments: "
                f"{missing_inputs[0]} and {missing_inputs[1]}"
            )
        elif missing_inputs:
            raise TypeError(
                f"{self.name}() missing {len(missing_inputs)} required keyword-only "
                f"arguments: {', '.join(missing_inputs[:-1])}, and {missing_inputs[-1]}"
            )

        return pipeline_task.PipelineTask(self.template, input_mapping)

    @property
    def inputs(self):
        # TODO(deepyaman): Add parameter names to the inputs list. Since
        #   both parameters and artifacts are keyword arguments funneled
        #   to the `__call__` method, there cannot be conflicting names.
        return [artifact.name for artifact in self.template.inputs.artifacts]
