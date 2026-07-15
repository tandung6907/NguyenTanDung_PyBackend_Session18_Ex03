from fastapi import HTTPException
from sqlalchemy.orm import Session

import models


def get_course_by_id(db: Session, course_id: int) -> models.Course:
    course = (
        db.query(models.Course)
        .filter(models.Course.id == course_id)
        .first()
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Khóa học không tồn tại"
        )

    return course


def count_enrollments_of_course(db: Session, course_id: int) -> int:
    return (
        db.query(models.Enrollment)
        .filter(models.Enrollment.course_id == course_id)
        .count()
    )


def get_courses_of_student(db: Session, student_id: int) -> list:
    return (
        db.query(models.Course)
        .join(models.Enrollment, models.Enrollment.course_id == models.Course.id)
        .filter(models.Enrollment.student_id == student_id)
        .all()
    )
