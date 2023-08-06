import git
import os
import click
from github import Github
from github import GithubException
from git import GitCommandError

@click.command()
@click.pass_context
@click.option('-m', '--message', 'message')
@click.option('-p', '--push', is_flag=True)
def save(ctx, message, push):
    "Git add ., git commit -m, git pull, git push if possible"

    # Recover repo from context
    repo = ctx.obj['REPO']

    try:
        repo.git.diff("--check")
    except GitCommandError as e:
        click.echo("Please fix the following conflicts before saving")
        click.echo(e.stdout.split("'")[1])
    else: 
        #git add .
        #En teoría esto no agrega .git, queda probar
        if not message:
            message = click.prompt('Commit message')
    
        repo.git.add(A=True)

        #git commit -m ""
        repo.git.commit("-m", message)

        if push:
            if repo.remotes.origin.exists():
                try:
                    repo.git.pull()
                except Exception as e:
                    #click.echo(type(e))
                    #click.echo(e.args)
                    error_array = find_conflict(repo)
                    # We'll use this as a flag to determine whether we found any files with conflicts
                    #found_a_conflict = find_conflict(repo)

                    if error_array:
                        click.echo('Merge conflicts in:')
                        for error in error_array: 
                            click.echo("- " + error)
                        click.echo('Please fix conflicts then use "gt save -p" again')    
                else:
                    repo.git.push()

            else:
                click.echo('Remote repository does not exist!')

def find_conflict(repo):
    # This gets the dictionary discussed above 
    unmerged_blobs = repo.index.unmerged_blobs()
    error_array = []
    # We're really interested in the stage each blob is associated with.
    # So we'll iterate through all of the paths and the entries in each value
    # list, but we won't do anything with most of the values.
    for path in unmerged_blobs:
        list_of_blobs = unmerged_blobs[path]
        for (stage, blob) in list_of_blobs:
            # Now we can check each stage to see whether there were any conflicts
            if stage != 0:
                if path not in error_array:
                    error_array.append(path)
    return error_array
