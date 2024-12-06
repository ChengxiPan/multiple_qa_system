from transformers import AutoTokenizer, AutoModelForMultipleChoice
from datasets import Dataset
import torch
import numpy as np

model_dir = './model'
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForMultipleChoice.from_pretrained(model_dir)

options = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
option_to_index = {option: idx for idx, option in enumerate(options)}
index_to_option = {idx: option for option, idx in option_to_index.items()}

def preprocess(example, max_choices=5):
    answers = [example.get(option, "N/A") for option in options if option in example]    
    if len(answers) < max_choices:
        answers += ["N/A"] * (max_choices - len(answers))
    sentences = [[example['prompt'], ans] for ans in answers]
    tokenized = tokenizer(sentences, truncation=True, padding=True, return_tensors='pt')
    tokenized['label'] = option_to_index.get(example.get('answer', 'A'), 0)
    return tokenized

def predict(example):
    tokenized_example = preprocess(example)
    inputs = {key: value.unsqueeze(0) for key, value in tokenized_example.items() if key in ['input_ids', 'attention_mask', 'token_type_ids']}
    answers = [example.get(option, "N/A") for option in options if option in example]
    
    predictions = model(**inputs)
    filtered_logits = predictions.logits[:, :len(answers)]   # Only take the first len(answers) logits
    predicted_answer_idx = torch.argmax(filtered_logits, dim=1).item()
    predicted_answer = index_to_option[predicted_answer_idx]
    return predicted_answer

if __name__ == '__main__':
    Question = "What is the capital of France?"
    A = "Paris"
    B = "Berlin"
    C = "Madrid"
    example = {'prompt': Question, 'A': A, 'B': B, 'C': C}

    tokenized_example = preprocess(example)
    inputs = {key: value.unsqueeze(0) for key, value in tokenized_example.items() if key in ['input_ids', 'attention_mask', 'token_type_ids']}
    answers = [example.get(option, "N/A") for option in options if option in example]
    print("Answers:", answers)
    predictions = model(**inputs)
    filtered_logits = predictions.logits[:, :len(answers)]   # Only take the first len(answers) logits
    print("Predicted Logits:", filtered_logits)

    predicted_answer_idx = torch.argmax(filtered_logits, dim=1).item()
    predicted_answer = index_to_option[predicted_answer_idx]
    print("Predicted Answer:", predicted_answer)