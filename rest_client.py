import sys
import logging
import requests
from requests.exceptions import RequestException, HTTPError
from dotenv import dotenv_values
from os.path import abspath, dirname, join

config = dotenv_values(join(dirname(abspath(__file__)), '.env'))
logging.getLogger().setLevel(config.get('log_level', 'INFO'))


class NPM_client:
    def __init__(self):
        self.token = ''
        self.api_url = f"http://{config.get('npm_address', 'localhost')}:{config.get('npm_port', '81')}/api"

    def __enter__(self):
        try:
            response = requests.post(f'{self.api_url}/tokens',
                                     data={
                'identity': config.get('npm_login', 'admin@example.com'),
                'scope': 'user',
                'secret': config.get('npm_password', 'changeme'),
            })
            response.raise_for_status()
            self.token = f"Bearer {response.json()['token']}"
            logging.info('Login successfull')
            return self
        except HTTPError as exc:
            logging.error(f'Login unsuccessful: {response.json()}')
            logging.debug('Exception details', exc_info=exc)
        except RequestException as exc:
            logging.error(f'Connection to {self.api_url} unsuccessful')
            logging.debug('Exception details', exc_info=exc)
        sys.exit()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        return

    def get_proxy_hosts(self):
        response = requests.get(f'{self.api_url}/nginx/proxy-hosts',
                                headers={'Authorization': self.token})
        return response.json()

    def delete_forward_dest(self, forward_host: str, forward_port: int):
        hosts = self.get_proxy_hosts()
        hosts = list(filter(lambda host: host['forward_host'] == forward_host and host['forward_port'] == forward_port))
        logging.info(f'Deleting {forward_host}:{forward_port} proxies. Got {len(hosts)}.')
        for host in hosts:
            response = requests.delete(f'{self.api_url}/nginx/proxy-hosts/{str(host['id'])}',
                                       headers={'Authorization': self.token})
            response.raise_for_status()
        logging.info(f'Destination {forward_host}:{forward_port} deleted')

    def delete_domain(self, domain: str, host: dict):
        if len(host['domain_names']) == 1:
            logging.info('Proxy has single domain, deleting proxy')
            response = requests.delete(f'{self.api_url}/nginx/proxy-hosts/{str(host['id'])}',
                                       headers={'Authorization': self.token})
        else:
            logging.info('Proxy has multiple domains, removing domain from proxy')
            host['domain_names'].remove(domain)
            proxy_id = host['id']
            for key in {'id', 'created_on', 'modified_on', 'owner_user_id'}:
                host.pop(key, None)
            response = requests.put(f'{self.api_url}/nginx/proxy-hosts/{proxy_id}',
                                    headers={'Authorization': self.token},
                                    json=host)
        response.raise_for_status()
        logging.info('Domain deleted')

    def is_proxy_exist(self, domain: str,
                       forward_host: str = '',
                       forward_port: int = 0,
                       delete_inconsistent: bool = True):
        hosts = self.get_proxy_hosts()
        for host in hosts:
            if domain in host['domain_names']:
                if forward_host and forward_host != host['forward_host'] or \
                        int(forward_port) and forward_port != host['forward_port']:
                    logging.info(f'Proxy for domain {domain} already created, but forward host is different.'
                                 f'{forward_host}:{forward_port} (new) != (exist) {host['forward_host']}:{host['forward_port']}')
                    if delete_inconsistent:
                        self.delete_domain(domain, host)
                        return

                return True

    def add_proxy(self, domain: str,
                  forward_host: str,
                  forward_port: int,
                  project_name: str = None,
                  forward_scheme: str = 'http',
                  ssl_forced: bool = True):
        if not self.is_proxy_exist(domain, forward_host, forward_port):
            # TODO get or create ssl cert id for domain
            json = {
                "forward_scheme": forward_scheme,
                "forward_host": forward_host,
                "forward_port": int(forward_port),
                "advanced_config": "",
                "domain_names": [domain],
                "access_list_id": "0",
                "certificate_id": 1,
                "ssl_forced": ssl_forced,
                "meta": {
                    "letsencrypt_agree": False,
                    "dns_challenge": False
                },

                "block_exploits": True,
                "caching_enabled": False,
                "allow_websocket_upgrade": False,
                "http2_support": False,
                "hsts_enabled": False,
                "hsts_subdomains": False
            }
            if project_name:
                json = json | {"locations": [
                    {
                        "path": "staticfiles",
                        "advanced_config": "",
                        "forward_scheme": forward_scheme,
                        "forward_host": f"{forward_host}/data/{project_name}/staticfiles",
                        "forward_port": str(forward_port)
                    }
                ]}
            response = requests.post(f'{self.api_url}/nginx/proxy-hosts',
                                     headers={'Authorization': self.token},
                                     json=json)
            response.raise_for_status()
            logging.info('Proxy created')
        else:
            logging.info(f'Proxy for domain {domain} and forward host {forward_host}:{forward_port} already created')


if __name__ == "__main__":
    with NPM_client() as npm:
        # npm.add_proxy(
        #     domain='test_domain',
        #     forward_host='192.168.1.254',
        #     forward_port=8081,
        #     project_name='test_project'
        # )
        hosts = npm.get_proxy_hosts()
    from pprint import pprint
    pprint(hosts)
