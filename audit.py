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

for container in containers:
    name = container.get('name')
    resources = container.get('resources')
    print(f"{name}: resources = {resources}")
    if resources is None:
        print("Define resources!")
        continue
    requests = resources.get('requests')
    if requests is None:
        print("Define requests")
        continue
    limits = resources.get('limits')
    if limits is None:
        print("Define limits")
        continue
    else:
        print("All good")
        continue

if apis in DEPRECATED_APIS.keys():
    print(f"Fix {apis}! Because {DEPRECATED_APIS[apis]}")


