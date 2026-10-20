# 🗄️ Data Schema

## 🌐 Data type used

1. int -> integer
2. string -> string
3. hashed -> password, sensitive data
4. choices -> has selected values only
5. timestamp -> full date time YYYY-MM-DD HH:MM:SS
6. time (hh:mm) -> hour:min

---

## 🏢 Site Data - Global

#### 1. Login Credential

NOTE: Using Django default user table with minor changes / additions shown in given table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| email | string | not null, unique | User | institute email |
| role | choices | not null | User | Management, HOD, Faculty, Student (default) |
| institute | int | not null | User | Foreign key, institute in which user belongs |

---

#### 2. Session Table

NOTE: Using Django default session table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|

---

## 🏫 Institute Data

### Onboarding

#### 1. Institute Table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| name | string | not null | User | |
| location | string | not null | User | |
| affiliation | string | not null | User | |
| contact_email | string | not null | User | official email |
| contact_number | string | not null | User | official contact |
| email_domain | string | not null, unique | User | for authentication |

#### 2. Period

| Field | Data Type | Constraint | Value By | Remark |
|-------|-----------|------------|----------|--------|
| institute | int | not null | User | FK, CASCADE |
| period | int | not null | User | Primary key |
| start_time | time (hh:mm) | not null | User | |
| end_time | time (hh:mm) | not null | User | |

#### 3. TimeSlot

| Field | Data Type | Constraint | Value By | Remark |
|-------|-----------|------------|----------|--------|
| day | choices | not null | User | mon, tue, wed, thu, fri, sat, sun |
| period | int | not null | User | FK, M:1, CASCADE |

NOTE: unique(`day`, `period`)

#### 4. Department Table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| institute | int | not null | User | FK, CASCADE |
| department_name | string | not null | User | |
| department_code | string | not null | User | |

NOTE: unique(institute, department_code)

#### 5. Course Table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| course_name | string | not null | User | |
| course_type | choices | not null | User | `major` / `minor` / `open_elective` |
| department | int | not null | User | FK, M:1, CASCADE |
| total_semester | int | not null | User | |

NOTE: Adjust for minor courses

---

### Users

#### 6. Faculty Table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| employee_id | string | not null, unique | User | |
| faculty_name | string | not null | User | |
| qualification | string | not null | User | |
| user | int | unique | User | FK, 1:1, SETNULL |

#### 7. Student Table 

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| enrollment_no | string | not null, unique | User | |
| student_name | string | not null | User | |
| department | int | not null | User | FK, M:1, CASCADE |
| course | | not null | User | FK, M:M |
| semester | int | not null | User | |
| user | int | unique | User | FK, 1:1, SETNULL |

#### 8. Student Group Table (incomplete)

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|

NOTE: define schema and constraints

---

### Curriculum

#### 9. Subject Table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| subject_code | string | not null, unique | User | |
| subject_name | string | not null | User | |
| course | int | not null | User | FK, M:1, CASCADE |
| semester | int | not null | User | |
| faculty | | not null | User | FK, M:M |
| weekly_theory_hours | int | not null | User | |
| weekly_practical_hours | int | not null | User | |

---

### Resources

#### 10. Building Table

| Field | Data Type | Constraint | Value By | Remark |
|-------|-----------|------------|----------|--------|
| institute | int | not null | User | FK, CASCADE |
| building_name | string | not null | User | |

#### 11. Room Table (Classrooms / Labs)

| Field | Data Type | Constraint | Value By | Remark |
|-------|-----------|------------|----------|--------|
| room_no | string | not null | User | room num or lab name |
| building | int | not null | User | FK, M:1, CASCADE |
| departments | | not null | User | FK, M:M |
| room_type | choices | not null | User | `class` (theory), `smartclass` (projector), `lab` |
| subjects | | not null | User | FK, M:M |
| capacity | int | not null | User | Maximum seating capacity |

NOTE: unique(building, room_no)

---

### Availability

#### 12. Faculty Unavailability Table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| faculty | int | not null | User | FK, M:1, CASCADE |
| timeslot | int | not null | User | FK, M:1, CASCADE |
| no_of_weeks | int | not null | User | | 
| reason | string | not null | User | Reason for unavailability |
| created_at | timestamp | system | auto_now_add | |

#### 13. Room Unavailability Table

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| room | int | not null | User | FK, M:1, CASCADE |
| timeslot | int | not null | User | FK, M:1, CASCADE |
| no_of_weeks | int | not null | User | | 
| reason | string | not null | User | Reason for unavailability |
| created_at | timestamp | system | auto_now_add | |

---

### M:M RELATIONSHIP TABLE

#### 14. Faculty - Department

NOTE: each faculty is assign for what department

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| faculty | int | not null | User | FK |
| department | int | not null | User | FK |
| designation | choices | not null | User | hod, professor, ass_professor |

NOTE: unique(faculty, department)

---

## scheduler

### 1. Occupancy Table (Actual Timetable)

| Field | Data Type | Constraint | Value By | Remark |
|-------|------------|-------------|-----------|---------|
| room_id | int | not null | AI | Foreign key, default primary sorting |
| timeslot_id | int | not null | AI | Foreign key, default secondary sorting |
| subject_id | int | not null | AI | Foreign key |
| faculty_id | int | not null | AI | Foreign key |
| student_group_id | int | not null | AI | Foreign key |

#### 🔒 Constraints

1. `room_id` and `timeslot_id` cannot both be identical for two rows → no duplicate slot-room entries
2. If two rows have the same `faculty` but different `room`, their `timeslot` must differ (faculty cannot be in two rooms at once)
3. Rule #2 also applies to `student_group` (a student group can’t attend two classes at once)
4. `faculty` and `student_group` must correspond to the same `subject`

NOTE: Constraint 3 and 4 are not enforced yet

---

## 🧩 Notes

- Primary key of every table is auto-generated by Django, unless stated otherwise
- Time-related fields use IST timestamps for consistency.
