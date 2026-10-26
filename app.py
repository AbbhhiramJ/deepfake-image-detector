import os

import streamlit as st
import torch
from PIL import Image, UnidentifiedImageError
from transformers import AutoImageProcessor, AutoModelForImageClassification

MODEL_ID = os.getenv("AI_IMAGE_MODEL", "umm-maybe/AI-image-detector")
MAX_FILE_MB = 10

st.set_page_config(page_title="AI Image Detector", page_icon="🔎", layout="centered")


@st.cache_resource(show_spinner="Downloading/loading the image classifier (first run may take a few minutes)…")
def load_model():
    processor = AutoImageProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForImageClassification.from_pretrained(MODEL_ID)
    model.eval()
    return processor, model


def interpret_label(label: str) -> str:
    value = label.lower().replace("_", " ").replace("-", " ")
    if any(word in value for word in ("artificial", "generated", "synthetic", "fake", "ai")):
        return "Likely AI-generated"
    if any(word in value for word in ("human", "real", "natural", "authentic")):
        return "Likely real / camera-captured"
    return f"Model class: {label}"


st.title("AI-Generated Image Detector")
st.caption("Research prototype · image classification · hosted web demo")
st.info(
    "Upload an image to get a model prediction. This is a screening aid, not proof of origin: "
    "edited photos, unseen generators, compression, and model bias can cause mistakes."
)

uploaded = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp", "bmp"])
if uploaded:
    if uploaded.size > MAX_FILE_MB * 1024 * 1024:
        st.error(f"Please upload an image smaller than {MAX_FILE_MB} MB.")
        st.stop()
    try:
        image = Image.open(uploaded).convert("RGB")
    except (UnidentifiedImageError, OSError):
        st.error("This file could not be read as an image.")
        st.stop()

    st.image(image, caption=f"Uploaded image · {image.width} × {image.height}", use_container_width=True)
    if st.button("Analyze image", type="primary", use_container_width=True):
        try:
            processor, model = load_model()
            inputs = processor(images=image, return_tensors="pt")
            with torch.inference_mode():
                logits = model(**inputs).logits
                probabilities = torch.softmax(logits, dim=-1)[0]
            index = int(torch.argmax(probabilities).item())
            labels = model.config.id2label
            raw_label = str(labels.get(index, labels.get(str(index), index)))
            confidence = float(probabilities[index].item())

            st.subheader(interpret_label(raw_label))
            st.metric("Model confidence for predicted class", f"{confidence:.1%}")
            st.caption(f"Model: {MODEL_ID} · raw class: {raw_label}")
            st.write("Class scores")
            score_rows = []
            for i, score in enumerate(probabilities.tolist()):
                label = str(labels.get(i, labels.get(str(i), i)))
                score_rows.append({"Class": label, "Score": f"{score:.1%}"})
            st.table(score_rows)
            st.warning(
                "Confidence is the model's score, not a calibrated probability that the image is AI-generated. "
                "Do not use this result as forensic proof."
            )
        except Exception as exc:
            st.error("The model could not be loaded or inference failed.")
            st.code(f"{type(exc).__name__}: {exc}")
            st.caption("Check internet access for the first model download and try again.")
else:
    st.markdown("**Demo flow:** upload image → Analyze image → inspect predicted class and class scores.")

with st.expander("Project scope and limitations"):
    st.markdown(
        "- This demo detects likely AI-generated versus real-looking images; it is not a face-swap/deepfake-video detector.\n"
        "- The pretrained model is downloaded from Hugging Face on first launch and then cached.\n"
        "- Results depend on the model's training data and may not generalize to new generators.\n"
        "- For a defensible evaluation, test on a held-out dataset containing generators absent from training."
    )
