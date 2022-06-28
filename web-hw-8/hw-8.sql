-- teacher --

CREATE TABLE IF NOT EXISTS teachers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	full_name VARCHAR(30) UNIQUE NOT NULL
);

-- subject --

CREATE TABLE IF NOT EXISTS subjects (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	subject_name VARCHAR(30) UNIQUE NOT NULL
);

-- group --

CREATE TABLE IF NOT EXISTS groups (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	group_name VARCHAR(30) UNIQUE NOT NULL,
	group_year TINYINT NOT NULL
);

-- teacher_subject --

CREATE TABLE IF NOT EXISTS teacher_subject (
	id_teacher INTEGER NOT NULL,
	id_subject INTEGER NOT NULL,
    foreign key (id_teacher) references teacher (id)
    	on update cascade,
    foreign key (id_subject) references subject (id)
    	on update cascade
);

INSERT OR REPLACE into teacher_subject (id_teacher, id_subject)
VALUES (1, 1),
(1, 2),
(2, 3),
(3, 4),
(3, 5),
(2, 5)
returning *;


-- student --

CREATE TABLE IF NOT EXISTS students (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	full_name VARCHAR(30) UNIQUE NOT NULL,
	id_group INTEGER NOT NULL,
	foreign key (id_group) references groups (id)
    	on update cascade
);

-- mark --

CREATE TABLE IF NOT EXISTS marks (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	marks INTEGER NOT NULL,
	id_student INTEGER NOT NULL,
	id_subject INTEGER NOT NULL,
	id_teacher INTEGER NOT NULL,
	mark_date date default current_date,
	foreign key (id_student) references students (id)
    	on update cascade,
    foreign key (id_subject) references subjects (id)
    	on update cascade,
    foreign key (id_teacher) references teachers (id)
    	on update cascade
);

-- select max(mark_date) from mark;
-- select * from mark;



-- --  5 students with the highest GPA in all subjects.

-- select avg(mark) as avgMark, stud.full_name
-- from mark m
-- join subject sub on sub.id = m.id_subject
-- join student stud on stud.id = m.id_student
-- group by stud.full_name
-- order by avgMark desc limit 5;


-- --  1 student with the highest GPA in one subject.

-- select avg(mark) as avgMark, stud.full_name
-- from mark m
-- join subject sub on sub.id = m.id_subject
-- join student stud on stud.id = m.id_student
-- where sub.subject_name = 'English'
-- group by stud.full_name
-- order by avgMark desc limit 1;



-- --  average score in a group in one subject.

-- select avg(mark) as avgMark
-- from "groups" g
-- join student stud on g.id = stud.id_group
-- join mark m on stud.id = m.id_student
-- join subject sub on m.id_subject = sub.id
-- where g.group_name = 'G-2' and sub.subject_name = 'English';


-- --  average score in the stream.

-- select avg(m.mark) as avgMark
-- from "groups" g
-- join student stud on g.id = stud.id_group
-- join mark m on stud.id = m.id_student
-- where g.group_year = 2020;


-- -- what courses are taught by the teacher.

-- select sub.subject_name, t.full_name
-- from teacher_subject ts
-- join teacher t on ts.id_teacher = t.id
-- join subject sub on ts.id_subject = sub.id
-- where t.full_name = 'Frieda Evans';


-- -- list of students in the group.

-- select stud.full_name, g.group_name
-- from student stud
-- join "groups" g on stud.id_group = g.id
-- where g.group_name = 'G-2';


-- -- grades of students in a group on a subject.

-- select m.mark, stud.full_name, sub.subject_name
-- from mark m
-- join student stud on m.id_student = stud.id
-- join subject sub on m.id_subject = sub.id
-- join "groups" g on stud.id_group = g.id
-- where sub.subject_name = 'Physics' and g.group_name = 'G-1'
-- order by stud.full_name desc;


-- -- grades of students in the group on the subject in the last lesson.

-- select mark_date, m.mark, stud.full_name, sub.subject_name, g.group_name
-- from mark m
-- join student stud on m.id_student = stud.id
-- join subject sub on m.id_subject = sub.id
-- join "groups" g on stud.id_group = g.id
-- where sub.subject_name = 'Physics' and g.group_name = 'G-1' and mark_date = '2021-05-28';


-- -- list of courses that the student is attending.

-- select  sub.subject_name
-- from student_subject ss
-- join student stud on ss.id_student = stud.id
-- join subject sub on ss.id_subject = sub.id
-- where stud.full_name = 'Adam Chase';


-- -- list of courses that the teacher reads to the student.

-- select sub.subject_name
-- from mark m
-- join teacher t on m.id_teacher = t.id
-- join student stud on m.id_student = stud.id
-- join subject sub on m.id_subject = sub.id
-- where t.full_name = 'Vladimir Hayes' and stud.full_name = 'Adam Chase'
-- group by sub.subject_name;


-- -- the average grade given by the teacher to the student.

-- select avg(m.mark) as avgMark
-- from mark m
-- join teacher t on m.id_teacher = t.id
-- join student s on m.id_student = s.id
-- where t.full_name = 'Vladimir Hayes' and s.full_name = 'Liliana Johnson';

-- -- the average mark given by the teacher.

-- select avg(m.mark) as avgMark
-- from mark m
-- join teacher t on m.id_teacher = t.id
-- join student s on m.id_student = s.id
-- where t.full_name = 'Vladimir Hayes'