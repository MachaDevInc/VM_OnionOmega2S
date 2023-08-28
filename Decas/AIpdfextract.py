import pandas as pd
from transformers import DistilBertTokenizerFast, DistilBertForTokenClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import torch

# Step 1: Preprocess the text data and create the dataset
# Replace this with the actual data in the format described in your question
data = [
    ("# Item Quantity Unit price Tax Discount Total\n1 HD Monitor 1 132.00 _ 0.00% 132.00", "ITEM QUANTITY PRICE TAX DISCOUNT TOTAL"),
    # Add more examples here
]

# Tokenize the text and labels
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
tokenized_data = [tokenizer(example[0], example[1], padding="max_length", truncation=True) for example in data]

# Map labels to unique IDs
label_to_id = {label: i for i, label in enumerate(set(label for example in tokenized_data for label in example["labels"]))}
id_to_label = {i: label for label, i in label_to_id.items()}

# Create a PyTorch dataset from the tokenized data
class ReceiptDataset(torch.utils.data.Dataset):
    def __init__(self, tokenized_data):
        self.tokenized_data = tokenized_data

    def __getitem__(self, idx):
        return {key: torch.tensor(value[idx]) for key, value in self.tokenized_data.items()}

    def __len__(self):
        return len(self.tokenized_data["input_ids"])

dataset = ReceiptDataset(tokenized_data)
train_dataset, val_dataset = train_test_split(dataset, test_size=0.1)

# Step 2: Train the sequence tagging model
model = DistilBertForTokenClassification.from_pretrained("distilbert-base-uncased", num_labels=len(label_to_id))

# Set up the training arguments and the Trainer
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    logging_dir="./logs",
    logging_steps=10,
    save_steps=10,
    evaluation_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Train the model
trainer.train()

# Step 3: Use the trained model to predict fields in new receipts
def predict_fields(text, model, tokenizer, id_to_label):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    labels = [id_to_label[prediction.item()] for prediction in predictions[0]]
    return labels

# Example usage
text = "1 HD Monitor 1 132.00 _ 0.00% 132.00"
labels = predict_fields(text, model, tokenizer, id_to_label)
print(labels)
