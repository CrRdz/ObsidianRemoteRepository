# Obsidian + Git 使用与故障修复指南
  
本文档旨在提供一套 **稳定、可复制、可恢复** 的使用规范，避免常见冲突，并在出现问题时可以快速修复。

  

---

  

## 一、基本原则

  

1. Git 只用于管理**笔记内容和必要配置**，不管理本地状态

2. Obsidian 的部分配置文件**不适合纳入版本控制**

3. 只选择一种 Git 使用方式：

- 命令行，或

- Obsidian Git 插件

不建议多种工具混用

  

---

  

## 二、推荐的 `.gitignore`

  

在仓库根目录创建或编辑 `.gitignore`：

  

```gitignore

# macOS

.DS_Store

  

# Obsidian 本地状态文件

.obsidian/workspace*

.obsidian/cache/

.obsidian/graph.json

.obsidian/hotkeys.json

.obsidian/appearance.json

  

# 如不希望同步插件配置，可取消注释

# .obsidian/plugins/

```

  

说明：

- `workspace*`：窗口与面板布局，不同设备必然冲突

- `cache`：缓存文件，不具备同步意义

  

---

  

## 三、已经误提交上述文件的修复方法

  

`.gitignore` 只对**尚未被跟踪的文件**生效，已提交文件需要手动移除其 Git 记录。

  

```bash

git rm -r --cached .DS_Store

git rm -r --cached .obsidian/workspace*

git rm -r --cached .obsidian/cache

```

  

然后提交并推送：

  

```bash

git add .gitignore

git commit -m "chore: remove local Obsidian and OS files"

git push

```

  

---

  

## 四、日常标准推送流程

  

每一次修改并推送时，严格遵循以下顺序：

  

```bash

git pull

# 编辑或新增笔记

git add .

git commit -m "docs: update notes"

git push

```

  

该流程可以最大限度避免远程与本地历史分叉。

  

---

  

## 五、常见问题与处理方案

  

### 1. 推送时提示 rejected / diverged

  

原因：本地分支与远程分支历史不一致。

  

若确认以远程仓库为准，可直接重置本地：

  

```bash

git reset --hard

git clean -fd

git fetch origin

git reset --hard origin/master

```

  

> 若你的主分支不是 `master`，请替换为实际分支名

  

---

  

### 2. Obsidian Git 插件频繁报错

  

常见原因：

- 自动 pull / push 与手动操作冲突

- 与命令行 Git 混用

  

建议插件设置：

- 关闭 Auto pull

- 关闭 Auto commit

- 关闭 Auto push

  

仅在需要时手动执行 Commit 与 Push。

  

---

  

## 六、彻底清理方案（不建议频繁使用）

  

当仓库历史已不可维护时，可选择以下方案之一。

  

### 方案 A：删除本地仓库并重新克隆（推荐）

  

```bash

cd ..

rm -rf <repo-directory>

git clone <repo-url>

```

  

### 方案 B：重建 Git 历史（会覆盖远程）

  

```bash

rm -rf .git

git init

git remote add origin <repo-url>

git add .

git commit -m "chore: reinitialize repository"

git branch -M main

git push -f origin main

```

  

---

  

## 七、推荐仓库结构

  

```text

Vault/

├─ README.md

├─ .gitignore

├─ y3s1/

│ ├─ course1.md

│ ├─ course2.md

│ └─ ...

└─ .obsidian/

├─ plugins/ # 可选同步

└─ core-plugins.json

```

  

---

  

## 八、总结

  

- Git 用于内容版本管理，而非环境同步

- 避免提交系统文件与 Obsidian 本地状态

- 严格遵循 `pull → edit → commit → push` 的工作流

  

当出现问题时，本 README 中的命令可直接用于恢复仓库状态。