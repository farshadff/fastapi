from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime


class ServiceResult(Base):
    __tablename__ = "service_results"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(50), index=True)
    type = Column(String(50))
    result = Column(Text)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    date_fa = Column(String(50))


class MainResponse(Base):
    __tablename__ = "lang_ai_main_response"

    id = Column(Integer, primary_key=True, index=True)
    overall_score = Column(Float)
    mock_ielts_prediction = Column(Float)
    mock_cefr_prediction = Column(String(10))
    mock_pte_prediction = Column(Float)
    feedback_text = Column(Text)
    overall_fluency_score = Column(Float)
    overall_vocabulary_score = Column(Float)
    overall_grammar_score = Column(Float)
    overall_pronunciation_score = Column(Float)
    tagged_transcript = Column(Text)
    expected_text = Column(Text)
    user_id = Column(Text)
    question = Column(Text)
    description = Column(Text)

    # Relationships
    pronunciation = relationship("Pronunciation", back_populates="main_response", cascade="all, delete-orphan")
    fluency = relationship("Fluency", back_populates="main_response", cascade="all, delete-orphan")
    vocabulary = relationship("Vocabulary", back_populates="main_response", cascade="all, delete-orphan")
    grammar = relationship("Grammar", back_populates="main_response", cascade="all, delete-orphan")
    words = relationship("Words", back_populates="main_response", cascade="all, delete-orphan")


class Pronunciation(Base):
    __tablename__ = "lang_ai_pronunciation"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey('lang_ai_main_response.id'))
    overall_score = Column(Float)
    lowest_scoring_phonemes = Column(JSON)
    mock_cefr_prediction = Column(String, nullable=True)  # New column for storing the mock CEFR score
    mock_ielts_prediction = Column(Float, nullable=True)  # New column for storing the mock IELTS score

    # Relationship
    main_response = relationship("MainResponse", back_populates="pronunciation")


class Fluency(Base):
    __tablename__ = "lang_ai_fluency"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey('lang_ai_main_response.id'))
    overall_score = Column(Float)
    speech_rate = Column(Integer)
    pauses = Column(Integer)
    filler_words = Column(Integer)
    feedback_text = Column(Text)
    speech_rate_over_time = Column(JSON)
    filler_words_per_min = Column(Float)

    # Relationship
    main_response = relationship("MainResponse", back_populates="fluency")


class Vocabulary(Base):
    __tablename__ = "lang_ai_vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey('lang_ai_main_response.id'))
    overall_score = Column(Float)
    vocabulary_complexity = Column(String(50))
    feedback_text = Column(Text)

    # Relationship
    main_response = relationship("MainResponse", back_populates="vocabulary")


class Grammar(Base):
    __tablename__ = "lang_ai_grammar"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey('lang_ai_main_response.id'))
    overall_score = Column(Float)
    feedback_text = Column(Text)

    # Relationship
    main_response = relationship("MainResponse", back_populates="grammar")


class Words(Base):
    __tablename__ = "lang_ai_words"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey('lang_ai_main_response.id'))
    word_text = Column(String(255))
    word_score = Column(Float)
    phoneme_data = Column(JSON)

    # Relationship
    main_response = relationship("MainResponse", back_populates="words")
