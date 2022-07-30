import yaml

from exedra.backends.argo.importer_node import importer


def test_importer():
    importer1 = importer(artifact_uri="http://127.0.0.1:8080/test.csv")

    expected_template = yaml.full_load(
        """
        name: importer
        inputs:
          artifacts:
          - name: uri
            path: /tmp/data
        outputs:
          artifacts:
          - name: artifact
            path: /tmp/data
        container:
          image: hello-world
        """
    )
    expected_input_mapping = {
        "uri": yaml.full_load(
            """
            name: uri
            http:
              url: http://127.0.0.1:8080/test.csv
            """
        )
    }

    assert importer1.template.to_dict() == expected_template
    assert {
        k: v.to_dict() for k, v in importer1.input_mapping.items()
    } == expected_input_mapping
