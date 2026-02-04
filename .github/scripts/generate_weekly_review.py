import os
import re
import subprocess
import datetime
from openai import OpenAI

# 配置
API_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat" 
REVIEWS_DIR = "Reviews/Weekly"

EXCLUDE_PATHS = [
    '.git', '.github', '.gitignore', '.obsidian',
    'node_modules', 'Assets', 'assets',
    'Reviews', 'README', 'LICENSE'
]

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=API_BASE_URL
)

def get_beijing_time():
    """获取北京时间（UTC+8）"""
    utc_now = datetime.datetime.utcnow()
    beijing_time = utc_now + datetime.timedelta(hours=8)
    return beijing_time

def get_week_info():
    """智能判断：周日生成本周，其他时间生成上周"""
    today = datetime.date.today()
    
    if today.weekday() == 6:  # 周日
        last_sunday = today
        last_monday = today - datetime.timedelta(days=6)
        print("ℹ️  Generating THIS WEEK's review")
    else:
        days_since_last_sunday = (today.weekday() + 1) % 7
        last_sunday = today - datetime.timedelta(days=days_since_last_sunday)
        last_monday = last_sunday - datetime.timedelta(days=6)
        print("ℹ️  Generating LAST WEEK's review")
    
    year, week, _ = last_sunday.isocalendar()
    
    return {
        'year': year,
        'week': week,
        'start': last_monday,
        'end': last_sunday,
        'week_str': f"{year}-W{week:02d}"
    }

def should_exclude_path(path):
    """判断路径是否应该被排除"""
    path_lower = path.lower()
    basename = os.path.basename(path_lower)
    
    if basename.startswith('readme') or basename.startswith('license'):
        return True
    
    parts = path.split('/')
    for part in parts:
        for exclude in EXCLUDE_PATHS:
            if exclude.lower() in part.lower():
                return True
    
    return False

def extract_topic_from_path(file_path):
    """从文件路径提取主题"""
    parts = file_path.split('/')
    
    if len(parts) == 1:
        return 'Other'
    
    top_folder = parts[0]
    
    if re.match(r'Y\d+S\d+\s*Notes?', top_folder, re.IGNORECASE):
        if len(parts) > 1:
            return parts[1]
        else:
            return top_folder
    
    return top_folder

def get_weekly_changes(start_date, end_date):
    """获取本周的笔记变更，按主题分类"""
    try:
        cmd = [
            'git', 'log',
            f'--since={start_date}',
            f'--until={end_date} 23:59:59',
            '--pretty=format:',
            '--name-only',
            '--diff-filter=AM',
            '--',
            '*.md'
        ]

        result = subprocess.check_output(cmd, text=True)
        files = [f.strip() for f in result.splitlines() if f.strip()]
        files = list(set(files))
        files = [f for f in files if not should_exclude_path(f)]

        print(f"📄 Found {len(files)} modified files this week")

        topics = {}

        for file in files:
            try:
                topic = extract_topic_from_path(file)

                cmd_diff = [
                    'git', 'log',
                    f'--since={start_date}',
                    f'--until={end_date} 23:59:59',
                    '-p',
                    '--',
                    file
                ]

                diff = subprocess.check_output(cmd_diff, text=True)

                # ✅ 优化：保留标题
                added_lines = []
                for line in diff.splitlines():
                    if line.startswith('+') and not line.startswith('+++'):
                        content = line[1:].strip()
                        
                        if not content:
                            continue
                        if content == '---':
                            continue
                        if content.startswith('```'):
                            continue
                        if len(content) < 3:
                            continue
                        
                        added_lines.append(content)

                if not added_lines:
                    continue

                # ✅ 增加到 1500 字符
                content = '\n'.join(added_lines)[:1500]

                if topic not in topics:
                    topics[topic] = []

                topics[topic].append({
                    'file': os.path.basename(file),
                    'content': content
                })

            except subprocess.CalledProcessError as e:
                print(f"⚠️  Skip {file}: {e}")
                continue

        return topics

    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

def generate_review_with_ai(topics, week_info):
    """使用 AI 生成周报"""
    if not topics:
        print("⚠️  No changes this week")
        return None

    content_parts = []
    for topic, files in sorted(topics.items()):
        content_parts.append(f"## 📁 主题: {topic}\n")
        for file_data in files[:6]:
            content_parts.append(f"### 📄 文件: {file_data['file']}\n")
            content_parts.append(f"{file_data['content']}\n\n")

    combined_content = "".join(content_parts)
    topics_list = ', '.join(sorted(topics.keys()))
    total_files = sum(len(files) for files in topics.values())

    prompt = f"""你是一位专业的学习助手，擅长总结学生的学习笔记。

## 📊 任务背景
我是 XJTLU 的计算机专业学生，本周（{week_info['week_str']}）更新了以下笔记：
- 涉及主题: {topics_list}
- 笔记文件数: {total_files} 篇

请根据下面的笔记内容，生成一份**简洁、专业、有深度**的学习周报。

---

## 📝 周报格式要求

### 第一部分: 📊 Weekly Overview（本周概览）

用 **2-3 句话** 总结：
1. 本周学了哪些主题（列举具体的课程或技术方向）
2. 学习的深度和广度如何（是深入某个点，还是广泛涉猎）
3. 整体学习状态的评价（充实、节奏快、某个主题学得特别深入等）

**示例**：
> 本周主要学习了 CPT304 数据库系统和 CPT401 高级算法，深入研究了 B+ Tree 索引优化和动态规划问题。整体学习深度较高，特别是在索引失效场景的排查上有了系统性理解。

---

### 第二部分: 📚 Learning Content（学习内容）

**按主题（topic）分别总结**，每个主题用一个 **二级标题 ##**：

**格式要求**：
- 每个主题独立成段，用 `## 主题名` 开头
- 总结该主题的 **核心知识点**（3-5 个要点）
- 专业术语**保留英文**，必要时加中文注释
- 如果某个主题内容特别深入，多写 1-2 段
- 用 **列表** 或 **分点** 呈现，不要大段文字

**示例**：

## CPT304

### B+ Tree 索引优化
- 理解了为什么数据库用 B+ Tree 而不是 Binary Tree：
  - 减少磁盘 I/O（一个节点存多个 key）
  - 叶子节点有链表，范围查询 O(k + log n)
  
- **索引失效的 5 种场景**（重要）：
  - `WHERE YEAR(date) = 2026` ❌ → 应改为范围查询
  - 复合索引不满足最左前缀原则

---

### 第三部分: 💡 Key Insights（关��收获）

**从笔记中提取 1-2 句最有价值的内容**，格式如下：

> "引用的原文或自己的核心理解"

**要求**：
- 必须是本周学习中最重要的顿悟或总结
- 用引用格式（`> "..."`）

---

## 🎯 语言风格要求

1. **中英混合自然**：
   - ✅ "学习了 Binary Search Tree 的平衡性优化"
   
2. **简洁专业**：
   - ✅ 提炼核心，用列表呈现
   - ❌ 大段文字、流水账

3. **像学长写的复盘**：
   - ✅ 专业但不生硬，有个人见解

---

## ⚠️ 严格禁止

1. ❌ 不要添加"下周计划"、"学习建议"等我没要求的内容
2. ❌ 不要过度分类（如分"课程学习"和"自学内容"）
3. ❌ 不要机械罗列笔记内容，必须提炼总结

---

## 📚 本周笔记原始内容

{combined_content}

---

**请严格按照上述格式生成周报，只输出三个部分：Weekly Overview + Learning Content + Key Insights**
"""

    try:
        print("🤖 Calling DeepSeek API...")

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """你是一位专业的学习助手，专门帮助大学生总结学习笔记。

你的特点：
1. 擅长从大量笔记中提炼核心知识点
2. 输出简洁、结构化，不啰嗦
3. 中英混合自然（专业术语英文，解释中文）
4. 语言风格像学长写的复盘，有深度但不生硬

你绝对不会：
1. 添加用户未要求的内容
2. 过度分类或嵌套结构
3. 机械罗列笔记"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000
        )

        review_content = response.choices[0].message.content

        # ✅ 使用北京时间
        beijing_now = get_beijing_time()
        
        footer = f"""

---

<div align="center">

*Generated by [DeepSeek Chat](https://www.deepseek.com) | {beijing_now.strftime('%Y-%m-%d %H:%M')} (UTC+8)*

</div>
"""

        header = f"""---
week: {week_info['week_str']}
period: {week_info['start']} ~ {week_info['end']}
topics: [{topics_list}]
files: {total_files}
generated: {beijing_now.strftime('%Y-%m-%d %H:%M')}
timezone: UTC+8
model: deepseek-chat
---

# 📅 Week {week_info['week']} Learning Review

> 🎓 **XJTLU** | {week_info['start'].strftime('%b %d')} - {week_info['end'].strftime('%b %d, %Y')}

---

"""

        return header + review_content + footer

    except Exception as e:
        print(f" API Error: {e}")
        return None

def save_review(content, week_info):
    """保存周报"""
    os.makedirs(REVIEWS_DIR, exist_ok=True)

    filename = f"Weekly-Review-{week_info['week_str']}.md"
    filepath = os.path.join(REVIEWS_DIR, filename)

    if os.path.exists(filepath):
        print(f"⚠️  File exists: {filepath}")
        if not os.environ.get('GITHUB_ACTIONS'):
            response = input("Overwrite? (y/n): ").lower()
            if response != 'y':
                return False
        print("Overwriting...")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Saved: {filepath}")
    return True

def main():
    print("=" * 70)
    print("📚 Weekly Review Generator")
    print("=" * 70)

    week_info = get_week_info()
    print(f"\n📅 Week: {week_info['week_str']}")
    print(f"   Period: {week_info['start']} ~ {week_info['end']}")

    topics = get_weekly_changes(week_info['start'], week_info['end'])

    if not topics:
        print("\n⚠️  No changes found.")
        return

    print(f"\n📊 Topics this week:")
    for topic, files in sorted(topics.items()):
        print(f"   • {topic}: {len(files)} files")

    review = generate_review_with_ai(topics, week_info)

    if not review:
        print("\n❌ Failed to generate review")
        return

    # ✅ 显示当前时间
    beijing_now = get_beijing_time()
    print(f"\n⏰ Current time: {beijing_now.strftime('%Y-%m-%d %H:%M')} (UTC+8)")
    
    print("\n📝 Preview:")
    print("-" * 70)
    print(review[:600] + "\n...")
    print("-" * 70)

    if save_review(review, week_info):
        print("\n" + "=" * 70)
        print("✅ Complete!")
        print(f"📂 {REVIEWS_DIR}/Weekly-Review-{week_info['week_str']}.md")
        print("=" * 70)

if __name__ == "__main__":
    main()
