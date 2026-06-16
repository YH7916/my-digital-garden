---
title: OOP 04 左值右值、移动语义、异常处理
tags:
  - learning
  - courses
  - oop
  - cpp
  - finals
updated: 2026-06-16
publish: true
blog_dest: Notes/OOP/04-move-exception.md
---
# 4. 左值右值 / 移动语义 / 异常处理 / 断言

> 这一章里**异常处理是高频考点**（尤其"throw 时调用了几次析构"）。移动语义偶尔考概念和填空。

---

## 4.1 左值 (lvalue) 与右值 (rvalue)

理解移动语义之前，先分清这两个词。**最简单的判断法：能取地址（用 `&`）的就是左值，不能的就是右值。**

```text
左值 lvalue：有名字、有确定内存地址的东西
    • 变量名 x
    • arr[i] 下标表达式
    • 返回引用的函数调用
    → 它能出现在赋值号左边，也能取地址 &x

右值 rvalue：临时的、没有稳定地址的东西，表达式结束就没了
    • 字面量 42、true
    • 算术表达式结果 a + b
    • 返回值（非引用）的函数调用
    → 取不了地址
```

```cpp
int x = 10;   // x 是左值，10 是右值
int* p = &x;  // ✅ 能取 x 的地址
// int* q = &10;   ❌ 10 是右值，取不了地址
```

---

## 4.2 左值引用与右值引用

```cpp
int a = 10;
int& refA = a;      // 左值引用 T&，只能绑左值
// int& refB = 10;  ❌ 不能绑右值

int&& refC = 10;    // 右值引用 T&&（两个 &），专门绑右值（C++11 新增）
// int&& refD = a;  ❌ 不能绑左值
```

```text
T&   左值引用：只能绑左值
T&&  右值引用：只能绑右值（C++11 引入，是移动语义的基础）
const T&  常量左值引用：左值右值都能绑（所以常用作函数参数）
```

---

## 4.3 移动语义：把资源"搬走"而不是"复制"

**动机**：深拷贝大对象（如装了一百万个元素的 vector）很慢。如果源对象是个"马上要死的临时对象"，与其复制它的资源再把它销毁，不如直接把它的资源**搬过来**。

```text
深拷贝（旧做法，慢）：           移动（新做法，快）：
  ① 给新对象申请内存             ① 直接把旧对象的指针"抢"过来
  ② 逐个复制数据                 ② 把旧对象的指针置空
  ③ 销毁临时对象                 （没有复制数据，O(1)）
```

### 移动构造函数

```cpp
class Buffer {
public:
    int* data;
    int  size;
    Buffer(int s) : size(s), data(new int[s]) {}
    ~Buffer() { delete[] data; }

    // 移动构造：参数是右值引用 &&
    Buffer(Buffer&& other) : data(other.data), size(other.size) {
        other.data = nullptr;   // ⚠️ 关键：把源对象指针置空
        other.size = 0;         //    否则源对象析构时会把搬走的内存 delete 掉
    }
};
```

```text
函数签名：
  移动构造：  ClassName(ClassName&& other)
  移动赋值：  ClassName& operator=(ClassName&& other)
              （移动赋值同样要判断 other 是不是自己，且要先释放自己旧资源）
关键动作：搬完后把源对象置于"安全的空状态"，防止它析构时释放已搬走的资源
```

### std::move：把左值"伪装"成右值

正常情况下对象名是左值，直接赋值会走拷贝。想触发移动，要用 `std::move`：

```cpp
Buffer a(100);
Buffer b = std::move(a);   // 强制走移动构造，a 的资源被搬到 b，a 变空
```

> ⚠️ 易错点：`std::move` **本身不移动任何东西**！它只是个强制类型转换，把左值转成右值引用，"告诉编译器：这个可以被搬走"。真正的搬运是移动构造/移动赋值做的。

---

## 4.4 ⭐异常处理：try / catch / throw

C 用"返回错误码"处理错误，问题是错误处理代码把真正的业务逻辑淹没了。C++ 用异常机制分离它们。

三个关键字：

```text
try    包住"可能出错"的代码，后面跟一个或多个 catch
throw  发现无法处理的问题时，"抛出"一个异常
catch  "接住"并处理抛出的异常
```

```cpp
double divide(double a, double b) {
    if (b == 0)
        throw invalid_argument("Division by zero!");   // 抛异常
    return a / b;
}

try {
    double result = divide(x, y);
    cout << "Result: " << result << endl;
} catch (invalid_argument& e) {     // 接住特定类型的异常
    cerr << e.what() << endl;        // e.what() 取异常信息
} catch (...) {                      // ... 接住所有其他类型的异常
    cerr << "Unknown exception" << endl;
}
```

### ⭐关键机制：栈展开 (Stack Unwinding)

这是"throw 调用了几次析构"那类题的原理：

```text
异常被抛出后，程序沿着【函数调用栈】向上找匹配的 catch。
在这个"往回退"的过程中：
  • 所有已经构造的【局部对象】会被【自动析构】（这就是栈展开）
  • throw 之后、同一作用域里的代码会被【跳过】（不执行）
如果一路退到顶都没找到匹配的 catch → 调用 std::terminate() 终止程序
```

### catch 的匹配顺序（判断题考点）

```text
• catch 块按【书写顺序】从上往下匹配，第一个匹配的就执行
• 如果基类和派生类异常都可能抛，【派生类 catch 必须写在基类 catch 前面】
  （否则基类 catch 会先把派生类异常截走）
• catch(...) 要放最后（它接所有，放前面会挡住后面的）
```

> 判断题：try 块可以没有 catch 吗？题库口径给 **T**（注意：标准 C++ 实际上 try 必须配 catch，但本课题库按 T 记）。

### ⭐经典原题：异常 + 析构计数（2023-2024，必背）

```cpp
class A {
public:
    A()  { cout << "A()\n"; }
    ~A() { cout << "~A()\n"; }
};
void foo(A a) {        // ① 按值传参 → 拷贝出 1 个 A
    A arr[5];          // ② 栈上 5 个 A
    A* p = new A[3];   // ③ 堆上 3 个 A（不随栈展开自动析构）
    throw p;           // 抛出后开始栈展开
}
int main() {
    try {
        A a;           // ④ main 里 1 个 A
        foo(a);
    } catch (A* p) {
        delete[] p;    // ⑤ 手动析构堆上 3 个
        cout << "catched\n";
    }
}
```

**问：A 的析构 `~A()` 被调用几次？答案：10**

```text
栈展开时析构：foo 里的 arr[5]  →  5 次
            foo 的形参 a    →  1 次
delete[] p 析构堆上的 3 个    →  3 次
main 里的局部 a              →  1 次
─────────────────────────────────────
合计                          → 5 + 1 + 3 + 1 = 10 次
```

关键点：堆上 `new A[3]` 的 3 个对象**不会**随栈展开自动析构，只有手动 `delete[] p` 才析构。

### 经典原题：throw; 重抛 + 跳过后续（题库）

```cpp
void f3() { double a = 0; try { throw a; } catch(double){ cout<<"OK3! "; throw; } cout<<"end3 "; }
void f2() { try { f3(); } catch(int){ cout<<"Ok2! "; } cout<<"end2 "; }
void f1() { try { f2(); } catch(char){ cout<<"OK1!"; } cout<<"end1 "; }
int main() { try { f1(); } catch(double){ cout<<"OK0! "; } cout<<"end0 "; }
```

**输出：`OK3! OK0! end0`**

```text
f3 抛 double，自己的 catch(double) 接住 → 打印 "OK3! "
  然后 throw; 重新抛出同一个 double 异常
  → f3 的 "end3" 被跳过（异常正在传播）
f2 的 catch(int) 不匹配 double → "end2" 被跳过
f1 的 catch(char) 不匹配 double → "end1" 被跳过
main 的 catch(double) 匹配！ → 打印 "OK0! "
  异常处理完毕，正常继续 → 打印 "end0"
```

记忆：**`throw;`（不带参数）= 把当前异常原样再抛一次。异常传播路上的代码全部跳过。**

---

## 4.5 断言 Assertion：抓"绝不该发生"的逻辑错误

断言用来验证"程序运行时是否满足某个条件"。条件为真就继续，为假就立刻报错退出。

```text
断言 vs 异常 的区别（概念题）：
  断言 assert：抓【绝对不该发生】的程序逻辑 bug（如数组越界），只在开发期用，
              生产环境会被关掉，一触发程序直接停
  异常 exception：处理【可能遇到】的问题（如网络发送失败），生产环境照常用
```

### 运行时断言 assert（`<cassert>`）

```cpp
#include <cassert>
int* arr = new int[5];
assert(arr != nullptr);   // 条件为假就报错退出。定义了 NDEBUG 宏时会被禁用
```

### 编译期断言 static_assert（C++11）

```cpp
static_assert(sizeof(void*) == 8, "仅支持 64 位系统");
// 编译期就检查，条件不成立直接编译报错，无运行时开销
// 但只能检查编译期能确定的常量表达式
```

---

## 4.6 本章自测

```text
1. 怎么判断左值右值？                       → 能取地址 & 的是左值，不能的是右值
2. T&& 是什么引用？绑什么？                  → 右值引用，绑右值
3. std::move 真的移动东西吗？                → 不！它只是把左值转成右值引用
4. 移动构造里为什么要把源对象指针置空？      → 防止源对象析构时释放已搬走的内存
5. 栈展开过程中局部对象会怎样？              → 被自动析构
6. throw; 不带参数是什么意思？               → 把当前异常原样重新抛出
7. 派生类异常的 catch 该放在基类前还是后？   → 前面（否则被基类先接走）
8. 堆上 new[] 的对象会随栈展开自动析构吗？   → 不会，必须手动 delete[]
9. assert 和异常的核心区别？                 → assert 抓不该发生的逻辑 bug，开发期用；异常处理可能的问题
```

---

上一章 → [继承与多态](03-inheritance-polymorphism.md) ｜ 下一章 → [模板与 STL](05-template-stl.md)
