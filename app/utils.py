from enum import Enum


class QuestionType(Enum):
    MULTI_CHOICE = 'MULTI_CHOICE'
    SINGLE_CHOICE = 'SINGLE_CHOICE'


class QuestionDifficulty(Enum):
    BEGINNER = 'BEGINNER'
    MEDIUM = 'MEDIUM'
    ADVANCED = 'ADVANCED'
