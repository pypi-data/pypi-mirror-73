import git
import os
import click

@click.command()
@click.pass_context
@click.option('-m', '--message', 'message')
@click.option('-p', '--push', is_flag=True)
def save(ctx, message, push):
    "Git add ., git commit -m, git push if possible"
    if not message:
        message = click.prompt('Commit message:')
    
    # Recover repo from context, add all files
    # Also recover repo_dir?
    repo.index.add([repo_dir])
    repo.index.commit(message)
    