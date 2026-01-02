from pydantic import BaseModel
from typing import Optional, List, Any
# TODO: this file is very out of sync, uppdate it once api goes into full prod for the sake
# of data validation
# -------------------------
# COLLEGE
# -------------------------
class CollegeBase(BaseModel):
    name: str
    abbreviation: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    region: Optional[str] = None

class CollegeCreate(CollegeBase):
    pass

class CollegeUpdate(CollegeBase):
    pass

class CollegeOut(CollegeBase):
    college_id: int
    class Config:
        orm_mode = True


# -------------------------
# COLLEGE YEARLY DATA
# -------------------------
class CollegeYearlyDataBase(BaseModel):
    college_id: int
    year: int
    enrollment_undergraduate: Optional[int] = None
    enrollment_graduate: Optional[int] = None
    enrollment_doctoral: Optional[int] = None
    enrollment_online: Optional[int] = None
    enrollment_total: Optional[int] = None

class CollegeYearlyDataCreate(CollegeYearlyDataBase):
    pass

class CollegeYearlyDataUpdate(CollegeYearlyDataBase):
    pass

class CollegeYearlyDataOut(CollegeYearlyDataBase):
    id: int
    class Config:
        orm_mode = True


# -------------------------
# DEPARTMENT
# -------------------------
class DepartmentBase(BaseModel):
    college_id: int
    name: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    total_enrollment_year: Optional[int] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    department_id: int
    class Config:
        orm_mode = True


# -------------------------
# PROFESSOR
# -------------------------
class ProfessorBase(BaseModel):
    first_name: str
    last_name: str
    title: Optional[str] = None
    cv_data: Optional[Any] = None
    emails: Optional[Any] = None
    phone_numbers: Optional[Any] = None
    office_location: Optional[str] = None
    department_id: Optional[int] = None
    resume_url: Optional[str] = None
    bio: Optional[str] = None
    picture_url: Optional[str] = None
    personal_website: Optional[str] = None
    college_id: Optional[int] = None

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorUpdate(ProfessorBase):
    pass

class ProfessorOut(ProfessorBase):
    professor_id: int
    class Config:
        orm_mode = True


# -------------------------
# PUBLICATION
# -------------------------
class PublicationBase(BaseModel):
    title: str
    publication_type: Optional[str] = None
    journal_or_conference: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[Any] = None
    citation_count: Optional[int] = None

class PublicationCreate(PublicationBase):
    pass

class PublicationUpdate(PublicationBase):
    pass

class PublicationOut(PublicationBase):
    publication_id: int
    class Config:
        orm_mode = True


# -------------------------
# COURSE
# -------------------------
class CourseBase(BaseModel):
    department_id: int
    course_code: str
    course_level: str
    course_title: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    learning_objectives: Optional[Any] = None
    credit_hours: Optional[float] = None
    instruction_mode: Optional[str] = None
    level: Optional[str] = None
    avg_enrollment: Optional[float] = None
    sections_count: Optional[int] = None
    market_size: Optional[float] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseOut(CourseBase):
    course_id: int
    class Config:
        orm_mode = True


# -------------------------
# COURSE SECTION
# -------------------------
class CourseSectionBase(BaseModel):
    course_id: int
    professor_id: Optional[int] = None
    section_code: Optional[str] = None
    semester: Optional[str] = None
    term_year: Optional[int] = None
    instruction_mode: Optional[str] = None
    credit_hours: Optional[float] = None
    file_url: Optional[str] = None
    description: Optional[str] = None
    learning_objectives: Optional[str] = None
    readings: Optional[str] = None
    enrollment: Optional[int] = None
    capacity: Optional[int] = None
    class_size: Optional[int] = None

class CourseSectionCreate(CourseSectionBase):
    pass

class CourseSectionUpdate(CourseSectionBase):
    pass

class CourseSectionOut(CourseSectionBase):
    section_id: int
    class Config:
        orm_mode = True


# -------------------------
# TEXTBOOK
# -------------------------
class TextbookBase(BaseModel):
    title: str
    author: Optional[str] = None
    edition: Optional[str] = None
    publisher: Optional[str] = None
    isbn_10: Optional[str] = None
    isbn_13: Optional[str] = None
    publication_year: Optional[int] = None
    format: Optional[str] = None
    print_length: Optional[int] = None
    item_weight: Optional[float] = None
    dimensions: Optional[str] = None
    url: Optional[str] = None
    amazon_price: Optional[float] = None
    list_price: Optional[float] = None

class TextbookCreate(TextbookBase):
    pass

class TextbookUpdate(TextbookBase):
    pass

class TextbookOut(TextbookBase):
    textbook_id: int
    class Config:
        orm_mode = True


# -------------------------
# LIBRARY YEARLY DATA
# -------------------------
class LibraryYearlyDataBase(BaseModel):
    college_id: int
    year: int
    expenditures_per_100_fte: Optional[float] = None
    physical_books: Optional[float] = None
    electronic_books: Optional[float] = None
    electronic_databases: Optional[float] = None
    physical_media: Optional[float] = None

class LibraryYearlyDataCreate(LibraryYearlyDataBase):
    pass

class LibraryYearlyDataUpdate(LibraryYearlyDataBase):
    pass

class LibraryYearlyDataOut(LibraryYearlyDataBase):
    id: int
    class Config:
        orm_mode = True
