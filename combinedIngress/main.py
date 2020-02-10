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
@click.argument("prefix")
def combine_ingress(servicename, port, dns_domain, prefix):
    click.echo(
        "Starting run, service: %s, port: %s,  domain: %s git_prefix: %s"
        % (servicename, port, dns_domain, prefix)
    )
    services = []

    sites = services_from_git_branch(prefix)

    if len(sites) == 0:
        raise ValueError('No valid branches found')

    for site in sites:
        service_dict = {
            "ServiceName": servicename,
            "Namespace": site,
            "dns_entry": f"{site}.{dns_domain}",
            "port": port,
            "domain": dns_domain,
        }
        services.append(service_dict)

    services_dict = ingress_controller_generate(services, f"demo-shared-{servicename}")
    write_to_yaml(services_dict, "output/ingress.yml")


if __name__ == "__main__":
    combine_ingress()
