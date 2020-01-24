import pytest
import yaml
import os

from combinedIngress.helper import *

#### HELPER FUNCTIONS FOR THE TEST
def load_controller_yaml():
    with open("./combinedIngress/tests/fixtures/controller.yml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


def rule_object():
    return [
        {
            "host": "echo-demo.example.org",
            "http": {
                "paths": [
                    {"backend": {"serviceName": "echoserver.dev", "servicePort": 80,}}
                ]
            },
        }
    ]


def get_services():
    services = [
        {
            "ServiceName": "echoserver",
            "Namespace": "dev",
            "dns_entry": "echo-demo.example.org",
            "port": 80,
        },
        {
            "ServiceName": "hello",
            "Namespace": "prod",
            "dns_entry": "shared-demo.example.org",
            "port": 80,
        },
    ]

    return services


#### END HELPER FUNCTIONS


def test_ingress_controller_generate():
    real_code = ingress_controller_generate(get_services())
    test_fixture = load_controller_yaml()

    for key, value in test_fixture.items():
        assert key in real_code.keys()
        assert value == real_code[key]

    assert len(test_fixture) == len(real_code)


def test_generate_rules():
    real_code = generate_rules(get_services()[:1])
    test_fixture = rule_object()

    assert test_fixture == real_code


def test_write_to_yaml(fs):
    out_file = "/test.yml"
    write_to_yaml(["test"], out_file)
    assert os.path.exists(out_file)
    with open(out_file, "r") as file:
        assert yaml.safe_load(file) == ["test"]
