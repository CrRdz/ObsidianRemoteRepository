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
        print(f"  [WARN] Git log failed: {e}")
    
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
        print(f"  [WARN] Git log failed: {e}")
    
    return datetime.now().strftime('%Y-%m-%d %H:%M')


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
    
    print(f"  [AI DEBUG] Starting AI tag generation")
    print(f"  [AI DEBUG] API Base URL: {API_BASE_URL}")
    print(f"  [AI DEBUG] Model: {MODEL}")
    print(f"  [AI DEBUG] API Key present: {'Yes' if os.environ.get('OPENAI_API_KEY') else 'No'}")
    print(f"  [AI DEBUG] Topic: {topic}")
    print(f"  [AI DEBUG] Content preview length: {len(preview)} chars")
    
    try:
        print(f"  [AI DEBUG] Sending request to API...")
        
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
        
        print(f"  [AI DEBUG] API response received")
        print(f"  [AI DEBUG] Response ID: {response.id if hasattr(response, 'id') else 'N/A'}")
        print(f"  [AI DEBUG] Model used: {response.model if hasattr(response, 'model') else 'N/A'}")
        
        tags_str = response.choices[0].message.content.strip()
        
        print(f"  [AI DEBUG] Raw response: '{tags_str}'")
        
        tags_str = re.sub(r'^(标签|Tags?)[：:：\s]*', '', tags_str, flags=re.IGNORECASE)
        tags_str = tags_str.strip('[](){}「」《》""\'`')
        
        print(f"  [AI DEBUG] After cleanup: '{tags_str}'")
        
        tags = [t.strip() for t in re.split(r'[,，、;；]', tags_str) if t.strip()]
        
        print(f"  [AI DEBUG] After split: {tags}")
        
        tags = [t for t in tags if 2 <= len(t) <= 10][:5]
        
        print(f"  [AI DEBUG] After filter: {tags}")
        
        if tags:
            print(f"  [AI] Generated tags: {tags}")
            return tags
        else:
            print(f"  [AI DEBUG] Tags empty after filter, raising error")
            raise ValueError("AI returned empty tags")
    
    except Exception as e:
        print(f"  [AI ERROR] Exception occurred: {type(e).__name__}")
        print(f"  [AI ERROR] Error message: {str(e)}")
        
        import traceback
        print(f"  [AI ERROR] Full traceback:")
        for line in traceback.format_exc().split('\n'):
            if line.strip():
                print(f"    {line}")
        
        print(f"  [WARN] AI failed, using fallback")
        return fallback_tags(topic, content, file_path)


def extract_keywords_from_content(content: str, top_n=15) -> list:
    """从内容中提取高频技术关键词"""
    
    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', '', text)
    
    keywords = []
    
    camel_case = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text)
    keywords.extend(camel_case)
    
    acronyms = re.findall(r'\b[A-Z]{2,6}\b', text)
    keywords.extend(acronyms)
    
    capitalized = re.findall(r'\b[A-Z][a-z]{2,12}\b', text)
    keywords.extend(capitalized)
    
    chinese_terms = re.findall(r'[\u4e00-\u9fa5]{2,6}', text)
    keywords.extend(chinese_terms)
    
    word_freq = Counter(keywords)
    
    stopwords = {
        '的', '了', '是', '在', '和', '有', '我', '你', '他', '她', '这个', '那个',
        '可以', '需要', '如果', '因为', '所以', '但是', '然后', '就是', '一个',
        '我们', '它们', '什么', '怎么', '为什么', '这样', '那样',
        'The', 'This', 'That', 'These', 'Those', 'And', 'But', 'For', 'With',
        'From', 'Into', 'When', 'Where', 'Which', 'What', 'How', 'Why',
        'Can', 'Will', 'Should', 'Would', 'Could', 'May', 'Might',
    }
    
    filtered = [
        word for word, count in word_freq.most_common(top_n * 2)
        if word not in stopwords and len(word) >= 2
    ]
    
    return filtered[:top_n]


def extract_technical_keywords(file_path: str, topic: str, content: str) -> list:
    """综合提取技术关键词"""
    
    keywords = []
    
    path_parts = file_path.split('/')
    for part in path_parts[:-1]:
        tech_words = re.findall(r'[A-Z][a-z]+|[A-Z]{2,}', part)
        keywords.extend(tech_words)
    
    topic_words = re.findall(r'[A-Z][a-z]+|[A-Z]{2,}', topic)
    keywords.extend(topic_words)
    
    content_keywords = extract_keywords_from_content(content, top_n=10)
    keywords.extend(content_keywords)
    
    seen = set()
    unique_keywords = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower not in seen and len(kw) >= 2:
            seen.add(kw_lower)
            unique_keywords.append(kw)
    
    return unique_keywords


def match_tech_categories(keywords: list, content: str) -> list:
    """匹配技术分类标签"""
    
    categories = []
    
    tech_map = {
        'Java': ['java', 'jvm', 'spring', 'maven', 'mybatis'],
        'Python': ['python', 'django', 'flask', 'numpy', 'pandas'],
        'JavaScript': ['javascript', 'js', 'node', 'vue', 'react', 'typescript'],
        'Spring': ['spring', 'springboot', 'ioc', 'aop', 'mvc'],
        'Vue': ['vue', 'vuex', 'router', '响应式', 'composition'],
        'React': ['react', 'jsx', 'hooks', 'redux'],
        'MySQL': ['mysql', 'sql', '数据库', 'select', 'join'],
        'Redis': ['redis', '缓存', 'nosql', 'key-value'],
        'Git': ['git', 'github', 'commit', 'branch', '版本控制'],
        'Docker': ['docker', '容器', 'dockerfile', 'compose'],
        'Linux': ['linux', 'shell', 'bash', 'ubuntu', 'centos'],
        'API': ['api', 'rest', 'restful', 'http', '接口'],
        '算法': ['算法', 'algorithm', '时间复杂度', '动态规划', '排序'],
        '设计模式': ['设计模式', 'pattern', '单例', '工厂', '观察者'],
    }
    
    all_text = ' '.join(keywords).lower() + ' ' + content.lower()
    
    for category, patterns in tech_map.items():
        for pattern in patterns:
            if pattern in all_text:
                if category not in categories:
                    categories.append(category)
                break
    
    return categories


def fallback_tags(topic: str, content: str, file_path: str) -> list:
    """完善的兜底规则"""
    
    print(f"  [FALLBACK] Using rule-based extraction")
    print(f"  [FALLBACK DEBUG] Topic: {topic}")
    print(f"  [FALLBACK DEBUG] File path: {file_path}")
    print(f"  [FALLBACK DEBUG] Content length: {len(content)} chars")
    
    keywords = extract_technical_keywords(file_path, topic, content)
    print(f"  [FALLBACK DEBUG] Extracted keywords: {keywords[:10]}")
    
    categories = match_tech_categories(keywords, content)
    print(f"  [FALLBACK DEBUG] Matched categories: {categories}")
    
    tags = []
    
    tags.extend(categories[:3])
    print(f"  [FALLBACK DEBUG] Tags after categories: {tags}")
    
    for kw in keywords:
        if kw not in tags and len(tags) < 5:
            tags.append(kw)
    
    print(f"  [FALLBACK DEBUG] Tags after keywords: {tags}")
    
    if not tags:
        tags = [topic]
        print(f"  [FALLBACK DEBUG] No tags found, using topic")
    
    print(f"  [FALLBACK] Generated tags: {tags[:5]}")
    return tags[:5]


def parse_frontmatter(content: str) -> dict:
    """解析 frontmatter 为字典"""
    
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None
    
    frontmatter_text = match.group(1)
    frontmatter_dict = {}
    
    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if key == 'tags' and value.startswith('[') and value.endswith(']'):
                tags_str = value[1:-1]
                tags = [t.strip() for t in tags_str.split(',') if t.strip()]
                frontmatter_dict[key] = tags
            else:
                frontmatter_dict[key] = value
    
    return frontmatter_dict


def build_frontmatter(data: dict) -> str:
    """从字典构建 frontmatter 文本"""
    
    frontmatter = "---\n"
    
    order = ['topic', 'created', 'modified', 'tags']
    
    for key in order:
        if key in data:
            value = data[key]
            
            if key == 'tags' and isinstance(value, list):
                frontmatter += f"{key}: [{', '.join(value)}]\n"
            else:
                frontmatter += f"{key}: {value}\n"
    
    for key, value in data.items():
        if key not in order:
            if isinstance(value, list):
                frontmatter += f"{key}: [{', '.join(value)}]\n"
            else:
                frontmatter += f"{key}: {value}\n"
    
    frontmatter += "---\n\n"
    
    return frontmatter


def update_or_add_frontmatter(file_path: str, content: str, force_rebuild=False) -> tuple:
    """更新或添加 frontmatter"""
    
    existing_fm = parse_frontmatter(content)
    
    if existing_fm and not force_rebuild:
        new_modified = get_modified_time(file_path)
        old_modified = existing_fm.get('modified', '')
        
        if old_modified == new_modified:
            return (content, 'unchanged')
        
        print(f"  [UPDATE] Modified: {old_modified} -> {new_modified}")
        
        existing_fm['modified'] = new_modified
        
        match = re.match(r'^---\n.*?\n---\n\n?', content, re.DOTALL)
        body = content[match.end():] if match else content
        
        new_frontmatter = build_frontmatter(existing_fm)
        new_content = new_frontmatter + body
        
        return (new_content, 'updated')
    
    else:
        body = content
        if existing_fm:
            match = re.match(r'^---\n.*?\n---\n\n?', content, re.DOTALL)
            if match:
                body = content[match.end():]
            print(f"  [REBUILD] Regenerating frontmatter")
        
        topic = extract_topic(file_path)
        
        created = existing_fm.get('created') if existing_fm else get_created_time(file_path)
        modified = get_modified_time(file_path)
        
        print(f"  [INFO] Topic: {topic}")
        print(f"  [INFO] Created: {created}")
        print(f"  [INFO] Modified: {modified}")
        
        tags = generate_tags_by_ai(topic, body, file_path)
        
        data = {
            'topic': topic,
            'created': created,
            'modified': modified,
            'tags': tags
        }
        
        new_frontmatter = build_frontmatter(data)
        new_content = new_frontmatter + body
        
        status = 'rebuilt' if existing_fm else 'added'
        return (new_content, status)


def process_file(file_path: str, force_rebuild=False) -> str:
    """处理单个文件"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  [ERROR] Read failed: {e}")
        return None
    
    new_content, status = update_or_add_frontmatter(file_path, content, force_rebuild)
    
    if status == 'unchanged':
        print(f"  [SKIP] No changes needed")
        return 'unchanged'
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        if status == 'added':
            print(f"  [SUCCESS] Added frontmatter")
        elif status == 'updated':
            print(f"  [SUCCESS] Updated frontmatter")
        elif status == 'rebuilt':
            print(f"  [SUCCESS] Rebuilt frontmatter")
        
        return status
    except Exception as e:
        print(f"  [ERROR] Write failed: {e}")
        return None


def get_changed_files():
    """获取变更的文件"""
    
    try:
        event_path = os.environ.get('GITHUB_EVENT_PATH')
        if event_path and os.path.exists(event_path):
            import json
            try:
                with open(event_path) as f:
                    event = json.load(f)
                    before_sha = event.get('before')
                    after_sha = event.get('after', 'HEAD')
                    
                    if before_sha and before_sha != '0000000000000000000000000000000000000000':
                        print(f"\n[INFO] Using GitHub push event")
                        print(f"[INFO] Range: {before_sha[:7]}...{after_sha[:7]}")
                        
                        cmd = ['git', 'diff', '--name-only', before_sha, after_sha, '--', '*.md']
                        result = subprocess.check_output(cmd, text=True, encoding='utf-8').strip()
                        
                        if result:
                            print(f"[INFO] Files from push event:")
                            for f in result.split('\n'):
                                print(f"  - {f}")
                            return [f.strip() for f in result.split('\n') if f.strip()]
            except Exception as e:
                print(f"[WARN] Failed to parse GitHub event: {e}")
        
        cmd_check = ['git', 'rev-parse', '--verify', 'HEAD^2']
        is_merge = subprocess.run(cmd_check, capture_output=True, text=True).returncode == 0
        
        if is_merge:
            print(f"\n[INFO] Detected merge commit")
            
            cmd = ['git', 'diff', '--name-only', 'HEAD^1...HEAD^2', '--', '*.md']
            result = subprocess.check_output(cmd, text=True, encoding='utf-8').strip()
            
            if result:
                print(f"[INFO] Files from merge:")
                for f in result.split('\n'):
                    print(f"  - {f}")
                return [f.strip() for f in result.split('\n') if f.strip()]
            
            cmd = ['git', 'diff', '--name-only', 'HEAD^1', 'HEAD', '--', '*.md']
            result = subprocess.check_output(cmd, text=True, encoding='utf-8').strip()
            
            if result:
                print(f"[INFO] Files from merge (fallback):")
                for f in result.split('\n'):
                    print(f"  - {f}")
                return [f.strip() for f in result.split('\n') if f.strip()]
        
        print(f"\n[INFO] Using HEAD~2...HEAD")
        cmd = ['git', 'diff', '--name-only', 'HEAD~2', 'HEAD', '--', '*.md']
        result = subprocess.check_output(cmd, text=True, encoding='utf-8').strip()
        
        if result:
            print(f"[INFO] Files from HEAD~2:")
            for f in result.split('\n'):
                print(f"  - {f}")
            return [f.strip() for f in result.split('\n') if f.strip()]
        
        print(f"\n[INFO] Fallback to HEAD~1...HEAD")
        cmd = ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD', '--', '*.md']
        result = subprocess.check_output(cmd, text=True, encoding='utf-8').strip()
        
        if result:
            print(f"[INFO] Files from HEAD~1:")
            for f in result.split('\n'):
                print(f"  - {f}")
            return [f.strip() for f in result.split('\n') if f.strip()]
        
        return []
        
    except Exception as e:
        print(f"\n[ERROR] Git diff failed: {e}")
        return []


def test_api_connection():
    """测试 API 连接"""
    print("\n[DEBUG] Testing API connection...")
    
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not set!")
        return False
    
    print(f"[DEBUG] API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else '***'}")
    print(f"[DEBUG] API Base URL: {API_BASE_URL}")
    print(f"[DEBUG] Model: {MODEL}")
    
    try:
        print("[DEBUG] Sending test request...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": "测试连接，请回复'OK'"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"[DEBUG] Test response: {result}")
        print("[SUCCESS] API connection successful!")
        return True
        
    except Exception as e:
        print(f"[ERROR] API connection failed: {type(e).__name__}")
        print(f"[ERROR] Error message: {str(e)}")
        return False


def main():
    print("=" * 70)
    print("Frontmatter AutoWired")
    print("=" * 70)
    
    try:
        subprocess.run(
            ['git', 'config', 'core.quotepath', 'false'],
            check=False,
            capture_output=True
        )
    except:
        pass
    
    test_api_connection()
    
    force_rebuild = os.environ.get('FORCE_REBUILD', 'false').lower() == 'true'
    
    if force_rebuild:
        print("\n[MODE] Force rebuild: Will regenerate all frontmatter including tags")
    else:
        print("\n[MODE] Update: Will only update modified time for existing frontmatter")
    
    # 获取 PR 中已修改的文件
    pr_modified_files = os.environ.get('PR_MODIFIED_FILES', '').strip()
    pr_files_set = set()
    
    if pr_modified_files:
        pr_files_set = set(line.strip() for line in pr_modified_files.split('\n') if line.strip())
        if pr_files_set:
            print(f"\n[INFO] Files already in PR: {len(pr_files_set)}")
            for f in pr_files_set:
                print(f"  - {f}")
    
    files = get_changed_files()
    
    if not files:
        print("\n[INFO] No .md files changed")
        return
    
    files = [f for f in files if should_process_file(f)]
    
    # 过滤掉 PR 中已处理的文件
    if pr_files_set:
        original_count = len(files)
        files = [f for f in files if f not in pr_files_set]
        skipped = original_count - len(files)
        if skipped > 0:
            print(f"\n[INFO] Skipped {skipped} file(s) already in PR")
    
    if not files:
        print("\n[INFO] No new files to process")
        if pr_files_set:
            print("[INFO] All changed files are already in the open PR")
        return
    
    print(f"\n[INFO] Files to process: {len(files)}")
    
    added = 0
    updated = 0
    rebuilt = 0
    unchanged = 0
    failed = 0
    
    for i, file in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file}")
        result = process_file(file, force_rebuild)
        
        if result == 'added':
            added += 1
        elif result == 'updated':
            updated += 1
        elif result == 'rebuilt':
            rebuilt += 1
        elif result == 'unchanged':
            unchanged += 1
        else:
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Summary:")
    print(f"  Added:     {added}")
    print(f"  Updated:   {updated}")
    print(f"  Rebuilt:   {rebuilt}")
    print(f"  Unchanged: {unchanged}")
    print(f"  Failed:    {failed}")
    print(f"  Total:     {len(files)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
