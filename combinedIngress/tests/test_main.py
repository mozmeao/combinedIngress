from click.testing import CliRunner
from deepdiff import DeepDiff

from combinedIngress.main import *


def get_services_obj():
    services = [
        {
            "ServiceName": "test",
            "Namespace": "demo1",
            "dns_entry": "www-demo1.example.org",
            "port": "80",
            "domain": "example.org",
        },
        {
            "ServiceName": "test",
            "Namespace": "demo2",
            "dns_entry": "www-demo2.example.org",
            "port": "80",
            "domain": "example.org",
        },
    ]
    return services


mocks = {}


def customer_setup(mocker):
    generate_mock = mocker.MagicMock()
    write_mock = mocker.MagicMock()
    services_mock = mocker.MagicMock(return_value=["demo1", "demo2"])

    mocks["generate_mock"] = generate_mock
    mocks["write_mock"] = write_mock
    mocks["services_mock"] = services_mock

    mocker.patch("combinedIngress.main.ingress_controller_generate", generate_mock)
    mocker.patch("combinedIngress.main.write_to_yaml", write_mock)
    mocker.patch("combinedIngress.main.services_from_git_branch", services_mock)

    runner = CliRunner()
    runner.invoke(combine_ingress, ["test", "80", "example.org", 'demo/', 'www'])


def test_ingress_controller_generates(mocker):
    customer_setup(mocker)
    mocks["generate_mock"].assert_called_with(get_services_obj(), "demo-shared-test")


def test_yaml_write(mocker):
    customer_setup(mocker)
    mocks["write_mock"].assert_called_with(
        mocks["generate_mock"].return_value, "output/ingress.yml"
    )


def test_git_branch(mocker):
    customer_setup(mocker)
    mocks["services_mock"].assert_called()
