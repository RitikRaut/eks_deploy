from flask import Flask, jsonify
from kubernetes import client, config

app = Flask(__name__)

# Load Kubernetes configuration (works within the cluster)
config.load_incluster_config()

v1 = client.CoreV1Api()

@app.route('/pod-details')
def pod_details():
    pod_list = v1.list_namespaced_pod(namespace='default')
    pod_info = []

    for pod in pod_list.items:
        pod_info.append({
            'pod_name': pod.metadata.name,
            'pod_ip': pod.status.pod_ip,
            'node_name': pod.spec.node_name,
            'node_ip': pod.status.host_ip,
        })

    return jsonify(pod_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
