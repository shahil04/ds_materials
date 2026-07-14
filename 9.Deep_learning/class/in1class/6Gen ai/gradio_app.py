
import gradio as gr
from transformers import pipeline
from diffusers import StableDiffusionPipeline
from PIL import Image
import torch
import tempfile
import os


# -----------------------------
# requirements.txt
# gradio
# transformers
# torch
# diffusers
# accelerate
# safetensors
# sentencepiece
# Pillow

# -----------------------------
# -------- Lazy loading --------
_sentiment = _textcls = _textgen = _summ = _trans = None
_zero = _img = _asr = _embed = None
_sd = None

def sentiment():
    global _sentiment
    if _sentiment is None:
        _sentiment = pipeline("sentiment-analysis")
    return _sentiment

def textcls():
    global _textcls
    if _textcls is None:
        _textcls = pipeline("text-classification", model="distilbert-base-uncased")
    return _textcls

def textgen():
    global _textgen
    if _textgen is None:
        _textgen = pipeline("text-generation", model="gpt2")
    return _textgen

def summ():
    global _summ
    if _summ is None:
        _summ = pipeline("summarization", model="facebook/bart-large-cnn")
    return _summ

def trans():
    global _trans
    if _trans is None:
        _trans = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
    return _trans

def zero():
    global _zero
    if _zero is None:
        _zero = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return _zero

def imgcls():
    global _img
    if _img is None:
        _img = pipeline("image-classification", model="google/vit-base-patch16-224")
    return _img

def asr():
    global _asr
    if _asr is None:
        _asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    return _asr

def embed():
    global _embed
    if _embed is None:
        _embed = pipeline("feature-extraction",
                          model="sentence-transformers/all-MiniLM-L6-v2")
    return _embed

def sd():
    global _sd
    if _sd is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=dtype
        ).to(device)
        _sd = pipe
    return _sd

# -------- Functions --------
def run_sentiment(text): return sentiment()(text)
def run_textcls(text): return textcls()(text)

def run_textgen(prompt, max_len):
    out = textgen()(prompt, max_length=int(max_len), do_sample=True)
    return out[0]["generated_text"]

def run_summary(text):
    return summ()(text)[0]["summary_text"]

def run_translation(text):
    return trans()(text)[0]["translation_text"]

def run_zero(text, labels):
    return zero()(text, candidate_labels=[x.strip() for x in labels.split(",")])

def run_image(image):
    return imgcls()(image)

def run_asr(audio):
    return asr()(audio)["text"]

def run_embedding(text):
    e = embed()(text)
    return f"Shape: [1,{len(e[0])},{len(e[0][0])}]\\nFirst 10 values: {e[0][0][:10]}"

def run_sd(prompt):
    return sd()(prompt).images[0]

with gr.Blocks(title="Hugging Face Multi-Model Playground") as demo:
    gr.Markdown("# 🤗 Hugging Face Multi-Model Playground (Gradio)")

    with gr.Tab("Sentiment"):
        t = gr.Textbox(value="I love Hugging Face!")
        o = gr.JSON()
        gr.Button("Analyze").click(run_sentiment, t, o)

    with gr.Tab("Text Classification"):
        t = gr.Textbox()
        o = gr.JSON()
        gr.Button("Classify").click(run_textcls, t, o)

    with gr.Tab("Text Generation"):
        p = gr.Textbox()
        m = gr.Slider(20,200,60,step=1)
        o = gr.Textbox(lines=8)
        gr.Button("Generate").click(run_textgen,[p,m],o)

    with gr.Tab("Summarization"):
        t = gr.Textbox(lines=8)
        o = gr.Textbox(lines=6)
        gr.Button("Summarize").click(run_summary,t,o)

    with gr.Tab("Translation EN→HI"):
        t = gr.Textbox()
        o = gr.Textbox()
        gr.Button("Translate").click(run_translation,t,o)

    with gr.Tab("Zero-shot"):
        t = gr.Textbox()
        l = gr.Textbox(value="education,technology,sports")
        o = gr.JSON()
        gr.Button("Run").click(run_zero,[t,l],o)

    with gr.Tab("Image Classification"):
        i = gr.Image(type="pil")
        o = gr.JSON()
        gr.Button("Classify").click(run_image,i,o)

    with gr.Tab("Speech to Text"):
        a = gr.Audio(type="filepath")
        o = gr.Textbox()
        gr.Button("Transcribe").click(run_asr,a,o)

    with gr.Tab("Embeddings"):
        t = gr.Textbox()
        o = gr.Textbox(lines=6)
        gr.Button("Extract").click(run_embedding,t,o)

    with gr.Tab("Text to Image"):
        p = gr.Textbox(value="A cute robot teaching AI")
        img = gr.Image()
        gr.Button("Generate").click(run_sd,p,img)

demo.launch()
