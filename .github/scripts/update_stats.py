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
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'[#*>`~-]', '', text)
    
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    text_without_cn = re.sub(r'[\u4e00-\u9fff]', ' ', text)
    english_words = len(re.findall(r'\b[a-zA-Z0-9]+\b', text_without_cn))
    
    return chinese_chars + english_words

def get_git_activity(days=30):
    """
    获取过去 N 天的提交次数（只统计当前仓库）
    返回字典: {'2026-02-01': 5, '2026-02-02': 0, ...}
    """
    activity = {}
    today = datetime.datetime.now().date()
    
    # 初始化日期
    for i in range(days):
        date = today - datetime.timedelta(days=i)
        activity[date.strftime('%Y-%m-%d')] = 0

    try:
        cmd = ['git', 'log', f'--since={days} days ago', '--format=%cd', '--date=short']
        result = subprocess.check_output(cmd).decode('utf-8')
        
        for line in result.splitlines():
            date_str = line.strip()
            if date_str in activity:
                activity[date_str] += 1
                
    except Exception as e:
        print(f"Git log warning: {e}")

    return activity

def generate_isometric_svg(activity_data):
    """
    生成 3D 等距视图热力图（Isometric Heatmap）
    类似建筑沙盘效果，方块高度代表提交次数
    """
    # === 配置参数 ===
    block_width = 16       # 方块底部宽度
    block_depth = 16       # 方块底部深度
    block_unit_height = 3  # 每次提交增加的高度
    gap = 2                # 方块间距
    
    # 等距投影角度（30度）
    angle_rad = math.radians(30)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    
    # 投影后的尺寸
    iso_x = block_width * cos_angle    # X轴投影
    iso_y = block_depth * cos_angle    # Y轴投影
    
    # === 数据处理 ===
    sorted_dates = sorted(activity_data.keys())
    if not sorted_dates:
        return '<svg width="100" height="100"><text x="10" y="50" fill="#666">No data</text></svg>'
    
    # 按周分组（7天一列）
    start_date = datetime.datetime.strptime(sorted_dates[0], '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(sorted_dates[-1], '%Y-%m-%d').date()
    
    weeks = []
    current_week = []
    
    for single_date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days + 1)):
        date_str = single_date.strftime('%Y-%m-%d')
        weekday = (single_date.weekday() + 1) % 7  # 0=周日, 6=周六
        
        if weekday == 0 and current_week:
            weeks.append(current_week)
            current_week = []
        
        current_week.append({
            'date': date_str,
            'count': activity_data.get(date_str, 0),
            'weekday': weekday
        })
    
    if current_week:
        weeks.append(current_week)
    
    max_commits = max(activity_data.values()) if activity_data.values() else 1
    if max_commits == 0:
        max_commits = 1
    
    # === 计算画布尺寸 ===
    num_weeks = len(weeks)
    max_height = min(max_commits, 15) * block_unit_height  # 限制最大高度
    
    canvas_width = int(num_weeks * (iso_x + gap) + 7 * (iso_y + gap) + 100)
    canvas_height = int(7 * (iso_y + gap) + max_height + 150)
    
    # === 开始生成 SVG ===
    svg = []
    svg.append(f'<svg width="{canvas_width}" height="{canvas_height}" xmlns="http://www.w3.org/2000/svg">')
    
    # 深色背景（GitHub 风格）
    svg.append(f'<rect width="{canvas_width}" height="{canvas_height}" fill="#0d1117"/>')
    
    # 渐变定义（增强立体感）
    svg.append('''
    <defs>
        <filter id="shadow">
            <feDropShadow dx="2" dy="2" stdDeviation="2" flood-opacity="0.3"/>
        </filter>
    </defs>
    ''')
    
    # === 绘制方块（从后往前，保证遮挡关系） ===
    blocks = []  # 存储所有方块数据，用于排序
    
    for week_idx, week in enumerate(weeks):
        for day_data in week:
            count = day_data['count']
            if count == 0:
                continue  # 跳过没有提交的日子
            
            weekday = day_data['weekday']
            
            # 计算基座位置（等距投影）
            base_x = 50 + week_idx * (iso_x + gap) + weekday * iso_y
            base_y = canvas_height - 80 - weekday * iso_y * sin_angle
            
            # 方块高度（限制最大值避免太高）
            height = min(count, 15) * block_unit_height
            
            # 颜色（根据提交数）
            intensity = count / max_commits
            if intensity < 0.25:
                top_color = "#9be9a8"
                left_color = "#7bc96f"
                right_color = "#5da55a"
            elif intensity < 0.5:
                top_color = "#40c463"
                left_color = "#30a14e"
                right_color = "#258a3e"
            elif intensity < 0.75:
                top_color = "#30a14e"
                left_color = "#216e39"
                right_color = "#1a5027"
            else:
                top_color = "#216e39"
                left_color = "#1a5027"
                right_color = "#0d2818"
            
            # 存储方块数据（用于深度排序）
            blocks.append({
                'x': base_x,
                'y': base_y,
                'height': height,
                'top_color': top_color,
                'left_color': left_color,
                'right_color': right_color,
                'date': day_data['date'],
                'count': count,
                'depth': week_idx + weekday  # 用于排序
            })
    
    # 按深度排序（从远到近绘制）
    blocks.sort(key=lambda b: -b['depth'])
    
    # 绘制所有方块
    for block in blocks:
        x = block['x']
        y = block['y']
        h = block['height']
        
        # 右侧面（深色）
        right_points = [
            (x + iso_x, y),
            (x + iso_x, y - h),
            (x + iso_x + iso_y, y - h - iso_y * sin_angle),
            (x + iso_x + iso_y, y - iso_y * sin_angle)
        ]
        svg.append(f'<polygon points="{" ".join([f"{p[0]:.1f},{p[1]:.1f}" for p in right_points])}" fill="{block["right_color"]}" stroke="#000" stroke-width="0.5" opacity="0.9"/>')
        
        # 左侧面（中等深度）
        left_points = [
            (x, y),
            (x, y - h),
            (x + iso_y, y - h - iso_y * sin_angle),
            (x + iso_y, y - iso_y * sin_angle)
        ]
        svg.append(f'<polygon points="{" ".join([f"{p[0]:.1f},{p[1]:.1f}" for p in left_points])}" fill="{block["left_color"]}" stroke="#000" stroke-width="0.5" opacity="0.95"/>')
        
        # 顶面（最亮）
        top_points = [
            (x, y - h),
            (x + iso_x, y - h),
            (x + iso_x + iso_y, y - h - iso_y * sin_angle),
            (x + iso_y, y - h - iso_y * sin_angle)
        ]
        svg.append(f'<polygon points="{" ".join([f"{p[0]:.1f},{p[1]:.1f}" for p in top_points])}" fill="{block["top_color"]}" stroke="#000" stroke-width="0.5"><title>{block["date"]}: {block["count"]} commits</title></polygon>')
    
    # === 添加标题和图例 ===
    svg.append(f'<text x="20" y="30" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#c9d1d9">📊 Contribution Landscape (Last 30 Days)</text>')
    svg.append(f'<text x="20" y="50" font-family="Arial, sans-serif" font-size="12" fill="#8b949e">Height represents commit count</text>')
    
    # 图例
    legend_x = canvas_width - 150
    legend_y = 30
    svg.append(f'<text x="{legend_x}" y="{legend_y}" font-family="Arial, sans-serif" font-size="10" fill="#8b949e">Less</text>')
    colors = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
    for i, color in enumerate(colors):
        svg.append(f'<rect x="{legend_x + 30 + i * 15}" y="{legend_y - 10}" width="12" height="12" fill="{color}" stroke="#000" stroke-width="0.5"/>')
    svg.append(f'<text x="{legend_x + 30 + len(colors) * 15 + 5}" y="{legend_y}" font-family="Arial, sans-serif" font-size="10" fill="#8b949e">More</text>')
    
    svg.append('</svg>')
    return "".join(svg)

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
    readme_path = 'Readme.md'
    
    # 获取最后一次提交时间（更准确）
    try:
        cmd = ['git', 'log', '-1', '--format=%cd', '--date=format:%Y--%m--%d %H:%M', '--', '*.md']
        last_update = subprocess.check_output(cmd).decode('utf-8').strip()
        if not last_update:
            raise Exception("No commit found")
    except:
        utc_now = datetime.datetime.utcnow()
        beijing_time = utc_now + datetime.timedelta(hours=8)
        last_update = beijing_time.strftime("%Y--%m--%d %H:%M")
    
    # 格式化字数
    word_str = f"{word_count / 1000:.1f}k" if word_count > 1000 else str(word_count)

    # 1. 生成 3D 等距 SVG 热力图
    activity = get_git_activity(30)
    svg_content = generate_isometric_svg(activity)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(SVG_OUTPUT_PATH), exist_ok=True)
    with open(SVG_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    # 2. 构造 README 内容
    stats_content = (
        f"\n"
        f"<p align=\"center\">\n"
        f"  <img src=\"{get_shield_url('Notes', file_count, '2ea44f')}\" />\n"
        f"  <img src=\"{get_shield_url('Words', word_str, '007ec6')}\" />\n"
        f"  <img src=\"{get_shield_url('Last_Update', last_update, 'critical')}\" />\n"
        f"</p>\n"
        f"<p align=\"center\">\n"
        f"  <img src=\"{SVG_OUTPUT_PATH}\" alt=\"3D Contribution Heatmap\" width=\"100%\" />\n"
        f"</p>\n"
        f"\n"
    )
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 保留标记本身
    new_content = re.sub(
        r'(<!-- STATS START -->).*?(<!-- STATS END -->)', 
        r'\1' + stats_content + r'\2', 
        content, 
        flags=re.DOTALL
    )
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ README updated with 3D isometric heatmap!")

if __name__ == "__main__":
    files, words = count_stats('.')
    print(f"Stats: {files} files, {words} words")
    update_readme(files, words)
