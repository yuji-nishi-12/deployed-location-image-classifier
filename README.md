# Location Image Classifier

Streamlit app + CNN model that classifies a location image into one of:

- `buildings`, `forest`, `glacier`, `mountain`, `sea`, `street`

The current app performs **multi-class label** prediction (softmax + argmax) and displays the top class with confidence.

## Repo contents

- `app.py` — Streamlit UI + inference
- `model.py` — Location Image Classifier model
- `models/image_intel_model_0.pth` — trained weights (model_0.state_dict())
- `Dockerfile` — container image for the app
- `K8s/` — Kubernetes manifests
  - `deployment.yaml`
  - `service.yaml`
- `cloudbuild.yaml` — Google Cloud Build pipeline (build → push → deploy)

## Deploy to Kubernetes (GKE)

The manifests in `K8s/` deploy the Streamlit container and expose it via a `LoadBalancer` service.

1) Build and push an image to a registry (example: GCR)

```bash
gcloud auth login
gcloud config set project <YOUR_GCP_PROJECT_ID>
gcloud builds submit --config cloudbuild.yaml .
```

2) Ensure the image reference in `K8s/deployment.yaml` matches your pushed image:

- `gcr.io/<YOUR_GCP_PROJECT_ID>/location-classifier:v1`

3) Apply manifests (if not using `gke-deploy`):

```bash
kubectl apply -f K8s/
kubectl get svc
```

When the external IP is assigned, open it in your browser.

## Notes

- The model weights must be present at `models/image_intel_model_0.pth` for inference.
