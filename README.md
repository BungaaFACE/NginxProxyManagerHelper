# NginxProxyManagerHelper
## Description
NginxProxyManagerHelper is a tool that helps you to automate proxy check and creation during CD process.  
With that tool you can create proxy for domain with command line using your gitlab-runer/other automation tools.  
  
## Installation
1. Clone repo to your desirable folder and cd into it  
`git clone https://github.com/BungaaFACE/NginxProxyManagerHelper && cd NginxProxyManagerHelper`  
2. Create and enter venv  
`python3 -m venv .venv`  
`source .venv/bin/activate`  
3. Install requirements  
`pip install -r requirements.txt`  
4. Rename .env.tmp -> .env and enter your parameters  
`mv .env.tmp .env`  
  
## Usage
Tool can be run from command line:  
`.venv/bin/python NPMHelper.py --domain DOMAIN --forward_host FORWARD_HOST --forward_port FORWARD_PORT --project_name PROJECT_NAME [--forward_scheme {http,https}] [--force_ssl {True,False}]`  
List of arguments can be viewed with `python NPMHelper.py -h` or in the next section.  
  
## Arguments
| Argument | Required | Description |
|----------|----------|-------------|
|--domain/-d|No|domain for proxy, required for adding proxy|
|--forward_host/-fh|Yes|forward ip for proxy|
|--forward_port/-fp|Yes|forward port for proxy|
|--project_name/n|No|project folder name for locations, dont add location if not specified|
|--forward_scheme/-fs|No|forward scheme, default=http|
|--force_ssl/-ssl|No|make strict ssl, default=True|
|--delete/-dl|No|delete forward host:port proxies, default=False |
  
## New features
You can suggest new feature or report a bug in the issues.  
