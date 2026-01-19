# Obsidian 跨平台 Git 同步指南

本文档规范了在 Windows 和 macOS 之间同步 Obsidian 笔记的标准流程。

---
**核心原则：**

1. **初始化阶段**：使用命令行（CLI）进行仓库克隆。

2. **日常使用**：完全依赖 **Obsidian Git 插件** 自动化管理。

3. **同步策略**：10分钟无操作自动同步 + 启动时自动拉取。

4. Git 只用于管理**笔记内容和必要配置**，不管理本地状态; Obsidian 的部分配置文件**不适合纳入版本控制**
  
---

## 一、新设备初始化流程 

当你在一台**从未安装过**此笔记库的新电脑（Mac 或 PC）上配置时，请严格按照以下步骤操作：

### 1. 准备环境

- 安装 [Git](https://git-scm.com/)。
    
- 安装 [Obsidian](https://obsidian.md/)。
    

### 2. 克隆仓库 (使用命令行)

打开终端 (Mac Terminal 或 Win PowerShell)，进入你想存放笔记的目录：

```Bash
# 1. 进入目录
cd ~/Documents  # 或其他你想要的位置

# 2. 克隆远程仓库
git clone git@github.com:CrRdz/ObsidianRemoteRepository.git
```

### 3. 打开与插件配置

1. 打开 Obsidian，选择 **"打开现有仓库" (Open folder as vault)**，选中刚才克隆下来的文件夹。
    
2. Obsidian 会自动加载 `.obsidian` 中的插件（如果你同步了插件文件夹）。
    
3. **检查 Obsidian Git 插件配置**（见下文 "插件核心设置"），确保每台设备配置一致。

## 二、Obsidian Git 插件核心设置 

为了实现自动化和统一的日志格式，请在 **Settings -> Obsidian Git** 中进行如下设置：

### 1. 自动化策略

- **Backup interval (minutes):** `10`
    
    - _(设置 10 分钟自动备份)_
        
- **Auto Backup after changes:** `开启` (建议)
    
    - _(配合上一条，确保是有变动才备份)_
        
- **Pull updates on startup:** `开启`
    
    - _(**关键**：每次打开软件自动拉取，防止冲突)_
        
- **Push on backup:** `开启`
    
    - _(备份同时推送到远程)_
        

### 2. 提交信息格式 (Commit Message)

请严格复制以下内容填入对应设置项，以保持日志整洁：

- **Commit Message:**
    
    Plaintext
    
    ```
    vault sync: {{date}} | {{hostname}} | {{numFiles}} files
    ```
    
- **List changed files in commit body:** `开启`
    
    - _(这会自动在 commit message 下一行附带 affected files 列表)_
        
- **Date format:** `YYYY-MM-DD HH:mm:ss`
    

---

## 三、日常使用指南

### 正常工作流

1. **打开 Obsidian**：插件自动运行 `Pull`。
    
2. **写作/编辑**：正常使用。
    
3. **自动同步**：每隔 10 分钟，如果有变动，插件会自动 `Commit` 并 `Push`。
    
4. **手动同步 (可选)**：
    
    - 如果你写完想立刻关机，按 `Cmd/Ctrl + P` 调出命令面板。
        
    - 输入并执行：`Git: Create backup`。
        

### 状态检查

- 查看底部状态栏：
    
    - `git: ready` 表示无变动。
        
    - `git: pushing...` 表示正在上传。
        
    - `git: synced` 表示同步完成。

## 二、推荐的 `.gitignore`

  

在仓库根目录创建或编辑 `.gitignore`：

  

```gitignore

# macOS

.DS_Store

  

# Obsidian 本地状态文件

.obsidian/workspace*

.obsidian/cache/

.obsidian/graph.json
  

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