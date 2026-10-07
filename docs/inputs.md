# 🧾 User Input

## 0. Input Types

dropdown - dropdown with search as type

## 1. Login Page

| Field | Type | Required | constraints | remark / options |
|-------|------|----------|-------------|------------------|
| username | string | yes | college email domain | |
| password | string | yes | encrypted | |
| institute | dropdown search | yes | |
| role | dropdown | search | 

NOTE: Dashboard layout and content based on role, username
NOTE: Check wether given username elligable for the role

## 1️⃣ Institute Registration

| Field | Type | Required | Description |
|--------|------|-----------|-------------|
| Institute Name | String | yes | Name of the college |
| Affiliation | String | yes | University or governing body |
| Location | String | yes | City, state |
| Institute Contact Info | String | yes | Official contact number/email |
| College Email Domain | String | yes | Used for admin verification |

---

## 2️⃣ Admin Inputs

| Field | Type | Required | Description |
|--------|------|-----------|-------------|
| Department Name | String | yes | Name of department |
| Classroom/Lab Info | Object | yes | Room number, type, capacity, department |
| Time Slots | Object | yes | Periods, start time, end time |
| Faculty Info | List | yes | Name |
| Student Info | List | yes | Enrollment no, opted major/minor/electives |


---

## 3️⃣ HOD Inputs

| Field | Type | Required | Description |
|--------|------|-----------|-------------|
| Course info | Objects | yes | Course Name, type |
| Subjects | List | yes | Subject name, theory/practical hours |

---

## 4️⃣ Faculty Inputs

| Field | Type | Required | Description |
|--------|------|-----------|-------------|
| Unavailability | Schedule | yes | Days and times faculty is available |

---

## 🧠 Additional Inputs for Optimization

| Parameter | Description |
|------------|-------------|
| Maximum teaching hours/week | AICTE workload limit |
| Minimum gap between classes | Faculty relaxation constraint |
| Preferred Lab Times | Department-level rules |
| Weightage Settings | Admin chooses optimization priorities (faculty balance vs. room use) |
