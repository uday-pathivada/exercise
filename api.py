# api.py
from flask import Flask, request, jsonify
from kubernetes import client, config

app = Flask(__name__)

# Load Kubernetes configuration
config.load_kube_config()

@app.route('/createDeployment/<deployment_name>', methods=['POST'])
def create_deployment(deployment_name):
    # Define the deployment object
    container = client.V1Container(
        name=deployment_name,
        image="nginx",
        ports=[client.V1ContainerPort(container_port=80)]
    )
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
        spec=client.V1PodSpec(containers=[container])
    )
    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {'app': deployment_name}}
    )
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=spec
    )
    api_instance = client.AppsV1Api()
    api_instance.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
    return jsonify({"message": f"Deployment {deployment_name} created"}), 201

@app.route('/getPromdetails', methods=['GET'])
def get_prom_details():
    # Simulate retrieving Prometheus details
    return jsonify({"prometheus": "details"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

