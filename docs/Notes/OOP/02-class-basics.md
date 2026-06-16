---
title: OOP 02 类与对象：封装、构造析构、拷贝
tags:
  - learning
  - courses
  - oop
  - cpp
  - finals
updated: 2026-06-16
publish: true
blog_dest: Notes/OOP/02-class-basics.md
---
# 2. 类与对象（封装 / 构造析构 / 深浅拷贝 / this）

> ⭐ 这一章是**全卷第一考点**。"看程序写结果"里出现最多的就是"构造和析构按什么顺序打印"。
> 把这一章吃透，及格线就稳了一半。

---

## 2.1 类和对象：图纸与房子

先建立最基本的直觉：

```text
类 (Class)   = 图纸。规定了"这种东西有哪些数据、能做哪些事"
对象 (Object) = 按图纸盖出来的房子。每盖一栋都有自己独立的数据

例：Rectangle 类规定"所有矩形都有宽和高，都能算面积"
    一个宽 5 高 10 的具体矩形，就是一个对象
```

```cpp
class Rectangle {        // 图纸
    int width, height;   // 数据（成员变量）
public:
    int area() { return width * height; }   // 行为（成员函数）
};

Rectangle r;             // r 是一个对象（实例 instance）
```

- **成员变量 / 属性**：类里的数据（width、height）
- **成员函数 / 方法**：类里的操作（area）
- **实例化 instance**：用类创建对象的过程

---

## 2.2 封装：把数据藏起来，只留接口

**封装 (Encapsulation)** = 把"数据"和"操作数据的逻辑"捆在一起，并对外隐藏内部细节。外面只能通过你开放的接口来访问。

C++ 用三个**访问修饰符**控制谁能访问：

```text
public      任何地方都能访问（对外开放的接口）
protected   类内部 + 派生类能访问（留给子类的）
private     只有类内部能访问（藏起来的秘密）
```

```cpp
class Stack {
private:                       // 藏起来：外面不能直接动 data 和 top
    int data[100];
    int top = 0;
public:                        // 开放接口
    void push(int x) { data[top++] = x; }
    int  pop()       { return data[--top]; }
};
```

**封装的好处：**

```text
① 安全：外面只能走接口，不能乱改内部数据
② 可维护：内部实现随便改，只要接口不变，外面代码不用动
③ 职责清晰
```

> ⚠️ **必考冷知识**：`struct` 和 `class` 在 C++ 里**本质完全一样**，都是类。
> **唯一区别**：默认访问权限不同。
> - `class` 默认 `private`
> - `struct` 默认 `public`

---

## 2.3 构造函数 Constructor：让对象"出身即合法"

### 为什么需要构造？

C 里 `malloc` 出来的内存是**未初始化的随机值**（脏数据）。如果不初始化就用，会读到垃圾，产生诡异 bug。**构造函数的任务就是：把这块原始内存按你的逻辑初始化，让对象一出生就合法可用。**

### 构造函数的三条规则（判断题高频）

```text
① 名字必须和类名完全相同
② 没有返回值（连 void 都不是！）
③ 支持重载（可以有多个不同参数的构造函数）
```

```cpp
class Player {
public:
    Player() { score = 0; cout << "Default Constructor\n"; }   // 默认构造（无参）
    Player(int s) { score = s; }                               // 带参构造
    int score;
};

Player p1;        // 调默认构造，score = 0
Player p2(100);   // 调带参构造，score = 100
```

### 默认构造函数的"消失"规则（⭐必考判断题）

```text
• 如果你一个构造函数都没写 → 编译器自动送你一个默认构造函数
• 但只要你写了任意一个构造函数（哪怕是带参的）→ 编译器就不再送了
```

```cpp
class A {
public:
    A(int x) {}    // 只定义了带参构造
};
A a;               // ❌ 错误！编译器不再送默认构造，A a; 无法编译
```

> 判断题原题：Default constructor must be defined, if parameterized constructor is defined and the object is to be created without arguments. → **T（对）**

如果你既想要带参构造，又想要默认构造，用 `= default` 让编译器把默认构造"加回来"：

```cpp
class Player {
public:
    Player() = default;                  // 提示编译器：给我生成默认构造
    Player(int s) : score(s) {}
    int score;
};
```

### 初始化列表（⭐高频，必须会写）

`Player(int s) : score(s) {}` 里冒号后面那部分叫**初始化列表**。它直接构造成员变量。

```cpp
Player(int s) : score(s) {}     // ✅ 初始化列表：直接用 s 构造 score
Player(int s) { score = s; }    // 函数体内赋值：先默认构造 score，再赋值（多一步）
```

两条必须记的理由：

```text
① 效率更高：初始化列表是"直接构造"，函数体赋值是"先构造再赋值"，多一步
② 有些成员只能用初始化列表初始化：
   - const 成员（常量，不能先建再赋值）
   - 引用成员（引用必须建时绑定）
```

```cpp
class C {
    const int x;     // const 成员
    int& r;          // 引用成员
public:
    C(int v, int& ref) : x(v), r(ref) {}   // 只能用初始化列表，函数体内赋值会报错
};
```

---

## 2.4 析构函数 Destructor：对象临终前的"清理工"

对象生命结束时**自动调用**，负责释放它占用的资源（堆内存、文件句柄等）。

### 析构函数的规则

```text
① 名字是 ~类名（前面加波浪号）
② 没有参数
③ 没有返回值
④ 不支持重载（一个类只能有一个析构函数）
```

```cpp
class Buffer {
public:
    int* data;
    Buffer(int size) { data = new int[size]; }   // 构造：申请内存
    ~Buffer() { delete[] data; }                 // 析构：归还内存
};
```

### 析构什么时候被触发？（⭐看程序写结果的核心）

```text
① 局部变量：离开作用域时（函数结束、或离开 { } 块）
② new 出来的对象：对它 delete 时
③ static / 全局对象：整个程序结束时
```

```cpp
cout << "----A----\n";
{
    Buffer buf(10);     // 进入块，构造
}                       // ← 离开 } 块，buf 在这里析构
cout << "----B----\n";
```

输出：

```text
----A----
（buf 析构发生在这里）
----B----
```

---

## 2.5 ⭐核心题型：构造析构顺序

这是**必考**的"看程序写结果"。先记住三类对象的时机规律：

```text
全局对象     最先构造（main 之前）、最后析构（程序结束）
static 局部  第一次执行到声明时才构造、程序结束才析构（只构造一次）
普通局部     执行到声明时构造、离开作用域立即析构
通用规律     "后构造的先析构"（像叠盘子，后放的先拿走）
```

### 经典原题（2013-2014 真题，⭐⭐必背）

```cpp
class Obj {
    char c;
public:
    Obj(char cc) { c = cc; cout << "Obj::Obj for " << c << endl; }
    ~Obj()       { cout << "Obj::~Obj for " << c << endl; }
};

void f() { static Obj b('b'); }   // static 局部对象
void g() { Obj c('c'); }          // 普通局部对象
Obj a('a');                       // 全局对象

int main() {
    cout << "inside main()" << endl;
    f();   // 第一次进 f，构造 b
    g();   // 构造 c，g 结束析构 c
    f();   // 第二次进 f，b 已存在，不再构造
    g();   // 又构造一个 c，g 结束析构 c
    cout << "leaving main()" << endl;
    return 0;
}
```

**慢动作逐行推导：**

```text
程序启动 → 全局对象 a 最先构造          → "Obj::Obj for a"
进入 main                              → "inside main()"
f() 第一次：static b 第一次构造          → "Obj::Obj for b"
g() 第一次：局部 c 构造                  → "Obj::Obj for c"
        g() 结束，c 离开作用域析构        → "Obj::~Obj for c"
f() 第二次：b 已经构造过了，啥也不发生   →（无输出）
g() 第二次：又一个局部 c 构造            → "Obj::Obj for c"
        g() 结束析构                     → "Obj::~Obj for c"
                                        → "leaving main()"
main 结束，开始析构存活的对象：
        static b 析构（后构造的先析构）   → "Obj::~Obj for b"
        全局 a 析构（最先构造，最后析构） → "Obj::~Obj for a"
```

**完整答案：**

```text
Obj::Obj for a
inside main()
Obj::Obj for b
Obj::Obj for c
Obj::~Obj for c
Obj::Obj for c
Obj::~Obj for c
leaving main()
Obj::~Obj for b
Obj::~Obj for a
```

**三个记忆钩子：**
- static 对象**只构造一次**（第二次进 f 没有输出）
- 全局对象**最先生、最后死**
- 同一批对象**后构造先析构**

---

## 2.6 new 和 delete：C++ 的动态内存

C 用 `malloc/free`（只管内存）。C++ 用 `new/delete`，它们在分配/释放内存的同时，**还会自动调用构造/析构函数**。

```cpp
Buffer* p1 = new Buffer(10);   // 申请内存 + 调用构造函数
delete p1;                     // 调用析构函数 + 归还内存

int* p2 = new int[4];          // 数组形式
delete[] p2;                   // ⚠️ 数组必须用 delete[]
```

两条铁律（判断题高频）：

```text
① new/delete 不能和 malloc/free 混用
② new[] 申请的数组，必须用 delete[] 释放
```

> ⚠️ 判断题原题：用 `delete[]` 释放 `new[]` 的数组，会**对每个元素都调用析构函数** → **T（对）**。
> 而"只对第一个元素调析构" → **F（错）**。
> 如果错用了 `delete`（没中括号）去删数组 → 未定义行为，可能只析构第一个、漏掉其余 → 内存泄漏。

---

## 2.7 ⭐深拷贝 vs 浅拷贝：double free 的根源

这是**必考重点**。当一个对象拷贝给另一个对象时，如果成员里有**指针**，问题就来了。

### 浅拷贝（Shallow Copy）—— 危险

逐个成员"按二进制原样复制"。如果成员是指针，只复制了**地址**，两个对象的指针指向**同一块内存**：

```text
浅拷贝后的内存：

   对象 m1            对象 m2
  ┌────────┐        ┌────────┐
  │ data ──┼───┐    │ data ──┼───┐
  └────────┘   │    └────────┘   │
               ▼                 ▼
            ┌──────────────────────┐
            │   同一块堆内存         │   ← 两个对象指向同一块！
            └──────────────────────┘

后果：m1 和 m2 析构时，各 delete 一次 → 同一块内存被释放两次
      → double free → 程序崩溃 💥
```

### 深拷贝（Deep Copy）—— 安全

不仅复制成员，还**为指针成员重新申请一块新内存**，把内容也复制过去：

```text
深拷贝后的内存：

   对象 m1            对象 m2
  ┌────────┐        ┌────────┐
  │ data ──┼───┐    │ data ──┼───┐
  └────────┘   │    └────────┘   │
               ▼                 ▼
        ┌───────────┐      ┌───────────┐
        │ 各自的内存 │      │ 各自的内存 │   ← 两块独立的内存
        └───────────┘      └───────────┘

各自析构各自的内存，互不干扰 ✅
```

---

## 2.8 拷贝构造函数：用一个对象造一个新对象

**用一个已存在的对象，去初始化一个新对象**时调用。函数签名固定：

```cpp
ClassName(const ClassName& other);   // 参数是"同类对象的常引用"
```

正确的深拷贝写法（以 Buffer 为例，必须会默写）：

```cpp
Buffer(const Buffer& other) : size(other.size) {
    data = new int[size];                  // ⚠️ 重新申请一块内存（深拷贝关键）
    for (int i = 0; i < size; i++)
        data[i] = other.data[i];           // 把内容逐个复制过去
}
```

### 拷贝构造的三个触发场景（⭐高频）

```cpp
ClassA obj2 = obj1;    // ① 用 obj1 初始化 obj2（注意：这是拷贝构造，不是赋值！）
ClassA obj2(obj1);     // ② 同上，另一种写法
func(obj1);            // ③ 以值传递方式向函数传对象（拷贝一份进去）
```

> ⚠️ 第①个最坑：`obj2 = obj1` 里有等号，但因为 obj2 **正在被创建**，所以调的是**拷贝构造**，不是拷贝赋值。区别看下一节。

> 判断题：Copy constructors are overloaded constructors. → **T（对）**（拷贝构造是构造函数的一种重载）

---

## 2.9 拷贝赋值运算符：把一个已有对象的值赋给另一个已有对象

注意和拷贝构造的区别：**两个对象都已经存在了**，现在把右边的值赋给左边。函数签名固定：

```cpp
ClassName& operator=(const ClassName& other);
```

正确写法（比拷贝构造多了"先释放旧资源"和"防自赋值"，必须会默写）：

```cpp
Buffer& operator=(const Buffer& other) {
    if (this == &other) return *this;   // ① 防止自赋值（a = a 时别把自己删了）
    delete[] data;                      // ② 先释放自己原有的旧资源
    size = other.size;
    data = new int[size];               // ③ 申请新内存 + 深拷贝
    for (int i = 0; i < size; i++)
        data[i] = other.data[i];
    return *this;                       // ④ 返回 *this，支持链式 a = b = c
}
```

**拷贝构造 vs 拷贝赋值 —— 一句话区分：**

```text
拷贝构造：  ClassA b = a;     ← b 是"新生的"，从无到有
拷贝赋值：  ClassA b;          ← b 已经存在
           b = a;            ← 这一行才是拷贝赋值（把 a 的值赋给已存在的 b）
```

> 这就是为什么拷贝赋值要先 `delete[] data` —— 因为 b 之前已经持有资源了，不先释放就泄漏。

---

## 2.10 this 指针：指向"调用这个函数的对象自己"

每个**非静态成员函数**内部，都隐藏着一个 `this` 指针，**指向当前正在调用该函数的那个对象**。

```cpp
Buffer(const Buffer& other) : size(other.size) {
    this->data = new int[size];              // this->data 就是当前对象的 data
    for (int i = 0; i < this->size; i++)
        this->data[i] = other.data[i];
}
```

```text
• 成员函数里访问成员变量，编译器都会偷偷加上 this->（你不写也有）
• this 其实是成员函数的"隐藏第一个参数"（学过 Python 的话，类似 self）
• this 的类型是 ClassName* const（指针本身不能改，但能改它指向的对象）
```

`this == &other` 那行就是用 this 来判断"是不是在自己给自己赋值"。

---

## 2.11 本章自测

```text
1. struct 和 class 唯一的区别？               → 默认访问权限（struct public, class private）
2. 构造函数有返回值吗？                       → 没有，连 void 都不是
3. 定义了带参构造后还能 A a; 吗？             → 不能，除非写 A() = default
4. const 成员只能怎么初始化？                 → 初始化列表
5. 浅拷贝为什么会崩溃？                        → 两对象指向同一内存，析构时 double free
6. ClassA b = a; 调的是拷贝构造还是赋值？     → 拷贝构造（b 正在被创建）
7. 拷贝赋值为什么要先 delete[]？              → b 已存在持有旧资源，不释放会泄漏
8. 全局、static、局部对象谁先构造谁先析构？   → 全局最先构造最后析构；后构造的先析构
```

---

上一章 → [C++ 基础](01-cpp-basics.md) ｜ 下一章 → [继承与多态](03-inheritance-polymorphism.md)
