import enum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from backend.database import Base


class Status(enum.Enum):
    correct = "correct"
    wrong = "wrong"


class CSV_StructureTable(Base):
    __tablename__ = "CSV_Structure"
    course_id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int]
    module_position: Mapped[int]
    lesson_id: Mapped[int]
    lesson_position: Mapped[int]
    step_id: Mapped[int]
    step_position: Mapped[int]
    step_type: Mapped[str]
    step_cost: Mapped[int]


class CSV_SubmissionsTable(Base):
    __tablename__ = "CSV_Submissions"
    submission_id: Mapped[int] = mapped_column(primary_key=True)
    step_id: Mapped[int]
    user_id: Mapped[int]
    last_name: Mapped[str | None]
    first_name: Mapped[str | None]
    attempt_time: Mapped[int]
    submission_time: Mapped[int]
    status: Mapped[Status]
    score: Mapped[float]
    dataset: Mapped[str | None]
    clue: Mapped[str | None]
    reply: Mapped[str]
    reply_clear: Mapped[str | None]
    hint: Mapped[str | None]


class CSV_UserTable(Base):
    __tablename__ = "CSV_User"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str | None]
    first_name: Mapped[str | None]
    last_login_utc: Mapped[str]
    date_joined_utc: Mapped[str]


class CommentTable(Base):
    __tablename__ = "Comment"
    comment_id: Mapped[int] = mapped_column(primary_key=True)
    parent_comment_id: Mapped[int]
    time_utc: Mapped[int]
    deleted: Mapped[str]
    text_clear: Mapped[str]
    user_step_id: Mapped[int]


class LessonTable(Base):
    __tablename__ = "Lesson"
    lesson_id: Mapped[int] = mapped_column(primary_key=True)
    lesson_position: Mapped[int]
    module_id: Mapped[int]


class ModuleTable(Base):
    __tablename__ = "Module"
    module_id: Mapped[int] = mapped_column(primary_key=True)
    module_position: Mapped[int]


class SolutionTable(Base):
    __tablename__ = "Solution"
    attempt_time: Mapped[int] = mapped_column(primary_key=True)
    submission_time: Mapped[int]
    status: Mapped[Status]
    score: Mapped[str | None]
    reply: Mapped[str]
    step_id: Mapped[int]
    user_id: Mapped[int]


class StepTable(Base):
    __tablename__ = "Step"
    step_id: Mapped[int] = mapped_column(primary_key=True)
    step_position: Mapped[int]
    step_cost: Mapped[int]
    lesson_id: Mapped[int]
    step_type: Mapped[int]


class Step_typeTable(Base):
    __tablename__ = "Step_type"
    step_type_id: Mapped[int] = mapped_column(primary_key=True)
    step_type: Mapped[str]


class Step_userTable(Base):
    __tablename__ = "Step_user"
    step_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]

class UserTable(Base):
    __tablename__ = "User"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]


"""class sqlite_sequenceTable(Base):
    __tablename__ = "sqlite_sequence"
    name: Mapped[str]
    seq: Mapped[int]"""
