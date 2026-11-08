import typer

from .commands import add, init, load, toplevel

app = typer.Typer(help="csvファイルをpqに変換します")

app.command()(init.init)
app.command()(add.add)
app.command()(load.load)
app.command()(toplevel.toplevel)
