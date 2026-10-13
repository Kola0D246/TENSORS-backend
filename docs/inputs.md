# 🧾 User Input

## 4️⃣ Role responsibilities 

| Action | Management/Admin | HOD | Faculty | Student |
| -------------------- | ----- | ---- | ---- | ---- |
| Configure institute | Yes | No | No | No | 
| Manage users | Yes | Limited, if permitted | No | No |
| Manage rooms and time slots | Yes | View / request changes | No | No |
| Manage subjects and teaching requirements | Policy-dependent | Yes, within department | No | No |
| Assign faculty to subjects | Optional central oversight | Yes | No | No |
| Generate timetable | Authorized operator | Request / review | No | No
| Approve and publish timetable | According to institute policy | Department approval | No | No |
| View timetable | Yes | Yes | Personal | class timetable |
| Request a schedule change | Yes | Yes | Yes | Optional, if supported |

## 0. Input Types

dropdown - dropdown with search as type

## 1. Login (Admin and Users-Student, Faculty, HOD)

| Field | Type | Required | constraints | remark / options |
|-------|------|----------|-------------|------------------|
| username | string | yes | college email domain | |
| password | string | yes | encrypted | |

NOTE: Dashboard layout and content based on role, username
NOTE: Check wether given username eligable for the role

---

## 1️⃣ Login and Instititute registration

| Field | Type | Required | Description |
|--------|------|-----------|-------------|
| Institute Name | String | yes | Name of the college |
| Username / College Email | String | yes | Used for admin verification |
| Affiliation | String | yes | University or governing body |
| Location | String | yes | City, state |
| Institute Contact Info | String | yes | Official contact number/email according to the selected type|
| College Email Domain | String | yes | Normalised domain Eg - @satiengg.in |


---

## 2️⃣ Admin Inputs

| Field | Type | Required | Description |
|--------|------|-----------|-------------|
| Department Name | String | yes | Department name, code (Eg. - CSE or EE) |
| Classroom/Lab Info | Object | yes | Room number, type, capacity, Department|
| Time Slots | Object | yes | Period (Slot no.), start time, end time |
| Faculty Info | List | yes | Name |
| Student Info | List | yes | Enrollment no, Course, Semester, opted major/minor/electives |


---

## 3️⃣ HOD Inputs

| Field | Type | Required | Description |
|--------|------|----------|------------|-------------|
| Course Info | Objects | yes | Course Name, type |
| Subject | List | yes | Subject name, Subject Code, type, credits |
| Faculty assignment | List | yes | Faculty name, subject offering - subject code and name |
| Teaching requirements | List | yes | Weekly lecture periods, lab periods |

---

## 4️⃣ Faculty Inputs

| Field | Type | Required | Description |
|--------|------|-----------|-------------|
| Unavailability | Schedule | No | Unavailable days and timeslot with reason |

---

## 🧠 Additional Inputs for Optimization

| Parameter | Description |
|------------|-------------|
| Maximum teaching hours/week | AICTE workload limit |
| Minimum gap between classes | Faculty relaxation constraint |
| Preferred Lab Times | Department-level rules |
| Weightage Settings | Admin chooses optimization priorities (faculty balance vs. room use) |
