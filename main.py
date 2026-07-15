"""
PHẦN 1: BÁO CÁO PHÂN TÍCH VÀ THIẾT KẾ GIẢI PHÁP

1. Phân tích dữ liệu đầu vào và đầu ra

API POST /enrollments
- Dữ liệu lấy từ request body: student_id, course_id.
- Dữ liệu cần truy vấn từ cơ sở dữ liệu:
    + Bản ghi Student theo student_id.
    + Bản ghi Course theo course_id.
    + Bản ghi Enrollment trùng (student_id, course_id) nếu có.
    + Số lượng Enrollment hiện tại của course_id.
- Điều kiện trả về 404 Not Found:
    + student_id không tồn tại trong bảng Student.
    + course_id không tồn tại trong bảng Course.
- Điều kiện trả về 400 Bad Request:
    + Student.status khác ACTIVE.
    + Course.status khác OPEN.
    + Đã tồn tại Enrollment với cùng student_id và course_id.
    + Số lượng Enrollment hiện tại của course_id >= max_students.
- Chỉ được phép tạo Enrollment mới khi toàn bộ các điều kiện trên đều hợp lệ,
  tức là student tồn tại và ACTIVE, course tồn tại và OPEN, chưa đăng ký trùng,
  và course chưa đủ số lượng. Khi đó API trả về 201 Created cùng bản ghi Enrollment.

API GET /students/{student_id}/courses
- Dữ liệu lấy từ path parameter: student_id.
- Dữ liệu cần truy vấn từ cơ sở dữ liệu:
    + Bản ghi Student theo student_id.
    + Danh sách Course mà student đó đã đăng ký, thông qua join Enrollment với Course
      theo điều kiện Enrollment.student_id == student_id.
- Điều kiện trả về 404 Not Found:
    + student_id không tồn tại trong bảng Student.
- Không có điều kiện trả về 400 cho API này, vì đây là API đọc dữ liệu.

2. Trình tự xử lý API POST /enrollments
    1) Tìm Student theo student_id, nếu không có -> 404.
    2) Tìm Course theo course_id, nếu không có -> 404.
    3) Kiểm tra Student.status == ACTIVE, nếu không -> 400.
    4) Kiểm tra Course.status == OPEN, nếu không -> 400.
    5) Kiểm tra đã tồn tại Enrollment (student_id, course_id) chưa, nếu có -> 400.
    6) Đếm số Enrollment hiện tại của course_id, nếu >= max_students -> 400.
    7) Tạo mới Enrollment, commit và trả về 201.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import schema
import enrollment_service
import student_service
import course_service
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enrollment API")


@app.post(
    "/enrollments",
    response_model=schema.EnrollmentResponse,
    status_code=201
)
def create_enrollment(
    data: schema.EnrollmentCreate,
    db: Session = Depends(get_db)
):
    return enrollment_service.create_enrollment(db, data)


@app.get(
    "/students/{student_id}/courses",
    response_model=schema.StudentCoursesResponse
)
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = student_service.get_student_by_id(db, student_id)
    courses = course_service.get_courses_of_student(db, student_id)

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": courses
    }
