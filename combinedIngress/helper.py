from git import Repo
from jinja2 import Environment, FileSystemLoader
import yaml


def ingress_controller_generate(services, ingress_namespace):
    # This is a nice list of services from the more complex object that includes some additional content
    dns_entries_list = [config["dns_entry"] for config in services]
    rules = generate_rules(services)

    file_loader = FileSystemLoader("combinedIngress/templates")
    env = Environment(loader=file_loader)
    template = env.get_template("controller.yml.j2")

    rendered_ingress_template = template.render(
        dns_entries=dns_entries_list, namespace=ingress_namespace, rules=rules
    )
    # return as yaml to make sure this is valid yaml (doing the load/dump cycle)
    return yaml.load(rendered_ingress_template, Loader=yaml.FullLoader)


def generate_rules(services):
    rules = []
    for service_config in services:
        service_name = f"{service_config['ServiceName']}.{service_config['Namespace']}"
        rule = {
            "service_name": service_name,
            "dns_entry": service_config["dns_entry"],
            "port": service_config["port"],
        }
        rules.append(rule)

    return rules


def write_to_yaml(python_object, filepath):
    with open(filepath, "w") as file:
        yaml.dump(python_object, file)


def validate_dns(dns_name):
    banned_chars = [".", "/", "\\"]
    if any([c in dns_name for c in banned_chars]):
        return False

    return True

def services_from_git_branch(prefix):
    r = Repo("/repo")
    branch_names = []
    for branch in r.branches:
        name = branch.name
        if name.startswith(prefix):
            dropped_prefix = name[len(prefix):]
            if not validate_dns(dropped_prefix):
                raise ValueError("Not a safe name for a website (slashes and dots not allowed)")
            branch_names.append(dropped_prefix)

    return branch_names
