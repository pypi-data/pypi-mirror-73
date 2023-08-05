import click
import git
from init.commands import init


@click.group()
@click.pass_context
def cli(ctx):
    """ Git the easy way """
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    try:
        repo = git.Repo(".", search_parent_directories=True)
        ctx.obj['REPO'] = repo
    except:
        print("not git repo")
        exit()
        return
    print( f"Location {repo.working_tree_dir}" )

cli.add_command(init)

def main():
    cli(obj={})
