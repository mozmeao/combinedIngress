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
            "dns_entry": "echo-demo.example.org",
            "port": 80,
            "service_name": "echoserver.dev",
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
    real_code = ingress_controller_generate(get_services(), "demo-shared-test")
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


def test_services_from_git_branch(mocker):
    branch_mock = mocker.MagicMock()
    branch_mock.configure_mock(name="demo/test-branch")
    repo_mock = mocker.MagicMock()

    mocker.patch("combinedIngress.helper.Repo", repo_mock)
    repo_mock.return_value.branches = [branch_mock]

    assert services_from_git_branch("demo/") == ["test-branch"]
