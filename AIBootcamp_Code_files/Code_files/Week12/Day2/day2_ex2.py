from transformers import BertTokenizer, TFBertModel

# Load a pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = TFBertModel.from_pretrained("bert-base-uncased")

# Tokenize a sample input
text = "Transformers are powerful models for NLP tasks"
inputs = tokenizer(text, return_tensors='tf')

# Pass the input through the model
outputs = model(**inputs)
print("Hidden States Shape:", outputs.last_hidden_state.shape)