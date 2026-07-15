from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schema
from student_service import get_student_by_id
from course_service import get_course_by_id, count_enrollments_of_course


def create_enrollment(db: Session, data: schema.EnrollmentCreate) -> models.Enrollment:
    student = get_student_by_id(db, data.student_id)
    course = get_course_by_id(db, data.course_id)

    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Sinh viên đã ngừng học"
        )

    if course.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đóng"
        )

    duplicate_enrollment = (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.student_id == data.student_id,
            models.Enrollment.course_id == data.course_id
        )
        .first()
    )

    if duplicate_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Sinh viên đã đăng ký khóa học này"
        )

    current_count = count_enrollments_of_course(db, data.course_id)

    if current_count >= course.max_students:
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đủ số lượng"
        )

    enrollment = models.Enrollment(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment
