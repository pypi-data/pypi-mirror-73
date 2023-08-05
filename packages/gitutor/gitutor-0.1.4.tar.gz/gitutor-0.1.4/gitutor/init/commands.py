import click

@click.command()
@click.pass_context
@click.option('-u', '--user', 'user_name' )
@click.option('-p', '--password', 'password', hide_input=True)
@click.option('-l', '--local', is_flag=True)
def init(ctx, user_name, password,local):
    "Create git repo and github remote"
    repo = ctx.obj['REPO']
    print(f"Remote from init: {repo.remote('origin').url} ")
    print("init command")
    print('user_name', user_name)
    print('pswd', password)
    if local:
        print('local repo only')
        return
    if not user_name:
        user_name = click.prompt('User name')
    
    if not password:
        password = click.prompt('Passwrod', hide_input=True)
