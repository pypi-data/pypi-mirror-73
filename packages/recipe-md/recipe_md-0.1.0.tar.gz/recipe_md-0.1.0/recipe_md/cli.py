import typer

from .recipe_md import Recipe


app = typer.Typer()


@app.command('name')
def runner(name):
    r = Recipe(name)
    r.make_md()


def main():
    app()
