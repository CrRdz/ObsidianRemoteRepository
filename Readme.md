# Obsidian-Git-Sync-Protocol 	<img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey?style=flat-square" />
<p align="center">
  <img src="https://img.shields.io/badge/Editor-Obsidian-483699?style=flat-square&logo=obsidian&logoColor=white" />
  <img src="https://img.shields.io/badge/Format-Markdown-000000?style=flat-square&logo=markdown&logoColor=white" />
  <img src="https://img.shields.io/badge/Storage-GitHub-181717?style=flat-square&logo=github&logoColor=white" />
	<img src="https://img.shields.io/badge/Workflow-Git--Based-F05032?style=flat-square&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/Method-Zettelkasten-black?style=flat-square&logo=icloud&logoColor=white" />
<img src="https://img.shields.io/badge/Sync-Automated-brightgreen?style=flat-square&logo=githubactions&logoColor=white" />

<!-- STATS START -->
<p align="center">
  <img src="https://img.shields.io/badge/Notes-62-2ea44f?style=flat-square" />
  <img src="https://img.shields.io/badge/Words-165.0k-007ec6?style=flat-square" />
  <img src="https://img.shields.io/badge/Last_Update-2026--02--04%2019%3A40-critical?style=flat-square" />
</p>
<p align="center">
  <img src="Assets/heatmap.svg" alt="2026 Contribution Heatmap" />
</p>

<!-- STATS END -->

</p>

本文档规范了在 Windows 和 macOS 之间同步 Obsidian 笔记的标准流程。

---
**核心原则：**

1. **初始化阶段**：使用命令行（CLI）进行仓库克隆。

2. **日常使用**：完全依赖 **Obsidian Git 插件** 自动化管理 避免同时多个设备编辑同一文档。

3. **同步策略**：10分钟无操作自动同步 + 启动时自动拉取。

4. Git 只用于管理**笔记内容和必要配置**，不管理本地状态

5. Obsidian 的部分配置文件**不适合纳入版本控制**

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

---
## 二、Obsidian Git 插件核心设置 

在clone完成之后 请先检查obsidian插件是否成功同步 如未按照预期 执行以下步骤

为了实现自动化和统一的日志格式，请在 **Settings -> Obsidian Git** 中进行如下设置：

### 1. 自动化策略

- **Auto commit-and-sync interval (minutes):** `10`
    
    - _(设置 10 分钟自动备份)_
    - _(建议搭配电脑休眠时间设置)_
        
- **Auto commit-and-sync after stop file edits:** `ON` 
    
    - _(配合上一条，确保是有变动才备份)_
        
- **Auto pull interval(minutes):** `30`
    
    - _(设置30分钟拉取远程仓库)_
        
- **Specify custom commit message on auto commit-and-sync**:`ON`
    
    - _(指定commit的message)_
	      
- **Pull on startup:**`ON`

### 2. 提交信息格式 (Commit Message)

请严格复制以下内容填入对应设置项，以保持日志整洁：

- **Commit Message:**
	```Plaintext
	vault sync: {{date}} | {{hostname}} | {{numFiles}} files
	```
	- _(Hostname: mac | windows 后续如有扩展 另行规范)_
	
- **List filenames affected by commit in commit body:** `开启`
    
    - _(这会自动在 commit message 下一行附带 affected files 列表)_
        
- **Date format:** `YYYY-MM-DD HH:mm

---

## 三、日常使用指南

### 正常工作流

1. **打开 Obsidian**：插件自动运行 `Pull`。
    
2. **写作/编辑**：正常使用 注意遵守命名规范。
    
3. **自动同步**：每隔 10 分钟，如果有变动，插件会自动 `Commit` 并 `Push`。
    
4. **手动同步 (可选)**：
    
    - 如果你写完想立刻关机，按 `Cmd/Ctrl + P` 调出命令面板。
        
    - 输入并执行：`Git: Create backup`。
### **更推荐的工作流**   

1. **打开 Obsidian**：插件自动运行 `Pull`。
    
2. **写作/编辑**：仅单个设备对仓库进行操作 注意遵守命名规范。
    
3. **自动同步**：每隔 10 分钟，如果有变动，插件会自动 `Commit` 并 `Push`。
	
4. **手动同步**：在完成一次笔记编辑之后 手动进行一次commit-and-sync 
	
5. **关闭程序**：每次短期的完成笔记任务后 关闭程序 以便于在打开时候运行一次pull 

---
## 四、跨平台命名/使用规范

由于 macOS 和 Windows 文件系统底层逻辑不同，在 Mac 上操作时必须遵守以下规则，否则会导致 Windows 端同步失败或文件无法打开。

### 1. 严禁使用的特殊字符

Windows 文件名不支持以下字符。**在 Mac 上创建笔记或附件时，绝对不能包含：**

| **字符** | **名称** | **替代方案**         |
| ------ | ------ | ---------------- |
| `/`    | 斜杠     | 使用 `-` 或空格       |
| `\`    | 反斜杠    | 使用 `-` 或空格       |
| `:`    | 冒号     | 使用中文冒号 `：` 或 `-` |
| `*`    | 星号     | (无)              |
| `?`    | 问号     | 使用中文问号 `？`       |
| `"`    | 双引号    | 使用单引号 `'`        |
| `<`    | 小于号    | (无)              |
| `>`    | 大于号    | (无)              |
| `      | `      | ｜                |

> **例子**：在 Mac 上命名 `2024/01/01:会议记录` 是合法的，但在 Windows 上会直接报错。请改为 `2024-01-01-会议记录`。

### 2. 文件名大小写敏感问题

- **Windows**: 不区分大小写 (`Note.md` 和 `note.md` 是同一个文件)。
    
- **Git/Linux**: 区分大小写。
    
- **操作禁忌**：不要在 Obsidian 中直接**仅修改文件名的大小写**（例如把 `Work.md` 重命名为 `work.md`）。
    
    - **后果**：这极易导致 Git 识别错误，产生两个看起来一样的文件，或者导致 Windows 端同步死循环。
        
    - **正确做法**：如果必须修改大小写，先重命名为其他名字（如 `Work_tmp.md`），提交一次，再改回 `work.md`。
        

### 3. 避免超长路径

Windows 对文件路径长度有限制（默认 260 字符）。尽量避免创建过深的文件夹层级（例如超过 5-6 层嵌套），防止同步失败。

---
## 五、推荐的 `.gitignore`

在仓库根目录创建或编辑 `.gitignore`：

```gitignore
# macOS
.DS_Store

# Obsidian local state
.obsidian/workspace*
.obsidian/graph.json
.obsidian/cache
```

  

说明：

- `workspace*`：窗口与面板布局，不同设备必然冲突

- `cache`：缓存文件，不具备同步意义

- 这里比较推荐将/plugin pull上去 以便同步插件


---

  

## 六、已经误提交上述文件的修复方法

  

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

  

## 六、常见问题与处理方案

### 1. 推送时提示 rejected / diverged (插件无法推送)

**场景**：远程版本比本地新，且历史分叉。 **修复**（强制以远程为准，注意备份本地未保存内容）：
若确认以远程仓库为准，可直接重置本地：
```bash
git reset --hard
git clean -fd
git fetch origin
git reset --hard origin/master
```
> 若你的主分支不是 `master`，请替换为实际分支名
---
### 2. 插件提示 "Pull failed" 或冲突

**场景**：本地和远程修改了同一个文件的同一行。 **修复**：


```Bash
# 1. 尝试手动拉取（可能会提示合并）
git pull

# 2. 如果提示冲突 (Conflict)，打开对应的 .md 文件
# 手动搜索 "<<<<<<<" 标记，修改内容后保存。

# 3. 提交修复
git add .
git commit -m "manual fix: resolve merge conflict"
git push
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

├─ .../

├─ .obsidian/

├─ Asserts

├─ plugins/ # 可选同步

└─ core-plugins.json

```

  

---
## 八、快捷键指南

`F11` 创建代码块

`Ctrl + F` 正则查找/替换（依赖Regex Find/replace)

`Ctrl + Shift + F` 原生查找/替换

---
## 九、字体asserts

代码块： Jetbrain mono

正文：仓耳今楷02-W04

---
## 十、总结

  

- Git 用于内容版本管理，而非环境同步

- 避免提交系统文件与 Obsidian 本地状态

- 严格遵循 `pull → edit → commit → push` 的工作流

  

当出现问题时，本 README 中的命令可直接用于恢复仓库状态。
