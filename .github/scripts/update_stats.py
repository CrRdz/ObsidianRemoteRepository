import os
import re
import datetime
import urllib.parse
import subprocess
import math

# 配置：需要排除的文件夹
EXCLUDE_DIRS = {'.git', '.obsidian', '.github', 'node_modules', 'Assets'}
# 配置：SVG 保存路径
SVG_OUTPUT_PATH = 'Assets/heatmap.svg'

def smart_count(text):
    """
    智能字数统计：
    1. 中文字符：每个算 1 个字
    2. 英文/数字：按单词/连续数字算 1 个字
    """
    # 移除所有 Markdown 语法 (简单的链接、加粗等)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text) # 链接只保留文本
    text = re.sub(r'[#*>`~-]', '', text)            # 移除特殊符号
    
    # 统计中文字符 (Unicode 范围 4E00-9FFF)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    
    # 统计英文单词 (移除中文后，按空格分割)
    # 先把中文替换为空格，避免粘连
    text_without_cn = re.sub(r'[\u4e00-\u9fff]', ' ', text)
    english_words = len(re.findall(r'\b[a-zA-Z0-9]+\b', text_without_cn))
    
    return chinese_chars + english_words

def get_git_activity(days=30):
    """
    获取过去 N 天的提交次数
    返回字典: {'2026-02-01': 5, '2026-02-02': 0, ...}
    """
    activity = {}
    today = datetime.datetime.now().date()
    
    # 初始化日期
    for i in range(days):
        date = today - datetime.timedelta(days=i)
        activity[date.strftime('%Y-%m-%d')] = 0

    try:
        # 使用 git log 获取提交日期
        # --since="30 days ago" --format="%cd" --date=short
        cmd = ['git', 'log', f'--since={days} days ago', '--format=%cd', '--date=short']
        result = subprocess.check_output(cmd).decode('utf-8')
        
        for line in result.splitlines():
            date_str = line.strip()
            if date_str in activity:
                activity[date_str] += 1
                
    except Exception as e:
        print(f"Git log warning (local test might fail if no git history): {e}")

    return activity

def generate_svg(activity_data):
    """
    手写一个简单的 SVG 热力图 (类似 GitHub 的绿色方块)
    """
    # 配置
    box_size = 12
    gap = 3
    days = list(activity_data.keys())[::-1] # 反转，从旧到新
    width = len(days) * (box_size + gap) + 10
    height = box_size + 20
    
    svg_parts = []
    svg_parts.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
    # 背景
    svg_parts.append(f'<rect width="{width}" height="{height}" fill="none"/>')
    # 标题 (可选)
    # svg_parts.append(f'<text x="0" y="10" font-family="sans-serif" font-size="10" fill="#666">Activity (30 Days)</text>')

    max_commits = max(activity_data.values()) if activity_data.values() else 1
    if max_commits == 0: max_commits = 1
    
    for i, date in enumerate(days):
        count = activity_data[date]
        x = i * (box_size + gap)
        y = 5 # 顶部边距
        
        # 计算颜色深浅 (GitHub 绿风格)
        # 0: #ebedf0, 1-low: #9be9a8, mid: #40c463, high: #216e39
        if count == 0:
            color = "#ebedf0" # 灰色
        else:
            intensity = count / max_commits
            if intensity < 0.25: color = "#9be9a8"
            elif intensity < 0.5: color = "#40c463"
            elif intensity < 0.75: color = "#30a14e"
            else: color = "#216e39"
            
        # 添加方块
        tooltip = f"{date}: {count} commits"
        rect = f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" rx="2"><title>{tooltip}</title></rect>'
        svg_parts.append(rect)
        
        # 添加日期文字 (每隔 5 天显示一次)
        if i % 5 == 0:
            day_label = date.split('-')[2]
            svg_parts.append(f'<text x="{x}" y="{y + box_size + 10}" font-family="sans-serif" font-size="8" fill="#999">{day_label}</text>')

    svg_parts.append('</svg>')
    return "".join(svg_parts)

def count_stats(root_dir):
    total_files = 0
    total_words = 0
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.lower().startswith('license') or file.lower().startswith('readme'):
                continue
              
            if file.endswith('.md'):
                total_files += 1
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        total_words += smart_count(content)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
    return total_files, total_words

def get_shield_url(label, value, color):
    safe_value = urllib.parse.quote(str(value))
    return f"https://img.shields.io/badge/{label}-{safe_value}-{color}?style=flat-square"

def update_readme(file_count, word_count):
    readme_path = 'README.md'
    utc_now = datetime.datetime.utcnow()
    beijing_time = utc_now + datetime.timedelta(hours=8)
    time_str = beijing_time.strftime("%Y--%m--%d %H:%M")
    
    # 格式化数字
    if word_count > 1000:
        word_str = f"{word_count / 1000:.1f}k"
    else:
        word_str = str(word_count)

    # 1. 生成 SVG 热力图
    activity = get_git_activity(30)
    svg_content = generate_svg(activity)
    
    # 确保 assets 文件夹存在
    os.makedirs(os.path.dirname(SVG_OUTPUT_PATH), exist_ok=True)
    with open(SVG_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    # 2. 构造 README 内容
    # 包含 Stats Shields 和 下方的 SVG 热力图
    stats_content = (
        f"\n"
        f"<p align=\"center\">\n"
        f"  <img src=\"{get_shield_url('Notes', file_count, '2ea44f')}\" />\n"
        f"  <img src=\"{get_shield_url('Words', word_str, '007ec6')}\" />\n"
        f"  <img src=\"{get_shield_url('Last_Update', time_str, 'critical')}\" />\n"
        f"</p>\n"
        f"<p align=\"center\">\n"
        f"  <img src=\"{SVG_OUTPUT_PATH}\" alt=\"Study Heatmap\" width=\"100%\" />\n"
        f"</p>\n"
        f""
    )
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(
        r'<!-- STATS START -->.*<!-- STATS END -->', 
        stats_content, 
        content, 
        flags=re.DOTALL
    )
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    files, words = count_stats('.')
    print(f"Stats: {files} files, {words} words")
    update_readme(files, words)
