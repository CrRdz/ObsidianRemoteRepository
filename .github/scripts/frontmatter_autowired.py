import os
import re
import subprocess
from datetime import datetime
from collections import Counter
from openai import OpenAI

# 配置
API_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=API_BASE_URL
)

# 排除文件
EXCLUDE_PATTERNS = [
    r'readme\.md$',
    r'^test\d*\.md$',
    r'^\.obsidian/',
    r'^\.github/',
    r'^Assets/',
    r'^Reviews/',
]


def should_process_file(file_path):
    """判断文件是否需要处理"""
    if not file_path.endswith('.md'):
        return False
    
    file_lower = file_path.lower()
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, file_lower, re.IGNORECASE):
            return False
    
    return True


def has_frontmatter(content):
    """检查是否已有 frontmatter"""
    return content.startswith('---\n') or content.startswith('---\r\n')


def extract_topic(file_path: str) -> str:
    """从文件名提取 topic"""
    filename = os.path.basename(file_path)
    topic = os.path.splitext(filename)[0]
    return topic


def get_created_time(file_path: str) -> str:
    """获取创建时间（Git 最早 commit，精确到分钟）"""
    try:
        cmd = ['git', 'log', '--follow', '--format=%aI', '--reverse', '--', file_path]
        result = subprocess.check_output(cmd, text=True).strip()
        
        if result:
            first_commit = result.split('\n')[0]
            dt = datetime.fromisoformat(first_commit.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
    except Exception as e:
        print(f"  ⚠️  Git log failed: {e}")
    
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def get_modified_time(file_path: str) -> str:
    """获取最后修改时间（Git 最新 commit，精确到分钟）"""
    try:
        cmd = ['git', 'log', '-1', '--format=%aI', '--', file_path]
        result = subprocess.check_output(cmd, text=True).strip()
        
        if result:
            dt = datetime.fromisoformat(result.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
    except Exception as e:
        print(f"  ⚠️  Git log failed: {e}")
    
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def generate_tags_by_ai(topic: str, content: str, file_path: str) -> list:
    """使用 AI 生成语义化标签"""
    
    # 取前 800 字（增加上下文）
    preview = content[:800]
    
    # 提取路径信息（辅助 AI 理解上下文）
    path_parts = file_path.split('/')
    context_hint = ""
    if len(path_parts) > 1:
        context_hint = f"\n文件路径: {'/'.join(path_parts[:-1])}"
    
    prompt = f"""你是一个专业的技术笔记标签生成助手。

笔记标题: {topic}{context_hint}
笔记内容（前800字）:
{preview}

请为这篇笔记生成 3-5 个**精准的技术标签**。

要求：
1. 标签应该是**核心技术概念、框架名、或专业术语**
2. 每个标签 2-10 个字符
3. 优先提取：
   - 编程语言（Java, Python, JavaScript）
   - 框架/库（Spring, Vue, React, Redis）
   - 技术概念（IoC, RESTful, 响应式）
   - 工具（Git, Docker, Maven）
4. 中英文混合可以，但保持专业
5. 直接返回标签，用逗号分隔，不要任何解释

示例：
- Spring 笔记 → Spring, IoC, 依赖注入, Java
- Git 笔记 → Git, 版本控制, 远程仓库
- Vue 笔记 → Vue3, 响应式, Composition API, JavaScript
- 算法笔记 → 算法, 动态规划, 时间复杂度

标签:"""
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是专业的技术标签生成助手，精准提取核心技术概念标签。"
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=60
        )
        
        tags_str = response.choices[0].message.content.strip()
        
        # 清理格式
        tags_str = re.sub(r'^(标签|Tags?)[：:：\s]*', '', tags_str, flags=re.IGNORECASE)
        tags_str = tags_str.strip('[](){}「」《》""\'`')
        
        # 分割标签
        tags = [t.strip() for t in re.split(r'[,，、;；]', tags_str) if t.strip()]
        
        # 过滤：长度 2-10，最多 5 个
        tags = [t for t in tags if 2 <= len(t) <= 10][:5]
        
        if tags:
            print(f"  🤖 AI tags: {tags}")
            return tags
        else:
            raise ValueError("AI returned empty tags")
    
    except Exception as e:
        print(f"  ⚠️  AI failed ({e}), using fallback")
        return fallback_tags(topic, content, file_path)


def extract_keywords_from_content(content: str, top_n=15) -> list:
    """
    从内容中提取高频技术关键词
    
    改进：
    1. 提取驼峰命名（SpringBoot, MyBatis）
    2. 提取大写缩写（IoC, API, HTTP）
    3. 提取中文技术词（依赖注入、控制反转）
    4. 统计频率，返回高频词
    """
    
    # 移除代码块和行内代码
    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', '', text)
    
    keywords = []
    
    # 1. 提取驼峰命名（SpringBoot, MyBatis, ArrayList）
    camel_case = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text)
    keywords.extend(camel_case)
    
    # 2. 提取大写缩写（IoC, API, HTTP, REST, 2-6 个字母）
    acronyms = re.findall(r'\b[A-Z]{2,6}\b', text)
    keywords.extend(acronyms)
    
    # 3. 提取首字母大写单词（Spring, Java, Git）
    capitalized = re.findall(r'\b[A-Z][a-z]{2,12}\b', text)
    keywords.extend(capitalized)
    
    # 4. 提取中文技术词（2-6 个字）
    chinese_terms = re.findall(r'[\u4e00-\u9fa5]{2,6}', text)
    keywords.extend(chinese_terms)
    
    # 统计频率
    word_freq = Counter(keywords)
    
    # 过滤停用词
    stopwords = {
        # 中文
        '的', '了', '是', '在', '和', '有', '我', '你', '他', '她', '这个', '那个',
        '可以', '需要', '如果', '因为', '所以', '但是', '然后', '就是', '一个',
        '我们', '它们', '什么', '怎么', '为什么', '这样', '那样',
        # 英文
        'The', 'This', 'That', 'These', 'Those', 'And', 'But', 'For', 'With',
        'From', 'Into', 'When', 'Where', 'Which', 'What', 'How', 'Why',
        'Can', 'Will', 'Should', 'Would', 'Could', 'May', 'Might',
    }
    
    # 过滤
    filtered = [
        word for word, count in word_freq.most_common(top_n * 2)
        if word not in stopwords and len(word) >= 2
    ]
    
    return filtered[:top_n]


def extract_technical_keywords(file_path: str, topic: str, content: str) -> list:
    """
    综合提取技术关键词
    
    来源：
    1. 文件路径（JavaNotes/SSM → Java, SSM）
    2. 文件名（SpringBoot → Spring, Boot）
    3. 内容高频词
    """
    
    keywords = []
    
    # 1. 从路径提取
    path_parts = file_path.split('/')
    for part in path_parts[:-1]:  # 排除文件名
        # 提取目录名中的技术词
        tech_words = re.findall(r'[A-Z][a-z]+|[A-Z]{2,}', part)
        keywords.extend(tech_words)
    
    # 2. 从文件名提取
    # "SpringBoot" → ["Spring", "Boot"]
    # "MySQL" → ["MySQL"]
    topic_words = re.findall(r'[A-Z][a-z]+|[A-Z]{2,}', topic)
    keywords.extend(topic_words)
    
    # 3. 从内容提取高频词
    content_keywords = extract_keywords_from_content(content, top_n=10)
    keywords.extend(content_keywords)
    
    # 去重（保持顺序）
    seen = set()
    unique_keywords = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower not in seen and len(kw) >= 2:
            seen.add(kw_lower)
            unique_keywords.append(kw)
    
    return unique_keywords


def match_tech_categories(keywords: list, content: str) -> list:
    """
    匹配技术分类标签
    
    根据关键词和内容，推断技术栈分类
    """
    
    categories = []
    
    # 技术分类规则
    tech_map = {
        # 编程语言
        'Java': ['java', 'jvm', 'spring', 'maven', 'mybatis'],
        'Python': ['python', 'django', 'flask', 'numpy', 'pandas'],
        'JavaScript': ['javascript', 'js', 'node', 'vue', 'react', 'typescript'],
        
        # 框架
        'Spring': ['spring', 'springboot', 'ioc', 'aop', 'mvc'],
        'Vue': ['vue', 'vuex', 'router', '响应式', 'composition'],
        'React': ['react', 'jsx', 'hooks', 'redux'],
        
        # 数据库
        'MySQL': ['mysql', 'sql', '数据库', 'select', 'join'],
        'Redis': ['redis', '缓存', 'nosql', 'key-value'],
        
        # 工具
        'Git': ['git', 'github', 'commit', 'branch', '版本控制'],
        'Docker': ['docker', '容器', 'dockerfile', 'compose'],
        'Linux': ['linux', 'shell', 'bash', 'ubuntu', 'centos'],
        
        # 概念
        'API': ['api', 'rest', 'restful', 'http', '接口'],
        '算法': ['算法', 'algorithm', '时间复杂度', '动态规划', '排序'],
        '设计模式': ['设计模式', 'pattern', '单例', '工厂', '观察者'],
    }
    
    # 组合所有文本（小写）
    all_text = ' '.join(keywords).lower() + ' ' + content.lower()
    
    # 匹配
    for category, patterns in tech_map.items():
        for pattern in patterns:
            if pattern in all_text:
                if category not in categories:
                    categories.append(category)
                break
    
    return categories


def fallback_tags(topic: str, content: str, file_path: str) -> list:
    """
    完善的兜底规则
    
    策略：
    1. 提取技术关键词（路径 + 文件名 + 内容）
    2. 匹配技术分类
    3. 组合去重
    4. 智能排序（优先级：分类 > 关键词）
    """
    
    print(f"  📏 Using fallback rules...")
    
    # 1. 提取所有技术关键词
    keywords = extract_technical_keywords(file_path, topic, content)
    
    # 2. 匹配技术分类
    categories = match_tech_categories(keywords, content)
    
    # 3. 组合 tags（分类优先）
    tags = []
    
    # 优先加分类标签
    tags.extend(categories[:3])
    
    # 补充关键词（避免重复）
    for kw in keywords:
        if kw not in tags and len(tags) < 5:
            tags.append(kw)
    
    # 4. 如果还是空，用文件名
    if not tags:
        tags = [topic]
    
    print(f"  📏 Fallback tags: {tags[:5]}")
    return tags[:5]


def generate_frontmatter(file_path: str, content: str) -> str:
    """生成 frontmatter"""
    
    print(f"\n📄 {file_path}")
    
    # 1. Topic：文件名
    topic = extract_topic(file_path)
    print(f"  📝 Topic: {topic}")
    
    # 2. 时间：从 Git 获取
    created = get_created_time(file_path)
    modified = get_modified_time(file_path)
    print(f"  📅 Created: {created}")
    print(f"  📅 Modified: {modified}")
    
    # 3. Tags：优先 AI，失败则用完善的规则
    tags = generate_tags_by_ai(topic, content, file_path)
    
    # 构建 frontmatter
    frontmatter = f"""---
topic: {topic}
created: {created}
modified: {modified}
tags: [{', '.join(tags)}]
---

"""
    
    return frontmatter


def process_file(file_path: str) -> bool:
    """处理单个文件"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ Read error: {e}")
        return False
    
    if has_frontmatter(content):
        print(f"  ⏭️  Skip (already has frontmatter)")
        return False
    
    frontmatter = generate_frontmatter(file_path, content)
    
    new_content = frontmatter + content
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ Added")
        return True
    except Exception as e:
        print(f"  ❌ Write error: {e}")
        return False
        
def main():
    print("=" * 70)
    print("🔧 Frontmatter AutoWired")
    print("=" * 70)
    
    # 配置 Git 正确处理中文文件名
    try:
        subprocess.run(
            ['git', 'config', 'core.quotepath', 'false'],
            check=False,
            capture_output=True
        )
    except:
        pass  # 忽略配置失败
    
    # 获取变更的 .md 文件
    try:
        cmd = ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD', '--', '*.md']
        result = subprocess.check_output(
            cmd, 
            text=True, 
            encoding='utf-8'  # 确保使用 UTF-8
        ).strip()
        
        print(f"\n🔍 Git diff result:")
        print(f"{result}")
        
        if not result:
            print("\n⚠️  No .md files changed in last commit")
            return
        
        files = result.split('\n')
        print(f"\n📝 Files from git diff: {files}")
        
    except Exception as e:
        print(f"\n❌ Git diff failed: {e}")
        print("⚠️  Falling back to processing all .md files")
        files = []
        for root, dirs, filenames in os.walk('.'):
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = os.path.join(root, filename).lstrip('./')
                    files.append(file_path)
    
    # 过滤
    files = [f for f in files if should_process_file(f)]
    
    if not files:
        print("\n⚠️  No files to process (after filtering)")
        print(f"   Exclusion patterns: {EXCLUDE_PATTERNS}")
        return
    
    print(f"\n📊 Files to process: {len(files)}")
    print("🤖 AI mode: enabled (all files)")
    
    # 处理
    processed = 0
    for file in files:
        if process_file(file):
            processed += 1
    
    print("\n" + "=" * 70)
    print(f"✅ Processed: {processed}/{len(files)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
