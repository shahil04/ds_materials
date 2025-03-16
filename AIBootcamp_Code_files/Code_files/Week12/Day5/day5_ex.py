# from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
# from datasets import load_dataset

# # # Load dataset
# # dataset = load_dataset("imdb")

# # # Tokenizer
# # tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# # # Tokenize the dataset
# # def tokenize_function(examples):
# #     return tokenizer(examples["text"], padding="max_length", truncation=True)

# # tokenized_datasets = dataset.map(tokenize_function, batched=True)

# # # Prepare data for training
# # tokenized_datasets = tokenized_datasets.remove_columns(["text"])
# # tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
# # tokenized_datasets.set_format("torch")

# # train_dataset = tokenized_datasets["train"]
# # test_dataset = tokenized_datasets["test"]

# # model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# # training_args = TrainingArguments(
# #     output_dir="./results",
# #     eval_strategy="epoch",
# #     learning_rate=2e-5,
# #     per_device_train_batch_size=8,
# #     per_device_eval_batch_size=8,
# #     num_train_epochs=3,
# #     weight_decay=0.01,
# #     logging_dir="./logs",
# #     logging_steps=10,
# #     save_steps=500
# # )

# # trainer = Trainer(
# #     model=model, 
# #     args=training_args, 
# #     train_dataset=train_dataset, 
# #     eval_dataset=test_dataset,
# #     processing_class=tokenizer
# # )

# # trainer.train()

# # results = trainer.evaluate()
# # print("Evaluation Results", results)

# # Experiment with GPT
# from transformers import AutoModelForCausalLM

# gpt_model = AutoModelForCausalLM.from_pretrained("gpt2")
# tokenizer = AutoTokenizer.from_pretrained("gpt2")

# input_text = "Once upon a time"
# input_ids = tokenizer.encode(input_text, return_tensors="pt")

# attention_mask = input_ids.ne(tokenizer.pad_token_id)

# output = gpt_model.generate(
#     input_ids,
#     attention_mask=attention_mask,
#     max_length=50,
#     num_return_sequences=1,
#     pad_token_id=tokenizer.eos_token_id
# )

# print("Generated Text:", tokenizer.decode(output[0], skip_special_tokens=True))

from transformers import AutoModelForCausalLM, AutoTokenizer

# Load pre-trained GPT model and tokenizer
gpt_model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Generate text
input_text = "Once upon a time"
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Define attention mask
attention_mask = input_ids.ne(tokenizer.pad_token_id)

# If eos_token_id is None, use pad_token_id as -1, otherwise use eos_token_id
pad_token_id = tokenizer.eos_token_id if tokenizer.eos_token_id is not None else -1

output = gpt_model.generate(
    input_ids,
    attention_mask=attention_mask,
    max_length=50,
    num_return_sequences=1,
    pad_token_id=pad_token_id
)

print("Generated Text:", tokenizer.decode(output[0], skip_special_tokens=True))
