---
topic: Test Existing Author
author: AnotherAuthor
created: 2026-01-01 10:00
modified: 2026-02-08 16:45
status: draft
tags:
- 待分类
---

# Test Existing Author

这个笔记已经有一个 author 字段设置为 "AnotherAuthor"。

## 验证点

自动化脚本应该：
1. 保留现有的 author 值 "AnotherAuthor"
2. 不覆盖为默认值 "Crzhu"
3. 正常更新其他字段（如 modified）