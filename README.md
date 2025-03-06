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
- 📦 **Clean Interface**: Rich text UI with split-screen layout
- 🔄 **Interactive Experience**: Dynamic response display
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
git clone https://github.com/yourusername/llm-wars.git
cd llm-wars

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Conda Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/llm-wars.git
cd llm-wars

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

1. **Select Providers**: Choose up to 4 providers from OpenAI, Anthropic, Google, and CodeGPT
   ```
   Select up to 4 providers:
   1. openai
   2. anthropic
   3. google
   4. codegpt
   
   Select provider by number, name, or type 'done' to continue: 1
   ```

2. **Choose Models**: Select specific models for each provider
   ```
   Available models for openai:
   1. gpt-4o
   2. gpt-4-turbo
   3. gpt-3.5-turbo
   
   Choose a model by number: 1
   ```

3. **Select Query Type**: Choose between predefined benchmark questions or custom prompts
   ```
   Query type [predefined/custom/exit]: predefined
   ```

4. **Choose Questions**: If using predefined questions, select a category and specific question
   ```
   Select a question category:
   1. General Knowledge (3 questions)
   2. Programming Tasks (3 questions)
   ...
   
   Choose a category by number: 1
   ```

5. **View Results**: Compare responses from all models in the split-screen interface
   - See token counts, response times, and full responses side-by-side
   - Continue with more questions or exit the application

## Roadmap

- [x] Add a file with predefined questions to test
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Rich](https://github.com/Textualize/rich) for the beautiful terminal UI
- [OpenAI](https://openai.com), [Anthropic](https://www.anthropic.com), [Google](https://deepmind.google/technologies/gemini/), and other LLM providers