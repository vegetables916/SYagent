---
name: "design-patterns-and-solid"
description: "Enforces GoF 23 design patterns and SOLID principles when writing code. Invoke when creating classes, modules, or complex logic to ensure maintainable, extensible, and loosely-coupled code. Applies to TypeScript, JavaScript, and other OOP languages."
---

# GoF 设计模式与 SOLID 原则

在编写代码时，必须遵守以下设计模式和原则，确保代码可维护、可扩展、低耦合。

## 一、GoF 23种设计模式

### 1. 创建型模式（5种）：管控对象创建逻辑

| 模式 | 英文名 | 适用场景 |
|------|--------|----------|
| 单例模式 | Singleton | 全局唯一实例，如配置管理器、日志器 |
| 工厂方法模式 | Factory Method | 延迟对象创建到子类，解耦创建与使用 |
| 抽象工厂模式 | Abstract Factory | 创建一系列相关对象，如不同主题的 UI 组件 |
| 建造者模式 | Builder | 分步构建复杂对象，如构建复杂查询参数 |
| 原型模式 | Prototype | 通过克隆已有对象创建新实例，避免重复初始化 |

### 2. 结构型模式（7种）：组装/包装类与对象，构建结构

| 模式 | 英文名 | 适用场景 |
|------|--------|----------|
| 适配器模式 | Adapter | 让不兼容接口协同工作，如封装第三方 SDK |
| 装饰器模式 | Decorator | 动态添加功能，如给请求添加缓存/重试逻辑 |
| 代理模式 | Proxy | 控制对象访问，如权限校验、延迟加载 |
| 外观模式 | Facade | 为复杂子系统提供统一接口，如封装多个 API 调用 |
| 桥接模式 | Bridge | 分离抽象与实现，如支持多种渲染引擎 |
| 组合模式 | Composite | 树形结构处理，如菜单、文件夹层级 |
| 享元模式 | Flyweight | 共享细粒度对象，减少内存占用，如缓存图标 |

### 3. 行为型模式（11种）：处理对象间交互、算法、流程

| 模式 | 英文名 | 适用场景 |
|------|--------|----------|
| 模板方法模式 | Template Method | 定义算法骨架，子类实现细节，如表单验证流程 |
| 策略模式 | Strategy | 封装可替换算法，如不同排序/校验策略 |
| 命令模式 | Command | 将请求封装为对象，支持撤销/重做，如操作历史 |
| 迭代器模式 | Iterator | 顺序访问集合元素，不暴露内部结构 |
| 中介者模式 | Mediator | 集中管理对象交互，如聊天室、表单联动 |
| 备忘录模式 | Memento | 保存/恢复对象状态，如撤销操作 |
| 观察者模式 | Observer | 一对多依赖，状态变更自动通知，如事件系统 |
| 状态模式 | State | 对象行为随状态改变，如订单状态流转 |
| 职责链模式 | Chain of Responsibility | 请求沿链传递，直到被处理，如中间件、审批流 |
| 解释器模式 | Interpreter | 定义语言语法并解释执行，如规则引擎 |
| 访问者模式 | Visitor | 在不修改类的前提下添加新操作，如 AST 遍历 |

---

## 二、SOLID 六大设计原则

### 1. 单一职责原则 SRP
**全称**：Single Responsibility Principle  
**一句话**：一个类/函数只负责一件事。  
**反例**：一个类既处理数据、又渲染页面、又保存文件，改一处全崩。  
**正例**：拆分为 `DataService`、`ViewRenderer`、`FileStorage` 三个类。

### 2. 开闭原则 OCP
**全称**：Open Closed Principle  
**一句话**：对扩展开放，对修改关闭。  
**核心**：新增功能不要改原有成熟代码，通过新增类/接口拓展。  
**示例**：使用策略模式替代 `if-else` 分支，新增策略无需修改原逻辑。

### 3. 里氏替换原则 LSP
**全称**：Liskov Substitution Principle  
**一句话**：子类可以完全替换父类，程序不出 bug。  
**反例**：子类重写父类方法后破坏原有逻辑（如 `Square` 继承 `Rectangle` 但破坏宽高独立设置）。  
**正例**：继承时保持父类契约，不随意改变行为。

### 4. 接口隔离原则 ISP
**全称**：Interface Segregation Principle  
**一句话**：不要用大而全的臃肿接口，拆分出多个细分小接口。  
**反例**：强迫类实现不需要的方法。  
**正例**：将 `Worker` 拆分为 `Workable`、`Eatable`、`Sleepable`。

### 5. 依赖倒置原则 DIP
**全称**：Dependency Inversion Principle  
**一句话**：高层模块不依赖底层具体实现，二者都依赖抽象（接口/抽象类）。  
**反例**：直接 `new` 具体类，导致强耦合。  
**正例**：依赖接口，通过工厂/依赖注入提供实现。

### 6. 迪米特法则 LoD（最少知道原则）
**全称**：Law of Demeter  
**一句话**：类只和自己直接朋友通信，不要和无关类深度耦合。  
**反例**：`a.getB().getC().doSomething()` 链式调用暴露内部结构。  
**正例**：通过中间方法封装，减少跨层调用。

---

## 三、编码检查清单

编写代码时，逐项检查：

- [ ] 类/函数是否职责单一？（SRP）
- [ ] 新增功能是否通过扩展而非修改？（OCP）
- [ ] 子类是否能无缝替换父类？（LSP）
- [ ] 接口是否精简，无冗余方法？（ISP）
- [ ] 是否依赖抽象而非具体实现？（DIP）
- [ ] 是否避免了跨层链式调用？（LoD）
- [ ] 是否选用了合适的设计模式？（GoF）

---

## 四、记忆口诀

1. **SRP** 分职责
2. **OCP** 不修改、只拓展
3. **LSP** 子类完美替代父类
4. **ISP** 接口拆小，按需实现
5. **DIP** 依赖抽象，不依赖具体
6. **LoD** 少和无关类打交道

所有 23 种设计模式，本质都是为了遵守这 6 条原则，解决耦合、难维护、难扩展的代码问题。
