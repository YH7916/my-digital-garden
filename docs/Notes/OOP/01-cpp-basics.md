---
title: OOP 01 C++ 基础
tags:
  - learning
  - courses
  - oop
  - cpp
  - finals
updated: 2026-06-16
publish: true
blog_dest: Notes/OOP/01-cpp-basics.md
---
# 1. C++ 基础（I/O、引用、函数、const、static、类型）

> 这一章是"地基"。考试里它们通常不是单独大题，而是藏在"看程序写结果"和"程序填空"里。
> 目标：看到 `const int* p`、`int& r`、`static int n`、lambda 这些写法，你能立刻说出它们是什么、会发生什么。

---

## 1.1 输入输出：C++ 用"流"

C++ 不用 `printf/scanf`，而是把数据想象成"水流"，从一个地方流到另一个地方。

四个预定义的"流对象"：

```text
std::cin    标准输入流   ← 从键盘读数据
std::cout   标准输出流   → 打印到屏幕
std::cerr   标准错误流   → 打印错误（不带缓冲，立即输出）
std::clog   标准日志流   → 记录日志（带缓冲）
```

`<<` 是"往流里塞"，`>>` 是"从流里取"。方向就是箭头方向，很好记：

```cpp
int n;
cin >> n;              // 从输入流取一个数，放进 n
cout << "n = " << n << endl;   // 把 "n = " 和 n 塞进输出流
```

读一个长度为 n 的数组并打印（这是机考最常见的输入套路，必须会写）：

```cpp
int n;
cin >> n;                       // 先读个数
vector<int> v(n);               // 开一个长度 n 的数组
for (int i = 0; i < n; i++) {
    cin >> v[i];                // 逐个读入
}
for (int i = 0; i < n; i++) {
    cout << v[i] << " ";        // 逐个打印
}
cout << endl;
```

几个**常考小坑**：

```text
• cin >> s 遇到空格就停。要读一整行（含空格）用 getline(cin, s)
• cin >> 会自动跳过前面的空格/换行
• endl 不只是换行，它还会"刷新缓冲区"（清空内部缓存，真正写出去）
• 格式化输出用 <iomanip> 头文件（如 setw、setprecision）
```

---

## 1.2 命名空间 namespace：解决"重名打架"

两个人都写了一个叫 `value` 的变量怎么办？C++ 用"命名空间"把它们装进不同的盒子，用 `::`（作用域解析运算符）指定从哪个盒子取。

```cpp
int value = 10;                 // 全局的 value
namespace ThirdParty {
    int value = 20;             // 第三方盒子里的 value
}

int main() {
    cout << ThirdParty::value << endl;   // 20  ← 指定从 ThirdParty 盒子取
    cout << value << endl;               // 10  ← 没指定，取全局的
}
```

`std` 就是标准库的盒子。规范写法是 `std::cout`，但平时偷懒写 `using namespace std;` 把整个盒子的东西一次性倒进当前作用域，这样就能直接写 `cout`。

---

## 1.3 引用 reference：变量的"别名"

这是 C++ 区别于 C 的核心特性，**必考**。

**一句话本质：引用就是给一个已存在的变量起了个外号。对外号做的任何事，都等于对本体做。**

```cpp
int x = 100;
int& y = x;     // y 是 x 的别名（外号）。注意 & 写在类型后面
y = 200;        // 改 y 就是改 x
cout << x;      // 200  ← x 真的被改了
```

引用的三条铁律（判断题常考）：

```text
① 引用不能为空（不像指针可以是 nullptr）
② 定义时必须立刻初始化（int& y; 是错的，必须 int& y = x;）
③ 一旦绑定就不能改绑别人（y 永远是 x 的别名）
```

**引用 vs 指针**（单选高频）：

| | 引用 `int&` | 指针 `int*` |
|---|---|---|
| 本质 | 变量的别名 | 存的是地址 |
| 能否为空 | ❌ 不能 | ✅ 可以 nullptr |
| 必须初始化 | ✅ 是 | ❌ 否 |
| 能否改绑 | ❌ 不能 | ✅ 可以 |

> 单选经典答案：References are an alias for a variable whereas pointer stores the address of a variable.

还有一个**常考陷阱**：普通引用 `&` 只能绑"左值"（有名字、有地址的东西），不能绑字面量：

```cpp
int& r = 1;     // ❌ 错误！1 是右值（临时的），没地址，普通引用绑不上
```

（什么是左值右值，[移动语义与异常](04-move-exception.md) 会专门讲。）

---

## 1.4 函数：传参的三种方式

这是"看程序写结果"和判断题的常客。三种传参方式：

```cpp
void byValue(int a)   { a = 99; }   // 值传递：a 是副本，改它不影响外面
void byPointer(int* a){ *a = 99; }  // 指针传递：传地址，能改外面
void byRef(int& a)    { a = 99; }   // 引用传递：传别名，能改外面
```

```text
值传递    → 拷贝一份，函数内改动"对外不可见"
指针传递  → 传地址，能改原变量，但写法啰嗦（要 *、&）
引用传递  → 传别名，能改原变量，写法干净 ← C++ 推荐
```

**大对象一定要用引用传**（如 `vector`），否则要承受整份拷贝的开销。如果不想被改，加 `const`：

```cpp
void func(const vector<int>& v)  // 既省了拷贝，又保证不被改
```

### 默认参数

调用时不给值，就用默认值。**只能从右往左给默认值**：

```cpp
void printSum(int a, int b = 10) { cout << a + b << endl; }

printSum(5);      // 输出 15  ← b 用默认值 10
printSum(5, 5);   // 输出 10  ← b 用传进来的 5
```

### 函数重载 overload

同一个名字，**参数列表不同**（类型或个数），编译器按你传的参数自动挑一个。

```cpp
void print(int i)            { cout << "Integer\n"; }
void print(double f)         { cout << "Double\n"; }
void print(int i, double f)  { cout << "Int & Double\n"; }
```

> ⚠️ **判断题陷阱**：仅返回值不同**不能**构成重载。`int f()` 和 `double f()` 会报错。

> ⚠️ **overload（重载）vs override（重写）是两回事**，判断题最爱混淆：
> - overload 重载：同名、**参数不同**、同一个类里、编译期决定
> - override 重写：派生类**重新实现**基类的虚函数、签名相同、运行期决定（见 03 章）
> - "overloading and overriding are essentially the same" → **F（错）**
> - "overloading and overriding are essentially different" → **T（对）**

### inline 内联函数

对"代码极短、调用极频繁"的函数加 `inline`，**建议**编译器把函数体直接展开到调用处，省掉函数调用开销。注意只是建议，编不编由编译器决定。

```cpp
inline int getMax(int a, int b) { return a > b ? a : b; }
```

---

## 1.5 Lambda 表达式：匿名函数

Lambda 就是"临时写一个没名字的函数"，最常见的用途是给 `sort` 传排序规则。

完整形式：

```text
[capture](parameters) -> return_type { body }
   │          │             │           │
 捕获列表    参数列表     返回类型    函数体
 (能用哪些    (和普通     (通常省略，   (具体逻辑)
  外部变量)   函数一样)    编译器推导)
```

最常见的用法 —— 降序排序：

```cpp
vector<int> nums = {1, 4, 3, 5, 2, 6};
sort(nums.begin(), nums.end(), [](int a, int b){ return a > b; });
//                              ↑ 这个 lambda 就是排序规则：a 排在 b 前当 a > b → 降序
```

**捕获列表 `[ ]`** 决定 lambda 能用外面哪些变量（考试会考按值 vs 按引用的区别）：

```text
[]      不捕获，外部局部变量一个都不能用
[x]     按值捕获 x（拷贝一份，外面的 x 改了里面不变）
[&x]    按引用捕获 x（用的是本体，能改外面的 x）
[=]     按值捕获所有用到的外部变量
[&]     按引用捕获所有用到的外部变量
```

```cpp
int x = 1;
auto f = [x]() { cout << x << endl; };   // 按值：拍了张快照
auto g = [&x]() { x++; };                // 按引用：用的是本体
g();
cout << x << endl;   // 2  ← g 通过引用把 x 改了
```

---

## 1.6 const：承诺"我不改你"

`const` 的核心含义就一句：**承诺不修改**。它能加的地方很多，逐个看。

### ① 修饰普通变量 —— 常量

```cpp
const int MAX = 100;   // MAX 定死，不能再改。C++ 推荐用 const 而不是 #define 宏
```

### ② 修饰指针 —— 看 const 在 `*` 的哪一边（⭐高频考点）

这是程序填空和单选的常客。**口诀：const 在 `*` 左边管"内容"，在右边管"指针本身"。**

```cpp
int a = 1, c = 4;

const int* p1 = &a;   // const 在 * 左边 → 不能改"指向的内容"，但能改 p1 指向谁
//  *p1 = 5;   ❌ 错（改内容不行）
    p1 = &c;   // ✅ 对（改指向可以）

int* const p2 = &a;   // const 在 * 右边 → p2 本身定死，但能改内容
    *p2 = 5;   // ✅ 对（改内容可以）
//  p2 = &c;   ❌ 错（改指向不行）

const int* const p3 = &a;   // 两边都 const → 内容和指向都不能改
```

记忆图：

```text
const int *  p   →  *p 不能变（内容只读），  p 能变（可改指向）
int  * const p   →   p 不能变（指针锁死），  *p 能变（可改内容）
       ↑
   const 紧挨 p，所以是"锁 p 本身"
```

### ③ 修饰函数参数（常引用）

```cpp
void printMsg(const string& msg) { cout << msg; }  // 既不拷贝，又防止改
```

### ④ 修饰成员函数 —— 承诺不改对象（⭐高频）

```cpp
class User {
    string name;
public:
    string getName() const {   // const 加在括号后面：承诺这个函数不改任何成员
        // name = "x";   ❌ 编译报错
        return name;
    }
};
```

铁律：**const 对象只能调用 const 成员函数。**（你都说对象不能改了，当然不能调可能改它的函数。）

> ⚠️ **重载分派陷阱**（真题原题）：const 和非 const 版本可以同时存在，const 对象/指针会挑 const 版本：
> ```cpp
> class A {
> public:
>     void f(int a, int b = 10)       { cout << a + b; }   // 非 const 版
>     void f(int a, int b = 10) const { cout << a - b; }   // const 版
> };
> A a;  const A* p = &a;
> p->f(25);   // 输出 15  ← p 是 const 指针，调 const 版，25 - 10 = 15
> ```

---

## 1.7 static：归"类"所有，活到程序结束

`static` 在不同位置含义不同，**全是考点**，分开记：

### ① 修饰局部变量 —— 只初始化一次，活到程序结束

```cpp
void f() {
    static int count = 0;   // 只在第一次进函数时初始化
    count++;
    cout << count << " ";
}
f(); f(); f();   // 输出 1 2 3  ← count 没被销毁，一直累加
```

```text
普通局部变量：每次进函数重新创建、出函数销毁
static 局部变量：第一次进函数才初始化，之后一直存在，程序结束才销毁
                作用域仍然只在函数内（外面访问不到）
```

### ② 修饰类的成员变量 —— 全类共享一份

```cpp
class Player {
public:
    static int total;        // 所有 Player 对象共享这一个 total
    Player() { total++; }
};
int Player::total = 0;       // ⚠️ 必须在类外定义初始化（程序填空常考这一行）

Player a, b, c;
cout << Player::total;       // 3  ← 可以直接用类名访问，不需要对象
```

```text
普通成员变量：每个对象一份（a 有自己的、b 有自己的）
static 成员变量：整个类只有一份，所有对象共用，存在全局数据区
                可以用 类名::变量 直接访问，不占对象的 sizeof 空间
```

### ③ 修饰成员函数 —— 没有 this，只能碰 static 成员

```cpp
class MathUtils {
public:
    static int add(int a, int b) { return a + b; }   // 静态成员函数
};
int sum = MathUtils::add(5, 3);   // 不用建对象，直接类名调用
```

铁律（判断题/改错题高频）：

```text
• 静态成员函数没有 this 指针（因为它不属于任何具体对象）
• 所以它不能访问非静态成员（不知道该访问哪个对象的）
• 静态成员函数也不能加 const（const 是承诺不改对象，但它根本没对象）
```

---

## 1.8 类型系统：union 与 enum（偶尔考）

### 联合体 union —— 几个成员"共用同一块内存"

```cpp
union Data { int i; float f; };   // i 和 f 共用一块内存，同时只能用一个
Data d;
d.i = 10;          cout << d.i;    // 10
d.f = 220.5;       cout << d.f;    // 220.5（此时 i 的值已被覆盖，读 i 是未定义行为）
```

```text
• 所有成员起始地址相同，读"非活跃成员"是未定义行为
• union 的大小至少是最大成员的大小
• 意义：节省内存（多个属性逻辑上互斥时）；底层数据拆解
```

### 枚举 enum —— 给一组整数常量起名字

```cpp
// 传统枚举：成员名"全局可见"，容易撞名
enum Color { RED, GREEN, BLUE };   // RED=0, GREEN=1, BLUE=2
Color c = RED;

// 强类型枚举 enum class（C++11，现代首选）
enum class Status { OK = 200, NOT_FOUND = 404 };
Status s = Status::OK;             // 必须带作用域 Status::
```

```text
enum（传统）：     成员名污染外部作用域；可隐式转 int
enum class（强类型）：成员名限定在内部，不会撞名；不隐式转 int（要 static_cast）
```

---

## 1.9 本章自测（能答出来就过关）

```text
1. int& y = x; 之后 y = 200，x 变不变？           → 变（y 是 x 的别名）
2. const int* p 和 int* const p 哪个能改内容？     → int* const p 能改内容
3. const 对象能调用非 const 成员函数吗？           → 不能
4. 仅返回值不同能构成重载吗？                       → 不能
5. static 局部变量什么时候销毁？                     → 程序结束时
6. 静态成员函数为什么不能访问非静态成员？          → 没有 this，不知道是哪个对象
7. lambda 里 [x] 和 [&x] 的区别？                   → [x]拷贝快照，[&x]用本体能改外面
```

---

上一章 → [考试地图](00-exam-map.md) ｜ 下一章 → [类与对象](02-class-basics.md)
