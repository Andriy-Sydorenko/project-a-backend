import re
from typing import Any, Dict

from markdown_it.rules_inline.autolink import EMAIL_RE
from starlette.requests import Request
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.exceptions import FormValidationError

from app.database import engine
from app.models import Issue, Organization, Project, Team, User
from app.services.user import ph

admin = Admin(engine, title="Project A Admin Panel")


class UserView(ModelView):
    form_columns = ["email", "username", "password_hash", "is_active", "is_superuser"]
    column_searchable_list = ["email", "username"]
    column_filters = ["email", "username", "is_active", "is_superuser"]
    save_state = True

    @staticmethod
    def validate_email(email: str) -> list:
        errors = []
        if not email:
            errors.append("Email field is required.")
        if not isinstance(email, str):
            errors.append("Email must be a string.")
        if len(email) < 5:
            errors.append("Email must be at least 5 characters long.")
        if not re.match(EMAIL_RE, email):
            errors.append("Email is not valid.")
        return errors

    @staticmethod
    def validate_password(password: str) -> list:
        errors = []
        if not password:
            errors.append("Password field is required.")
        if not isinstance(password, str):
            errors.append("Password must be a string.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", password):
            errors.append("Password must contain at least one digit.")
        return errors

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        errors = {}
        if email_errors := self.validate_email(data.get("email")):
            errors["email"] = email_errors
        if password_errors := self.validate_password(data.get("password_hash")):
            errors["password_hash"] = password_errors
        if errors:
            raise FormValidationError(errors)

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        await self.validate(request, data)
        db_session = request.state.session
        instance = self.model(**data)
        instance.password_hash = ph.hash(data["password_hash"])
        db_session.add(instance)
        await db_session.commit()
        return instance


admin.add_view(UserView(User, icon="fa-solid fa-users"))
admin.add_view(ModelView(Project, icon="fa-solid fa-diagram-project"))
admin.add_view(ModelView(Organization, icon="fa-solid fa-building-user"))
admin.add_view(ModelView(Team, icon="fa-solid fa-people-group"))
admin.add_view(ModelView(Issue, icon="fa-solid fa-list-check"))
