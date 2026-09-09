---
alwaysApply: true
globs: ["frontend/**/*"]
description: 如果需要在frontend下写代码，改代码就生效
---

你是本项目前端开发助手。开发 frontend 相关代码前，**必须读取项目本地文件 frontend/docs/前端开发规范.md**，所有输出的 tsx、ts、css 代码严格遵守该文档全部编码约定。

约束：
1. 技术栈为 React + TypeScript + Vite + Ant Design + Tailwind CSS，忽略任何 Vue 相关规则。
2. 文件命名、目录结构、TS类型、CSS写法、git commit 消息格式全部遵循该md文档。
3. 生成 git commit 示例时，type冒号**后面必须带上空格**。
4. 禁止滥用 any，尽量避免使用 @ts‑ignore。
5. 严格区分 src/assets 与 public 的资源使用规则。

当我要求编写页面、组件、工具函数时默认执行上述规范；若文档规则与我的显式指令冲突，以我的指令优先。