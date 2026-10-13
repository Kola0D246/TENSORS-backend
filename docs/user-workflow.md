# 🧭 User Workflow - Smart Classroom and Timetable Scheduler

## 1. Institute Onboarding (One-Time)

**Actor:** Institute Management  
**Goal:** Register college and create system anchor  

### Flow

1. Management visits platform → fills out `Institute Name, Location, Affiliations, Contact Info, College Email Domain`  
2. Verification (manual or automated via admin panel or email domain match)  
3. The platform verifies the institute and the applicant's authority.
4. A platform administrator approves the registration.
5. On approval → system generates:  
   - a new entry in institute row using provided information in step 1 
   - Default **Admin user (management email)** → `user_id`, password setup  
6. Admin logs in → proceeds to setup dashboard.  

---

## 2. Admin Setup (Institute-Level Configuration)**

**Actor:** Institute Management  
**Goal:** Define foundation for scheduling  

### Flow

1. **Add Departments**  
   - Creates entry in `department_table`  
   - Auto-generates `department_id` + default `HOD login credentials`  
2. **Add Infrastructure (infra_table)**  
   - Classrooms + Labs → number, capacity, department, special features (smart class/lab type)  
3. **Configure academic calendar**
   - Academic year, semester dates, working days/holidays
4. **Set Time Policies**  
   - Time slots, working days, start/end time. Configure academic rules
5. **Define Academic Parameters**  
   - Allowed majors, minors, electives  
   - Workload rules (e.g., max classes/day, hours/week)
5. **Register Users**
   - Other Management members
   - Faculty details - employee_id, 
   - Students details - enrollment, name, department, semester
6. **Activate Departments**  
   - Confirm required setup and enable scheduling
   - HOD credentials send along with secure invitation for password setup.

---

## 3. Department Setup (HOD-Level Configuration)

**Actor:** HOD 
**Goal:** Enter course and faculty-specific constraints  

### **Flow:**

1. **Login using department credentials**  
   - Change password (first-time)  
2. **Provide Department Info:**  
   - Course list (major, minor, elective)  
   - Subject list per course + theory/lab hours 
   - Define theory, practical and lab requirements.
3. **Assign Faculty**  
   - Faculty - name, designation, assigned subjects
   - Availability (days/time slots)  
4. **Add Students**  
   - Student record and subject selection/assigned.  
5. **Validate and Submit data for scheduling**  

---

## 4. Schedule Generation (AI/Constraint Engine)

**Actor:** Scheduler (Authorized Staff or System AI)  
**Goal:** Generate optimized timetable per department  

### **Flow:**

1. Collects all constraints:  
   - Infrastructure, faculty, subjects, student data, institute rules 
2. Detect impossible constraints
   - Missing faculty, insufficient rooms, conflicting requirements 
3. . Runs optimization algorithm (CSP / OR-Tools / GA)  
4. Generates:  
   - Base **department-wise timetable**  
   - Classroom allocations  
   - Faculty load summary  
5. Evaluate and compare
   - Check hard constraints and score timetable quality
4. Admin/HOD review → approve or regenerate alternate timetables.  

---

## 5. Publication & Integration

**Actor:** Admin / IT Cell  
**Goal:** Share approved timetables  

### **Flow:**

- Approved timetable pushed to institute website (embed / iframe)  
- Optional: auto-export to PDF or Excel for notice boards  
- Static timetable available publicly  

---

## 6. Dynamic Update (AI/Real-time Adjustment)

**Actor:** Faculty / Admin  
**Goal:** Handle absences or classroom unavailability  

### **Flow:**

1. Report an incident
   - Faculty reports leave, or Admin marks a room unavailable.
2. Find affected classes
   - Identify impacted periods, rooms, faculty and student groups.
3. Generate alternatives
   - Suggest room changes, swaps, substitute faculty or rescheduling.
4. Validate and approve
   - Check clashes and obtain approval according to the institute's policy.
5. Publish the update
   - Update the timetable version and notify affected students and faculty.

---

## 7. Reporting & Audit

**Actor:** Admin, HOD, Authorities  
**Goal:** Insights & compliance  

### **Flow:**

1. Room and lab utilization
2. Subject-wise and semester-wise teaching-hour completion
3. Unscheduled or unfulfilled classes
4. Faculty workload against configured limits
5. Timetable changes and their reasons
6. Approval history and the identity of the approver
7. Rescheduling success rate and unresolved conflicts
