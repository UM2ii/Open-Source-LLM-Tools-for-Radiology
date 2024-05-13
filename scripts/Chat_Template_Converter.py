from transformers import AutoTokenizer
import pandas as pd
import json
import os


def create_openai_chat_formatted_jsonl_file(df: pd.DataFrame, output_file_path: str):
    """
    Function to take a dataframe with columns labeled "instruction", "input", and "output" and convert it to a jsonl
    file in the standard format for OpenAI API calls.

    Args:
    df (pd.DataFrame): The DataFrame loaded from the csv file.
    output_file_path (string): The filepath to save the newly created jsonl file
    """
    data_list = []
    try:
        with open(output_file_path, "w") as output_jsonl_file:
            for _, row in df.iterrows():
                user_content = f"{row['instruction']} {row['input']}"
                assistant_content = row['output']

                json_object = {
                    "messages": [
                        {"role": "user", "content": user_content},
                        {"role": "assistant", "content": assistant_content}
                    ]
                }
                output_jsonl_file.write(json.dumps(json_object) + "\n")
                data_list.append(json_object)
        print(f"OpenAI chat formatted JSONL file saved to: {output_file_path}")
        return data_list
    except Exception as e:
        print(f"An error occurred: {e}")


def create_openai_chat_formatted_json_file(data_list, output_file_path):
    """
    Save the data as a single JSON file.

    Args:
    data_list (list): List of chat data entries.
    output_file_path (string): The filepath to save the JSON file.
    """
    try:
        with open(output_file_path, 'w') as output_json_file:
            json.dump(data_list, output_json_file)
        print(f"JSON file saved to: {output_file_path}")
    except Exception as e:
        print(f"Error while writing JSON file: {e}")

def load_jsonl_file(file_path):
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                data.append(json.loads(line))
        print(f"Data loaded from {file_path}")
    except Exception as e:
        print(f"Failed to load data: {e}")
    return data


def apply_chat_template_to_jsonl(data, tokenizer):
    transformed_data = []
    try:
        for entry in data:
            chat = entry.get("messages", [])
            transformed_entry = tokenizer.apply_chat_template(chat, tokenize=False)
            transformed_data.append(transformed_entry)
    except Exception as e:
        print(f"Failed to apply chat template: {e}")
    return transformed_data


def save_transformed_data(transformed_data, output_path, file_type='jsonl'):
    """
    Save transformed data to a file in either JSONL or JSON format.

    Args:
    transformed_data (list): List of transformed chat entries.
    output_path (string): The file path where the data will be saved.
    file_type (str, optional): Type of file to save ('jsonl' or 'json'). Defaults to 'jsonl'.
    """
    try:
        with open(output_path, 'w') as file:
            if file_type == 'jsonl':
                for entry in transformed_data:
                    file.write(json.dumps(entry) + '\n')
            elif file_type == 'json':
                json.dump(transformed_data, file)
        print(f"Transformed data saved to: {output_path}")
    except Exception as e:
        print(f"Error saving transformed data: {e}")


# File paths configuration
file_path = 'C:/Users/ADD_YOUR_FILE_PATH_HERE'
csv_file_name = 'NAME_OF_YOUR_CSV_FILE'
csv_file_path = os.path.join(file_path, f'{csv_file_name}.csv')
jsonl_file_path = os.path.join(file_path, f'{csv_file_name}_OpenAI_template.jsonl')
json_file_path = os.path.join(file_path, f'{csv_file_name}_OpenAI_template.json')
transformed_jsonl_path = os.path.join(file_path, f'{csv_file_name}_transformed_chat_template.jsonl')
transformed_json_path = os.path.join(file_path, f'{csv_file_name}_transformed_chat_template.json')

# Load csv file. Make sure you have the three columns of data: "instruction", "input", and "output"
df_main = pd.read_csv(csv_file_path)

# Create OpenAI API formatted jsonl file from your dataset
data_list = create_openai_chat_formatted_jsonl_file(df_main, jsonl_file_path)

# Create OpenAI API formatted json file from your dataset
create_openai_chat_formatted_json_file(data_list, json_file_path)

# Load the tokenizer of the model whose chat template you want to apply
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

# Load, transform, and save the chat template applied data
jsonl_data = load_jsonl_file(jsonl_file_path)
transformed_data = apply_chat_template_to_jsonl(jsonl_data, tokenizer)
save_transformed_data(transformed_data, transformed_jsonl_path, 'jsonl')  # Save as JSONL file
save_transformed_data(transformed_data, transformed_json_path, 'json')  # Save as JSON file
