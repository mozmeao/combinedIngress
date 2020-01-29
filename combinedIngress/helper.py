import yaml


def ingress_controller_generate(services, ingress_namespace):

    # This is a nice list of services from the more complex object that includes some additional content
    dns_entries_list = [config["dns_entry"] for config in services]
    # Turning the list
    dns_entries_string = ",".join(dns_entries_list)

    annotations = {
        "ingress.appscode.com/annotations-service": f'{{"external-dns.alpha.kubernetes.io/hostname" : "{dns_entries_string}"}}'
    }

    # Creating the yaml as a whole, and adding the CRD information/object creation
    yaml = {"apiVersion": "voyager.appscode.com/v1beta1", "kind": "Ingress"}

    # Creating the metadata section
    metadata = {
        "name": "ingress",
        "namespace": ingress_namespace,
        "annotations": annotations,
    }
    yaml["metadata"] = metadata

    # Creating the spec section, and adding it to the yaml
    spec = {}
    tls = [{"secretName": "tls-example", "hosts": dns_entries_list}]
    rules = generate_rules(services)
    spec["tls"] = tls
    spec["rules"] = rules
    yaml["spec"] = spec

    return yaml


def generate_rules(services):
    rules = []
    for service_config in services:
        service_name = f"{service_config['ServiceName']}.{service_config['Namespace']}"
        rule = {
            "host": service_config["dns_entry"],
            "http": {
                "paths": [
                    {
                        "backend": {
                            "serviceName": service_name,
                            "servicePort": service_config["port"],
                        }
                    }
                ]
            },
        }
        rules.append(rule)

    return rules


def write_to_yaml(python_object, filepath):
    with open(filepath, "w") as file:
        yaml.dump(python_object, file)
