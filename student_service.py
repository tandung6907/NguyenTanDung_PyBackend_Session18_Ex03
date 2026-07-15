from fastapi import HTTPException
from sqlalchemy.orm import Session

import models


def get_student_by_id(db: Session, student_id: int) -> models.Student:
    student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    return student
