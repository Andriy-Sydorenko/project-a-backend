import strawberry


@strawberry.input
class RegisterInput:
    email: str
    password: str
    username: str | None = None


@strawberry.input
class LoginInput:
    email: str
    password: str
