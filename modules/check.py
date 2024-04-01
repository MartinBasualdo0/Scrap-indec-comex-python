import os
from rich import print

# Function to check and create directories if needed
def check_and_create_directories():
    if not os.path.exists("downloads"):
        os.mkdir("downloads")
        print("[bold green]Created 'downloads' folder.[/bold green]")
    if not os.path.exists("output"):
        os.mkdir("output")
        print("[bold green]Created 'output' folder.[/bold green]")