# CLAUDE.md - Guidelines for LLM Comparison Tool

## Commands
- Run app: `python app.py`
- Install dependencies: `pip install -r requirements.txt`
- Run linting: `pylint app.py models.py`
- Run type checking: `mypy --strict app.py models.py`
- Run tests: `pytest`
- Run single test: `pytest test_file.py::test_function_name -v`

## Environment Setup
- Required API keys in .env file:
  - OPENAI_API_KEY
  - ANTHROPIC_API_KEY
  - GOOGLE_API_KEY
  - CODEGPT_API_KEY

## Code Style Guidelines
- **Imports**: Group standard library, third-party, local modules
- **Formatting**: 4 spaces for indentation
- **Types**: Use type hints from `typing` module for all functions
- **Naming**: 
  - snake_case for functions/variables
  - CamelCase for classes
  - UPPER_CASE for constants
- **Error Handling**: Use try/except with specific exceptions
- **Async**: Use asyncio for concurrent API calls
- **UI**: Rich library for console formatting and layouts
- **API Clients**: Follow provider documentation for client usage