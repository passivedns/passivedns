import click

from models.user import User
from db.database import ObjectNotFound

@click.group()
def cli():
    pass


@cli.command()
def list_users():
    users = User.list()
    for user in users:
        click.echo(
            f"Username: {user.username} | Role: {user.role}"
        )


@cli.command()
@click.argument("username")
@click.argument("password")
@click.argument("email")
@click.option("--scheduler", is_flag=True, default=False)
@click.option("--admin", is_flag=True, default=False)
def create_user(
    username: str, password: str, email: str, scheduler: bool = False, admin: bool = False
) -> None:
    """Creates a new user in the system."""
    if User.exists(username):
        raise RuntimeError(f"User with username {username} already exists")
    user = User.new(username, password, email, is_scheduler=scheduler, is_admin=admin)
    user.insert()
    click.echo(
        f"User {username} succesfully created!"
    )


@cli.command()
@click.argument("username")
def delete_user(username: str) -> None:
    """Deletes a user from the system."""
    try:
        user = User.get(username)
    except ObjectNotFound:
        raise RuntimeError(f"User with username {username} does not exist")
    user.delete()
    click.echo(f"User {username} succesfully deleted")


@cli.command()
@click.argument("username")
@click.argument("new_password")
def reset_password(username: str, new_password: str) -> None:
    """Resets a user's password."""
    try:
        user = User.get(username)
    except ObjectNotFound:
        raise RuntimeError(f"User with username {username} could not be found")
    user.update_password(new_password)
    user.insert()
    click.echo(
        f"Password for {username} succesfully reset."
    )


if __name__ == "__main__":
    cli()