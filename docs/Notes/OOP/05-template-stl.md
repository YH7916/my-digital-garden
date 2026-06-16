---
title: OOP 05 模板、STL、迭代器、智能指针
tags:
  - learning
  - courses
  - oop
  - cpp
  - finals
updated: 2026-06-16
publish: true
blog_dest: Notes/OOP/05-template-stl.md
---
# 5. 模板 / STL / 迭代器 / 智能指针

> 模板的特化和匹配优先级是"看程序写结果"考点；STL 容器是编程题的常用工具；智能指针偏概念题。

---

## 5.1 模板：写一份代码，适配所有类型

**问题**：求两个数的较大者，要为 int、float、double 各写一遍？

```cpp
int    max(int a, int b)    { return a < b ? b : a; }
double max(double a, double b) { return a < b ? b : a; }
// ... 每种类型都要重复，逻辑完全一样
```

**模板 (Template)** 把"类型"也变成参数，一份代码搞定所有类型：

```cpp
template <typename T>           // T 是类型参数（typename 和 class 在这里等价）
T max(T a, T b) { return a < b ? b : a; }

int    i = max(1, 2);       // 编译器自动推导 T = int，生成 max<int>
double d = max(2.5, -3.0);  // 自动推导 T = double，生成 max<double>
```

```text
泛型编程 = 把类型参数化，实现代码高度复用
前提：用到的运算（如这里的 <）对该类型有定义
```

### 函数模板 vs 类模板

```cpp
// 函数模板
template <class T>
T add(T a, T b) { return a + b; }

// 类模板：成员变量/函数的类型可变
template <typename T>
class Box {
    T data;
public:
    Box(T d) : data(d) {}
    T getData() { return data; }
};

Box<int>    intBox(100);      // 用的时候要指定类型 <int>
Box<string> strBox("Hello");
```

### 模板的实现机制（概念题）

```text
• 模板本身不是代码，不会被编译成机器指令
• 只有你"用"模板时（传入具体类型），编译器才【实例化】生成真正的代码
• 因为编译器要看见完整代码才能实例化，所以模板的【实现不能拆到 .cpp 里】，
  通常声明和实现都写在头文件中
• 代码膨胀：每种用到的类型都会生成一份代码，可能让二进制文件变大
```

### 多个类型参数 / 非类型模板参数

```cpp
// 多个类型参数
template <typename T, typename U>
class KeyValuePair {
    T key;  U value;
public:
    KeyValuePair(T k, U v) : key(k), value(v) {}
};

// 非类型模板参数（通常是整数）：典型用途是定长数组
template <typename T, int Size>
class GenericArray {
    T arr[Size];
public:
    T& operator[](int idx) { return arr[idx]; }
};
GenericArray<int, 10> int_arr;   // 长度固定为 10
```

---

## 5.2 模板特化与匹配优先级（⭐考点）

### 全特化：给特定类型"开小灶"

当通用模板对某个类型不合适时，为它单独写一套实现：

```cpp
template <typename T>           // 通用版本
class Storage {
public:
    void print() { cout << "General\n"; }
};

template <>                     // 全特化：专门针对 bool
class Storage<bool> {
public:
    void print() { cout << "Specialized for bool\n"; }
};

Storage<int> a;  a.print();    // General
Storage<bool> b; b.print();    // Specialized for bool
```

### ⭐重载决议的匹配顺序（看程序写结果常考）

当普通函数、模板函数同时存在，调谁？记住这个优先级：

```text
① 完全匹配的【普通函数】（非模板）       ← 最优先
② 完全匹配的【模板函数】
③ 需要【类型转换】的普通函数             ← 最次
```

经典原题：

```cpp
void f(int x)    { cout << "int\n"; }
void f(double x) { cout << "double\n"; }
template<typename T> void f(T x) { cout << "template\n"; }

f(1.0f);   // 调谁？1.0f 是 float 类型
```

```text
逐个分析候选：
  f(int)：    float → int 需要窄化转换（不完全匹配）
  f(double)： float → double 需要提升（不完全匹配）
  f(T)：      实例化为 f<float>，是【精确匹配】

精确匹配优先级最高 → 调用模板版本 f<float>(1.0f) → 输出 "template"
```

```text
另外两种报错情况：
  • 多个候选无法区分谁更匹配 → Ambiguous（二义性）
  • 一个都匹配不上 → No matching function（找不到匹配函数）
```

---

## 5.3 STL 容器：现成的数据结构

**STL (Standard Template Library)** 用模板把"数据结构"和"算法"分开，现成可用。

### 序列容器

```cpp
// vector：动态数组，随机访问 O(1)，尾部增删快  ← 最常用
vector<int> v = {1, 2, 3};       // 列表初始化
vector<int> v2(5, 0);            // 长度 5，初值都是 0
v.push_back(6);                  // 尾部加
v.pop_back();                    // 尾部删
v[2] = 10;                       // 下标随机访问
int n = v.size();                // 大小（几乎所有容器都有）
bool e = v.empty();              // 判空
vector<vector<int>> g(10, vector<int>(5, 0));   // 10×5 二维数组

// deque：双端队列，两端增删快
// list：双向链表，任意位置增删快，但不支持随机访问（不能 lst[i]）
```

### 关联容器

```cpp
// set / unordered_set：集合，元素唯一，用于去重 / 判断存在
unordered_set<int> s;
s.insert(5);
if (s.find(5) != s.end()) { /* 存在 */ }
s.erase(5);

// map / unordered_map：键值对，用于统计 / 按键查找
unordered_map<int, int> cnt;
for (int x : v) cnt[x]++;   // 统计每个数出现次数（访问不存在的键会自动创建并初始化为 0）
for (auto& p : cnt)
    cout << p.first << ":" << p.second << endl;   // first 是键，second 是值
```

**底层区别（必考对比）：**

```text
set / map：           底层【红黑树】，元素【自动排序】，查找 O(log n)
unordered_set/map：   底层【哈希表】，【不保证顺序】，查找 O(1)，但键必须可哈希
```

### pair：打包两个值

```cpp
pair<string, int> p = {"Alice", 90};
cout << p.first << ": " << p.second;   // Alice: 90
auto p2 = make_pair("Bob", 85);
```

### 容器适配器（基于底层容器包装的新接口）

```text
名称              底层默认容器   特性
stack            deque         后进先出 LIFO
queue            deque         先进先出 FIFO
priority_queue   vector        大顶堆（默认最大值在顶）
```

```cpp
stack<int> st;  st.push(1);  st.top();  st.pop();       // pop 不返回值
queue<int> q;   q.push(1);   q.front(); q.back(); q.pop();
priority_queue<int> maxHeap;                            // 默认大顶堆
priority_queue<int, vector<int>, greater<int>> minHeap; // 小顶堆要用 greater<int>
```

### 常用算法（通过迭代器操作，不直接碰容器）

```cpp
sort(v.begin(), v.end());                  // 升序
sort(v.begin(), v.end(), greater<int>());  // 降序
sort(v.begin(), v.end(), [](int a,int b){ return a > b; });  // lambda 自定义
reverse(v.begin(), v.end());               // 反转
auto it = find(v.begin(), v.end(), 5);     // 查找，找不到返回 v.end()
cout << *max_element(v.begin(), v.end());  // 最大值（返回迭代器，要 * 解引用）
int c = count_if(v.begin(), v.end(), [](int x){ return x > 3; });  // 计数
```

---

## 5.4 迭代器 Iterator：容器和算法之间的"通用接口"

**迭代器**是一种"特殊的指针"，用来遍历容器，且不用关心容器内部是数组、链表还是树。

```text
为什么需要迭代器？
  vector 底层连续，可以 v[i]
  list 是链表，没有"第 i 个"的快速访问
  set/map 是树，本身没有"第几个"的概念
迭代器提供【统一的遍历方式】，让算法不依赖具体容器 → 容器和算法解耦
```

### 基本操作（语法像指针）

```cpp
vector<int> v = {1, 3, 5, 7, 9};
for (vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";   // *it 解引用取元素
}
```

```text
*it       解引用，取当前元素
++it      移到下一个
== / !=   比较两个迭代器位置
it->成员   访问元素的成员
begin()   指向第一个元素
end()     指向【最后一个元素的后一个位置】（哨兵，不是最后一个元素！）
          → it == end() 表示遍历完了
```

range-for 循环本质就是迭代器：

```cpp
for (int& x : v) x *= 2;   // 等价于用 begin()/end() 遍历
```

### ⭐迭代器失效（易错点）

```text
对 vector 做 push_back 触发扩容 → 底层数组换了地址 → 之前所有迭代器失效
对 vector 做 erase → 被删位置【及之后】的迭代器失效

正确的边遍历边删写法：
```

```cpp
for (auto it = v.begin(); it != v.end(); ) {
    if (*it == 3)
        it = v.erase(it);   // erase 返回下一个有效迭代器，接住它
    else
        ++it;
}
```

```text
不同容器失效规则不同：
  • vector 扩容 → 所有迭代器失效
  • vector::erase → 删除点及之后失效
  • list 删一个结点 → 只有指向该结点的失效
  • map/set 插入 → 通常不失效
```

---

## 5.5 智能指针：自动管理内存（RAII）

### RAII 思想：把资源绑到对象生命周期上

```text
RAII = Resource Acquisition Is Initialization（资源获取即初始化）
  • 构造对象时获取资源（如 new 内存）
  • 对象离开作用域自动析构
  • 析构函数里释放资源

好处：哪怕中途 return 或抛异常，只要栈对象正常析构，资源就一定被释放
     → 不会忘记 delete，杜绝内存泄漏
```

```cpp
void f() {
    int* p = new int(10);
    if (error()) return;   // ❌ 忘了 delete，内存泄漏
    delete p;
}
// 智能指针把 delete 放进析构函数，让释放自动发生
```

C++11 提供三种智能指针（在 `<memory>`）：

### unique_ptr：独占所有权

```cpp
unique_ptr<int> p1(new int(10));
// unique_ptr<int> p2 = p1;       ❌ 不能拷贝（独占）
unique_ptr<int> p2 = move(p1);    // ✅ 只能移动，p1 交出所有权后变空
```

```text
• 同一时间只能有一个 unique_ptr 指向某对象
• 只支持移动，不支持拷贝
• 开销极小，几乎和原始指针一样
• 适合：明确只有一个拥有者的场景
```

### shared_ptr：共享所有权，引用计数

```cpp
auto p1 = make_shared<int>(20);   // 推荐用 make_shared 创建
{
    auto p2 = p1;                 // 引用计数 +1 → 变 2
}                                 // p2 离开作用域，计数 -1 → 变 1
// 计数降到 0 时，自动释放内存
```

```text
内部维护一个【引用计数】：
  • 新增一个 shared_ptr 指向对象 → 计数 +1
  • 一个 shared_ptr 销毁/重置    → 计数 -1
  • 计数降为 0 → 自动 delete

⚠️ 不要用同一个原始指针构造多个 shared_ptr（会产生两个独立计数 → 重复 delete）
   正确做法：从已有的 shared_ptr 拷贝
```

### weak_ptr：弱引用，解决循环引用

```text
shared_ptr 的问题——循环引用：
  A 内部有 shared_ptr<B>，B 内部有 shared_ptr<A>
  → 它们互相保住对方，引用计数永远归不了零 → 都不析构 → 内存泄漏

         A ──shared──► B
         ▲             │
         └──shared─────┘     互相指着，计数都是 1，谁也死不了

解决：把其中一个改成 weak_ptr。weak_ptr【不拥有对象、不增加引用计数】，
     只是"观察"对象，不会阻止它被释放。
```

```cpp
class A { public: shared_ptr<B> ptrB; };
class B { public: weak_ptr<A>   ptrA; };   // 把 B 指向 A 的改成 weak_ptr，打破循环
```

weak_ptr 不能直接 `*` 或 `->`，用前要 `lock()` 拿一个临时 shared_ptr：

```cpp
if (auto sp = wp.lock()) { cout << *sp; }   // lock 成功说明对象还活着
```

### 选择建议（概念题）

```text
明确只有一个拥有者     → unique_ptr
确实需要多个拥有者     → shared_ptr
只想观察、不延长寿命   → weak_ptr
只是临时借用           → 用引用或原始指针
口诀：谁负责释放资源，谁才该拥有智能指针。别无脑全用 shared_ptr。
```

---

## 5.6 本章自测

```text
1. typename 和 class 在模板参数里有区别吗？      → 没有，等价
2. 模板的实现为什么不能放进 .cpp？               → 实例化需要看见完整代码，放头文件
3. f(1.0f) 在 普通f(int)/f(double)/模板f(T) 里调谁？ → 模板（精确匹配优先于类型转换）
4. set 和 unordered_set 底层和复杂度？           → 红黑树 O(log n) 有序 / 哈希表 O(1) 无序
5. priority_queue 默认大顶堆还是小顶堆？小顶堆怎么写？ → 大顶堆；小顶堆用 greater<int>
6. end() 指向最后一个元素吗？                     → 不，指向最后一个的后一个（哨兵）
7. vector push_back 后老迭代器还能用吗？          → 可能扩容失效，不能用
8. unique_ptr 能拷贝吗？                          → 不能，只能 move
9. shared_ptr 循环引用怎么解决？                  → 一方改用 weak_ptr
```

---

上一章 → [移动语义与异常](04-move-exception.md) ｜ 下一章 → [考试经典题](06-exam-classics.md)
