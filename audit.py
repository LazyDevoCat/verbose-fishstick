import pathlib

import yaml

DEPRECATED_APIS = {
    "apps/v1beta1": "removed in v1.16, use apps/v1",
    "apps/v1beta2": "removed in v1.16, use apps/v1",
    "extensions/v1beta1": "removed in v1.16, use apps/v1",
}


def audit_file(path_to_file):
    with open(path_to_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load_all(f)
        all_data = list(data)
        findings = []
        data = all_data[0]
        apis = data['apiVersion']
        kind = data.get('kind')
        path = get_path(data, kind)
        findings.extend(check_resources(path, 'requests'))
        findings.extend(check_resources(path, 'limits'))
        api_finding = check_api(apis)
        if api_finding is not None:
            findings.append(api_finding)
        return findings


def get_path(manifest, resource_type):
    if resource_type in ("Job", "Deployment", "StatefulSet", "DaemonSet"):
        containers = manifest['spec']['template']['spec']['containers']
    elif resource_type == "CronJob":
        containers = manifest['spec']['jobTemplate']['spec']['template']['spec']['containers']
    elif resource_type == "Pod":
        containers = manifest['spec']['containers']
    else:
        containers = []
        print(f"Unknown! And container will be {containers}")
    return containers


def check_resources(containers_spec, field):
    findings = []
    for container in containers_spec:
        name = container.get('name')
        resources = container.get('resources')
        if resources is None:
            findings.append(f"{name}: no resources block")
            continue
        value = resources.get(field)
        if value is None:
            findings.append(f"{name}: no {field} block but resources are defined")
            continue
    return findings


def check_api(api_list):
    if api_list in DEPRECATED_APIS.keys():
        return f"Fix {api_list}! Because {DEPRECATED_APIS[api_list]}"
    else:
        pass


# findings = audit_file(pathlib.Path("examples").glob("*.yaml"))

findings = audit_file("examples/statefulset-no-resources-deprecated-api.yaml")
print(findings)
