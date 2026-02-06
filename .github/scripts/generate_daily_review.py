import os
import re
import subprocess
import datetime
import sys
import argparse
from openai import OpenAI

# 配置
API_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
REVIEWS_DIR = "Reviews/Daily"

# 排除路径
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

def get_beijing_time():
    """获取北京时间（UTC+8）"""
    utc_now = datetime.datetime.utcnow()
    beijing_time = utc_now + datetime.timedelta(hours=8)
    return beijing_time

def parse_date_input(date_str):
    """
    解析日期输入
    支持格式：
    - YYYY-MM-DD (2026-02-05)
    - YYYYMMDD (20260205)
    - MM-DD (02-05, 默认当前年份)
    """
    try:
        # 尝试 YYYY-MM-DD
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        pass
    
    try:
        # 尝试 YYYYMMDD
        return datetime.datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        pass
    
    try:
        # 尝试 MM-DD（使用当前年份）
        current_year = datetime.date.today().year
        return datetime.datetime.strptime(f"{current_year}-{date_str}", '%Y-%m-%d').date()
    except ValueError:
        pass
    
    raise ValueError(f"Invalid date format: {date_str}. Supported formats: YYYY-MM-DD, YYYYMMDD, MM-DD")

def get_date_info(days_ago=None, target_date=None):
    """
    获取日期信息
    days_ago: 0=今天, 1=昨天, 2=前天...
    target_date: 指定日期 (datetime.date 对象)
    """
    if target_date:
        date_obj = target_date
    elif days_ago is not None:
        date_obj = datetime.date.today() - datetime.timedelta(days=days_ago)
    else:
        date_obj = datetime.date.today()
    
    # 中文星期
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    weekday_cn = weekdays[date_obj.weekday()]
    
    return {
        'date': date_obj,
        'date_str': date_obj.strftime('%Y-%m-%d'),
        'date_cn': date_obj.strftime('%Y年%m月%d日'),
        'weekday': weekday_cn,
        'display': f"{date_obj.strftime('%Y-%m-%d')} 周{weekday_cn}"
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

def get_daily_changes(target_date):
    """获取指定日期的笔记变更"""
    date_str = target_date.strftime('%Y-%m-%d')
    next_date_str = (target_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        cmd = [
            'git', 'log',
            f'--since={date_str} 00:00:00',
            f'--until={next_date_str} 00:00:00',
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
        
        print(f"📄 Found {len(files)} modified files on {date_str}")
        
        if not files:
            return {}
        
        topics = {}
        
        for file in files:
            try:
                topic = extract_topic_from_path(file)
                
                cmd_diff = [
                    'git', 'log',
                    f'--since={date_str} 00:00:00',
                    f'--until={next_date_str} 00:00:00',
                    '-p',
                    '--',
                    file
                ]
                
                diff = subprocess.check_output(cmd_diff, text=True)
                
                added_lines = []
                for line in diff.splitlines():
                    if line.startswith('+') and not line.startswith('+++'):
                        content = line[1:].strip()
                        if (content 
                            and len(content) > 3
                            and content != '---'
                            and not content.startswith('```')):
                            added_lines.append(content)
                
                if not added_lines:
                    continue
                
                content = '\n'.join(added_lines)[:1200]
                
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

def generate_daily_review(topics, date_info):
    """使用 AI 生成日报"""
    if not topics:
        return None
    
    content_parts = []
    
    for topic, files in sorted(topics.items()):
        content_parts.append(f"## 📁 主题: {topic}\n")
        for file_data in files[:5]:
            content_parts.append(f"### 📄 文件: {file_data['file']}\n")
            content_parts.append(f"{file_data['content']}\n\n")
    
    combined_content = "".join(content_parts)
    topics_list = ', '.join(sorted(topics.keys()))
    total_files = sum(len(files) for files in topics.values())
    
    prompt = f"""你是一位专业的学习助手，擅长总结学生的每日学习笔记。

## 📊 任务背景
我是 XJTLU 的计算机专业学生，{date_info['display']} 这天更新了以下笔记：
- 涉及主题: {topics_list}
- 笔记文件数: {total_files} 篇

请根据下面的笔记内容，生成一份**简洁、专业**的学习日报。

---

## 📝 日报格式要求

### 第一部分: 📊 Today's Focus（今日聚焦）

用 **1-2 句话** 总结今天的学习重点。

**示例**：
> 今天主要学习了 CPT304 的数据库索引优化，深入理解了 B+ Tree 的工作原理和索引失效场景。

---

### 第二部分: 📚 Learning Notes（学习笔记）

**按主题（topic）分别总结**，每个主题用一个 **二级标题 ##**：

**格式要求**：
- 每个主题独立成段，用 `## 主题名` 开头
- 总结该主题的 **核心知识点**（2-3 个要点）
- 专业术语**保留英文**，必要时加中文注释
- 用 **列表** 呈���，简洁明了

**示例**：

## CPT304

- **B+ Tree 索引优化**
  - 理解了为什么数据库用 B+ Tree：减少磁盘 I/O，一个节点存多个 key
  - 学习了索引失效的几种场景：WHERE 条件用函数、隐式类型转换等

## Java Web

- 学习了 Spring Boot 的依赖注入 (DI) 机制
- 实践了 RESTful API 的设计

---

### 第三部分: 💡 Key Takeaway（关键收获）

**用 1 句话** 总结今天最大的收获或理解。

**示例**：
> "索引不是万能的，WHERE 条件用了函数会导致索引失效，这是优化慢查询的关键认知。"

---

## 🎯 语言风格要求

1. **中英混合自然**：专业术语英文，解释中文
2. **简洁专业**：提炼核心，不啰嗦
3. **像学习笔记**：直接、清晰

---

## ⚠️ 严格禁止

1. ❌ 不要添加"明天计划"、"学习建议"等我没要求的内容
2. ❌ 不要过度分类
3. ❌ 不要机械罗列笔记内容

---

## 📚 笔记原始内容

{combined_content}

---

**请严格按照上述格式生成日报，只输出三个部分：Today's Focus + Learning Notes + Key Takeaway**
"""

    try:
        print("🤖 Calling DeepSeek API...")
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """你是一位专业的学习助手，专门帮助大学生总结每日学习笔记。

你的特点：
1. 擅长从笔记中提炼核心知识点
2. 输出简洁、结构化
3. 中英混合自然（专业术语英文，解释中文）
4. 语言风格直接、清晰

你绝对不会：
1. 添加用户未要求的内容
2. 过度详细或啰嗦
3. 机械罗列笔记"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        review_content = response.choices[0].message.content
        
        beijing_now = get_beijing_time()
        
        footer = f"""

---

<div align="center">

*Generated by [DeepSeek Chat](https://www.deepseek.com) | {beijing_now.strftime('%Y-%m-%d %H:%M')} (UTC+8)*

</div>
"""
        
        header = f"""---
date: {date_info['date_str']}
weekday: {date_info['weekday']}
topics: [{topics_list}]
files: {total_files}
generated: {beijing_now.strftime('%Y-%m-%d %H:%M')}
timezone: UTC+8
model: deepseek-chat
---

# 📅 {date_info['date_cn']} 学习日报

> 周{date_info['weekday']}

---

"""
        
        return header + review_content + footer
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

def save_daily_review(content, date_info):
    """保存日报"""
    os.makedirs(REVIEWS_DIR, exist_ok=True)
    
    filename = f"Daily-{date_info['date_str']}.md"
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
    
    print(f"✅ Saved: {filepath}")
    return True

def main():
    print("=" * 70)
    print("📝 Daily Review Generator")
    print("=" * 70)
    
    # ✅ 解析命令行参数
    parser = argparse.ArgumentParser(description='Generate daily review')
    parser.add_argument('days_ago', nargs='?', type=int, default=0,
                        help='Generate review for N days ago (0=today, 1=yesterday, etc.)')
    parser.add_argument('--date', '-d', type=str,
                        help='Generate review for specific date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # 确定目标日期
    target_date = None
    if args.date:
        try:
            target_date = parse_date_input(args.date)
            print(f"ℹ️  Using specified date: {target_date}")
        except ValueError as e:
            print(f"❌ {e}")
            print("\n💡 Examples:")
            print("   python daily-review-gen.py --date 2026-02-05")
            print("   python daily-review-gen.py --date 20260205")
            print("   python daily-review-gen.py --date 02-05")
            return
    
    date_info = get_date_info(days_ago=args.days_ago if not target_date else None, 
                               target_date=target_date)
    
    print(f"\n📅 Generating review for: {date_info['display']}")
    
    topics = get_daily_changes(date_info['date'])
    
    if not topics:
        print(f"\n⚠️  No changes found on {date_info['date_str']}")
        print("💡 Tip: Make sure you have commits on that day")
        return
    
    print(f"\n📊 Topics:")
    for topic, files in sorted(topics.items()):
        print(f"   • {topic}: {len(files)} files")
    
    review = generate_daily_review(topics, date_info)
    
    if not review:
        print("\n❌ Failed to generate review")
        return
    
    beijing_now = get_beijing_time()
    print(f"\n⏰ Current time: {beijing_now.strftime('%Y-%m-%d %H:%M')} (UTC+8)")
    
    print("\n📝 Preview:")
    print("-" * 70)
    print(review[:500] + "\n...")
    print("-" * 70)
    
    if save_daily_review(review, date_info):
        print("\n" + "=" * 70)
        print("✅ Complete!")
        print(f"📂 {REVIEWS_DIR}/Daily-{date_info['date_str']}.md")
        print("=" * 70)

if __name__ == "__main__":
    main()
