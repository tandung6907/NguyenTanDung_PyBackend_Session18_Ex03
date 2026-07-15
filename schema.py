from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CourseBrief(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class StudentCoursesResponse(BaseModel):
    student_id: int
    full_name: str
    courses: List[CourseBrief]
