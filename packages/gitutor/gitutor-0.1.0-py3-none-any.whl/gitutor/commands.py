import click

@click.command()
@click.pass_context
def init(ctx):
    "Create git repo and github remote"
    repo = ctx.obj['REPO']
    print(f"Remote from init: {repo.remote('origin').url} ")
    print("init command")
