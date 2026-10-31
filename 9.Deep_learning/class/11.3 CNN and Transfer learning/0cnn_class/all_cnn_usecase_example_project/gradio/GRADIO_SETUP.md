# Run the Gradio Computer Vision Demo Lab

## Local setup
Recommended: Python 3.10 or 3.11.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Gradio prints a local URL (usually `http://127.0.0.1:7860`). Open it in your browser.

## Google Colab
1. Upload the project folder or `app.py` and `requirements.txt` to Colab.
2. Install packages with `!pip install -r requirements.txt`.
3. Launch with `!python app.py` or in a notebook cell:
   ```python
   import app
   ```
   For a public share URL, change the final line to `demo.launch(share=True)` in a trusted environment.
4. For training notebooks, open the relevant `.ipynb` directly in Colab and enable a GPU runtime.

## Topics in the interface
- Classical OpenCV edges and contours
- YOLO object detection
- Faster R-CNN object detection
- MobileNetV2 image classification
- DeepLabV3 semantic segmentation
- Facial-expression image classification
- ResNet feature similarity baseline
- DCGAN generation from MNIST

The app uses pretrained weights and internet downloads for several modes. The GAN mode uses a small subset for a bounded demo; for full training, use notebook 08 on Colab GPU. All results are educational examples, not validated high-stakes systems.
