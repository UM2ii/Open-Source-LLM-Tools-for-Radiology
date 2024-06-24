# Automated Radiology Report Processing Using LLMs

## Prerequisites
If you havent already, install the following:
- Download [Python 3.10](https://www.python.org/downloads/)
- Download [Anaconda](https://www.anaconda.com/download)
- Download [Git](https://github.com/git-guides/install-git)
- Download an IDE such as [Pycharm](https://www.jetbrains.com/pycharm/download/?section=windows) or [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/).

### Step 1: Install Text Generation Web UI
Text Generation Web UI is an extremely versitile and user friendly platform to load, inference, and even train LLMs. Detailed instructions can be found in the [repositiory](https://github.com/oobabooga/text-generation-webui/tree/main)
- Install Text Generation Web UI in your preffered folder: [download](https://github.com/oobabooga/text-generation-webui/archive/refs/heads/main.zip) the repositiory or clone it with Git:
```bash
cd /your_folder_path/
git clone https://github.com/oobabooga/text-generation-webui.git
```
- Run the one-click installer within the text-generation-webui-main folder corresponding to your operating system: `start_linux.sh`, `start_windows.bat`, `start_macos.sh`, or `start_wsl.bat`
- Complete the remaining installation steps per the text-generation-webui repository.

### Step 2: Open Text Generation Web UI and download a model
- To open Text Generation Web UI, run the one of the `start_linux.sh`, `start_windows.bat`, `start_macos.sh`, or `start_wsl.bat` files.
- This will print "Running on local URL: ..." followed by a URL. Copy this URL into your web browser to utilize the web user interface.
- In the 'model' tab, copy and paste the Hugging Face model location (e.g. mistralai/Mistral-7B-Instruct-v0.2) into the download bar. Alternatively, models can be added directly by placing the model into the 'models' folder of text-generation-webui
- Load your model with the appropriate loader per [loader doc](https://github.com/oobabooga/text-generation-webui/blob/main/docs/04%20-%20Model%20Tab.md)

### Step 3: Set instruction template and hyperparameters
- Navigate to the ‘Parameters’ tab and select the appropriate instruction template. This information can be found in the ‘config.json’ file within your downloaded model folder, under ‘model_type’
- Adjust the parameters as necessary for your use case. For example, to make responses near-deterministic, change ‘seed’ from random (i.e -1) to any other integer and ‘temperature’ to 0.01
- For more detailed information on hyperparameters, see [hyperparamaters doc](https://github.com/oobabooga/text-generation-webui/blob/main/docs/03%20-%20Parameters%20Tab.md)

### Step 4: Chat with your model
- Navigate to the ‘Chat’ tab and select ‘Chat-Instruct’ or ‘Instruct’ mode if you are using an instruct model. If not, ‘Chat’ should be chosen.
- You are now ready to chat with your model!


