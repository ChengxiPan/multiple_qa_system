from transformers import AutoTokenizer, AutoModelForMultipleChoice
from datasets import Dataset
import torch
import numpy as np

model_dir = './checkpoint-24624'
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

def get_predictions(example):
    tokenized_example = preprocess(example)
    inputs = {key: value.unsqueeze(0) for key, value in tokenized_example.items() if key in ['input_ids', 'attention_mask', 'token_type_ids']}
    
    # Extract the options and their text
    options = ['A', 'B', 'C', 'D']
    answers = [(option, example.get(option, "N/A")) for option in options if option in example]
    
    # Get the model's predictions
    predictions = model(**inputs)
    filtered_logits = predictions.logits[:, :len(answers)]   # Only take the first len(answers) logits
    
    # Combine the option (A/B/C/D), text, and logits, then sort by logits
    ranked_answers = sorted(
        zip([ans[0] for ans in answers], [ans[1] for ans in answers], filtered_logits[0].tolist()), 
        key=lambda x: x[2],  # Sort by logits
        reverse=True
    )
    
    # Return as [('A', 'Paris', score), ('C', 'Madrid', score), ...]
    return ranked_answers


if __name__ == '__main__':
    Question = "Which of the following is the most direct cause of polyteny in somatic cells of certain organisms?"
    A = "RNA transcription"
    B = "Supercoiling of chromatin"
    C = "Chromosome replication without cell division"
    D =  "Chromosome recombination"
    example = {'prompt': Question, 'A': A, 'B': B, 'C': C, 'D': D}

    print(get_predictions(example))