import os
import re
import datetime
import urllib.parse
import subprocess

# 配置：需要排除的文件夹
EXCLUDE_DIRS = {'.git', '.obsidian', '.github', 'node_modules', 'Assets', 'assets'}
# 配置：SVG 保存路径
SVG_OUTPUT_PATH = 'Assets/heatmap.svg'

def smart_count(text):
    """
    智能字数统计：
    1. 中文字符：每个算 1 个字
    2. 英文/数字：按单词/连续数字算 1 个字
    """
    # 移除所有 Markdown 语法 (简单的链接、加粗等)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # 链接只保留文本
    text = re.sub(r'[#*>`~-]', '', text)             # 移除特殊符号
    
    # 统计中文字符 (Unicode 范围 4E00-9FFF)
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    
    # 统计英文单词 (移除中文后，按空格分割)
    text_without_cn = re.sub(r'[\u4e00-\u9fff]', ' ', text)
    english_words = len(re.findall(r'\b[a-zA-Z0-9]+\b', text_without_cn))
    
    return chinese_chars + english_words

def get_git_activity_yearly(year=None):
    """
    获取整年的提交数据
    year: 指定年份，默认为当前年份
    返回: {'2026-01-01': 5, '2026-01-02': 0, ...}
    """
    if year is None:
        year = datetime.datetime.now().year
    
    activity = {}
    
    # 生成整年的日期
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    
    for single_date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days + 1)):
        activity[single_date.strftime('%Y-%m-%d')] = 0
    
    try:
        # 获取指定年份的提交
        cmd = [
            'git', 'log', 
            f'--since={year}-01-01', 
            f'--until={year}-12-31',
            '--format=%cd', 
            '--date=short'
        ]
        result = subprocess.check_output(cmd).decode('utf-8')
        
        for line in result.splitlines():
            date_str = line.strip()
            if date_str in activity:
                activity[date_str] += 1
                
    except Exception as e:
        print(f"Git log warning: {e}")
    
    return activity

def generate_github_style_heatmap(activity_data, year=None):
    """
    生成和 GitHub 完全一致的年度贡献热力图
    支持深色/浅色模式自适应
    """
    if year is None:
        year = datetime.datetime.now().year
    
    # GitHub 样式配置
    cell_size = 10
    cell_gap = 2
    title_height = 20       # 增加标题高度
    month_label_height = 15
    week_label_width = 30
    
    # 颜色方案（支持深色/浅色模式）
    colors_dark = {
        0: "#161b22",      # 深色背景
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }
    
    colors_light = {
        0: "#ebedf0",      # 浅色背景（灰色）
        1: "#9be9a8",      # 浅绿
        2: "#40c463",      # 中绿
        3: "#30a14e",      # 深绿
        4: "#216e39"       # 最深绿
    }
    
    # 计算从周日开始的第一天
    start_date = datetime.date(year, 1, 1)
    days_to_sunday = (start_date.weekday() + 1) % 7
    first_sunday = start_date - datetime.timedelta(days=days_to_sunday)
    
    # 计算总周数
    end_date = datetime.date(year, 12, 31)
    days_to_saturday = (5 - end_date.weekday()) % 7
    last_saturday = end_date + datetime.timedelta(days=days_to_saturday)
    
    total_days = (last_saturday - first_sunday).days + 1
    num_weeks = total_days // 7
    
    # 计算 SVG 尺寸（增加顶部空间）
    width = week_label_width + num_weeks * (cell_size + cell_gap) + 20
    height = title_height + month_label_height + 7 * (cell_size + cell_gap) + 40
    
    # 计算最大提交数
    max_commits = max(activity_data.values()) if activity_data.values() else 1
    if max_commits == 0:
        max_commits = 1
    
    def get_color_level(count):
        if count == 0:
            return 0
        elif count <= max_commits * 0.25:
            return 1
        elif count <= max_commits * 0.5:
            return 2
        elif count <= max_commits * 0.75:
            return 3
        else:
            return 4
    
    # 开始生成 SVG
    svg = []
    svg.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
    
    # 添加 CSS 样式（支持深色/浅色模式）
    svg.append('''
    <style>
        /* 默认浅色模式 */
        .bg { fill: #ffffff; }
        .text-primary { fill: #24292f; }
        .text-secondary { fill: #57606a; }
        .level-0 { fill: #ebedf0; }
        .level-1 { fill: #9be9a8; }
        .level-2 { fill: #40c463; }
        .level-3 { fill: #30a14e; }
        .level-4 { fill: #216e39; }
        
        /* 深色模式 */
        @media (prefers-color-scheme: dark) {
            .bg { fill: #0d1117; }
            .text-primary { fill: #c9d1d9; }
            .text-secondary { fill: #8b949e; }
            .level-0 { fill: #161b22; }
            .level-1 { fill: #0e4429; }
            .level-2 { fill: #006d32; }
            .level-3 { fill: #26a641; }
            .level-4 { fill: #39d353; }
        }
    </style>
    ''')
    
    # 背景
    svg.append(f'<rect width="{width}" height="{height}" class="bg"/>')
    
    # 标题（调整位置，避免与月份重叠）
    svg.append(f'<text x="10" y="15" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="14" class="text-primary" font-weight="600">{year} Contributions</text>')
    
    # 星期标签（左侧）
    week_labels = ['', 'Mon', '', 'Wed', '', 'Fri', '']
    for i, label in enumerate(week_labels):
        if label:
            y = title_height + month_label_height + i * (cell_size + cell_gap) + cell_size
            svg.append(f'<text x="5" y="{y}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="9" class="text-secondary" text-anchor="start">{label}</text>')
    
    # 月份标签（调整 Y 位置，增加间距）
    current_month = None
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for week in range(num_weeks):
        current_date = first_sunday + datetime.timedelta(weeks=week)
        month = current_date.month
        
        if month != current_month and current_date.year == year:
            current_month = month
            x = week_label_width + week * (cell_size + cell_gap)
            y = title_height + 12  # 调整月份标签位置
            svg.append(f'<text x="{x}" y="{y}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="10" class="text-secondary">{month_names[month - 1]}</text>')
    
    # 绘制方块网格
    for week in range(num_weeks):
        for day in range(7):
            current_date = first_sunday + datetime.timedelta(weeks=week, days=day)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # 只绘制当年的日期
            if current_date.year != year:
                continue
            
            count = activity_data.get(date_str, 0)
            color_level = get_color_level(count)
            
            x = week_label_width + week * (cell_size + cell_gap)
            y = title_height + month_label_height + day * (cell_size + cell_gap)
            
            # 使用 CSS 类名代替硬编码颜色
            svg.append(f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" class="level-{color_level}" rx="2" ry="2"><title>{date_str}: {count} contributions</title></rect>')
    
    # 图例（右下角）
    legend_x = width - 180
    legend_y = height - 15
    
    svg.append(f'<text x="{legend_x}" y="{legend_y}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="9" class="text-secondary">Less</text>')
    
    for i in range(5):
        x = legend_x + 30 + i * (cell_size + cell_gap)
        svg.append(f'<rect x="{x}" y="{legend_y - cell_size + 2}" width="{cell_size}" height="{cell_size}" class="level-{i}" rx="2" ry="2"/>')
    
    svg.append(f'<text x="{legend_x + 30 + 5 * (cell_size + cell_gap) + 5}" y="{legend_y}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="9" class="text-secondary">More</text>')
    
    # 统计信息
    total_contributions = sum(activity_data.values())
    svg.append(f'<text x="10" y="{height - 5}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="11" class="text-secondary">{total_contributions} contributions in {year}</text>')
    
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
    # 尝试多种文件名（兼容大小写）
    possible_names = ['README.md', 'Readme.md', 'readme.md']
    readme_path = None
    
    for name in possible_names:
        if os.path.exists(name):
            readme_path = name
            break
    
    if readme_path is None:
        print("Error: README.md not found!")
        return
    
    print(f"Found README: {readme_path}")
    
    # 获取最后一次修改 .md 文件的提交时间（更准确）
    try:
        cmd = ['git', 'log', '-1', '--format=%cd', '--date=format:%Y--%m--%d %H:%M', '--', '*.md']
        last_update = subprocess.check_output(cmd).decode('utf-8').strip()
        if not last_update:
            raise Exception("No markdown commits found")
    except:
        # 如果没有找到，使用当前时间
        utc_now = datetime.datetime.utcnow()
        beijing_time = utc_now + datetime.timedelta(hours=8)
        last_update = beijing_time.strftime("%Y--%m--%d %H:%M")
    
    # 格式化字数
    word_str = f"{word_count / 1000:.1f}k" if word_count > 1000 else str(word_count)

    # 1. 生成 GitHub 风格年度热力图
    current_year = datetime.datetime.now().year
    activity = get_git_activity_yearly(current_year)
    svg_content = generate_github_style_heatmap(activity, current_year)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(SVG_OUTPUT_PATH), exist_ok=True)
    with open(SVG_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Generated heatmap: {SVG_OUTPUT_PATH}")

    # 2. 构造 README 内容
    stats_content = (
        f"\n"
        f"<p align=\"center\">\n"
        f"  <img src=\"{get_shield_url('Notes', file_count, '2ea44f')}\" />\n"
        f"  <img src=\"{get_shield_url('Words', word_str, '007ec6')}\" />\n"
        f"  <img src=\"{get_shield_url('Last_Update', last_update, 'critical')}\" />\n"
        f"</p>\n"
        f"<p align=\"center\">\n"
        f"  <img src=\"{SVG_OUTPUT_PATH}\" alt=\"{current_year} Contribution Heatmap\" />\n"
        f"</p>\n"
        f"\n"
    )
    
    # 3. 读取 README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 保留占位符标记
    if '<!-- STATS START -->' not in content or '<!-- STATS END -->' not in content:
        print("Error: Placeholders not found in README!")
        print("Please add the following to your README.md:")
        print("<!-- STATS START -->")
        print("<!-- STATS END -->")
        return
    
    new_content = re.sub(
        r'(<!-- STATS START -->).*?(<!-- STATS END -->)',  # 使用捕获组
        r'\1' + stats_content + r'\2',                     # 保留标记
        content, 
        flags=re.DOTALL
    )
    
    # 4. 写入 README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"README updated successfully!")
    print(f"   - Files: {file_count}")
    print(f"   - Words: {word_count}")
    print(f"   - Last Update: {last_update}")

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Knowledge Base Stats Update")
    print("=" * 60)
    
    files, words = count_stats('.')
    print(f"\n Counted: {files} files, {words} words")
    
    update_readme(files, words)
    
    print("\n" + "=" * 60)
    print("Update Complete!")
    print("=" * 60)
