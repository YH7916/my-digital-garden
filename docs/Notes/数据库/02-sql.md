---
title: PPT 03 SQL 语句
tags:
  - learning
  - courses
  - database
  - finals
  - exam
  - ppt-expanded
  - docx-first
updated: 2026-06-16
publish: true
blog_dest: Notes/数据库/02-sql.md
---
## 2. PPT 03 SQL 语句：把自然语言翻译成查表动作

这一章以 `第三章 introduction to SQL.docx` 为主要讲解来源。PPT 给了 SQL 的题型范围，但 Word 笔记里真正有用的是那些“为什么这么写”的解释：外键删除/更新策略、natural join 的坑、分组和 having、嵌套查询、`some/all/exists`。

本章只抓一件事：

```text
SQL = 从哪些表拿数据 + 表怎么接起来 + 保留哪些行 + 最后显示哪些列。
```

### 2.1 SQL 做题先问四句话

任何 SQL 题都先别写代码，先翻译题意：

```text
1. 最后输出什么？        -> SELECT
2. 信息在哪些表里？      -> FROM
3. 表和表怎么接上？      -> JOIN 条件 / WHERE 连接条件
4. 需要筛选/分组/排序吗？ -> WHERE / GROUP BY / HAVING / ORDER BY
```

例子：

```text
查询 CS 专业中，选了 Database 课程且成绩不低于 85 的学生姓名。
```

你要先在脑子里定位：

```text
学生姓名 name 在 student 表。
专业 major 在 student 表。
成绩 score 在 takes 表。
课程名 title 在 course 表。
```

三张表要靠共同钥匙接起来：

```text
student.sid = takes.sid
takes.cid = course.cid
```

所以答案是：

```sql
SELECT s.name
FROM student AS s, takes AS t, course AS c
WHERE s.sid = t.sid
  AND t.cid = c.cid
  AND s.major = 'CS'
  AND c.title = 'Database'
  AND t.score >= 85;
```

这类题的考场第一笔：

```text
先把 SELECT / FROM 写出来，再补连接条件，最后补筛选条件。
```

### 2.2 建表、主键、外键：别只会写 `CREATE TABLE`

Word 笔记里强调了外键的真实含义：一张表中的某列必须能在另一张表的主键列里找到。

比如：

```sql
CREATE TABLE instructor (
  ID        CHAR(5),
  name      VARCHAR(20),
  dept_name VARCHAR(20),
  salary    NUMERIC(8,2),
  PRIMARY KEY (ID),
  FOREIGN KEY (dept_name) REFERENCES department(dept_name)
);
```

这句话不是装饰。它的意思是：

```text
instructor 表里的每个 dept_name，
都必须是 department 表里真实存在的 dept_name。
```

如果某个系撤销了，`department` 里要删除这个系，但 `course` 或 `instructor` 里还有行指向它，数据库就要决定怎么办。这就是外键的 delete / update 策略。

### 2.3 外键 delete / update 四种策略

假设：

```text
course.dept_name references department.dept_name
```

如果一个 department 被删除，course 里相关课程怎么办？

| 策略 | 人话 | 例子 |
|---|---|---|
| `cascade` | 跟着一起删/改 | 系撤销，属于这个系的课程也删除 |
| `set null` | 指向它的外键改成 NULL | 课程暂时没有所属系 |
| `restrict` | 不允许删/改被引用的行 | 还有课程属于这个系，所以不能删系 |
| `set default` | 改成默认值 | 课程所属系改成默认系 |

更新也是同理。如果 department 改名，`cascade` 就让引用它的 course 也跟着改名。

易错点：

```text
如果外键列有 NOT NULL 约束，就不能 set null。
restrict 的含义不是“删掉引用它的行”，而是“不让你删被引用的行”。
```

### 2.4 `natural join`：它很方便，也很危险

Word 笔记里有一个非常重要的坑：`natural join` 会自动拿所有同名属性做等值连接。

比如：

```text
student(ID, name, dept_name)
takes(ID, course_id)
course(course_id, title, dept_name)
```

如果你写：

```sql
student NATURAL JOIN takes NATURAL JOIN course
```

数据库可能会用两个同名列一起连：

```text
ID
course_id
dept_name
```

这可能变成：

```text
学生所在系 = 课程开课系
```

但题目如果是“找上了不是自己系课程的学生”，这就错了。更稳的写法是显式写连接条件：

```sql
SELECT s.name
FROM student AS s, takes AS t, course AS c
WHERE s.ID = t.ID
  AND t.course_id = c.course_id
  AND s.dept_name <> c.dept_name;
```

A4 规则：

```text
natural join 只在确认所有同名列都应该相等时使用；考试更推荐显式连接条件。
```

### 2.5 `LIKE` 和转义字符

`LIKE` 用来做字符串匹配：

```sql
WHERE name LIKE 'Li%'
```

含义：

```text
找以 Li 开头的字符串。
```

符号：

```text
% 代表任意长度字符串
_ 代表任意一个字符
```

如果你真的要找字符串里的 `%`，就要转义。比如找名字等于 `100%` 的行，不能写：

```sql
WHERE name LIKE '100%%'
```

这会让第二个 `%` 仍然被当作通配符。应该写：

```sql
WHERE name LIKE '100#%' ESCAPE '#';
```

意思是：

```text
# 后面的 % 不再是通配符，而是普通字符。
```

### 2.6 排序和 limit

```sql
ORDER BY salary
```

默认升序。

```sql
ORDER BY salary DESC
```

降序。

多个排序字段：

```sql
ORDER BY dept_name, salary DESC
```

意思是：

```text
先按 dept_name 排；
同一个 dept 内，再按 salary 从高到低排。
```

`LIMIT` 常用来取前几名：

```sql
ORDER BY salary DESC
LIMIT 3;
```

如果写：

```sql
LIMIT a, b
```

含义是：

```text
从下标 a 开始，取 b 个。
```

注意：如果题目要求“并列第一全部输出”，不要用 `LIMIT 1`，因为并列会被截断。

### 2.7 集合操作：默认去重

SQL 的集合操作：

```text
UNION      并
INTERSECT  交
EXCEPT     差
```

默认会去重。如果不想去重，要写：

```sql
UNION ALL
INTERSECT ALL
EXCEPT ALL
```

这点常出选择题。

### 2.8 NULL：它不是 0，也不是空字符串

`NULL` 表示未知或不存在。

不能写：

```sql
WHERE age = NULL
```

要写：

```sql
WHERE age IS NULL
```

或者：

```sql
WHERE age IS NOT NULL
```

聚合函数里：

```text
COUNT(*) 会数所有行。
COUNT(attribute) 通常不数 NULL。
```

### 2.9 GROUP BY：看到“每个”就分组

看到这些词，先想到分组：

```text
每个系
每门课
每个 group
最多
平均
超过平均
数量不少于...
```

例子：

```text
找每个系的老师人数。
```

```sql
SELECT dept_name, COUNT(*) AS cnt
FROM instructor
GROUP BY dept_name;
```

重要规则：

```text
SELECT 里出现的普通列，要么在 GROUP BY 后面，
要么放在聚合函数里。
```

所以这个是错的：

```sql
SELECT dept_name, name, COUNT(*)
FROM instructor
GROUP BY dept_name;
```

因为每个系有很多老师，分组后数据库不知道该显示哪个 `name`。

### 2.10 WHERE 和 HAVING：一个筛行，一个筛组

```text
WHERE 在 GROUP BY 之前执行，筛原始行。
HAVING 在 GROUP BY 之后执行，筛分组结果。
```

例子：

```sql
SELECT dept_name, COUNT(*) AS cnt
FROM instructor
WHERE salary > 100000
GROUP BY dept_name
HAVING COUNT(*) > 10;
```

这句话分三步读：

```text
先筛出 salary > 100000 的老师；
再按 dept_name 分组；
最后只保留“高薪老师超过 10 个”的系。
```

如果你想筛聚合结果，就必须用 HAVING。

### 2.11 `IN` / `NOT IN`：结果在不在一个集合里

```sql
SELECT name
FROM student
WHERE ID IN (
  SELECT ID
  FROM takes
  WHERE course_id = 'DB'
);
```

人话：

```text
先找选了 DB 的学生 ID 集合；
再找 ID 在这个集合里的学生姓名。
```

`NOT IN` 反过来。但要小心 NULL：如果子查询结果里有 NULL，`NOT IN` 可能变得很别扭。考试如果要表达“不存在”，更稳的是 `NOT EXISTS`。

### 2.12 `SOME` / `ALL`：和一堆值比较

Word 笔记里提到：如果子查询只返回一个值，可以直接比较：

```sql
WHERE salary * 10 > (
  SELECT budget
  FROM department
  WHERE dept_name = 'CS'
)
```

但如果子查询可能返回多个值，就要写 `SOME` 或 `ALL`。

```text
> SOME：大于其中至少一个。
> ALL：大于所有。
```

找 CS 系 credits 最大的课程，可以写：

```sql
SELECT *
FROM course
WHERE department = 'CS'
  AND credits >= ALL (
    SELECT credits
    FROM course
    WHERE department = 'CS'
  );
```

这句的意思：

```text
这门课的 credits 大于等于 CS 系所有课程的 credits，
所以它就是最大值课程。
```

### 2.13 `EXISTS`：有没有这样一行

`EXISTS` 不关心子查询具体返回什么，只关心有没有行。

例子：

```text
找有重名课程 title 的课程名。
```

可以写：

```sql
SELECT C1.title
FROM course AS C1
WHERE EXISTS (
  SELECT *
  FROM course AS C2
  WHERE C2.title = C1.title
    AND C2.course_id <> C1.course_id
);
```

人话：

```text
对每一门 C1，去找有没有另一门 C2：
title 一样，但 course_id 不一样。
如果有，说明这个 title 重名。
```

### 2.14 “每组最大/平均以上”题型模板

2025 review 很喜欢这种题。

例题：

```text
输出女性用户最多的 group_name；如果并列，全部输出。
```

先写每组女性人数：

```sql
SELECT group_name, COUNT(user_id) AS female_count
FROM user
WHERE gender = 'female'
GROUP BY group_name;
```

再找最大：

```sql
WITH T AS (
  SELECT group_name, COUNT(user_id) AS female_count
  FROM user
  WHERE gender = 'female'
  GROUP BY group_name
)
SELECT group_name
FROM T
WHERE female_count = (
  SELECT MAX(female_count)
  FROM T
);
```

这个写法比 `ORDER BY ... LIMIT 1` 更稳，因为并列第一也能全部输出。

再看“高于平均”：

```text
在 game group 中，找粉丝数高于 game group 用户平均粉丝数的用户。
```

核心是先造一张临时表：

```text
T(user_id, follower_count)
```

再和平均值比较：

```sql
WITH T AS (
  SELECT u.user_id, COUNT(f.follower_id) AS follower_count
  FROM user AS u, followship AS f
  WHERE u.user_id = f.user_id
    AND u.group_name = 'game'
  GROUP BY u.user_id
)
SELECT u.user_id, u.name, T.follower_count
FROM user AS u, T
WHERE u.user_id = T.user_id
  AND T.follower_count > (
    SELECT AVG(follower_count)
    FROM T
  );
```

考场第一笔：

```text
复杂聚合题先造中间表 T，再在 T 上比较 max/avg。
```

### 2.15 SQL A4 规则

```text
SQL 四问：输出什么、来自哪些表、怎么连接、怎么筛选/分组。
外键策略：cascade / set null / restrict / set default。
natural join 会用所有同名列，慎用。
LIKE 中 % 和 _ 是通配符；查真实 % 要 ESCAPE。
GROUP BY 后，SELECT 普通列必须出现在 GROUP BY 中。
WHERE 筛原始行，HAVING 筛分组结果。
子查询多值比较用 SOME / ALL。
EXISTS 只问“有没有行”。
每组最大/平均以上：先构造分组统计表 T，再比较。
```
