import re
from contextlib import nullcontext as does_not_raise

import pytest
from argo_workflows.model.io_argoproj_workflow_v1alpha1_artifact import (
    IoArgoprojWorkflowV1alpha1Artifact,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_inputs import (
    IoArgoprojWorkflowV1alpha1Inputs,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_template import (
    IoArgoprojWorkflowV1alpha1Template,
)

from exedra.backends.argo import component


@pytest.fixture
def mock_component(request):
    return component.Component(
        template=IoArgoprojWorkflowV1alpha1Template(
            name="test_component",
            inputs=IoArgoprojWorkflowV1alpha1Inputs(
                artifacts=[
                    IoArgoprojWorkflowV1alpha1Artifact(name=key)
                    for key in request.param
                ]
            ),
        )
    )


@pytest.fixture
def expectation(request):
    return (
        pytest.raises(TypeError, match=re.escape(request.param))
        if request.param is not None
        else does_not_raise()
    )


@pytest.mark.parametrize(
    "mock_component,args,kwargs,expectation",
    [
        ([], [], {}, None),
        ([], [1], {}, "test_component() takes 0 positional arguments but 1 was given"),
        (
            [],
            [1, 2],
            {},
            "test_component() takes 0 positional arguments but 2 were given",
        ),
        (
            [],
            [1],
            {"input2": 2},
            "test_component() takes 0 positional arguments but 1 positional argument "
            "(and 1 keyword-only argument) were given",
        ),
        (
            [],
            [1, 2, 3],
            {"input4": 4, "input5": 5},
            "test_component() takes 0 positional arguments but 3 positional arguments "
            "(and 2 keyword-only arguments) were given",
        ),
    ],
    indirect=["mock_component", "expectation"],
)
def test_too_many_arguments(mock_component, args, kwargs, expectation):
    with expectation:
        mock_component(*args, **kwargs)


@pytest.mark.parametrize(
    "mock_component,args,kwargs,expectation",
    [
        (
            ["input1"],
            [],
            {},
            "test_component() missing 1 required keyword-only argument: 'input1'",
        ),
        (
            ["input1", "input2", "input3"],
            [],
            {"input2": 2},
            "test_component() missing 2 required keyword-only arguments: 'input1' and "
            "'input3'",
        ),
        (
            ["input1", "input2", "input3", "input4", "input5"],
            [],
            {},
            "test_component() missing 5 required keyword-only arguments: 'input1', "
            "'input2', 'input3', 'input4', and 'input5'",
        ),
    ],
    indirect=["mock_component", "expectation"],
)
def test_too_few_and_missing_arguments(mock_component, args, kwargs, expectation):
    with expectation:
        mock_component(*args, **kwargs)
