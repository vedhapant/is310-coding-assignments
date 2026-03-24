from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import csv
import os
from datetime import datetime

console = Console()

existing_artworks = [
    {"Title": "The Starry Night",        "Artist": "Vincent van Gogh", "Year": "1889", "Medium": "Oil on canvas", "Location": "MoMA, New York"},
    {"Title": "Girl with a Pearl Earring","Artist": "Johannes Vermeer", "Year": "1665", "Medium": "Oil on canvas", "Location": "Mauritshuis, The Hague"},
    {"Title": "The Persistence of Memory","Artist": "Salvador Dalí",   "Year": "1931", "Medium": "Oil on canvas", "Location": "MoMA, New York"},
    {"Title": "Water Lilies",             "Artist": "Claude Monet",    "Year": "1906", "Medium": "Oil on canvas", "Location": "Art Institute of Chicago"},
]

def show_banner():
    console.print(Panel.fit(
        "[bold white] THE ART VAULT  🎨[/bold white]\n[orange1]Your personal artwork collection tracker[/orange1]",
        border_style="orange1",
        padding=(1, 4),
    ))
    console.print()

def show_existing_artworks():
    table = Table(
        title="[bold orange1]  Existing Artworks in the Vault[/bold orange1]",
        box=box.HEAVY_EDGE,
        border_style="orange1",
        header_style="bold white on black",
        show_lines=True,
    )
    table.add_column("Title",    style="bold white",  min_width=28)
    table.add_column("Artist",   style="orange1",     min_width=20)
    table.add_column("Year",     style="white",        min_width=6,  justify="center")
    table.add_column("Medium",   style="dim white",   min_width=16)
    table.add_column("Location", style="orange1",     min_width=26)

    for aw in existing_artworks:
        table.add_row(aw["Title"], aw["Artist"], aw["Year"], aw["Medium"], aw["Location"])

    console.print(table)
    console.print()

def ask_how_many():
    while True:
        raw = console.input("[orange1]How many artworks would you like to add?[/orange1] [dim](enter a number)[/dim] ")
        if raw.strip().isdigit() and int(raw.strip()) > 0:
            return int(raw.strip())
        console.print("[bold red]Please enter a valid number greater than 0.[/bold red]")

def collect_one_artwork(index: int, total: int) -> dict:
    """Prompt the user for one artwork, with confirm / re-enter loop."""
    console.print(f"\n[bold white]── Artwork {index} of {total} ──[/bold white]", style="on black")

    while True:
        title    = console.input("[orange1]  Title:[/orange1]    ")
        artist   = console.input("[orange1]  Artist:[/orange1]   ")
        year     = console.input("[orange1]  Year:[/orange1]     ")
        medium   = console.input("[orange1]  Medium:[/orange1]   [dim](e.g. Oil on canvas, Watercolour)[/dim] ")
        location = console.input("[orange1]  Location:[/orange1] [dim](museum / city)[/dim] ")

        # Show summary for confirmation
        console.print()
        summary = Table(box=box.SIMPLE, border_style="white", show_header=False, padding=(0, 2))
        summary.add_column(style="dim white")
        summary.add_column(style="bold white")
        summary.add_row("Title",    title)
        summary.add_row("Artist",   artist)
        summary.add_row("Year",     year)
        summary.add_row("Medium",   medium)
        summary.add_row("Location", location)
        console.print(Panel(summary, title="[orange1]Is this correct?[/orange1]", border_style="orange1"))

        confirm = console.input("[white]  Type [bold orange1]yes[/bold orange1] to save or [bold orange1]no[/bold orange1] to re-enter: [/white]").strip().lower()

        if confirm in ("yes", "y"):
            return {
                "Title":    title,
                "Artist":   artist,
                "Year":     year,
                "Medium":   medium,
                "Location": location,
            }
        else:
            console.print("[dim]  Let's try again...[/dim]\n")

def save_to_csv(new_artworks: list) -> str:
    filename = f"my_artworks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(os.getcwd(), filename)

    all_artworks = existing_artworks + new_artworks
    fieldnames = ["Title", "Artist", "Year", "Medium", "Location"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_artworks)

    return filepath

def show_final_table(new_artworks: list):
    table = Table(
        title="[bold orange1] Your Newly Added Artworks[/bold orange1]",
        box=box.HEAVY_EDGE,
        border_style="white",
        header_style="bold black on orange1",
        show_lines=True,
    )
    table.add_column("Title",    style="bold white",  min_width=28)
    table.add_column("Artist",   style="orange1",     min_width=20)
    table.add_column("Year",     style="white",        min_width=6,  justify="center")
    table.add_column("Medium",   style="dim white",   min_width=16)
    table.add_column("Location", style="orange1",     min_width=26)

    for aw in new_artworks:
        table.add_row(aw["Title"], aw["Artist"], aw["Year"], aw["Medium"], aw["Location"])

    console.print()
    console.print(table)

def main():
    show_banner()
    show_existing_artworks()

    total        = ask_how_many()
    new_artworks = []

    for i in range(1, total + 1):
        artwork = collect_one_artwork(i, total)
        new_artworks.append(artwork)
        console.print(f"[bold white]  ✔ Artwork {i} saved to session.[/bold white]")

    show_final_table(new_artworks)

    filepath = save_to_csv(new_artworks)

    console.print(Panel.fit(
        f"[bold white]All done! 🎨[/bold white]\n"
        f"[orange1]Your collection has been saved to:[/orange1]\n"
        f"[bold white]{filepath}[/bold white]",
        border_style="orange1",
        padding=(1, 4),
    ))

if __name__ == "__main__":
    main()
