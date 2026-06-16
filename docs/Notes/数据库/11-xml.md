---
title: 补充题型 XML / DTD / XPath / XQuery
tags:
  - learning
  - courses
  - database
  - finals
  - exam
  - ppt-expanded
updated: 2026-06-16
publish: true
blog_dest: Notes/数据库/11-xml.md
---
## 11. 补充题型 XML / DTD / XPath / XQuery：拿保底分

XML 不是主线，但老样卷常考。目标是拿模板分。

### 10.1 DTD 读法

```xml
<!ELEMENT campus_cards (pos+, card+)>
<!ELEMENT pos (campus, location)>
<!ATTLIST pos pno ID #REQUIRED>
```

翻译：

```text
campus_cards 里面有一个或多个 pos，和一个或多个 card。
pos 里面必须有 campus 和 location。
pos 有一个属性 pno，它是 ID，必须写。
```

符号：

```text
+：一个或多个
*：零个或多个
?：零个或一个
ID：唯一标识
IDREF：引用某个 ID
IDREFS：引用多个 ID
```

### 10.2 XPath 模板

XPath 是路径查询。

```text
/A/B/C：从根开始找 A 下的 B 下的 C
//C：任意位置的 C
[@attr='x']：属性筛选
[child='x']：子元素筛选
```

例子：

```text
找 pno='p003' 的 pos 的 location
```

```xpath
//pos[@pno='p003']/location
```

### 10.3 XQuery 模板

```xquery
for $x in doc("file.xml")//movie
where $x/director = "Yimou Zhang"
return $x/@title
```

背住三个词：

```text
for：遍历
where：筛选
return：输出
```
