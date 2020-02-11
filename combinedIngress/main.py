#!/usr/bin/env python3

import click

from combinedIngress.helper import (
    ingress_controller_generate,
    write_to_yaml,
    services_from_git_branch,
)


@click.command()
@click.argument("servicename")
@click.argument("port")
@click.argument("dns_domain")
@click.argument("git_prefix")
@click.option("--service_prefix", default=None)
def combine_ingress(servicename, port, dns_domain, git_prefix, service_prefix):
    click.echo(
        "Starting run, service: %s, port: %s,  domain: %s domain-prefix: %s"
        % (servicename, port, dns_domain, service_prefix)
    )
    services = []

    sites = services_from_git_branch(git_prefix)

    if len(sites) == 0:
        raise ValueError("No valid branches found")

    for site in sites:

        if service_prefix:
            dns_entry = f"{service_prefix}-{site}.{dns_domain}"
        else:
            dns_entry = f"{site}.{dns_domain}"

        service_dict = {
            "ServiceName": servicename,
            "Namespace": site,
            "dns_entry": dns_entry,
            "port": port,
            "domain": dns_domain,
        }
        services.append(service_dict)

    services_dict = ingress_controller_generate(services, f"demo-shared-{servicename}")
    write_to_yaml(services_dict, "output/ingress.yml")


if __name__ == "__main__":
    combine_ingress()
