from rest_client import NPM_client
import argparse
import logging
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='NginxProxyManagerHelper',
                                     description='Tool helps to automate proxy creation in Nginx Proxy Manager.')
    parser.add_argument("--domain", "-d",
                        required=False, type=str,
                        help='domain for proxy', dest='domain')
    parser.add_argument("--forward_host", "-fh",
                        required=True, type=str,
                        help='forward ip for proxy', dest='forward_host')
    parser.add_argument("--forward_port", "-fp",
                        required=True, type=int,
                        help='forward port for proxy', dest='forward_port')
    parser.add_argument("--project_name", "-n",
                        required=False, type=str, default=None,
                        help='project folder for locations, default=None', dest='project_name')
    parser.add_argument("--forward_scheme", "-fs",
                        type=str, default='http',
                        help='forward scheme, default=http',
                        choices=['http', 'https'], dest='forward_scheme')
    parser.add_argument("--force_ssl", "-ssl",
                        type=str, default=True,
                        help='make strict ssl, default=True',
                        choices=[True, False], dest='ssl_forced')
    parser.add_argument("--delete", "-dl", action=argparse.BooleanOptionalAction, default=False,
                        help='Delete specified proxy for forward host:port')
    args = parser.parse_args()

    if args.delete:
        if not args.forward_host or not args.forward_port:
            logging.exception('For delete action --forward_port and --forward_port need to be specified.')
            sys.exit()
        else:
            with NPM_client() as npm:
                npm.delete_forward_dest(
                    forward_host=args.forward_host,
                    forward_port=args.forward_port
                )
    else:
        if not args.forward_host or not args.forward_port or not args.domain:
            logging.exception('For add action --domain, --forward_port and --forward_port need to be specified.')
            sys.exit()
        else:
            with NPM_client() as npm:
                npm.add_proxy(
                    domain=args.domain,
                    forward_host=args.forward_host,
                    forward_port=args.forward_port,
                    project_name=args.project_name,
                    forward_scheme=args.forward_scheme,
                    ssl_forced=args.ssl_forced
                )
