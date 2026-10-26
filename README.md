# AI-Generated Image Detector

A small Streamlit research prototype that classifies an uploaded image using a pretrained Hugging Face image-classification model.

## Run locally

Python 3.10–3.12 is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501). The first run downloads the model, so an internet connection is required.

## Model

Default model ID: `umm-maybe/AI-image-detector`. To change it, set the environment variable `AI_IMAGE_MODEL` to another compatible image-classification model before launching.

## Deploy to Streamlit Community Cloud

1. Connect this public GitHub repository at https://share.streamlit.io/.
2. Select branch `main`.
3. Set the main file path to `app.py`.
4. Deploy.

## Limitations

This is an educational screening prototype, not forensic evidence. Predictions may be wrong on edited, compressed, or out-of-distribution images. The model score is not a calibrated probability. This app does not detect deepfake videos or face swaps.
