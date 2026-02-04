import os
import re
import subprocess
import datetime
from openai import OpenAI

# 配置
API_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
REVIEWS_DIR = "Reviews"

# 要排除的路径
EXCLUDE_PATHS = [
    '.git', '.github', '.gitignore', '.obsidian',
    'node_modules', 'Assets', 'assets',
    'Reviews', 'README', 'LICENSE'
]

# 初始化 API
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=API_BASE_URL
)


def get_week_info():
    """获取当前周信息"""
    today = datetime.date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    last_sunday = today - datetime.timedelta(days=days_since_sunday)
    last_monday = last_sunday - datetime.timedelta(days=6)

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

    # 检查文件名
    basename = os.path.basename(path_lower)
    if basename.startswith('readme') or basename.startswith('license'):
        return True

    # 检查路径中的文件夹
    parts = path.split('/')
    for part in parts:
        for exclude in EXCLUDE_PATHS:
            if exclude.lower() in part.lower():
                return True

    return False


def extract_topic_from_path(file_path):
    """
    从文件路径提取主题
    例如：
    - Y3S2 Notes/CPT203/Week1.md → CPT203
    - Java Notes/JVM.md → Java Notes
    - LeetCode/Tree.md → LeetCode
    """
    parts = file_path.split('/')

    if len(parts) == 1:
        # 根目录下的文件
        return 'Other'

    # 第一层文件夹名称
    top_folder = parts[0]

    # 如果是学期文件夹（Y3S2 Notes），取第二层（课程代码）
    if re.match(r'Y\d+S\d+\s*Notes?', top_folder, re.IGNORECASE):
        if len(parts) > 1:
            return parts[1]  # CPT203, CPT205...
        else:
            return top_folder

    # 否则直接返回第一层文件夹名称
    return top_folder


def get_weekly_changes(start_date, end_date):
    """获取本周的笔记变更，按主题分类"""
    try:
        # 获取本周新增/修改的 .md 文件
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
        files = list(set(files))  # 去重

        # 过滤排除的文件
        files = [f for f in files if not should_exclude_path(f)]

        print(f"📄 Found {len(files)} modified files this week")

        # 按主题分类
        topics = {}  # {topic: [{file, content}]}

        for file in files:
            try:
                # 提取主题
                topic = extract_topic_from_path(file)

                # 获取文件的 diff 内容
                cmd_diff = [
                    'git', 'log',
                    f'--since={start_date}',
                    f'--until={end_date} 23:59:59',
                    '-p',
                    '--',
                    file
                ]

                diff = subprocess.check_output(cmd_diff, text=True)

                # 提取新增的行
                added_lines = []
                for line in diff.splitlines():
                    if line.startswith('+') and not line.startswith('+++'):
                        content = line[1:].strip()
                        # 过滤无用内容
                        if (content
                                and len(content) > 5
                                and not content.startswith('---')
                                and not content.startswith('```')
                                and not content.startswith('#')):  # 过滤标题
                            added_lines.append(content)

                if not added_lines:
                    continue

                # 每个文件最多保留 1000 字符
                content = '\n'.join(added_lines)[:1000]

                # 存储
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
        print(f"Error: {e}")
        return {}


def generate_review_with_ai(topics, week_info):
    """使用 AI 生成周报"""
    if not topics:
        print("No changes this week")
        return None

    # 构建内容摘要
    content_parts = []

    for topic, files in sorted(topics.items()):
        content_parts.append(f"## {topic}\n")
        for file_data in files[:5]:  # 每个主题最多 5 个文件
            content_parts.append(f"### {file_data['file']}\n")
            content_parts.append(f"{file_data['content']}\n\n")

    combined_content = "".join(content_parts)

    # 统计
    topics_list = ', '.join(sorted(topics.keys()))
    total_files = sum(len(files) for files in topics.values())

    # ✅ 简化的 Prompt
    prompt = f"""你是一位学习助手。我是 XJTLU 的学生，请根据我本周（{week_info['week_str']}）的笔记新增内容，生成一份简洁的学习周报。

## 📊 本周统计
- 学习主题：{topics_list}
- 笔记数量：{total_files} 篇

## 📝 周报格式要求

请按以下结构输出：

### 1. 📊 本周概览
用 2-3 句话总结：
- 本周学了哪些主题（如 CPT203, CPT205, Java Web, Redis）
- 整体学习强度和深度的评价

### 2. 📚 学习内容
**按主题（topic）分别总结**，直接用二级标题，例如：

## CPT203
- 学习了...
- 掌握了...

## CPT205  
- 深入理解了...

## Java Web
- 搭建了...

## Redis
- 学习了...

**要求**：
- 每个主题单独一个二级标题（##）
- 总结核心知识点，不要流水账
- 专业术语保留英文，解释用中文
- 如果某个主题学得特别深入，多写一些

### 3. 💡 本周金句
从笔记中提取 1-2 句最有价值的原文或关键理解

## 🎯 语言风格
- **中英混合**：专业术语英文（如 Binary Search Tree），解释中文
- **简洁专业**：提炼核心，不啰嗦
- **自然流畅**：像学长写的总结，不要太正式

## 📚 本周笔记内容

{combined_content}

---

请生成周报，记住：
1. 只输出 3 个部分（概览、学习内容、金句）
2. 学习内容部分按主题平铺，不要嵌套分类
3. 不要添加"下周计划""学习建议"等额外内容
"""

    try:
        print("🤖 Calling DeepSeek API...")

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """你是一位学习助手，擅长总结笔记。

特点：
- 按主题（topic）平铺总结，不做嵌套分类
- 中英混合自然（专业术语英文，解释中文）
- 简洁专业，提炼核心
- 语言自然，像学长写的复盘

你不会：
- 过度分类（如分"课程"和"自学"）
- 添加用户未要求的内容
- 机械罗列笔记"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2500
        )

        review_content = response.choices[0].message.content

        # 添加头部
        header = f"""---
week: {week_info['week_str']}
period: {week_info['start']} ~ {week_info['end']}
topics: [{topics_list}]
files: {total_files}
generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
---

# 📅 Week {week_info['week']} Learning Review

> {week_info['start'].strftime('%b %d')} - {week_info['end'].strftime('%b %d, %Y')}

---

"""

        return header + review_content

    except Exception as e:
        print(f"API Error: {e}")
        return None


def save_review(content, week_info):
    """保存周报"""
    os.makedirs(REVIEWS_DIR, exist_ok=True)

    filename = f"Weekly-Review-{week_info['week_str']}.md"
    filepath = os.path.join(REVIEWS_DIR, filename)

    if os.path.exists(filepath):
        print(f"File exists: {filepath}")
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
    print(f"\n Week: {week_info['week_str']}")
    print(f"   Period: {week_info['start']} ~ {week_info['end']}")

    # 获取本周变更
    topics = get_weekly_changes(week_info['start'], week_info['end'])

    if not topics:
        print("\n⚠️  No changes found.")
        return

    # 统计
    print(f"\n📊 Topics this week:")
    for topic, files in sorted(topics.items()):
        print(f"   • {topic}: {len(files)} files")

    # 生成周报
    review = generate_review_with_ai(topics, week_info)

    if not review:
        print("\nFailed to generate review")
        return

    print("\n📝 Preview:")
    print("-" * 70)
    print(review[:600] + "\n...")
    print("-" * 70)

    # 保存
    if save_review(review, week_info):
        print("\n" + "=" * 70)
        print("Complete!")
        print(f"{REVIEWS_DIR}/Weekly-Review-{week_info['week_str']}.md")
        print("=" * 70)


if __name__ == "__main__":
    main()
