from sqlalchemy import (
    create_engine, Column, Integer, String, Text, ForeignKey,
    Float, Boolean, Table, DateTime, UniqueConstraint, Numeric, JSON
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# ---------------------------------------------------------------
# Association Tables
# ---------------------------------------------------------------

course_textbooks = Table(
    "course_textbooks",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("course_id", ForeignKey("courses.course_id", ondelete="CASCADE")),
    Column("isbn_13", ForeignKey("textbooks.isbn_13", ondelete="CASCADE")),
    Column("required", Boolean, default=True)
)

publication_authors = Table(
    "publication_authors",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("publication_id", ForeignKey("publications.publication_id", ondelete="CASCADE")),
    Column("professor_id", ForeignKey("professors.professor_id", ondelete="CASCADE")),
    Column("author_order", Integer),
    UniqueConstraint("publication_id", "professor_id", name="uq_publication_professor")
)

professor_textbooks = Table(
    "professor_textbooks",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("professor_id", ForeignKey("professors.professor_id", ondelete="CASCADE")),
    Column("isbn_13", ForeignKey("textbooks.isbn_13", ondelete="CASCADE")),
    Column("role", String(100)),
    Column("semester", String(50)),
    Column("term_year", Integer),
    Column("notes", Text),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    UniqueConstraint("professor_id", "isbn_13", "semester", "term_year", name="uq_professor_textbook_semester_year")
)


# ---------------------------------------------------------------
# Core Models
# ---------------------------------------------------------------

class College(Base):
    __tablename__ = "colleges"
    college_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    abbreviation = Column(String(50))
    location = Column(String(255))
    website = Column(Text) 
    contact_email = Column(String(255))
    phone = Column(String(50))
    
    addr = Column(String(255))
    city = Column(String(255))
    state = Column(String(10))
    zip = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow) 
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    departments = relationship("Department", back_populates="college")
    yearly_data = relationship("CollegeYearlyData", back_populates="college", cascade="all, delete-orphan")
    library_data = relationship("LibraryYearlyData", back_populates="college", cascade="all, delete-orphan")
    professors = relationship("Professor", back_populates="college")
    schools = relationship("School", back_populates="college", cascade="all, delete-orphan")

class CollegeYearlyData(Base):
    __tablename__ = "college_yearly_data"
    id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("colleges.college_id", ondelete="CASCADE"))
    year = Column(Integer, nullable=False)

    enrollment_undergraduate = Column(Integer)
    enrollment_graduate = Column(Integer)
    enrollment_doctoral = Column(Integer)
    enrollment_online = Column(Integer)
    enrollment_total = Column(Integer)

    completions_associates = Column(Integer)
    completions_bachelors = Column(Integer)
    completions_masters = Column(Integer)
    completions_doctoral_research = Column(Integer)
    completions_doctoral_professional = Column(Integer)
    completions_other = Column(Integer)
    completions_total = Column(Integer)

    completions_by_cip = Column(JSON)
    completions_by_awlevel = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("college_id", "year", name="uq_college_year"),)

    college = relationship("College", back_populates="yearly_data")

class School(Base):
    __tablename__ = "schools"
    school_id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("colleges.college_id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    website = Column(Text)
    contact_email = Column(String(255))
    contact_phone = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    college = relationship("College", back_populates="schools")
    departments = relationship("Department", back_populates="school", cascade="all, delete-orphan")
    courses = relationship("Course", back_populates="school", cascade="all, delete-orphan")

class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="CASCADE"), nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.college_id"))
    
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    contact_email = Column(String(255))
    contact_phone = Column(String(255))
    website = Column(Text)
    
    school = relationship("School", back_populates="departments")
    college = relationship("College", back_populates="departments")
    professors = relationship("Professor", back_populates="department")
    courses = relationship("Course", back_populates="department")

class Publication(Base):
    __tablename__ = "publications"
    publication_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    publication_type = Column(String(100))
    journal_or_conference = Column(String(255))
    publisher = Column(String(255))
    publication_year = Column(Integer)
    doi = Column(String(255))
    url = Column(Text)
    abstract = Column(Text)
    keywords = Column(JSON)
    citation_count = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(Integer, primary_key=True)

    name = Column(Text, nullable=False)
    title = Column(Text)

    cv_data = Column(JSON)
    emails = Column(JSON)
    phone_numbers = Column(JSON)
    office_location = Column(Text)

    resume_url = Column(Text)
    profile_url = Column(Text)
    picture_url = Column(Text)
    linkedin_url = Column(Text)
    bio = Column(Text)

    personal_website = Column(JSON, nullable=True)
    research_interests = Column(JSON)
    publications = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department_id = Column(Integer, ForeignKey("departments.department_id"))
    department = relationship("Department", back_populates="professors")

    college_id = Column(Integer, ForeignKey("colleges.college_id"))
    college = relationship("College", back_populates="professors")

    textbooks = relationship(
        "Textbook",
        secondary=professor_textbooks,
        back_populates="professors"
    )

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="CASCADE"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True)
    
    course_code = Column(String(50), nullable=False)
    course_level = Column(String(50), nullable=False)
    course_title = Column(String(255), nullable=False)
    short_description = Column(Text)
    long_description = Column(Text)
    learning_objectives = Column(JSON)
    credit_hours = Column(Float)
    instruction_mode = Column(String(50))
    level = Column(String(50))
    avg_enrollment = Column(Float)
    sections_count = Column(Integer)
    market_size = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    school = relationship("School", back_populates="courses")
    department = relationship("Department", back_populates="courses")
    textbooks = relationship("Textbook", secondary=course_textbooks, back_populates="courses")
    sections = relationship("CourseSection", back_populates="course", cascade="all, delete-orphan")


# TODO: have a list of textbook IDs, query these individually, get rid of course_textbooks / course_section_textbooks table,
# do not need a many-many rltn
class CourseSection(Base):
    __tablename__ = "course_sections"
    section_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professors.professor_id"))
    
    section_code = Column(String(50))
    course_code = Column(String(50))
    semester = Column(String(50))
    term_year = Column(Integer)
    instruction_mode = Column(String(50))
    credit_hours = Column(Float)
    file_url = Column(Text)
    description = Column(Text)
    learning_objectives = Column(Text)
    readings = Column(Text)
    enrollment = Column(Integer)
    capacity = Column(Integer)
    class_size = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    course = relationship("Course", back_populates="sections")
    professor = relationship("Professor")


class Textbook(Base):
    __tablename__ = "textbooks"

    isbn_13 = Column(String(25), primary_key=True)
    title = Column(String(255), nullable=False)
    edition = Column(String(50))
    publisher = Column(String(255))
    contributors = Column(JSON)  
    isbn_10 = Column(String(20)) 
    publication_year = Column(Integer)
    format = Column(String(50))
    print_length = Column(Integer)
    item_weight = Column(Float)
    dimensions = Column(String(100))
    url = Column(Text)
    amazon_price = Column(Numeric(10, 2))
    list_price = Column(Numeric(10, 2))
    asin = Column(String(20))

    created_at = Column(DateTime, default=datetime.utcnow)

    work_id = Column(Integer, ForeignKey("textbook_works.work_id"), nullable=True)
    work = relationship("TextbookWork", back_populates="editions")

    courses = relationship("Course", secondary="course_textbooks", back_populates="textbooks")
    professors = relationship("Professor", secondary="professor_textbooks", back_populates="textbooks")

class TextbookWork(Base):
    __tablename__ = "textbook_works"

    work_id = Column(Integer, primary_key=True)
    contributors = Column(JSON)
    title = Column(String(255), nullable=False) 
    description = Column(Text)

    editions = relationship("Textbook", back_populates="work")

class LibraryYearlyData(Base):
    __tablename__ = "library_yearly_data"
    id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("colleges.college_id", ondelete="CASCADE"), nullable=False)

    year = Column(Integer, nullable=False)

    expenditures_per_100_fte = Column(Float)
    physical_books = Column(Float)
    electronic_books = Column(Float)
    electronic_databases = Column(Float)
    physical_media = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    college = relationship("College", back_populates="library_data")
