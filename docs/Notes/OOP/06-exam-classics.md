---
title: OOP 06 必背经典题 + 判断题答案串 + 编程题骨架
tags:
  - learning
  - courses
  - oop
  - cpp
  - finals
  - exam-classics
updated: 2026-06-16
publish: true
blog_dest: Notes/OOP/06-exam-classics.md
---
# 6. 考前必背：13 道经典题 + 判断题答案串 + 编程题骨架

> 这是**考前一晚最该看的一页**。前面 5 章是讲原理，这一页是把原理变成"看到题就能写出答案"。
> 用法：每道题先把代码遮住答案自己推一遍，推不出来再回去看对应章节。

---

## Part A. 看程序写结果 —— 13 道必背经典

### ⭐题 1：全局 / static / 局部对象的构造析构顺序

```cpp
class Obj {
    char c;
public:
    Obj(char cc) { c = cc; cout << "Obj for " << c << endl; }
    ~Obj()       { cout << "~Obj for " << c << endl; }
};
void f() { static Obj b('b'); }
void g() { Obj c('c'); }
Obj a('a');
int main() {
    cout << "inside main()" << endl;
    f(); g(); f(); g();
    cout << "leaving main()" << endl;
}
```

<details><summary>答案</summary>

```text
Obj for a          ← 全局对象最先构造
inside main()
Obj for b          ← static 第一次进 f() 才构造
Obj for c          ← g() 局部对象
~Obj for c         ← g() 结束析构
Obj for c          ← 第二次 g()
~Obj for c
leaving main()
~Obj for b         ← static 程序结束才析构（后构造先析构）
~Obj for a         ← 全局对象最后析构
```
**钩子**：static 只构造一次；全局最先生最后死；后构造先析构。详见 [类与对象](02-class-basics.md) 2.5。
</details>

---

### ⭐题 2：构造/析构顺序 + 析构里读成员

```cpp
class A {
    int i;
public:
    A() : i(0) {}
    ~A() { cout << get(); }
    void set(int x) { this->i = x; }
    int  get() { return i; }
};
int main() {
    A* p = new A[2];   // 构造 2 个 A，i 都是 0
    delete[] p;        // 析构 2 个，各打印 get() = 0
}
```

<details><summary>答案</summary>

```text
00
```
`delete[]` 对数组每个元素都调析构，2 个 A 各打印一个 0。
</details>

---

### ⭐题 3：构造/析构里调用虚函数（退化成静态绑定）

```cpp
class Base {
public:
    Base()  { cout << "Base::Ctor\n"; }
    virtual ~Base() { cout << "Base::Dtor\n"; }
    virtual void foo() { cout << "Base::foo\n"; }
};
class Derived : public Base {
public:
    Derived() { cout << "Derived::Ctor\n"; foo(); }   // 构造里调虚函数
    ~Derived(){ cout << "Derived::Dtor\n"; }
    void foo() override { cout << "Derived::foo\n"; }
};
int main() { Base* p = new Derived(); delete p; }
```

<details><summary>答案</summary>

```text
Base::Ctor
Derived::Ctor
Derived::foo      ← 构造体内调 foo，此时对象已是 Derived，输出 Derived 版
Derived::Dtor     ← 因为 ~Base 是 virtual，delete 基类指针正确调到派生类析构
Base::Dtor
```
**钩子**：构造函数体执行时，对象已经"是"当前类了，所以 `foo()` 调 Derived 版。但如果在 **Base 的构造函数里**调 `foo()`，那时 Derived 还没建好，会调 Base 版。详见 [继承与多态](03-inheritance-polymorphism.md) 3.6。
</details>

---

### ⭐题 4：operator++ 前置/后置 + operator int 计数循环

```cpp
class counter {
    int value;
public:
    counter() : value(0) {}
    counter& operator++()    { if (5 == value) value = 0; else value++; return *this; }  // 前置
    int      operator++(int) { int t = value; if (5 == value) value = 0; else value++; return t; }  // 后置
    operator int() const { return value; }   // 类型转换：counter 能当 int 用
};
int main() {
    counter a;
    while (++a) cout << "*\n";   // 前置
    cout << 0 + a << endl;
    while (a++) cout << "*\n";   // 后置
    cout << 0 + a << endl;
}
```

<details><summary>答案</summary>

```text
*
*
*
*
*
0
1
```
**推导**：
- `while(++a)`：前置先加再判断。value 从 0→1→2→3→4→5 各打印一个 `*`（5 个），再 ++ 时 value 由 5 变 0，循环退出。然后 `0+a` = 0。
- `while(a++)`：后置返回旧值。当前 value=0，返回旧值 0 → 直接退出（0 个 `*`），但 value 已变成 1。然后 `0+a` = 1。

**钩子**：前置返回 `*this`（新值），后置返回旧值。`operator int()` 让对象能被当 int 判断真假。详见 [继承与多态](03-inheritance-polymorphism.md) 3.5。
</details>

---

### ⭐题 5：成员对象的 operator= 按声明顺序合成调用

```cpp
class A { public: A& operator=(const A&) { cout << "A::operator=\n"; return *this; } };
class B { public: B& operator=(const B&) { cout << "B::operator=\n"; return *this; } };
class C { A a; B b; int c; };   // 成员声明顺序：a 在前，b 在后
int main() { C m, n; m = n; }   // 编译器合成 C::operator=
```

<details><summary>答案</summary>

```text
A::operator=
B::operator=
```
编译器合成的 `C::operator=` 按**成员声明顺序**逐个调用成员的赋值运算符。如果把声明改成 `B b; A a;`，输出就先 B 后 A。
</details>

---

### ⭐题 6：异常 + 栈展开析构计数

```cpp
class A {
public:
    A()  { cout << "A()\n"; }
    ~A() { cout << "~A()\n"; }
};
void foo(A a) {           // 按值传参 → 拷贝 1 个
    A arr[5];             // 栈上 5 个
    A* p = new A[3];      // 堆上 3 个
    throw p;
}
int main() {
    try { A a; foo(a); }
    catch (A* p) { delete[] p; cout << "catched\n"; }
}
```

<details><summary>答案：~A() 共 10 次</summary>

```text
栈展开析构：foo 里 arr[5] = 5 次 + 形参 a = 1 次
delete[] p：堆上 3 个 = 3 次
main 里 a：1 次
合计 = 5 + 1 + 3 + 1 = 10 次
```
**钩子**：堆对象不随栈展开自动析构，靠 `delete[]`。详见 [移动语义与异常](04-move-exception.md) 4.4。
</details>

---

### ⭐题 7：throw; 重抛 + 跳过后续代码

```cpp
void f3(){ double a=0; try{ throw a; } catch(double){ cout<<"OK3! "; throw; } cout<<"end3 "; }
void f2(){ try{ f3(); } catch(int){ cout<<"Ok2! "; } cout<<"end2 "; }
void f1(){ try{ f2(); } catch(char){ cout<<"OK1!"; } cout<<"end1 "; }
int main(){ try{ f1(); } catch(double){ cout<<"OK0! "; } cout<<"end0 "; }
```

<details><summary>答案</summary>

```text
OK3! OK0! end0
```
f3 抛 double 被自己接住打印 `OK3! `，`throw;` 重抛 → 后面所有 `endN` 被跳过，catch(int)/catch(char) 不匹配，一路传到 main 的 catch(double) 打印 `OK0! `，处理完正常打印 `end0`。
</details>

---

### ⭐题 8：dynamic_cast 三种结果

```cpp
class A { public: virtual ~A() {} };
class B : public A {};
int main() {
    A a1;  B b;  A& a2 = b;  B* bp;
    bp = dynamic_cast<B*>(&a1);   // a1 是真 A → 失败 → nullptr
    cout << (bp ? "OK1 " : "Fail1 ");
    bp = dynamic_cast<B*>(&a2);   // a2 实际是 B → 成功
    cout << (bp ? "OK2 " : "Fail2 ");
    try { B& b1 = dynamic_cast<B&>(a1); cout << "OK3"; }  // 引用失败 → 抛异常
    catch(...) { cout << "Fail3"; }
}
```

<details><summary>答案</summary>

```text
Fail1 OK2 Fail3
```
**钩子**：dynamic_cast 失败时，**指针返回 nullptr，引用抛 bad_cast 异常**。详见 [继承与多态](03-inheritance-polymorphism.md) 3.9。
</details>

---

### ⭐题 9：const 对象/指针的重载分派

```cpp
class A {
public:
    void f(int a, int b = 10)       { cout << a + b; }   // 非 const 版
    void f(int a, int b = 10) const { cout << a - b; }   // const 版
};
int main() {
    A a;
    const A* p = &a;
    p->f(25);
}
```

<details><summary>答案</summary>

```text
15
```
`p` 是 `const A*`，只能调 const 版本，25 - 10 = 15。详见 [C++ 基础](01-cpp-basics.md) 1.6。
</details>

---

### ⭐题 10：签名不同 = 隐藏而非覆盖（虚分派失效）

```cpp
class Base {
    int x;
public:
    Base(int x = 0) : x(x) {}
    virtual void display() const { cout << x << "\n"; }   // 注意有 const
};
class Derived : public Base {
    int y;
public:
    Derived(int y) : y(y) {}
    void display() { cout << y << "," << "\n"; }   // ⚠️ 漏写 const → 签名不同
};
int main() {
    Derived d(2);
    Base* p = &d;
    p->display();
}
```

<details><summary>答案</summary>

```text
0
```
Derived 的 `display()` 漏写 `const`，签名和基类 `display() const` 不同 → **没有覆盖，只是隐藏**。所以通过 `Base*` 调用走的是 `Base::display() const`，输出 Base 的 x（默认 0）。
**钩子**：重写虚函数签名必须**完全一致（含 const）**，否则虚分派失效。加 `override` 能让编译器报错提醒你。
</details>

---

### ⭐题 11：模板与全特化分派

```cpp
template <typename T>
class FF {
    T a1, a2, a3;
public:
    FF(T b1, T b2, T b3) : a1(b1), a2(b2), a3(b3) {}
    T Sum() const { return a1 + a2 + a3; }
};
int main() {
    FF<int> x(2, 3, 4), y(-2, -3, -4);
    cout << x.Sum() << "\t" << y.Sum();
}
```

<details><summary>答案</summary>

```text
9	-9
```
模板实例化为 `FF<int>`，Sum 就是三个数相加：2+3+4=9，-2-3-4=-9。详见 [模板与 STL](05-template-stl.md) 5.2。
</details>

---

### ⭐题 12：引用返回的副作用

```cpp
int& f(int& i) { i += 10; return i; }   // 返回引用 = 返回本体
int main() {
    int k = 0;
    int& m = f(k);     // f 让 k=10，返回 k 的引用，m 是 k 的别名
    cout << k << "#";
    f(m)++;            // f(m) 让 k=20 并返回 k 的引用，再 ++ → k=21
    cout << k << endl;
}
```

<details><summary>答案</summary>

```text
10#21
```
**钩子**：函数返回引用 = 返回"本体"，可以继续对它操作并影响原变量。`f(m)++` 先让 k 变 20，再自增到 21。详见 [C++ 基础](01-cpp-basics.md) 1.3。
</details>

---

### ⭐题 13：作用域遮蔽

```cpp
int main() {
    int i = 1;  double x = 1.111;
    cout << i << " " << x << endl;
    {
        int x = 2;  double i = 2.222;   // 内层重新定义同名变量，遮蔽外层
        cout << i << " " << x << endl;
    }
}
```

<details><summary>答案</summary>

```text
1 1.111
2.222 2
```
内层块里 `i` 和 `x` 被重新定义，类型和值都换了（i 现在是 double 2.222，x 是 int 2），遮蔽外层同名变量。
</details>

---

## Part B. 判断题答案串（背下来直接得分）

> 这些是题库 joja4f12 和期中卷的原题答案。**按组背诵**，考试遇到原题直接秒选。

### 第 1 组（构造/析构/重载/拷贝）答案：`T F F T F T F F`

```text
T  定义了带参构造、又想无参建对象时，必须定义默认构造（编译器不再合成）
F  析构可以在构造之前被调用 —— 错
F  overload 重载和 override 重写本质相同 —— 错（是两回事）
T  overload 和 override 本质不同 —— 对
F  "拷贝构造传对象" 和 "按值传递" 相同 —— 错（措辞陷阱）
T  拷贝构造是重载的构造函数 —— 对
F  一个类内含多个类对象就能称为那些类的基类 —— 错（混淆组合与继承）
F  基类加新成员后子类必须也改 —— 错
```

### 第 2 组（delete[]/继承/运算符）答案：`F T F F F T`

```text
F  delete[] 只调数组第一个元素的析构 —— 错
T  delete[] 自动对每个元素调析构 —— 对
F  一个类私有继承基类后，另一个类就不能公有继承该基类 —— 错
F  层次继承中各派生类只能访问基类少数成员 —— 错
F  所有运算符都能用成员函数重载 —— 错（. :: ?: sizeof 不能）
T  同一程序里函数可有 const 和非 const 两个版本 —— 对
```

### 第 3 组（访问控制/异常/引用）答案：`F F T T F F`

```text
F  派生类的私有函数能被父类访问 —— 错
F  派生类对象无论何种继承方式都能访问基类 public 成员 —— 错（private/protected 继承后外部访问不到）
T  可以有 try 块无 catch 块，反之不行 —— 题库口径 T
T  基类和派生类都能捕获异常时，派生类 catch 应写在基类 catch 之前 —— 对
F  传引用和传值不能在同一函数参数表同时出现 —— 错
F  对象按引用传入就必须按引用返回 —— 错
```

### 期中卷判断题答案串：`F F F T F  T T T`

### 单选高频陷阱（直接记答案）

```text
• friend 函数【不能】重载的运算符 → [] （= [] () -> 必须是成员函数）
• static polymorphism（静态多态）在 → compile time（编译期）解决
• this 指针的类型 → ClassName * const this
• 纯虚函数在 → 派生类中实现
• 哪个函数编译器不会自动生成 → inline 函数（构造/析构/拷贝构造都会自动生成）
• 纯虚函数正确写法 → virtual void foo() = 0;
• 可以是虚函数的 → 析构函数（构造函数/静态成员函数/友元都不行）
• 赋值方向：派生类对象能赋给基类对象（切片），反过来不行；
           基类指针不能直接赋给派生类指针
```

---

## Part C. 编程题骨架（人工批阅，写全这些就有分）

> 编程题无在线评测，人工批阅，可以用 Markdown 写。**先把下面 5 条通用得分点写对，再填业务逻辑。**

通用得分点（每道编程题都先做到）：

```text
① 基类析构加 virtual         virtual ~Base() {}
② 管堆内存写"三件套"          拷贝构造 + 拷贝赋值 + 析构（Rule of Three）
③ 接口用纯虚函数              virtual void area() = 0;
④ 派生类初始化列表调基类构造  Derived(...) : Base(...) {}
⑤ 重写虚函数签名完全一致      void foo() override
```

### 骨架 1：带深拷贝的类（MyString 类型，最经典）

```cpp
class MyString {
    char* data;
    int   len;
public:
    MyString(const char* s = "") {                 // 构造
        len = strlen(s);
        data = new char[len + 1];
        strcpy(data, s);
    }
    MyString(const MyString& o) : len(o.len) {      // 拷贝构造（深拷贝）
        data = new char[len + 1];
        strcpy(data, o.data);
    }
    MyString& operator=(const MyString& o) {        // 拷贝赋值
        if (this == &o) return *this;               //   防自赋值
        delete[] data;                              //   释放旧资源
        len = o.len;
        data = new char[len + 1];
        strcpy(data, o.data);
        return *this;
    }
    ~MyString() { delete[] data; }                  // 析构

    int size() const { return len; }
    char& operator[](int i) { return data[i]; }     // 下标访问
    bool operator==(const MyString& o) const { return strcmp(data, o.data) == 0; }
    friend ostream& operator<<(ostream& os, const MyString& s) {  // 输出
        os << s.data; return os;
    }
};
```

考点：**深拷贝 + Rule of Three + 运算符重载（[] == <<）**。

### 骨架 2：继承 + 虚函数 + 抽象接口（Shape 类型）

```cpp
class Shape {                                  // 抽象基类
public:
    virtual double area() const = 0;           // 纯虚函数：接口
    virtual void print() const { cout << "area = " << area() << "\n"; }
    virtual ~Shape() {}                        // 虚析构
};
class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}                 // 派生类构造
    double area() const override { return 3.14159 * r * r; }  // 实现接口
};
class Rectangle : public Shape {
    double w, h;
public:
    Rectangle(double w, double h) : w(w), h(h) {}
    double area() const override { return w * h; }
};

int main() {
    vector<Shape*> shapes;                     // 用基类指针存不同派生类
    shapes.push_back(new Circle(2));
    shapes.push_back(new Rectangle(3, 4));
    for (Shape* s : shapes) s->print();        // 多态：各自调自己的 area()
    for (Shape* s : shapes) delete s;          // 虚析构保证正确释放
}
```

考点：**抽象类 + 纯虚函数 + 动态绑定 + 基类指针容器**。

### 骨架 3：类模板（带异常的定长数组）

```cpp
template <typename T, int Size>
class Array {
    T arr[Size];
public:
    T& operator[](int i) {
        if (i < 0 || i >= Size)
            throw out_of_range("index out of range");   // 越界抛异常
        return arr[i];
    }
    int size() const { return Size; }
};

Array<int, 5> a;
a[0] = 10;
```

考点：**类模板 + 非类型模板参数 + 运算符重载 + 异常**。

### 设计模式骨架（2023 新趋势，了解结构即可）

近年大题偏设计模式。它们的**共同骨架**都是"抽象基类定义接口 + 多个派生类各自实现 + 虚析构"，记住这个套路就能套：

```cpp
// 以 Observer（观察者）为例
class Observer {                                       // 抽象观察者
public:
    virtual void update(int data) = 0;
    virtual ~Observer() {}
};
class ConcreteObserver : public Observer {
public:
    void update(int data) override { cout << "got " << data << "\n"; }
};
class Subject {                                        // 被观察者
    vector<Observer*> observers;
public:
    void attach(Observer* o) { observers.push_back(o); }
    void notify(int data) {                            // 一对多通知
        for (Observer* o : observers) o->update(data);
    }
};
```

```text
常考的设计模式（结构都是"抽象接口 + 派生实现"）：
  Builder    建造者：抽象 Builder + 具体 Builder + Director 组装
  Observer   观察者：Subject 维护 observer 列表，notify 时挨个 update
  Command    命令：Command 基类 + 具体命令 + Receiver 执行 + Invoker 调用
  State      状态机：State 基类 + 各状态子类，返回下一个状态
  Interpreter 解释器：表达式基类 + And/Or/Not/常量/变量，递归 Evaluate
```

---

## 考前最后检查清单

```text
□ 题 1（构造析构顺序）能默写输出
□ 题 3、题 10（虚函数绑定 / 隐藏 vs 覆盖）能分辨
□ 题 4（++ 计数）能数清几个星号
□ 题 6（异常析构计数）会数 10 次
□ 题 8（dynamic_cast 指针 nullptr / 引用抛异常）记牢
□ 判断题三组答案串 + friend 不能重载 [] 背下来
□ 编程题：MyString 深拷贝三件套 + Shape 抽象类两个骨架能默写
□ 5 条编程通用得分点（virtual 析构、三件套、纯虚、初始化列表调基类、override）
```

---

上一章 → [模板与 STL](05-template-stl.md) ｜ 回到 → [OOP 首页](index.md)
