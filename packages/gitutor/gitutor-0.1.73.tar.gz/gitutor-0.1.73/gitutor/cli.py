import click
import git
from gitutor.init.commands import init


@click.group()
@click.pass_context
def cli(ctx):
    """ Git the easy way """
    #Check ctx was initialized
    ctx.ensure_object(dict)
    
    if ctx.invoked_subcommand != 'init':
        try:
            repo = git.Repo(".", search_parent_directories=True)
            ctx.obj['REPO'] = repo
            print( f"Location {repo.working_tree_dir}" )
            print(f"Remote from init: {repo.remote('origin').url} ")
        except:
            print("not git repo")
            exit()

cli.add_command(init)

def main():
    cli(obj={})

if __name__ == '__main__':
    cli(obj={})
