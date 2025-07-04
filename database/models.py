import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	telegram_id = Column(Integer, unique=True, nullable=False)
	username = Column(String(50))
	full_name = Column(String(50), nullable=False)
	language = Column(String(2), default='en')
	subjects = Column(String(200))
	level = Column(String(20), default='beginner')
	study_groups = relationship(
		'StudyGroup',
		secondary='group_members',
		back_populates='members'
	)


class StudyGroup(Base):
	__tablename__ = 'study_groups'

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	subject = Column(String(50), nullable=False)
	description = Column(Text)
	schedule = Column(String(100))
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	creator_id = Column(Integer, ForeignKey('users.id'))
	members = relationship(
		'User',
		secondary='group_members',
		back_populates='study_groups'
	)
	materials = relationship('StudyMaterial', back_populates='group')


class GroupMember(Base):
	__tablename__ = 'group_members'

	user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
	group_id = Column(Integer, ForeignKey('study_groups.id'), primary_key=True)
	is_admin = Column(Boolean, default=False)


class StudyMaterial(Base):
	__tablename__ = 'study_materials'

	id = Column(Integer, primary_key=True)
	title = Column(String(100), nullable=False)
	content = Column(Text)
	file_id = Column(String(200))  # Telegram file_id
	group_id = Column(Integer, ForeignKey('study_groups.id'))
	user_id = Column(Integer, ForeignKey('users.id'))
	group = relationship('StudyGroup', back_populates='materials')
	user = relationship('User')


class Flashcard(Base):
	__tablename__ = 'flashcards'

	id = Column(Integer, primary_key=True)
	front = Column(Text, nullable=False)
	back = Column(Text, nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'))
	last_reviewed = Column(DateTime)
	next_review = Column(DateTime)
	difficulty = Column(Integer, default=1)  # 1-5 scale


class QuizQuestion(Base):
	__tablename__ = 'quiz_questions'

	id = Column(Integer, primary_key=True)
	question = Column(Text, nullable=False)
	options = Column(Text)  # JSON: ["opt1", "opt2", "opt3"]
	correct_option = Column(Integer, nullable=False)
	subject = Column(String(50))
	difficulty = Column(String(20))
