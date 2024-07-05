import requests
import pandas as pd
import re
import csv
import os

# Load the CSV file
file_path = ('C:/Users/ADD_YOUR_FILE_PATH_HERE')
csv_file_name = 'NAME_OF_YOUR_CSV_FILE'
df_main = pd.read_csv(file_path + csv_file_name + '.csv')

# Convert the 'report_id' and 'raw_report' columns to a list, remove empty cells, and remove line breaks and carriage return for more consistent processing by the LLM
report_id_list = df_main['report_id'].dropna().apply(lambda x: x.lower().replace('\n', ' ').replace('\r', ' ').replace('  ', ' ').replace('   ', ' ').replace('    ', ' ').replace('  ', ' ')).tolist()
radiology_report_list = df_main['radiology_reports'].dropna().apply(lambda x: x.lower().replace('\n', ' ').replace('\r', ' ').replace('  ', ' ').replace('   ', ' ').replace('    ', ' ').replace('  ', ' ')).tolist()

# Set up API
model_url = "http://127.0.0.1:5000/v1/chat/completions"
headers = {
    "Content-Type": "application/json; charset=utf-8"
}
assistant_message_list = []

# Specify model name, instruction template, and chat template names. Using ‘None’ will make ooba try to find it from the config.json file with the model
model_name = 'mistralai_Mistral-7B-Instruct-v0.2'
instruction_template = 'Mistral'

# File to save the responses as CSV
response_csv_file_path = file_path + model_name + '_responses' + '.csv'

# Check if the file exists to decide whether to write headers
file_exists = os.path.isfile(response_csv_file_path)

# Initialize the report and batch counter. This is so that the progress is saved every 50 reports for longer runtimes
report_counter = 0
batch_size = 50
batched_responses = []

"""
Iteratively input your reports to the model and collect responses:
- You can create your own instruction template and preset (i.e. generation hyperparameter settings). Additional 
information can be found in the docs folder of text-generation-webui-main folder.
- Three commonly adjusted hyperparameters are listed below. Temperature adjusts the randomness of generation. Studies of 
LLMs for radiology related tasks have shown the strongest performance with a lower temperature. This also increases the 
reproducibility. To increase reproducibility further, set the seed to any integer. Setting it to -1 makes it a random 
seed for text-generation-webui. 
- Further information for each hyperparameter can be found in the Parameters Tab of the docs folder.
"""
for report, report_id in zip(radiology_report_list, report_id_list):
    user_message = ("Classify if the following radiology report indicated the presence of cirrhosis: ") + report
    data = {
        "mode": "instruct",
        "messages": [{"role": "user", "content": user_message}],
        "model": model_name,
        "instruction_template": instruction_template,
        "chat_template_str": "None",
        "preset": "LLaMA-Precise",
        "temperature": 0.01,
        "max_tokens": 15000,
        "truncation_length": 32768,
        "seed": 1
    }

    response = requests.post(model_url, headers=headers, json=data, verify=False)
    assistant_message = response.json()['choices'][0]['message']['content']
    assistant_message_list.append([report_id, report, assistant_message])

    # Start counting
    report_counter += 1

    # Write to CSV every 50 reports or at the end
    if report_counter % batch_size == 0 or report_counter == len(report_id_list):
        with open(response_csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            if not file_exists:  # This will be True only the first time the file is being created
                csv_writer.writerow(['report_id', 'radiology_reports', 'model_full_response'])
                file_exists = True  # Ensure headers aren't written again
            for response_row in assistant_message_list:
                csv_writer.writerow(response_row)

        batched_responses = []  # Reset the batched responses after writing
