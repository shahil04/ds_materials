from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TrainingArguments, Trainer
import evaluate
import torch
import os

# Set environment variable to avoid potential conflicts
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# Load a smaller dataset for summarization
dataset = load_dataset("samsum")
#print(dataset["train"][0])

# Load tokenizer and model
model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Tokenize for summarization
def tokenize_function(examples):
    inputs = ["summarize: " + doc for doc in examples["dialogue"]]
    model_inputs = tokenizer(
        inputs, max_length=512, truncation=True, padding="max_length"
    )
    
    # Tokenize targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            examples["summary"], max_length=150, truncation=True, padding="max_length"
        )
        
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    load_best_model_at_end=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    processing_class=tokenizer
)

#trainer.train()

# Set device
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)

# Define a sample text for summarization
sample_text = "The Transformer model has revolutionized NLP by enabling parallel processing of sequences."
inputs = tokenizer("summarize: " + sample_text, return_tensors="pt", max_length=512, truncation=True).to(device)
outputs = model.generate(inputs["input_ids"], max_length=150, num_beams=4, early_stopping=True)

print("Generated Summary: ", tokenizer.decode(outputs[0], skip_special_tokens=True))

# Load metric
# metric = evaluate.load("rouge")
# predictions = [tokenizer.decode(g, skip_special_tokens=True) for g in outputs]
# references = [tokenizer.decode(r, skip_special_tokens=True) for r in tokenized_datasets["validation"]["summary"]]

# results = metric.compute(predictions=predictions, references=references)
# print(results)
