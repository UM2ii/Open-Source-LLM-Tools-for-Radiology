# LLaMA Factory Setup Guide

## Prerequisites
Before starting, ensure you have a JSON file of your training data formatted with keys for "instruction", "input", "output". Optionally, you can include "history" to incorporate conversations in your training data. For more information, refer to the **Chat_Template_Converter_Guide**.

## Installation Steps

### Step 1: Setup
- Download [Python 3.10](https://www.python.org/downloads/)
- Download [Anaconda](https://www.anaconda.com/download)
- Download [Git](https://github.com/git-guides/install-git)
- Download an IDE such as [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows) or [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/).

### Step 2: Navigate to Project Directory
- **Windows**: Open Anaconda Powershell Prompt and navigate to a preffered folder using:

```bash
cd C:\Users\your_folder_path\
```

- **Mac or Linux**: Open a terminal and navigate using:
```bash
cd C:/Users/your_folder_path/
```

### Step 3: Clone LLaMA Factory and Install Dependencies
Enter the following commands into the Anaconda Powershell Prompt to download LLaMA Factory and it’s required packages:
```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
conda create -n llama_factory python=3.10
conda activate llama_factory
pip install -r requirements.txt
pip install -e .[torch,metrics]
```

### Step 4: Setup GPU Usage
To enable the use of your GPU, enter the following commands:
```bash
conda install cuda -c nvidia/label/cuda-12.1.0
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
conda install typing-extensions
```

### Step 5: Add Training Data
To add your training data, add a json file of your dataset to the 'data' folder within the 'LLaMA-Factory' folder. Update 'dataset_info.json' with an entry for the name of your dataset. For example, if your dataset file name is 'open_LLM_dataset' it can be added in the following way:
```bash
},
  "other_training_data": {
    "file_name": "other_training_data.json",
    "file_sha1": "9db59f6b7007dc4b17529fc62179b9cd61640f37",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output",
      "history": "history"
    }
  },
  "open_LLM_dataset": {
    "file_name": "open_LLM_dataset.json",
    "file_sha1": "ADD your SHA1 CODE HERE",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output",
      "history": "history"
    }
  },
```
To find the SHA1 code:
- **Windows**: Open the windows powershell and enter the following:
```bash
Get-FileHash C:\path_to_your_LLaMA_Factory_folder\LLaMA-Factory\data\open_LLM_dataset.json -Algorithm SHA1
```
- **macOS or Linux**: Open the terminal app and enter the following:
```bash
shasum /path_to_your_LLaMA_Factory_folder/LLaMA-Factory/data/open_LLM_dataset.json
```

### Step 6: Configure GPU Settings
Next you will set how many GPUs to use for your fine-tune by entering the following command in the Anaconda Powershell Prompt:
- **Windows**:
```bash
$env:CUDA_VISIBLE_DEVICES = "0"
```
- **macOS or Linux**:
```bash
export CUDA_VISIBLE_DEVICES=0
```
> [!TIP]
> Numbering starts at 0, so "0" is one GPU, "0,1" is two GPUs, and so on.

### Step 7: Start Fine-Tuning
Now you can begin fine-tuning your model. An example of training a LORA with supervised fine-tuning is shown below. Enter the following into the Anaconda Powershell Prompt, adjusting the arguments as necessary:
- **Windows**:
```bash
python src/train_bash.py --stage sft --do_train True --model_name_or_path mistral-community/Mistral-7B-v0.2 --finetuning_type lora --template mistral --flash_attn auto --dataset_dir data --dataset open_LLM_dataset --cutoff_len 32768 --learning_rate 5e-5 --num_train_epochs 3.0 --max_samples 10000 --per_device_train_batch_size 1 --gradient_accumulation_steps 4 --lr_scheduler_type cosine --max_grad_norm 0.3 --logging_steps 30 --save_steps 1000 --warmup_steps 5 --neftune_noise_alpha 0 --lora_rank 16 --lora_dropout 0.05 --lora_target q_proj,v_proj --output_dir saves\Mistral-7B-v0-2 --bf16 True --val_size 0.1 --evaluation_strategy steps --eval_steps 1000 --load_best_model_at_end True --plot_loss True --overwrite_output_dir True
```
- **macOS or Linux**:
```bash
python src/train_bash.py --stage sft --do_train True --model_name_or_path mistral-community/Mistral-7B-v0.2 --finetuning_type lora --template mistral --flash_attn auto --dataset_dir data --dataset open_LLM_dataset --cutoff_len 32768 --learning_rate 5e-5 --num_train_epochs 3.0 --max_samples 10000 --per_device_train_batch_size 1 --gradient_accumulation_steps 4 --lr_scheduler_type cosine --max_grad_norm 0.3 --logging_steps 30 --save_steps 1000 --warmup_steps 5 --neftune_noise_alpha 0 --lora_rank 16 --lora_dropout 0.05 --lora_target q_proj,v_proj --output_dir saves/Mistral-7B-v0-2-LORA --bf16 True --val_size 0.1 --evaluation_strategy steps --eval_steps 1000 --load_best_model_at_end True --plot_loss True --overwrite_output_dir True
```

### Step 8: Testing and Using Your Fine-Tuned Model
- Test to see if it worked by copying the new folder created “Mistral-7B-v0-2-LORA” within the “saves” folder of LLaMA-Factory to the “loras” folder of your “text-generation-webui-main” folder (Please see [Radiology report processing with Text Generation Web UI](https://github.com/csavages/Open-Source-LLM-Tools-for-Radiology/edit/main/docs/Radiology%20report%20processing%20with%20Text%20Generation%20Web%20UI.md) for installation and other tips).
- Start text-generation-webui by running the “start_windows.bat” (or start_macos.sh; or start_linux.sh) in the text-generation-webui-main folder.
- Using the web user interface, select the model tab and load the correct model that you trained the lora for (e.g. mistral-community_Mistral-7B-v0.2) using the Transformers loader. For more information on loaders read the Model Tab document in [text-generation-webui](https://github.com/oobabooga/text-generation-webui/tree/main/docs).
- Then select the name of your lora in the dropdown menu for loras (e.g., Mistral-7B-v0-2-LORA) and load it.
- Next, select the “Parameters” tab and then select “Instruction template”. Select the appropriate chat template (e.g., Mistral) and load the template.
- Finally, select the “Chat” tab and then select “Instruct” for the mode. Now you can chat directly with your fine-tuned model using the chatbot interface or have your fine-tuned model iteratively process data (e.g., radiology reports). See [Radiology report processing with Text Generation Web UI](https://github.com/csavages/Open-Source-LLM-Tools-for-Radiology/edit/main/docs/Radiology%20report%20processing%20with%20Text%20Generation%20Web%20UI.md) for more information.
