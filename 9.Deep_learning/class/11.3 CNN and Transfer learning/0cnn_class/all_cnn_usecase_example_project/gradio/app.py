import gradio as gr
from PIL import Image
import numpy as np
import io
import traceback

TITLE_TO_KEY = {
    "1. Classical CV — edges and contours": "classical",
    "2. YOLO — modern object detection": "yolo",
    "3. Faster R-CNN — two-stage detection": "fasterrcnn",
    "4. Image classification — MobileNetV2": "classification",
    "5. Semantic segmentation — DeepLabV3": "segmentation",
    "6. Facial-expression classification": "expression",
    "7. Siamese-style image similarity": "similarity",
    "8. GAN — generate MNIST-like images": "gan",
}

def run_demo(topic, image, second_image):
    """Run the selected computer vision example and return (image, summary, table)."""
    if topic not in TITLE_TO_KEY:
        return None, "Please choose a project.", []
    key = TITLE_TO_KEY[topic]
    try:
        if key == "classical":
            if image is None:
                return None, "Upload an image first.", []
            import cv2
            rgb = np.array(image.convert("RGB"))
            bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            annotated = bgr.copy()
            kept = 0
            for c in contours:
                if cv2.contourArea(c) < 150:
                    continue
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)
                kept += 1
            # Show annotated image; edge image is also described in the text.
            out = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            return Image.fromarray(out), f"OpenCV found {kept} contour(s) above the area threshold. This is rule-based shape detection, not semantic object recognition.", [
                {"metric": "Contours found", "value": kept},
                {"metric": "Method", "value": "Gaussian blur + Canny + contours"},
            ]

        if key == "yolo":
            if image is None:
                return None, "Upload an image first.", []
            from ultralytics import YOLO
            import torch
            model = YOLO("yolo11n.pt")
            device = 0 if torch.cuda.is_available() else "cpu"
            result = model.predict(source=image, conf=0.25, device=device, verbose=False)[0]
            out = Image.fromarray(result.plot()[..., ::-1])
            rows = []
            for b in result.boxes:
                rows.append({
                    "metric": model.names[int(b.cls[0])],
                    "value": f"confidence={float(b.conf[0]):.3f}; box={[round(float(v),1) for v in b.xyxy[0]]}"
                })
            return out, f"YOLO detected {len(rows)} object(s). Confidence values are model estimates, not guarantees.", rows

        if key == "fasterrcnn":
            if image is None:
                return None, "Upload an image first.", []
            import torch
            from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
            from PIL import ImageDraw
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
            model = fasterrcnn_resnet50_fpn(weights=weights).to(device).eval()
            x = weights.transforms()(image.convert("RGB")).to(device)
            with torch.no_grad():
                pred = model([x])[0]
            categories = weights.meta["categories"]
            out = image.convert("RGB").copy()
            draw = ImageDraw.Draw(out)
            rows = []
            for box, label, score in zip(pred["boxes"].cpu(), pred["labels"].cpu(), pred["scores"].cpu()):
                score = float(score)
                if score < 0.5:
                    continue
                x1, y1, x2, y2 = [float(v) for v in box.tolist()]
                name = categories[int(label)]
                draw.rectangle((x1, y1, x2, y2), outline="lime", width=3)
                draw.text((x1, max(0, y1-15)), f"{name} {score:.2f}", fill="red", stroke_width=1, stroke_fill="white")
                rows.append({"metric": name, "value": f"confidence={score:.3f}"})
            return out, f"Faster R-CNN returned {len(rows)} detection(s) above 0.50 confidence. It is a two-stage detector.", rows

        if key == "classification":
            if image is None:
                return None, "Upload an image first.", []
            import tensorflow as tf
            from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
            model = MobileNetV2(weights="imagenet")
            arr = np.array(image.convert("RGB").resize((224, 224)), dtype=np.float32)[None, ...]
            pred = model.predict(preprocess_input(arr), verbose=0)
            top = decode_predictions(pred, top=5)[0]
            rows = [{"metric": label, "value": f"{float(score):.1%}"} for _, label, score in top]
            return image.convert("RGB"), "MobileNetV2 predicts ImageNet categories for the whole image. Showing the top five labels.", rows

        if key == "segmentation":
            if image is None:
                return None, "Upload an image first.", []
            import torch
            from torchvision.models.segmentation import deeplabv3_resnet50, DeepLabV3_ResNet50_Weights
            weights = DeepLabV3_ResNet50_Weights.DEFAULT
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = deeplabv3_resnet50(weights=weights).to(device).eval()
            x = weights.transforms()(image.convert("RGB")).unsqueeze(0).to(device)
            with torch.no_grad():
                mask = model(x)["out"][0].argmax(0).cpu().numpy().astype(np.uint8)
            # Use a color palette so the pixel classes are visible.
            palette = np.zeros((256, 3), dtype=np.uint8)
            rng = np.random.default_rng(10)
            palette[:] = rng.integers(0, 256, size=(256, 3), dtype=np.uint8)
            mask_rgb = palette[mask]
            cats = weights.meta["categories"]
            vals, counts = np.unique(mask, return_counts=True)
            rows = [{"metric": cats[int(v)] if int(v) < len(cats) else str(int(v)), "value": f"{int(c)} pixels"} for v, c in zip(vals, counts) if int(v) < len(cats)]
            return Image.fromarray(mask_rgb), "DeepLabV3 predicted a semantic class for each pixel. The mask uses colors for class IDs; it is a demo model, not a medical or safety system.", rows

        if key == "expression":
            if image is None:
                return None, "Upload a face image first. Use only images you have permission to use.", []
            from transformers import pipeline
            clf = pipeline("image-classification", model="trpakov/vit-face-expression")
            pred = clf(image.convert("RGB"))
            rows = [{"metric": p["label"], "value": f"{float(p['score']):.1%}"} for p in pred[:5]]
            return image.convert("RGB"), "These are predicted visible facial-expression categories, not evidence of a person's actual internal feelings. Model download requires internet.", rows

        if key == "similarity":
            if image is None or second_image is None:
                return None, "Upload both images to compare them.", []
            import torch
            import torch.nn.functional as F
            from torchvision.models import resnet18, ResNet18_Weights
            weights = ResNet18_Weights.DEFAULT
            model = resnet18(weights=weights)
            model.fc = torch.nn.Identity()
            model.eval()
            tfm = weights.transforms()
            a = tfm(image.convert("RGB")).unsqueeze(0)
            b = tfm(second_image.convert("RGB")).unsqueeze(0)
            with torch.no_grad():
                za = F.normalize(model(a), dim=1)
                zb = F.normalize(model(b), dim=1)
                sim = float(F.cosine_similarity(za, zb))
            return image.convert("RGB"), f"Cosine similarity between pretrained ResNet18 features: {sim:.3f}. Higher values indicate more similar features, but this is not a validated identity-verification system.", [
                {"metric": "Cosine similarity", "value": f"{sim:.3f}"},
            ]

        if key == "gan":
            # Tiny subset for a bounded demo. For real GAN training use notebook 08 on Colab GPU.
            import torch
            import torch.nn as nn
            from torchvision import datasets, transforms
            from torch.utils.data import DataLoader, Subset
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            ds = datasets.MNIST("./data", train=True, download=True, transform=transforms.Compose([
                transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))
            ]))
            ds = Subset(ds, list(range(min(5000, len(ds)))))
            loader = DataLoader(ds, batch_size=128, shuffle=True, drop_last=True, num_workers=0)
            zdim = 100
            G = nn.Sequential(
                nn.Linear(zdim, 256*7*7), nn.BatchNorm1d(256*7*7), nn.ReLU(True),
                nn.Unflatten(1, (256,7,7)),
                nn.ConvTranspose2d(256,128,4,2,1), nn.BatchNorm2d(128), nn.ReLU(True),
                nn.ConvTranspose2d(128,64,4,2,1), nn.BatchNorm2d(64), nn.ReLU(True),
                nn.Conv2d(64,1,3,1,1), nn.Tanh()
            ).to(device)
            D = nn.Sequential(
                nn.Conv2d(1,64,4,2,1), nn.LeakyReLU(.2,True),
                nn.Conv2d(64,128,4,2,1), nn.BatchNorm2d(128), nn.LeakyReLU(.2,True),
                nn.Flatten(), nn.Linear(128*7*7,1)
            ).to(device)
            og = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(.5,.999))
            od = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(.5,.999))
            lossfn = nn.BCEWithLogitsLoss()
            # One pass through a 5k subset to keep the UI demo bounded.
            for real, _ in loader:
                real = real.to(device); n = real.size(0)
                od.zero_grad()
                loss_real = lossfn(D(real), torch.ones(n,1,device=device))
                fake = G(torch.randn(n,zdim,device=device)).detach()
                loss_fake = lossfn(D(fake), torch.zeros(n,1,device=device))
                (loss_real + loss_fake).backward(); od.step()
                og.zero_grad()
                fake = G(torch.randn(n,zdim,device=device))
                loss_g = lossfn(D(fake), torch.ones(n,1,device=device))
                loss_g.backward(); og.step()
            with torch.no_grad():
                samples = G(torch.randn(25,zdim,device=device)).cpu()
            grid = np.zeros((140,140), dtype=np.uint8)
            for i, sample in enumerate(samples):
                r, c = divmod(i, 5)
                digit = (((sample.squeeze().numpy()+1)/2).clip(0,1)*255).astype(np.uint8)
                grid[r*28:(r+1)*28, c*28:(c+1)*28] = digit
            return Image.fromarray(grid), "Generated 25 synthetic MNIST-like samples after one pass over a small training subset. Output quality is not guaranteed. For a fuller training demo, run notebook 08 in Colab GPU.", [
                {"metric": "Training subset", "value": "5,000 MNIST images"},
                {"metric": "Training", "value": "1 epoch / subset pass"},
            ]

    except Exception as e:
        return None, f"Error while running this demo: {type(e).__name__}: {e}\n\nCheck internet access and installed dependencies. For the full traceback, run locally and inspect the terminal.", []

    return None, "No output.", []

DESCRIPTION = """
Explore eight computer-vision demos: classical OpenCV, YOLO, Faster R-CNN, image classification,
semantic segmentation, facial-expression classification, image similarity, and GAN generation.
Pretrained models and datasets may download on first use. GPU is recommended for heavier models.
"""

with gr.Blocks(title="Computer Vision Demo Lab", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔎 Computer Vision Demo Lab")
    gr.Markdown(DESCRIPTION)
    gr.Markdown("> **Educational use only:** model predictions can be wrong. Facial-expression categories do not establish a person's true feelings.")
    with gr.Row():
        with gr.Column(scale=1):
            topic = gr.Dropdown(choices=list(TITLE_TO_KEY.keys()), value=list(TITLE_TO_KEY.keys())[1], label="Choose a project")
            image = gr.Image(type="pil", label="Upload image", sources=["upload", "webcam"])
            second_image = gr.Image(type="pil", label="Second image (similarity project only)", sources=["upload"])
            run = gr.Button("Run demo", variant="primary")
            clear = gr.ClearButton([image, second_image])
        with gr.Column(scale=2):
            output_image = gr.Image(type="pil", label="Output image")
            summary = gr.Textbox(label="Explanation / results", lines=5)
            table = gr.Dataframe(headers=["metric", "value"], datatype=["str", "str"], label="Predictions / measurements", interactive=False)
    run.click(run_demo, inputs=[topic, image, second_image], outputs=[output_image, summary, table])
    gr.Markdown("### Classroom questions\n- What does this model take as input and return as output?\n- Does it classify an image, draw boxes, label pixels, compare images, or generate new samples?\n- What errors could happen if lighting, background, or image quality changes?")

if __name__ == "__main__":
    demo.launch()
