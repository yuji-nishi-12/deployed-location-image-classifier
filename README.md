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

## Notes

- The model weights must be present at `models/image_intel_model_0.pth` for inference.
