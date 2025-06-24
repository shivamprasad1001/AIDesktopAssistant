# AIDesktopAssistant

## Overview

**AIDesktopAssistant** is a modular, intelligent desktop assistant designed to understand natural language commands and help automate everyday tasks on your computer. Powered by intent classification and customizable modules, it can perform actions like opening applications, controlling media playback, setting reminders, and more.

This project combines natural language understanding (NLU) with system-level automation, providing a personalized and extensible assistant experience on your desktop environment.

> **Note:** This project is currently under active development. Features may be incomplete or subject to change.

---

## Features

* Natural language intent recognition using a trainable intent classification model
* Support for launching applications, managing files, controlling system settings, and more
* Modular design allowing easy extension with new commands and functionalities
* Simple command training via JSON datasets
* Cross-platform support (Windows, macOS, Linux) — depending on implemented modules
* Easy integration with other AI tools or chatbots

---

## Project Structure

```
AIDesktopAssistant/
├── nlu/                         # Natural Language Understanding components (intent recognition, parsing)
├── utils/                       # Utility functions and helpers
├── app_registry.json            # JSON file listing registered applications for quick launch
├── config.json                  # Configuration settings for the assistant
├── unlisted_apps.log            # Log file for apps not listed in the registry but accessed
├── main.py                     # Main entry point to launch the desktop assistant
├── README.md                   # Project documentation
└── .github/workflows/           # GitHub Actions workflows for automation

```
---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/shivamprasad1001/AIDesktopAssistant
cd AIDesktopAssistant
````

2. (Optional) Customize your assistant:

* Edit `intent_model/intentData.json` to modify or add intents and example commands.
* Adjust settings in `config.json` or other configuration files.
> train your custom intent_model follow this [Repo](https://github.com/shivamprasad1001/intent-model). After train your custom intent model then replace nlu/intent_classifier_emmo0.1.joblib with you new model 
---

## Usage

Run the assistant:

```bash
python main.py
```

The assistant will listen for your commands, classify intent using the trained model, and execute matching system actions.

---

## Training the Intent Model

To update or train the intent classification model, please follow the instructions in the [intent-model repository](https://github.com/shivamprasad1001/intent-model):

1. Clone the intent-model repo or refer to it directly:

   [https://github.com/shivamprasad1001/intent-model](https://github.com/shivamprasad1001/intent-model)

2. Edit `intentData.json` to add or modify intents and example utterances.

3. Run the training script:

```bash
python train.py
```

4. Copy the trained model files into your `AIDesktopAssistant` project if necessary.

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request to help improve the assistant.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

**Shivam Prasad**
[https://github.com/shivamprasad1001](https://github.com/shivamprasad1001)
