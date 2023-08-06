import os

from cfn_tools import dump_yaml, load_yaml


def cleanup(template):
    if os.path.exists(template):
        os.remove(template)


def build(url, template_path="template.yml"):
    save_path = ".localfunk.yaml"
    template_yaml = parse(template_path)
    functions = get_functions(template_yaml)
    update_template(template_yaml, functions, url)
    save_template(template_yaml, save_path)
    return save_path


def update_template(template_yaml, functions, url):
    for name, details in template_yaml["Resources"].items():
        if details["Type"] == "AWS::Serverless::Function":
            del template_yaml["Resources"][name]["Properties"]["CodeUri"]
            template_yaml["Resources"][name]["Properties"]["Handler"] = "index.handler"
            function = functions[name]
            code = gen_code(function, url)
            template_yaml["Resources"][name]["Properties"]["InlineCode"] = code


def save_template(template_yaml, save_path):
    file = open(save_path, "w+")
    file.write(dump_yaml(template_yaml))
    file.close()


def gen_code(func, proxy):
    return f"""
import http.client
import json
import os

conn = http.client.HTTPConnection("{proxy}")
headers = {{"Content-type": "application/json"}}


def handler(event, context):
    data = {{
        "event": event, 
        "env": dict(os.environ.items()),
        "code_uri": "{func['code_uri']}",
        "file": "{func['file']}",
        "function": "{func['function']}" 
    }}

    try:
        conn.request("POST", "/", json.dumps(data), headers)
        response = conn.getresponse()
        return json.loads(response.read().decode())
    except Exception as e:
        return {{ "error": str(e) }}
    """


def get_functions(template_yaml):
    functions = {}
    for name, details in template_yaml["Resources"].items():
        props = details["Properties"]
        if details["Type"] == "AWS::Serverless::Function":
            handler = props["Handler"].split(".")
            functions[name] = {
                "code_uri": props["CodeUri"],
                "file": handler[0],
                "function": handler[1],
            }

    return functions


def parse(template_path):
    text = open(template_path, "r").read()
    return load_yaml(text)
