---
title: OOP 03 继承与多态
tags:
  - learning
  - courses
  - oop
  - cpp
  - finals
updated: 2026-06-16
publish: true
blog_dest: Notes/OOP/03-inheritance-polymorphism.md
---
# 3. 继承与多态（运算符重载 / 虚函数 / vtable / 抽象类 / 类型转换）

> ⭐ 全卷**第二大考点**。核心就一句话：**虚函数到底调谁的版本？** 把这个搞清楚，半张卷子的"看程序写结果"就拿下了。

---

## 3.1 继承：派生类"白嫖"基类的成员

**继承 (Inheritance)** 让一个类（派生类 / 子类）从另一个类（基类 / 父类）继承属性和行为，实现代码复用。

```cpp
// 基类（父类）
class Person {
public:
    string name;
    Person(string n) : name(n) {}
    void speak() { cout << "I'm " << name << endl; }
};

// 派生类（子类）：用 : public 表示继承
class Student : public Person {
public:
    int grade;
    Student(string n, int g) : Person(n), grade(g) {}   // ⚠️ 用初始化列表调基类构造
};
```

```text
Student 自动拥有了 Person 的 name 和 speak()，不用重写
派生类构造时，必须在初始化列表里调用基类构造： : Person(n)
```

### 三种继承方式：会改变成员的可见性（⭐考点）

`class Student : public Person` 里的 `public` 是继承方式，它决定**基类成员到了派生类里访问权限怎么变**：

```text
public 继承：   基类成员权限不变（public 还是 public，protected 还是 protected）
protected 继承：基类的 public 成员 → 在派生类里降级为 protected
private 继承：  基类的 public 和 protected 成员 → 在派生类里降级为 private
```

口诀：**取"继承方式"和"原权限"里更严格的那个**。private 是私有的，别人本来就访问不到，无论怎么继承都还是访问不到。

> ⚠️ 不写继承方式时：`class` 默认 **private** 继承，`struct` 默认 **public** 继承。
> 判断题：派生类对象**无论何种继承方式**都能访问基类 public 成员 → **F（错）**，private/protected 继承后外部就访问不到了。

---

## 3.2 ⭐继承体系的构造与析构顺序

又是"看程序写结果"的高频题。规律：

```text
构造顺序：先基类 → 后派生类      （盖房子先打地基）
析构顺序：先派生类 → 后基类      （拆房子先拆楼上，和构造相反）
```

如果基类里还有"成员对象"，完整顺序是：

```text
构造：基类 → 派生类的成员对象 → 派生类自己
析构：派生类自己 → 派生类的成员对象 → 基类       （完全倒过来）
```

```cpp
class Base {
public:
    Base()  { cout << "Base Constructor\n"; }
    virtual ~Base() { cout << "Base Deconstructor\n"; }
};
class Derived : public Base {
public:
    Derived() { cout << "Derived Constructor\n"; }
    ~Derived(){ cout << "Derived Deconstructor\n"; }
};

int main() { Derived d; }
```

**输出：**

```text
Base Constructor        ← 先基类
Derived Constructor     ← 后派生类
Derived Deconstructor   ← 析构倒过来：先派生类
Base Deconstructor      ← 后基类
```

---

## 3.3 多重继承与菱形继承问题

C++ 允许一个类继承**多个**基类。但这会带来"菱形继承"麻烦：

```cpp
class A { public: int x; };
class B : public A {};
class C : public A {};
class D : public B, public C {};   // D 同时继承 B 和 C，而 B、C 都继承 A
```

```text
菱形结构：

        A          ← D 里有几份 A 的 x？
       / \
      B   C        ← B 继承一份 A，C 也继承一份 A
       \ /
        D          ← D 里就有了两份 x！（从 B 来的 + 从 C 来的）

D d;
d.x;    // ❌ 二义性：到底是 B::x 还是 C::x？编译器懵了
```

**解决办法：虚继承**。在继承方式前加 `virtual`，保证基类 A 在 D 里**只存在一份共享实例**：

```cpp
class B : virtual public A {};   // 虚继承
class C : virtual public A {};
class D : public B, public C {};
// 现在 D 里只有一份 A，d.x 不再二义
```

---

## 3.4 多态是什么？分两类

**多态 (Polymorphism)** = 多种形态 = 同一个函数名，在不同对象上有不同的行为。C++ 分两类：

```text
编译时多态（静态，编译期就定好调谁）：
    • 函数重载 overload
    • 运算符重载
    • 模板

运行时多态（动态，运行时才决定调谁）：
    • 虚函数 virtual   ← 这才是 OOP 的灵魂，重点
```

> 单选题：static polymorphism（静态多态）的冲突在 **compile time（编译期）** 解决。

---

## 3.5 运算符重载：让对象能用 + - == << 等

**为自定义类型重新定义运算符的功能**，让对象能像 int 一样直观地运算。

三条基本约束（判断题/单选高频）：

```text
① 不能创造新运算符（不能发明一个 ** 运算符）
② 不能改变运算符的优先级和结合性
③ 不能改变操作数的个数
```

**不可重载的运算符**（必须背，单选直接考）：

```text
.     成员访问
::    作用域解析
?:    三目运算符
sizeof
.*    成员指针访问
```

记忆口诀：**"点、双冒号、问号冒号、sizeof"不能重载。**

### 方式一：成员函数重载

运算符作为成员函数时，**左操作数必须是该类对象**（由 this 隐式当左操作数）：

```cpp
class Vector2D {
public:
    double x, y;
    Vector2D(double x = 0, double y = 0) : x(x), y(y) {}
    Vector2D operator+(const Vector2D& other) const {     // a + b → a.operator+(b)
        return Vector2D(this->x + other.x, this->y + other.y);
    }
};
Vector2D a(1,2), b(3,4);
Vector2D c = a + b;   // c = (4, 6)
```

### ⭐ operator++ 前置与后置（必考）

前置 `++a` 和后置 `a++` 怎么区分？C++ 规定：**后置版本多一个 `int` 占位参数**。

```cpp
class Counter {
    int value = 0;
public:
    Counter& operator++()     { value++; return *this; }   // 前置：先加，返回自己的引用
    Counter  operator++(int)  { Counter t = *this; value++; return t; }  // 后置：返回加之前的旧值
    //              ↑ int 仅作占位，区分前置后置，没实际用途
};
```

```text
前置 ++a：先自增，返回自身引用（返回 Counter&）
后置 a++：先存旧值，再自增，返回旧值（返回 Counter，是个临时对象）
        所以后置效率略低（多拷贝一份旧值）
```

### 方式二：友元函数重载（重载 << 输出）

当**左操作数不是本类对象**时（如 `cout << obj`，左边是 cout），只能用友元函数。

先理解**友元 friend**：定义在类外、但有权访问该类 private 成员的函数。

```cpp
class Complex {
    double real, imag;
public:
    Complex(double r, double i) : real(r), imag(i) {}
    // 重载 <<，让 cout << c 能打印复数
    friend ostream& operator<<(ostream& os, const Complex& c) {
        os << c.real << " + " << c.imag << "i";
        return os;   // ⚠️ 返回 os 引用，才能支持链式 cout << a << b
    }
};
Complex c(3, 4);
cout << c << endl;   // 3 + 4i
```

**友元的四条特性（判断题高频）：**

```text
① 单向：A 是 B 的友元，不代表 B 是 A 的友元
② 不可传递：A 是 B 友元、B 是 C 友元，推不出 A 是 C 友元
③ 不可继承：基类的友元不会自动成为派生类的友元
④ 破坏封装：只在特定场景（如重载 <<）才用
```

> ⚠️ 单选原题（重复出现）：friend 函数**不能**用来重载的运算符是 `[]`（答案 D）。
> （因为 `=`、`[]`、`()`、`->` 这几个**必须**是成员函数，不能用友元/全局函数。）

---

## 3.6 ⭐⭐虚函数与动态绑定（全章最重要）

### 先看"不加 virtual"会发生什么 —— 静态绑定

```cpp
class Base    { public: void show() { cout << "Base\n"; } };
class Derived : public Base { public: void show() { cout << "Derived\n"; } };

Base* b = new Derived();   // 指针类型是 Base*，但实际指向 Derived
b->show();                 // 输出 "Base" ❗
```

**为什么输出 Base 而不是 Derived？**

```text
没加 virtual 时，编译器看 b 的"声明类型"是 Base*，
就在编译期直接定死调用 Base::show()。
这种"按声明类型决定调谁"的方式叫【静态绑定】。
```

### 加上 virtual —— 动态绑定

```cpp
class Base {
public:
    virtual void show() { cout << "Base\n"; }   // 加 virtual
    virtual ~Base() {}                          // 虚析构（见下）
};
class Derived : public Base {
public:
    void show() override { cout << "Derived\n"; }   // 重写
};

Base* b = new Derived();
b->show();    // 输出 "Derived" ✅
```

```text
加了 virtual 后，程序在【运行时】看 b 实际指向的对象是 Derived，
就调用 Derived::show()。
这种"按对象实际类型决定调谁"的方式叫【动态绑定】，这就是运行时多态。
```

### 触发动态绑定的三个条件（⭐必考，判断题/陷阱题）

```text
① 必须用【指针或引用】调用，直接用对象本身调用不触发动态绑定
② 基类函数必须声明为 virtual
③ 默认参数是【静态绑定】的（陷阱！默认值按声明类型取，函数体按实际类型）
④ 构造函数不能是虚函数
```

补充易错：

```text
• 虚函数被继承后【依旧是虚函数】，派生类里不用再写 virtual
• 在构造函数/析构函数里调用虚函数 → 退化成【静态绑定】到当前类
  （因为构造时派生类部分还没建好，析构时已经拆了）
```

### ⭐虚析构函数：基类析构必须加 virtual

```cpp
class Base    { public: ~Base() { cout << "~Base\n"; } };           // 没加 virtual
class Derived : public Base { public: ~Derived(){ cout << "~Derived\n"; } };

Base* b = new Derived();
delete b;    // 只输出 "~Base"！Derived 的析构没被调用 → 内存泄漏 💥
```

```text
基类析构不加 virtual + 通过基类指针 delete
→ 只调用基类析构，派生类的析构被跳过 → 派生类资源泄漏

规则：只要一个类【可能被继承且通过基类指针销毁】，基类析构就必须加 virtual
```

加上 `virtual ~Base()` 后，`delete b` 会先调 `~Derived` 再调 `~Base`，正确。

---

## 3.7 虚函数的实现机制：vtable 和 vptr

考试可能问"虚函数怎么实现的"。一张图说清：

```text
编译器给每个【有虚函数的类】建一张【虚函数表 vtable】，存这个类所有虚函数的地址。
每个【对象】内部藏一个指针【vptr】，指向它所属类的 vtable。

   Derived 对象
  ┌──────────────┐         Derived 的 vtable
  │ vptr ────────┼──────► ┌────────────────────┐
  ├──────────────┤        │ &Derived::show     │
  │ 其他成员...   │        │ &Derived::~Derived │
  └──────────────┘        └────────────────────┘

运行时调用 b->show() 的流程：
  ① 通过 b 找到对象
  ② 通过对象里的 vptr 找到 vtable
  ③ 在 vtable 里查到 show 的真实地址，跳过去执行
```

这也解释了为什么"构造函数不能是虚函数"：vptr 是在构造过程中才被设置的，构造还没完成时 vtable 还不可用。

---

## 3.8 抽象类与纯虚函数：定义"接口"

**纯虚函数**：只声明不实现，在虚函数声明末尾加 `= 0`：

```cpp
virtual void area() = 0;   // 纯虚函数，没有函数体
```

**抽象类**：只要一个类**含有至少一个纯虚函数**，它就是抽象类。

```cpp
class Shape {
public:
    virtual double area() = 0;     // 纯虚函数 → Shape 是抽象类
    virtual ~Shape() {}
};
class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}
    double area() override { return 3.14159 * r * r; }   // 必须实现，否则 Circle 也是抽象类
};
```

抽象类的规则：

```text
• 不能创建抽象类的对象（Shape s;  ❌ 错）
• 但可以创建抽象类的【指针或引用】，用于动态绑定（Shape* p = new Circle(2); ✅）
• 抽象类里的【非纯虚函数】会被所有派生类继承
• 派生类如果没实现全部纯虚函数，它自己也还是抽象类
```

核心价值：**强制子类实现某些行为**，定义一套统一接口。

> 单选原题：抽象类 A 有 4 个虚函数，B 只实现 2 个（B 仍是抽象类），C 继承 B 并实现剩下 2 个 → 程序**正常运行**（D）。

---

## 3.9 四种类型转换（⭐dynamic_cast 必考）

C++ 用四个转换符替代 C 的暴力 `(type)value`：

```text
static_cast       最常用。编译期认可的转换（基本类型互转、向上转换）
dynamic_cast      运行时检查的安全【向下转换】（基类指针→派生类指针）
const_cast        唯一能【去掉 const】的转换
reinterpret_cast  最危险。仅重新解释底层比特位
```

### static_cast vs dynamic_cast（最常考）

```text
向上转换（派生类指针 → 基类指针）：安全，两个都能做
向下转换（基类指针 → 派生类指针）：
    static_cast：不做运行期检查，强行转，可能转出错误的东西（不安全）
    dynamic_cast：运行期检查对象的【真实类型】
        - 如果真的是那个派生类 → 转换成功
        - 如果不是 → 指针返回 nullptr，引用抛 bad_cast 异常
        - 前提：基类必须至少有一个虚函数（否则编译错）
```

```cpp
Base* b = new Derived();
Derived* d = dynamic_cast<Derived*>(b);   // b 真的指向 Derived → 成功
if (d) { /* 安全使用 d */ }
```

### ⭐经典原题（2013-2014，必背三种结果）

```cpp
class A { public: virtual ~A() {} };
class B : public A {};
int main() {
    A a1;            // a1 是真正的 A
    B b;
    A& a2 = b;       // a2 实际指向 B 对象
    B* bp;
    bp = dynamic_cast<B*>(&a1);   // a1 是真 A，向下转 B 失败 → nullptr
        // 输出 "Fail!"
    bp = dynamic_cast<B*>(&a2);   // a2 实际是 B，成功
        // 输出 "OK!"
    try {
        B& b1 = dynamic_cast<B&>(a1);  // 引用版失败 → 抛 bad_cast 异常
    } catch(...) { /* 输出 "Fail!" */ }
}
```

**核心记忆：dynamic_cast 失败时，指针返回 nullptr，引用抛异常。**

---

## 3.10 组合优于继承（概念题）

不是所有"复用"都该用继承。**组合 (Composition)** = 把一个对象作为另一个对象的成员变量，表达"有一个 (has-a)"关系。

```cpp
class Engine { /*...*/ };
class Car {
    Engine engine;   // 组合：汽车"有一个"引擎
};
```

```text
继承的问题：
  • 灵活性差：继承关系编译期就定死，运行时改不了
  • 脆弱基类：基类一改，所有子类可能出 bug
  • 类爆炸：用继承组合多种特性，类的数量指数级增长

建议：优先用组合复用代码，而不是继承
```

---

## 3.11 本章自测

```text
1. public 继承下，基类 protected 成员到派生类里是什么权限？  → protected（不变）
2. 继承体系构造和析构顺序？                                  → 构造先基类，析构先派生类
3. 菱形继承怎么解决？                                        → 虚继承 virtual
4. Base* b = new Derived(); b->show() 输出谁的？             → 没 virtual 输出 Base；有 virtual 输出 Derived
5. 触发动态绑定的必要条件？                                  → 指针/引用调用 + virtual
6. 为什么基类析构要加 virtual？                              → 否则 delete 基类指针时派生类不析构 → 泄漏
7. 哪些运算符不能重载？                                      → . :: ?: sizeof
8. dynamic_cast 失败时指针和引用分别怎样？                   → 指针返回 nullptr，引用抛异常
9. 抽象类能创建对象吗？能创建指针吗？                        → 不能建对象，能建指针/引用
```

---

上一章 → [类与对象](02-class-basics.md) ｜ 下一章 → [移动语义与异常](04-move-exception.md)
