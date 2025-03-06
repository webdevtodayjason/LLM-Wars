# LLM Wars

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A powerful CLI tool for comparing LLM performance across multiple providers simultaneously. Test prompts against OpenAI, Anthropic, Google Gemini, and more in a single interface.

![LLM Wars Screenshot](https://via.placeholder.com/800x400?text=LLM+Wars+Screenshot)

## Features

- 🚀 **Multi-Provider Support**: Test prompts across OpenAI, Anthropic, Google Gemini, and CodeGPT
- 🧠 **Model Selection**: Choose specific models from each provider
- ⚡ **Parallel Querying**: Send prompts to all selected models simultaneously
- 📊 **Performance Metrics**: Track token usage and response times
- 📦 **Clean Interface**: Rich text UI with side-by-side comparison
- 🔄 **Multi-View Responses**: View full responses individually or sequentially
- 📝 **Question Library**: Comprehensive benchmark suite with questions from industry-standard tests:
  - Instruction Following (IFEval)
  - Big-Bench Hard (BBH)
  - Mathematical Reasoning (MATH)
  - Grade School Questions (GPQA)
  - Massive Multitask Language Understanding (MMLU)
  - Multi-Turn User Simulation (MUSR)

## Installation

### Option 1: Standard Python Environment

```bash
# Clone the repository
git clone https://github.com/webdevtodayjason/LLM-Wars.git
cd LLM-Wars

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Conda Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/webdevtodayjason/LLM-Wars.git
cd LLM-Wars

# Create and activate conda environment
conda env create -f environment.yml
conda activate llm-wars
```

### Configure API Keys

The repository includes an `.env.example` file with the structure for all required API keys.

1. Copy the example file to create your own `.env` file:

```bash
# Copy example env file
cp .env.example .env
```

2. Edit the `.env` file and add your API keys:

```bash
# Open the file in your editor
nano .env  # or use any text editor you prefer
```

3. Replace the placeholder values with your actual API keys:

```
OPENAI_API_KEY=sk-yourOpenAIKeyHere        # From OpenAI
ANTHROPIC_API_KEY=sk-ant-yourAnthropicKey  # From Anthropic
GOOGLE_API_KEY=AIza-yourGoogleKey          # From Google AI Studio
CODEGPT_API_KEY=yourCodeGPTKeyHere         # If applicable
```

Where to get API keys:
- OpenAI: https://platform.openai.com/account/api-keys
- Anthropic: https://console.anthropic.com/settings/keys
- Google: https://makersuite.google.com/app/apikey

Note: The application will work even if you don't have all API keys. You'll be able to select only the providers for which you have keys configured.

## Usage

```bash
# If using standard Python environment
python app.py

# If using conda environment
conda activate llm-wars
python app.py
```

### Step-by-Step Guide

1. **Select Providers**: Choose up to 4 LLM providers from the available options
2. **Choose Models**: Select specific models for each provider 
3. **Query Models**: Select from predefined benchmark questions or enter your own prompt
4. **View Responses**: Compare side-by-side responses with performance metrics
5. **Full Responses**: View complete responses for each model:
   - View individual model responses
   - View all responses sequentially
   - Return to the comparison view at any time

### Advanced Features

#### Predefined Question Categories

LLM Wars includes a comprehensive question library with categories designed to test different aspects of LLM capabilities:

- **General Knowledge**: Basic factual knowledge
- **Programming Tasks**: Code generation and explanation
- **Creative Writing**: Creativity and text generation
- **Logic & Reasoning**: Problem-solving capabilities
- **Instruction Following (IFEval)**: Following specific instructions
- **Big-Bench Hard (BBH)**: Complex reasoning tasks
- **Mathematical Reasoning (MATH)**: Mathematical problem-solving
- **Grade School Questions (GPQA)**: Simple educational questions
- **Massive Multitask Language Understanding (MMLU)**: Specialized knowledge
- **Multi-Turn User Simulation (MUSR)**: Conversational capabilities

#### Performance Metrics

For each model response, LLM Wars provides:

- **Completion Time**: How long the model took to generate the response
- **Token Count (Input)**: Number of tokens in the prompt
- **Token Count (Output)**: Number of tokens in the response

## Roadmap

- [x] Add a file with predefined questions to test
- [x] Create side-by-side comparison interface
- [x] Add multi-view response capability
- [ ] Export results to CSV/JSON for analysis
- [ ] Add scoring and benchmarking capabilities
- [ ] Support for custom provider integrations
- [ ] Web interface with visualization tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## About the Author

Created by [Jason Brashear](https://github.com/webdevtodayjason/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Rich](https://github.com/Textualize/rich) for the beautiful terminal UI
- [OpenAI](https://openai.com), [Anthropic](https://www.anthropic.com), [Google](https://deepmind.google/technologies/gemini/), and other LLM providers