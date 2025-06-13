#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.spinner import Spinner

class OllamaChat:
    def __init__(self, model="llama2", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.console = Console()
        self.conversation = []
        self.load_system_prompts()
        
    def load_system_prompts(self):
        prompts_dir = Path("prompts")
        
        system_file = prompts_dir / "system.md"
        if system_file.exists():
            with open(system_file, 'r', encoding='utf-8') as f:
                self.conversation.append({
                    "role": "system",
                    "content": f.read().strip(),
                    "timestamp": datetime.now().isoformat()
                })
        
        functions_file = prompts_dir / "functions.md"
        if functions_file.exists():
            with open(functions_file, 'r', encoding='utf-8') as f:
                self.conversation.append({
                    "role": "system", 
                    "content": f.read().strip(),
                    "timestamp": datetime.now().isoformat()
                })
    
    def save_conversation(self, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + "-" + self.model.replace(":", "-")
            filename = f"outputs/{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def get_multiline_input(self):
        self.console.print("\n[bold cyan]Enter your message (press Ctrl+D or type 'END' on a new line to finish):[/bold cyan]")
        lines = []
        
        try:
            while True:
                try:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                except EOFError:
                    break
        except KeyboardInterrupt:
            return None
        
        return "\n".join(lines).strip()
    
    def stream_response(self, messages):
        payload = {
            "model": self.model,
            "messages": [{"role": msg["role"], "content": msg["content"]} for msg in messages],
            "stream": True
        }
        
        try:
            full_response = ""
            first_chunk_received = False
            
            self.console.print()
            with Live(Spinner("dots", text="Waiting for response..."), refresh_per_second=10) as live:
                response = requests.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    stream=True,
                    timeout=60
                )
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'message' in data and 'content' in data['message']:
                                chunk = data['message']['content']
                                full_response += chunk
                                
                                if not first_chunk_received:
                                    first_chunk_received = True
                                
                                live.update(Panel(Markdown(full_response), title="[bold green]Assistant[/bold green]"))
                            
                            if data.get('done', False):
                                break
                        except json.JSONDecodeError:
                            continue
            
            return full_response
            
        except requests.exceptions.RequestException as e:
            self.console.print(f"[bold red]Error communicating with Ollama: {e}[/bold red]")
            return None
    
    def run(self):
        self.console.print(Panel(
            f"[bold green]Ollama Chat Client[/bold green]\n"
            f"Model: {self.model}\n"
            f"Server: {self.base_url}\n\n"
            f"Commands:\n"
            f"  /quit - Exit the chat\n"
            f"  /save - Save conversation\n"
            f"  /model <name> - Change model",
            title="Welcome"
        ))
        
        while True:
            try:
                user_input = self.get_multiline_input()
                
                if user_input is None:
                    break
                
                if not user_input:
                    continue
                
                if user_input.startswith('/'):
                    command_parts = user_input[1:].split()
                    command = command_parts[0].lower()
                    
                    if command == 'quit':
                        break
                    elif command == 'save':
                        filename = self.save_conversation()
                        self.console.print(f"[green]Conversation saved to {filename}[/green]")
                        continue
                    elif command == 'model' and len(command_parts) > 1:
                        self.model = command_parts[1]
                        self.console.print(f"[green]Model changed to {self.model}[/green]")
                        continue
                    else:
                        self.console.print("[red]Unknown command[/red]")
                        continue
                
                user_message = {
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().isoformat()
                }
                self.conversation.append(user_message)
                
                response = self.stream_response(self.conversation)
                
                if response:
                    assistant_message = {
                        "role": "assistant", 
                        "content": response,
                        "timestamp": datetime.now().isoformat()
                    }
                    self.conversation.append(assistant_message)
                
                self.console.print("\n" + "="*50 + "\n")
                
            except KeyboardInterrupt:
                break
        
        filename = self.save_conversation()
        self.console.print(f"\n[green]Conversation saved to {filename}[/green]")
        self.console.print("[bold cyan]Goodbye![/bold cyan]")

def main():
    model = "llama2"
    base_url = "http://localhost:11434"
    
    if len(sys.argv) > 1:
        model = sys.argv[1]
    if len(sys.argv) > 2:
        base_url = sys.argv[2]
    
    chat = OllamaChat(model=model, base_url=base_url)
    chat.run()

if __name__ == "__main__":
    main()
