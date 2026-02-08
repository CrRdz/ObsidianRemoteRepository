# React 开发笔记

React 是一个用于构建用户界面的 JavaScript 库，由 Facebook 开发和维护。它采用组件化的开发方式，使得代码更加模块化和可复用。

## 核心特性

1. **虚拟 DOM**：React 使用虚拟 DOM 来提高渲染性能，通过 diff 算法最小化实际 DOM 操作。

2. **JSX 语法**：JSX 是 JavaScript 的语法扩展，允许在 JavaScript 中编写类似 HTML 的代码。

3. **单向数据流**：数据从父组件流向子组件，保证了数据的可预测性。

4. **Hooks**：React 16.8 引入的 Hooks 让函数组件可以使用状态和其他 React 特性。

## 常用 Hooks

- useState：管理组件状态
- useEffect：处理副作用
- useContext：访问上下文
- useReducer：复杂状态管理
- useMemo 和 useCallback：性能优化