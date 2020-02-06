from click.testing import CliRunner
from deepdiff import DeepDiff

from combinedIngress.main import *


def get_services_obj():
    services = [
        {
            "ServiceName": "test",
            "Namespace": "demo1",
            "dns_entry": "demo1.example.org",
            "port": "80",
        },
        {
            "ServiceName": "test",
            "Namespace": "demo2",
            "dns_entry": "demo2.example.org",
            "port": "80",
        },
    ]
    return services


def get_formatted_services_obj():
    services = {
        "apiVersion": "voyager.appscode.com/v1beta1",
        "kind": "Ingress",
        "metadata": {
            "name": "ingress",
            "namespace": "demo-shared-test",
            "annotations": {
                "ingress.appscode.com/annotations-service": '{"external-dns.alpha.kubernetes.io/hostname" : "demo1.example.org,demo2.example.org"}'
            },
        },
        "spec": {
            "tls": [
                {
                    "secretName": "tls-example",
                    "hosts": ["demo1.example.org", "demo2.example.org"],
                }
            ],
            "rules": [
                {
                    "host": "demo1.example.org",
                    "http": {
                        "paths": [
                            {
                                "backend": {
                                    "serviceName": "test.demo1",
                                    "servicePort": 80,
                                }
                            }
                        ]
                    },
                },
                {
                    "host": "demo2.example.org",
                    "http": {
                        "paths": [
                            {
                                "backend": {
                                    "serviceName": "test.demo2",
                                    "servicePort": 80,
                                }
                            }
                        ]
                    },
                },
            ],
        },
    }

    return services


def test_ingress_controller_generates(mocker):
    runner = CliRunner()

    generate_mock = mocker.MagicMock()
    mocker.patch("combinedIngress.main.ingress_controller_generate", generate_mock)
    mocker.patch("combinedIngress.main.write_to_yaml")

    runner.invoke(combine_ingress, ["test", "80", "example.org", "demo1", "demo2"])
    generate_mock.assert_called_with(get_services_obj(), "demo-shared-test")


def test_yaml_write(mocker):
    runner = CliRunner()
    write_mock = mocker.MagicMock()
    mocker.patch("combinedIngress.main.write_to_yaml", write_mock)
    runner.invoke(combine_ingress, ["test", "80", "example.org", "demo1", "demo2"])
    write_mock.assert_called_with(get_formatted_services_obj(), "output/ingress.yml")
