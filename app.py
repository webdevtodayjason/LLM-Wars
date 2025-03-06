import os
import time
import json
import asyncio
import shutil
import math
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.tree import Tree
from typing import List, Dict, Tuple, Optional, Any

# API client imports
import openai
import anthropic
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Import providers and models from models.py
from models import providers

# Initialize API clients
def init_clients():
    # OpenAI
    if os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Anthropic
    if os.getenv("ANTHROPIC_API_KEY"):
        anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Google
    if os.getenv("GOOGLE_API_KEY"):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def select_providers(console: Console) -> List[str]:
    """Allow user to select up to 4 providers"""
    console.print("Select up to 4 providers:", style="bold magenta")
    
    available_providers = list(providers.keys())
    selected = []
    
    # Display provider options
    for i, provider in enumerate(available_providers, 1):
        console.print(f"{i}. {provider}")
    
    # Process selections
    while len(selected) < 4:
        # Show current selections if any exist
        if selected:
            console.print("\nCurrent selections:", style="bold green")
            for i, provider in enumerate(selected, 1):
                console.print(f"{i}. {provider}")
        
        choice = Prompt.ask(
            "\nSelect provider by number, name, or type 'done' to continue",
            default="done" if selected else None
        )
        
        if choice.lower() == 'done':
            if not selected:
                console.print("Please select at least one provider", style="red")
                continue
            break
        
        # Handle numeric input
        if choice.isdigit() and 1 <= int(choice) <= len(available_providers):
            provider = available_providers[int(choice) - 1]
            if provider in selected:
                selected.remove(provider)
                console.print(f"Removed {provider}", style="red")
            else:
                selected.append(provider)
                console.print(f"Added {provider}", style="green")
        # Handle provider name input
        elif choice in available_providers:
            if choice in selected:
                selected.remove(choice)
                console.print(f"Removed {choice}", style="red")
            else:
                selected.append(choice)
                console.print(f"Added {choice}", style="green")
        else:
            console.print(f"Invalid selection: {choice}", style="red")
    
    return selected

def select_model_for_provider(provider: str, console: Console) -> str:
    """Select a model for a specific provider"""
    models_list = providers[provider]
    console.print(f"Available models for {provider}:", style="bold blue")
    
    for i, model in enumerate(models_list, 1):
        console.print(f"{i}. {model}")
        
    choice = Prompt.ask(
        "Choose a model by number", 
        choices=[str(i) for i in range(1, len(models_list) + 1)]
    )
    return models_list[int(choice) - 1]

async def query_model(
    provider: str, 
    model: str, 
    query: str
) -> Dict[str, Any]:
    """Query a specific model with provider-specific implementations"""
    start_time = time.time()
    result = ""
    tokens_in = 0
    tokens_out = 0
    
    try:
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
                
            client = openai.OpenAI(api_key=api_key)
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=model,
                messages=[{"role": "user", "content": query}],
            )
            result = response.choices[0].message.content
            tokens_in = response.usage.prompt_tokens
            tokens_out = response.usage.completion_tokens
            
        elif provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
                
            client = anthropic.Anthropic(api_key=api_key)
            response = await asyncio.to_thread(
                client.messages.create,
                model=model,
                max_tokens=1000,
                messages=[{"role": "user", "content": query}],
            )
            result = response.content[0].text
            tokens_in = response.usage.input_tokens
            tokens_out = response.usage.output_tokens
            
        elif provider == "google":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
                
            genai.configure(api_key=api_key)
            model_obj = genai.GenerativeModel(model)
            response = await asyncio.to_thread(
                model_obj.generate_content,
                query
            )
            result = response.text
            # Gemini doesn't return token counts directly
            tokens_in = len(query) // 4  # Rough estimate
            tokens_out = len(result) // 4  # Rough estimate
            
        elif provider == "codegpt":
            # Placeholder for CodeGPT API - for demo purposes
            # Since there's no official Python package, this is a simulated response
            api_key = os.getenv("CODEGPT_API_KEY")
            if not api_key:
                # For demo, we'll allow this to continue with a simulated response
                pass
                
            await asyncio.sleep(1)  # Simulate API call
            result = f"CodeGPT response for: {query}"
            tokens_in = len(query) // 4
            tokens_out = len(result) // 4
    except Exception as e:
        result = f"Error: {str(e)}"
        
    elapsed_time = time.time() - start_time
    
    return {
        "provider": provider,
        "model": model,
        "result": result,
        "elapsed_time": elapsed_time,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out
    }

async def query_all_models(selections: List[Tuple[str, str]], query: str) -> List[Dict[str, Any]]:
    """Query all selected models in parallel"""
    tasks = []
    for provider, model in selections:
        tasks.append(query_model(provider, model, query))
    return await asyncio.gather(*tasks)

def create_response_table(selections: List[Tuple[str, str]], results: Optional[List[Dict[str, Any]]] = None, height: int = 10) -> Table:
    """Create a table with model responses horizontally"""
    # Create a table with equal width columns for each model
    table = Table(show_header=True, expand=True, box=None, padding=(0, 1))
    
    # Add columns for each selection
    for provider, model in selections:
        table.add_column(f"{provider}: {model}", justify="center")
    
    # If we have results, add them to the table
    if results:
        row = []
        for i, result in enumerate(results):
            if i < len(selections):
                # Truncate long responses to fit in the table
                result_text = result['result']
                max_chars = 200  # Limit characters per cell
                if len(result_text) > max_chars:
                    result_text = result_text[:max_chars] + "...\n[truncated]"
                
                # Create a panel with the response and metrics
                panel_content = f"{result_text}\n\n"
                panel_content += f"Time: {result['elapsed_time']:.2f}s | "
                panel_content += f"Tokens in: {result['tokens_in']} | "
                panel_content += f"Tokens out: {result['tokens_out']}"
                
                cell_panel = Panel(
                    panel_content,
                    border_style="blue",
                    title=f"Response",
                    height=height
                )
                row.append(cell_panel)
        
        table.add_row(*row)
    else:
        # Add placeholder row
        row = []
        for _ in selections:
            cell_panel = Panel(
                "Waiting for response...",
                border_style="blue",
                title="Response",
                height=height
            )
            row.append(cell_panel)
        table.add_row(*row)
    
    return table

def display_questions_menu(console: Console, questions_data: Dict[str, Any]) -> Optional[str]:
    """Display a menu to select a question from the questions.json file"""
    console.clear()  # Clear screen for better visibility
    
    if not questions_data or not questions_data.get("categories"):
        console.print("No questions found in questions.json", style="red")
        return None
    
    # Display categories
    console.print("\nSelect a question category:", style="bold magenta")
    categories = list(questions_data["categories"].keys())
    
    for i, category_key in enumerate(categories, 1):
        category = questions_data["categories"][category_key]
        console.print(f"{i}. {category['name']} ({len(category['questions'])} questions)")
    
    # Category selection
    category_choice = Prompt.ask(
        "Choose a category by number (or 'custom' for a custom query)",
        choices=[str(i) for i in range(1, len(categories) + 1)] + ["custom"]
    )
    
    if category_choice.lower() == "custom":
        return Prompt.ask("Enter your custom query")
    
    selected_category_key = categories[int(category_choice) - 1]
    selected_category = questions_data["categories"][selected_category_key]
    
    # Display questions in selected category
    console.print(f"\nQuestions in {selected_category['name']}:", style="bold blue")
    
    # Create a tree for better visualization
    tree = Tree(f"[bold]{selected_category['name']}[/bold]")
    
    for i, question in enumerate(selected_category["questions"], 1):
        difficulty_style = {
            "easy": "green",
            "medium": "yellow",
            "hard": "red"
        }.get(question["difficulty"], "white")
        
        tree.add(
            f"[{difficulty_style}]{i}. [{question['difficulty']}][/{difficulty_style}] {question['text'][:50]}..."
        )
    
    console.print(tree)
    
    # Question selection
    question_choice = Prompt.ask(
        "Choose a question by number",
        choices=[str(i) for i in range(1, len(selected_category["questions"]) + 1)]
    )
    
    selected_question = selected_category["questions"][int(question_choice) - 1]
    return selected_question["text"]

# Load questions from questions.json
def load_questions() -> Dict[str, Any]:
    try:
        with open("questions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"categories": {}}
    except json.JSONDecodeError:
        print("Error: questions.json file is invalid JSON")
        return {"categories": {}}

async def main():
    # Get terminal size
    terminal_width, terminal_height = shutil.get_terminal_size()
    
    # Create console with specific dimensions
    console = Console(width=terminal_width, height=terminal_height)
    console.clear()
    
    console.print("LLM Wars - LLM Comparison Tool", style="bold magenta")
    
    # Initialize API clients
    init_clients()
    
    # Load questions from questions.json
    questions_data = load_questions()
    
    # Setup phase: Select providers and models
    selected_providers = select_providers(console)
    
    if not selected_providers:
        console.print("No providers selected. Exiting.", style="red bold")
        return
    
    # Select models for each provider
    selections = []
    for provider in selected_providers:
        model = select_model_for_provider(provider, console)
        selections.append((provider, model))
    
    console.print("Selected models:", style="bold green")
    for provider, model in selections:
        console.print(f"• {provider}: {model}")
    
    # Calculate optimal panel height based on terminal size
    panel_height = min(terminal_height - 10, 15)  # Leave space for prompts
    
    # Main battle loop
    while True:
        console.clear()
        
        # Create the dashboard with empty panels
        response_table = create_response_table(selections, height=panel_height)
        
        # Show the battle dashboard
        console.print("LLM Wars - Comparison Dashboard", style="bold magenta")
        console.print(response_table)
        console.print("Status: Ready for query", style="yellow")
        
        # Get query type from user
        query_type = Prompt.ask(
            "Query type [P]redefined, [C]ustom, or [E]xit",
            choices=["p", "c", "e"],
            default="p"
        )
        
        if query_type.lower() == "e":
            break
            
        # Get query based on type
        if query_type.lower() == "p":
            # Show question menu
            query = display_questions_menu(console, questions_data)
            if not query:
                query = Prompt.ask("Enter your query (or type 'exit' to quit)")
        else:
            # Get custom query input
            query = Prompt.ask("Enter your query (or type 'exit' to quit)")
            
        if query.lower() == 'exit':
            break
            
        # Show processing status
        console.clear()
        console.print("LLM Wars - Comparison Dashboard", style="bold magenta")
        console.print(response_table)
        console.print("Status: Processing query across all models...", style="yellow bold")
        
        # Query all models in parallel
        results = await query_all_models(selections, query)
        
        # Create updated table with results
        response_table = create_response_table(selections, results, height=panel_height)
        
        # Show results dashboard
        console.clear()
        console.print("LLM Wars - Comparison Dashboard", style="bold magenta")
        console.print(response_table)
        console.print("Status: Results ready. Choose an option below.", style="green")
        
        # Enter "view response" loop for multiple viewing
        while True:
            # Create number choices for all models plus combined options
            choices_text = ", ".join([f"[{i+1}]" for i in range(len(selections))])
            choices = ["n", "a", "d"] + [str(i+1) for i in range(len(selections))]
            
            view_full = Prompt.ask(
                f"View responses: ([N]o, [A]ll sequentially, [D]one viewing, or model number {choices_text})",
                choices=choices,
                default="n"
            )
            
            # Exit response viewing loop
            if view_full.lower() == "n" or view_full.lower() == "d":
                break
                
            # View all responses sequentially
            if view_full.lower() == "a":
                for i in range(len(selections)):
                    provider, model = selections[i]
                    full_result = results[i]["result"]
                    
                    # Show full response in a full-screen panel
                    console.clear()
                    console.print(Panel(
                        full_result,
                        title=f"{provider} - {model} (Full Response {i+1}/{len(selections)})",
                        border_style="green",
                        height=terminal_height-4
                    ))
                    
                    # Wait for user acknowledgment between responses (except last one)
                    if i < len(selections) - 1:
                        Prompt.ask(f"Press Enter to view next response ({i+2}/{len(selections)})", default="")
                    else:
                        Prompt.ask("Press Enter to return to response selection", default="")
                        
                # Show the comparison view again after viewing all
                console.clear()
                console.print("LLM Wars - Comparison Dashboard", style="bold magenta")
                console.print(response_table)
                console.print("Status: Results ready. Continue viewing responses or proceed.", style="green")
                continue
            
            # View individual response
            model_idx = int(view_full) - 1
            if 0 <= model_idx < len(results):
                provider, model = selections[model_idx]
                full_result = results[model_idx]["result"]
                
                # Show full response in a full-screen panel
                console.clear()
                console.print(Panel(
                    full_result,
                    title=f"{provider} - {model} (Full Response)",
                    border_style="green",
                    height=terminal_height-4
                ))
                
                # Wait for user to acknowledge
                Prompt.ask("Press Enter to return to response selection", default="")
                
                # Show the comparison view again
                console.clear()
                console.print("LLM Wars - Comparison Dashboard", style="bold magenta")
                console.print(response_table)
                console.print("Status: Results ready. Continue viewing responses or proceed.", style="green")
        
        # Ask if user wants to continue with another query
        continue_query = Prompt.ask(
            "Continue with another query? ([Y]es/[N]o)",
            choices=["y", "n"],
            default="y"
        )
        
        if continue_query.lower() != "y":
            break

if __name__ == "__main__":
    asyncio.run(main())