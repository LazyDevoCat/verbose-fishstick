import yaml

DEPRECATED_APIS = {
    "apps/v1beta1": "removed in v1.16, use apps/v1",
    "apps/v1beta2": "removed in v1.16, use apps/v1",
    "extensions/v1beta1": "removed in v1.16, use apps/v1",
}

with open("examples/statefulset-no-resources-deprecated-api.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load_all(f)
    all_data = list(data)

data = all_data[0]

containers = data['spec']['template']['spec']['containers']
apis = data['apiVersion']


def check_requests(containers_spec):
    findings = []
    for container in containers_spec:
        name = container.get('name')
        resources = container.get('resources')
        if resources is None:
            findings.append(f"{name}: no resources block")
            continue
        requests = resources.get('requests')
        if requests is None:
            findings.append(f"{name}: no requests block but resources are defined")
            continue
    return findings


def check_limits(containers_spec):
    findings = []
    for container in containers_spec:
        name = container.get('name')
        resources = container.get('resources')
        if resources is None:
            findings.append(f"{name}: no resources block")
            continue
        limits = resources.get('limits')
        if limits is None:
            findings.append(f"{name}: no limits block but resources are defined")
            continue
    return findings


def check_api(api_list):
    if api_list in DEPRECATED_APIS.keys():
        return f"Fix {api_list}! Because {DEPRECATED_APIS[api_list]}"


print(check_requests(containers))
print(check_limits(containers))

print(check_api(apis))
