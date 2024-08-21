import click
import asyncio

from models import UserRole
from schemas import RegisterUser
from service import UserService


@click.command()
@click.option(
    "--username",
    required=True,
    type=str,
)
@click.option(
    "--password",
    required=True,
    type=str,
)
def main(username: str, password: str) -> None:
    """Создает пользователя поддержки с заданными именем пользователя и паролем."""

    async def create_support_user():
        user = RegisterUser(
            username=username,
            password=password,
            fingerprint=password,
            role=UserRole.support
        )
        async with UserService() as service:
            await service.register_user(user)
        print("Support user was created successfully")

    asyncio.run(create_support_user())


if __name__ == "__main__":
    main()