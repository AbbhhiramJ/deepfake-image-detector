# Presentation Brief — AI-Generated Image Detection

## Problem statement
AI-generated images are increasingly realistic and can be difficult to distinguish from camera-captured images by visual inspection alone. This prototype demonstrates an accessible image-screening workflow using a pretrained vision classifier.

## Objective
Provide a simple web interface in which a user uploads an image and receives a predicted class and class scores. The goal is demonstration and research exploration, not forensic certification.

## Architecture
1. Streamlit upload interface.
2. File type and size validation, then RGB conversion.
3. Hugging Face image processor converts image pixels to model inputs.
4. Pretrained image-classification transformer generates logits.
5. Softmax converts logits into relative class scores.
6. UI displays the predicted class, model score, and limitations.

## Current implementation
- Upload PNG/JPEG/WEBP/BMP images.
- Reject files over 10 MB and report unreadable images.
- Load/cache the pretrained model.
- Display predicted class and class scores.
- Surface model errors in the UI for troubleshooting.

## Suggested evaluation plan
Compare the selected pretrained model against a CNN baseline, a vision transformer baseline, and frequency/residual-based features. Use generator-disjoint train/validation/test splits. Report accuracy, precision, recall, F1, ROC-AUC, false-positive rate, confusion matrix, and latency. Test robustness to JPEG compression, resizing, blur, screenshots, and unseen generation models.

## Paper study
- Wang et al., “CNN-generated images are surprisingly easy to spot… for now,” CVPR 2020.
- Ojha et al., “Towards Universal Fake Image Detectors that Generalize Across Generative Models,” CVPR 2023.
- “DIRE for Diffusion-Generated Image Detection,” ICCV 2023.
- “GenImage: A Million-Scale Benchmark for Detecting AI-Generated Image,” NeurIPS 2023 Datasets and Benchmarks.

## Proposed next methodology
A research extension could combine a spatial vision branch with frequency/residual features, calibrate the combined score, and evaluate on generators excluded from training. This is proposed future work, not implemented in this prototype.

## Important existing-project caveat
The original repository's notebook appears to use a very small training split and has checkpoint-path inconsistencies. Do not present those old notebook results as a strong benchmark without retraining and evaluating on a suitable held-out dataset.
