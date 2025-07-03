from transformers import pipeline

def generate_script(prompt):
    generator = pipeline("text-generation", model="gpt2")
    result = generator(prompt, max_length=150, do_sample=True)[0]["generated_text"]
    return result
