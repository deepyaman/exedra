import inspect

import kfp.dsl

import exedra.dsl
from exedra.backends.kfp.component_decorator import component

# Because Kubeflow Pipelines includes the function source in the command
# for Python function-based components, we alias both ``exedra.dsl`` and
# ``kfp.dsl`` to ``dsl`` while testing. By doing so, the component specs
# are equal. This quirk also means that the underlying functions in user
# code should always use type annotations like ``dsl.Dataset`` or simply
# ``Dataset``, but not ``exedra.dsl.Dataset``. For more information, see
# https://github.com/kubeflow/pipelines/blob/8bb0d0e0253d1107f33ef51426d60c6470de2fd7/sdk/python/kfp/components/component_factory.py#L308-L344.


def test_component_decorator():
    dsl = exedra.dsl

    @component
    def transform(
        clean_data: dsl.Input[dsl.Dataset],
        transformed_data: dsl.Output[dsl.Dataset],
    ):
        ...  # pragma: no cover

    got = transform

    dsl = kfp.dsl

    @kfp.dsl.component
    def transform(
        clean_data: dsl.Input[dsl.Dataset],
        transformed_data: dsl.Output[dsl.Dataset],
    ):
        ...  # pragma: no cover

    expected = transform

    assert got.component_spec == expected.component_spec
    assert inspect.signature(got.python_func) == inspect.signature(expected.python_func)
    assert got.python_func.__code__.co_code == expected.python_func.__code__.co_code
