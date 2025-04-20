from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, DateTime, String, func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)

    avatar_url = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    # organization = relationship("Organization", back_populates="users")

    def __repr__(self):
        return f"<User {self.email}>"
