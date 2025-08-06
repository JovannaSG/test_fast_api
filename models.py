from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TaskModel(Base):
    """SQLAlchemy модель для таблицы задач"""
    __tablename__ = "task"

    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), nullable=False)
    description = Column(String(100), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    

    def __repr__(self):
        return f"""
            <Task(id={self.task_id}, 
            title='{self.title}', 
            description={self.description}
            completed={self.completed})>
        """
