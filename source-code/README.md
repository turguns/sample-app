# Build and push the image

From repository root:

cd roles/sample-app/source-code/sample-app-python
podman build -t HARBOR-CNAME/INFRA-HUB/app-python-web:3.14-slim .
podman push HARBOR-CNAME/INFRA-HUB/app-python-web:3.14-slim

Where:
- HARBOR-CNAME = value of `harbor_cname`
- INFRA-HUB = value of `ocp_infra_hub`

2. Deploy sample-app with Ansible

From repository root:

ansible-playbook -i inventories/<inventory>/inventory playbooks/sample-app.yml

Default namespace used by the role:
- infra-sample-app



