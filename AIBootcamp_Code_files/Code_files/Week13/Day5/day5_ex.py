import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_scheduler
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

# Load Dataset
dataset = load_dataset("imdb")
train_texts, test_texts, train_labels, test_labels = train_test_split(
    dataset['train']['text'], dataset['train']['label'], test_size=0.2, random_state=42
)

# Tokenization
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_data(texts, labels, tokenizer, max_length=128):
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length)
    return {
        "input_ids": encodings["input_ids"],
        "attention_mask": encodings["attention_mask"],
        "labels": labels
    }

train_data = tokenize_data(train_texts, train_labels, tokenizer)
test_data = tokenize_data(test_texts, test_labels, tokenizer)

class IMDBDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.input_ids = data["input_ids"]
        self.attention_mask = data["attention_mask"]
        self.labels = data["labels"]
        
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return {
            "input_ids": torch.tensor(self.input_ids[idx]),
            "attention_mask": torch.tensor(self.attention_mask[idx]),
            "labels": torch.tensor(self.labels[idx]),
        }

train_dataset = IMDBDataset(train_data)
test_dataset = IMDBDataset(test_data)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16)

# Load Pre-Trained Model
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Define Optimizer and STLR Scheduler
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)

# Define Slanted Triangular Learing Rate(STLR) Scheduler
num_training_steps = len(train_loader) * 3
warmup_steps = int(0.1 * num_training_steps)
scheduler = get_scheduler(
    "linear", optimizer=optimizer, num_warmup_steps=warmup_steps, num_training_steps=num_training_steps
)

#Training Loop

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def train_model():
    model.train()
    for epoch in range(3):
        for batch in train_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            
# train_model()

# Evaluate Model using F1-score
model.eval()
all_preds, all_labels = [], []

with torch.no_grad():
    for batch in test_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        preds = torch.argmax(outputs.logits, dim=-1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(batch["labels"].cpu().numpy())

f1 = f1_score(all_labels, all_preds, average="weighted")
print(f"F1-Score: {f1:.4f}")

from sacrebleu import BLEU

# Example Reference and Hypotheses
references = [["this is a test sentence", "this is a sample sentence"]]
hypotheses = ["This is a test"]

bleu = BLEU()

bleu_score = bleu.corpus_score(hypotheses, references).score
print(f"BLEU Score: {bleu_score:.2f}")