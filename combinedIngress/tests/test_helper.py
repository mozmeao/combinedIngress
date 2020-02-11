import pytest
import yaml
import os

from combinedIngress.helper import *

#### HELPER FUNCTIONS FOR THE TEST
def load_controller_yaml():
    with open("./combinedIngress/tests/fixtures/controller.yml") as f:
        data = yaml.load_all(f, Loader=yaml.FullLoader)
        return list(data)


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
            "domain": "example.org",
        },
        {
            "ServiceName": "hello",
            "Namespace": "prod",
            "dns_entry": "shared-demo.example.org",
            "port": 80,
            "domain": "example.org",
        },
    ]

    return services


#### END HELPER FUNCTIONS


def test_ingress_controller_generate_doc_1():
    real_code_docs = ingress_controller_generate(get_services(), "demo-shared-test")
    test_fixture_docs = load_controller_yaml()

    real_code = list(real_code_docs)[0]
    test_fixture = test_fixture_docs[0]

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
        assert yaml.safe_load(file) == "test"


def test_services_from_git_branch(mocker):
    branch_mock = mocker.MagicMock()
    branch_mock.branch.return_value = "origin/demo/test-branch\n"
    repo_mock = mocker.MagicMock()
    repo_mock.return_value.git = branch_mock
    mocker.patch("combinedIngress.helper.Repo", repo_mock)

    assert services_from_git_branch('demo/') == ["demo-test-branch"]


def test_services_from_git_branch_invalid_name(mocker):
    branch_mock = mocker.MagicMock()
    lots_of_xs = "x" * 65
    branch_mock.branch.return_value = f"origin/demo/{lots_of_xs}\n"
    repo_mock = mocker.MagicMock()
    repo_mock.return_value.git = branch_mock
    mocker.patch("combinedIngress.helper.Repo", repo_mock)

    with pytest.raises(ValueError):
        services_from_git_branch('demo/')

def test_services_from_git_branch_unmatched_prefx(mocker):
    branch_mock = mocker.MagicMock()
    branch_mock.branch.return_value = "origin/fake/test-branch\n"
    repo_mock = mocker.MagicMock()
    repo_mock.return_value.git = branch_mock
    mocker.patch("combinedIngress.helper.Repo", repo_mock)

    assert services_from_git_branch('demo/') == []



# def test_services_from_git_branch_invalid_name(mocker):
#     branch_mock = mocker.MagicMock()
#     branch_mock.branch.return_value = "origin/demo/1\n"
#     repo_mock = mocker.MagicMock()
#     repo_mock.return_value.git = branch_mock
#     mocker.patch("combinedIngress.helper.Repo", repo_mock)
#
#     assert services_from_git_branch("demo-1") == ["demo-test-branch"]

