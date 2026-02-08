import os
import re
import json
import subprocess
from datetime import datetime
from collections import Counter

import yaml
import frontmatter

from openai import OpenAI

# ── 配置 ──────────────────────────────────────────────────────────────────────
API_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=API_BASE_URL,
)

# 排除规则（统一用 basename 或全路径匹配）
# Note: Each pattern should be a valid, self-contained regex that can be safely combined with '|'
EXCLUDE_PATTERNS = [
    r'(?:^|/)readme\.md$',          # 任意目录下的 readme.md
    r'(?:^|/)test\d*\.md$',         # 任意目录下的 test.md / test1.md
    r'(?:^|/)\.obsidian/',
    r'(?:^|/)\.github/',
    r'(?:^|/)Assets/',
    r'(?:^|/)Reviews/',
]

# Pre-compiled regex for performance - combines all exclude patterns with OR
EXCLUDE_PATTERN_COMPILED = re.compile('|'.join(f'(?:{p})' for p in EXCLUDE_PATTERNS), re.IGNORECASE)


# ── 工具函数 ──────────────────────────────────────────────────────────────────

# Cache for git times to avoid redundant git commands
# Using dict instead of lru_cache to allow tuple keys
# Note: Python 3.7+ dicts maintain insertion order, so first 100 entries are oldest
# For GitHub Actions workflow (single run per push), cache won't grow unbounded
_git_time_cache = {}
_GIT_CACHE_MAX_SIZE = 1000  # Limit cache size for long-running processes

def should_process_file(file_path: str) -> bool:
    """判断文件是否需要处理"""
    if not file_path.endswith('.md'):
        return False
    file_lower = file_path.lower()
    return not EXCLUDE_PATTERN_COMPILED.search(file_lower)


def extract_topic(file_path: str) -> str:
    """从文件名提取 topic"""
    filename = os.path.basename(file_path)
    return os.path.splitext(filename)[0]


def _git_log_time(file_path: str, fmt_args: list) -> str:
    """通用的 git log 时间获取"""
    # Check cache first
    cache_key = (file_path, tuple(fmt_args))
    if cache_key in _git_time_cache:
        return _git_time_cache[cache_key]
    
    # Simple cache size management: clear oldest entries if cache is too large
    if len(_git_time_cache) >= _GIT_CACHE_MAX_SIZE:
        # Remove ~10% of oldest entries (first 100 items in dict)
        keys_to_remove = list(_git_time_cache.keys())[:100]
        for key in keys_to_remove:
            del _git_time_cache[key]
    
    try:
        cmd = ['git', 'log'] + fmt_args + ['--', file_path]
        result = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
        if result:
            line = result.split('\n')[0]
            dt = datetime.fromisoformat(line.replace('Z', '+00:00'))
            time_str = dt.strftime('%Y-%m-%d %H:%M')
            _git_time_cache[cache_key] = time_str
            return time_str
    except Exception as e:
        print(f"  [WARN] Git log failed for {file_path}: {e}")
    
    fallback_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    _git_time_cache[cache_key] = fallback_time
    return fallback_time


def get_created_time(file_path: str) -> str:
    """获取创建时间（Git 最早 commit）"""
    return _git_log_time(file_path, ['--follow', '--format=%aI', '--reverse'])


def get_modified_time(file_path: str) -> str:
    """获取最后修改时间（Git 最新 commit）"""
    return _git_log_time(file_path, ['-1', '--format=%aI'])


# ── YAML 安全值包装 ────────────────────────────────────────────────────────────

def _yaml_safe_str(value: str) -> str:
    """对 YAML 中可能引起解析问题的字符串加引号"""
    dangerous_chars = [':', '#', '[', ']', '{', '}', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']
    if any(c in value for c in dangerous_chars):
        # 用双引号包裹，内部双引号转义
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return value


# ── Frontmatter 解析/构建（使用 python-frontmatter 库）──────────────────────────

def parse_frontmatter_safe(content: str) -> tuple:
    """
    安全解析 frontmatter。
    返回 (metadata_dict, body_str) 或 (None, content) 。
    """
    try:
        post = frontmatter.loads(content)
        if post.metadata:
            return (dict(post.metadata), post.content)
    except Exception as e:
        print(f"  [WARN] python-frontmatter parse failed: {e}")
        # 兜底：尝试手动正则
        match = re.match(r'^---\n(.*?)\n---\n\n?', content, re.DOTALL)
        if match:
            try:
                meta = yaml.safe_load(match.group(1))
                if isinstance(meta, dict):
                    body = content[match.end():]
                    return (meta, body)
            except yaml.YAMLError:
                pass
    return (None, content)


def build_frontmatter_str(data: dict) -> str:
    """从字典构建标准 YAML frontmatter"""
    order = ['topic', 'created', 'modified', 'tags']
    ordered_data = {}

    for key in order:
        if key in data:
            ordered_data[key] = data[key]
    for key, value in data.items():
        if key not in order:
            ordered_data[key] = value

    # 使用 yaml.dump 生成标准 YAML
    yaml_str = yaml.dump(
        ordered_data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=1000,  # 避免自动换行
    )

    return f"---\n{yaml_str}---\n\n"


# ── AI 标签生成 ──────────────────────────────────────────────────────────────

def generate_tags_by_ai(topic: str, content: str, file_path: str) -> list:
    """使用 AI 生成语义化标签"""
    preview = content[:800]

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

    print(f"  [AI] Generating tags for: {topic}")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是专业的技术标签生成助手，精准提取核心技术概念标签。只返回标签，用逗号分隔。"
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=60
        )

        tags_str = response.choices[0].message.content.strip()
        print(f"  [AI] Raw response: '{tags_str}'")

        # 清理 AI 返回格式
        tags_str = re.sub(r'^(标签|Tags?)[：:：\s]*', '', tags_str, flags=re.IGNORECASE)
        tags_str = tags_str.strip('[](){}「」《》""\'`')

        tags = [t.strip() for t in re.split(r'[,，、;；]', tags_str) if t.strip()]
        tags = [t for t in tags if 2 <= len(t) <= 10][:5]

        if tags:
            print(f"  [AI] Generated tags: {tags}")
            return tags
        raise ValueError("AI returned empty tags after filtering")

    except Exception as e:
        print(f"  [AI ERROR] {type(e).__name__}: {e}")
        print(f"  [WARN] Falling back to rule-based extraction")
        return fallback_tags(topic, content, file_path)


# ── 兜底标签生成 ──────────────────────────────────────────────────────────────

# Pre-compiled regex patterns for keyword extraction
CAMEL_CASE_RE = re.compile(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b')
ACRONYM_RE = re.compile(r'\b[A-Z]{2,6}\b')
CAPITALIZED_RE = re.compile(r'\b[A-Z][a-z]{2,12}\b')
CHINESE_WORD_RE = re.compile(r'[\u4e00-\u9fa5]{2,6}')
PATH_EXTRACTION_RE = re.compile(r'[A-Z][a-z]+|[A-Z]{2,}')

# Pre-compiled tech category patterns for matching
# Note: Categories are designed to be mutually exclusive where possible to avoid redundant tags
# Framework-specific terms (Spring, Vue, React) are separated from language tags (Java, JavaScript)
TECH_CATEGORY_PATTERNS = {
    'Java': re.compile(r'\b(?:java|jvm|maven|mybatis)\b', re.IGNORECASE),
    'Python': re.compile(r'\b(?:python|django|flask|numpy|pandas)\b', re.IGNORECASE),
    'JavaScript': re.compile(r'\b(?:javascript|js|node|vue|react|typescript)\b', re.IGNORECASE),
    'Spring': re.compile(r'\b(?:spring|springboot|ioc|aop|mvc)\b', re.IGNORECASE),
    'Vue': re.compile(r'\b(?:vue|vuex|router|响应式|composition)\b', re.IGNORECASE),
    'React': re.compile(r'\b(?:react|jsx|hooks|redux)\b', re.IGNORECASE),
    'MySQL': re.compile(r'\b(?:mysql|sql|数据库|select|join)\b', re.IGNORECASE),
    'Redis': re.compile(r'\b(?:redis|缓存|nosql|key-value)\b', re.IGNORECASE),
    'Git': re.compile(r'\b(?:git|github|commit|branch|版本控制)\b', re.IGNORECASE),
    'Docker': re.compile(r'\b(?:docker|容器|dockerfile|compose)\b', re.IGNORECASE),
    'Linux': re.compile(r'\b(?:linux|shell|bash|ubuntu|centos)\b', re.IGNORECASE),
    'API': re.compile(r'\b(?:api|rest|restful|http|接口)\b', re.IGNORECASE),
    '算法': re.compile(r'\b(?:算法|algorithm|时间复杂度|动态规划|排序)\b', re.IGNORECASE),
    '设计模式': re.compile(r'\b(?:设计模式|pattern|单例|工厂|观察者)\b', re.IGNORECASE),
}

def extract_keywords_from_content(content: str, top_n: int = 15) -> list:
    """从内容中提取高频技术关键词"""
    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', '', text)

    keywords = []
    keywords.extend(CAMEL_CASE_RE.findall(text))  # CamelCase
    keywords.extend(ACRONYM_RE.findall(text))     # 缩写
    keywords.extend(CAPITALIZED_RE.findall(text)) # 首字母大写
    keywords.extend(CHINESE_WORD_RE.findall(text))# 中文词

    word_freq = Counter(keywords)

    stopwords = {
        '的', '了', '是', '在', '和', '有', '我', '你', '他', '她', '这个', '那个',
        '可以', '需要', '如果', '因为', '所以', '但是', '然后', '就是', '一个',
        '我们', '它们', '什么', '怎么', '为什么', '这样', '那样',
        'The', 'This', 'That', 'These', 'Those', 'And', 'But', 'For', 'With',
        'From', 'Into', 'When', 'Where', 'Which', 'What', 'How', 'Why',
        'Can', 'Will', 'Should', 'Would', 'Could', 'May', 'Might',
    }

    return [
        word for word, _ in word_freq.most_common(top_n * 2)
        if word not in stopwords and len(word) >= 2
    ][:top_n]


def match_tech_categories(keywords: list, content: str) -> list:
    """匹配技术分类标签"""
    all_text = (' '.join(keywords) + ' ' + content).lower()
    categories = []
    
    # Use pre-compiled patterns for each category
    for category, pattern in TECH_CATEGORY_PATTERNS.items():
        if pattern.search(all_text):
            categories.append(category)
    
    return categories


def fallback_tags(topic: str, content: str, file_path: str) -> list:
    """规则兜底标签"""
    print(f"  [FALLBACK] Rule-based extraction for: {topic}")

    keywords = []
    
    # 从路径提取
    for part in file_path.split('/')[:-1]:
        keywords.extend(PATH_EXTRACTION_RE.findall(part))
    # 从标题提取
    keywords.extend(PATH_EXTRACTION_RE.findall(topic))
    # 从内容提取
    keywords.extend(extract_keywords_from_content(content, top_n=10))

    # 去重
    seen = set()
    unique = []
    for kw in keywords:
        if kw.lower() not in seen and len(kw) >= 2:
            seen.add(kw.lower())
            unique.append(kw)

    categories = match_tech_categories(unique, content)

    tags = categories[:3]
    for kw in unique:
        if kw not in tags and len(tags) < 5:
            tags.append(kw)

    if not tags:
        tags = [topic]

    print(f"  [FALLBACK] Generated: {tags[:5]}")
    return tags[:5]


# ── 核心处理逻辑 ──────────────────────────────────────────────────────────────

def update_or_add_frontmatter(file_path: str, content: str, force_rebuild: bool = False) -> tuple:
    """
    更新或添加 frontmatter。
    返回 (new_content, status) ，status 为 'added' / 'updated' / 'rebuilt' / 'unchanged'
    """
    existing_fm, body = parse_frontmatter_safe(content)

    if existing_fm and not force_rebuild:
        # 已有 frontmatter，仅更新 modified 时间
        new_modified = get_modified_time(file_path)
        old_modified = str(existing_fm.get('modified', ''))

        if old_modified == new_modified:
            return (content, 'unchanged')

        print(f"  [UPDATE] Modified: {old_modified} -> {new_modified}")
        existing_fm['modified'] = new_modified

        new_content = build_frontmatter_str(existing_fm) + body
        return (new_content, 'updated')

    else:
        # 新建或强制重建
        if existing_fm:
            print(f"  [REBUILD] Regenerating frontmatter")

        topic = extract_topic(file_path)
        created = existing_fm.get('created') if existing_fm else get_created_time(file_path)
        modified = get_modified_time(file_path)

        # 确保 created 是字符串
        if not isinstance(created, str):
            created = str(created)

        print(f"  [INFO] Topic: {topic}")
        print(f"  [INFO] Created: {created}")
        print(f"  [INFO] Modified: {modified}")

        tags = generate_tags_by_ai(topic, body, file_path)

        data = {
            'topic': topic,
            'created': created,
            'modified': modified,
            'tags': tags,
        }

        new_content = build_frontmatter_str(data) + body
        status = 'rebuilt' if existing_fm else 'added'
        return (new_content, status)


def process_file(file_path: str, force_rebuild: bool = False) -> str:
    """处理单个文件，返回状态字符串"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [ERROR] Read failed: {e}")
        return 'failed'

    if not content.strip():
        print(f"  [SKIP] Empty file")
        return 'unchanged'

    new_content, status = update_or_add_frontmatter(file_path, content, force_rebuild)

    if status == 'unchanged':
        print(f"  [SKIP] No changes needed")
        return 'unchanged'

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [SUCCESS] {status.capitalize()} frontmatter")
        return status
    except Exception as e:
        print(f"  [ERROR] Write failed: {e}")
        return 'failed'


# ── 变更文件检测 ──────────────────────────────────────────────────────────────

def get_changed_files() -> list:
    """从 GitHub push event 获取变更的 .md 文件"""
    event_path = os.environ.get('GITHUB_EVENT_PATH')
    if not event_path or not os.path.exists(event_path):
        print("[WARN] No GITHUB_EVENT_PATH, using HEAD~1 fallback")
        return _git_diff_files('HEAD~1', 'HEAD')

    try:
        with open(event_path) as f:
            event = json.load(f)

        before_sha = event.get('before', '')
        after_sha = event.get('after', 'HEAD')

        if before_sha and before_sha != '0' * 40:
            print(f"\n[INFO] Push event: {before_sha[:7]}...{after_sha[:7]}")
            files = _git_diff_files(before_sha, after_sha)
            if files:
                return files

        # 合并提交或其他情况
        print("[INFO] Trying HEAD~1 fallback")
        return _git_diff_files('HEAD~1', 'HEAD')

    except Exception as e:
        print(f"[WARN] Failed to parse event: {e}")
        return _git_diff_files('HEAD~1', 'HEAD')


def _git_diff_files(from_ref: str, to_ref: str) -> list:
    """执行 git diff 获取 .md 文件列表"""
    try:
        cmd = ['git', 'diff', '--name-only', '--diff-filter=ACMR', from_ref, to_ref, '--', '*.md']
        result = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
        if result:
            files = [f.strip() for f in result.split('\n') if f.strip()]
            print(f"[INFO] Found {len(files)} changed .md file(s):")
            for f in files:
                print(f"  - {f}")
            return files
    except subprocess.CalledProcessError as e:
        print(f"[WARN] git diff {from_ref}..{to_ref} failed: {e}")
    return []


# ── API 连接测试 ──────────────────────────────────────────────────────────────

def test_api_connection() -> bool:
    """测试 API 连接"""
    print("\n[INFO] Testing API connection...")

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not set!")
        return False

    print(f"[INFO] API Key: {'*' * 8}...{'*' * 4} (present)")
    print(f"[INFO] Endpoint: {API_BASE_URL}")
    print(f"[INFO] Model: {MODEL}")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": "测试连接，请回复OK"}],
            max_tokens=10
        )
        print(f"[SUCCESS] API connection OK")
        return True
    except Exception as e:
        print(f"[ERROR] API connection failed: {type(e).__name__}: {e}")
        return False


# ── 主入口 ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Frontmatter AutoWired v2.0")
    print("=" * 70)

    # 支持中文路��
    try:
        subprocess.run(['git', 'config', 'core.quotepath', 'false'],
                       check=False, capture_output=True)
    except Exception:
        pass

    test_api_connection()

    force_rebuild = os.environ.get('FORCE_REBUILD', 'false').lower() == 'true'
    print(f"\n[MODE] {'Force rebuild' if force_rebuild else 'Update'}")

    # 获取本次 push 变更的文件
    changed_files = get_changed_files()

    if not changed_files:
        print("\n[INFO] No .md files changed in this push")
        return

    # 过滤排除文件
    files_to_process = [f for f in changed_files if should_process_file(f)]

    if not files_to_process:
        print("\n[INFO] No new files to process")
        return

    print(f"\n[INFO] Processing {len(files_to_process)} file(s):")

    stats = Counter()

    for i, file_path in enumerate(files_to_process, 1):
        print(f"\n[{i}/{len(files_to_process)}] {file_path}")

        if not os.path.exists(file_path):
            print(f"  [SKIP] File not found (may have been deleted)")
            stats['skipped'] += 1
            continue

        result = process_file(file_path, force_rebuild)
        stats[result] += 1

    print("\n" + "=" * 70)
    print("Summary:")
    print(f"  Added:     {stats.get('added', 0)}")
    print(f"  Updated:   {stats.get('updated', 0)}")
    print(f"  Rebuilt:   {stats.get('rebuilt', 0)}")
    print(f"  Unchanged: {stats.get('unchanged', 0)}")
    print(f"  Skipped:   {stats.get('skipped', 0)}")
    print(f"  Failed:    {stats.get('failed', 0)}")
    print(f"  Total:     {len(files_to_process)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
