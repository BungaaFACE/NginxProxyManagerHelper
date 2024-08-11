from rest_client import NPM_client
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='NginxProxyManagerHelper',
                                     description='Tool helps to automate proxy creation in Nginx Proxy Manager.')
    parser.add_argument("--domain", "-d",
                        required=True, type=str,
                        help='domain for proxy', dest='domain')
    parser.add_argument("--forward_host", "-fh",
                        required=True, type=str,
                        help='forward ip for proxy', dest='forward_host')
    parser.add_argument("--forward_port", "-fp",
                        required=True, type=int,
                        help='forward port for proxy', dest='forward_port')
    parser.add_argument("--project_name", "-n",
                        required=True, type=str,
                        help='project folder for locations', dest='project_name')
    parser.add_argument("--forward_scheme", "-fs",
                        type=str, default='http',
                        help='forward ip for proxy, default=http',
                        choices=['http', 'https'], dest='forward_scheme')
    parser.add_argument("--force_ssl", "-ssl",
                        type=str, default=True,
                        help='forward ip for proxy, default=True',
                        choices=[True, False], dest='ssl_forced')
    args = parser.parse_args()
    with NPM_client() as npm:
        npm.add_proxy(
            domain=args.domain,
            forward_host=args.forward_host,
            forward_port=args.forward_port,
            project_name=args.project_name,
            forward_scheme=args.forward_scheme,
            ssl_forced=args.ssl_forced
        )
