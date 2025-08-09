from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class RoleModel(Base):
    """SQLAlchemy модель для таблицы ролей"""
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), nullable=False, unique=True)

    # Связь с пользователями
    users = relationship("UserModel", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.role_id}, name='{self.role_name}')>"


class UserModel(Base):
    """SQLAlchemy модель для таблицы пользователей"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())

    # Связь с ролью
    role = relationship("RoleModel", back_populates="users")

    def __repr__(self):
        return f"""
            <User(id={self.user_id}, 
            full_name='{self.full_name}', 
            email='{self.email}',
            role_id={self.role_id})>
        """
