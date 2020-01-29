#!/usr/bin/env python3

import click

from combinedIngress.helper import ingress_controller_generate, write_to_yaml


@click.command()
@click.argument("servicename")
@click.argument("port")
@click.argument("dns_domain")
@click.argument("sites", nargs=-1)
def combine_ingress(servicename, port, dns_domain, sites):
    click.echo(
        "Starting run, service: %s, port: %s,  domain: %s sites: %s"
        % (servicename, port, dns_domain, sites)
    )
    services = []

    for site in sites:
        service_dict = {
            "ServiceName": servicename,
            "Namespace": site,
            "dns_entry": f"{site}.{dns_domain}",
            "port": port,
        }
        services.append(service_dict)

    services_dict = ingress_controller_generate(services)
    write_to_yaml(services_dict, "output/ingress.yml")


if __name__ == "__main__":
    combine_ingress()


# ./script bedrock 80 mozmar.org demo1,demo2,demo3
