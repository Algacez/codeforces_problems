from flask import Flask, render_template, request
import json

app = Flask(__name__)

TAG_CN = {
    # 基础算法
    'implementation': '实现',
    'math': '数学',
    'greedy': '贪心',
    'dp': '动态规划',
    'brute force': '暴力',
    'constructive algorithms': '构造',
    'sortings': '排序',
    'binary search': '二分查找',
    'two pointers': '双指针',
    'ternary search': '三分查找',
    'divide and conquer': '分治',
    'meet-in-the-middle': '折半搜索',
    'bitmasks': '位运算',

    # 数据结构
    'data structures': '数据结构',
    'dsu': '并查集',
    'trees': '树',
    'hashing': '哈希',
    'string suffix structures': '后缀结构',    # 后缀数组/后缀自动机/后缀树等
    'trie': '字典树',

    # 图论
    'graphs': '图论',
    'dfs and similar': 'DFS及其类似',
    'bfs': 'BFS',
    'shortest paths': '最短路',
    'graph matchings': '匹配',
    'flows': '网络流',
    'strongly connected components': '强连通分量',
    'topological sorting': '拓扑排序',

    # 字符串
    'strings': '字符串',
    'string suffix structures': '后缀结构',

    # 数学
    'number theory': '数论',
    'combinatorics': '组合数学',
    'probabilities': '概率',
    'fft': '快速傅里叶变换',
    'chinese remainder theorem': '中国剩余定理',
    'matrices': '矩阵',

    # 博弈 & 交互
    'games': '博弈论',
    'interactive': '交互式',

    # 2-SAT 与逻辑
    '2-sat': '2-SAT',

    # 其他经典技巧
    'expression parsing': '表达式解析',
    'sliding window': '滑动窗口',          # 新增常见标签
    'prefix sums': '前缀和',                # 2024-2025 常用
    'difference array': '差分',             # 常见中文叫法
    'segment trees': '线段树',
    'fenwick trees': '树状数组',            # 或 BIT
    'sparse tables': '稀疏表',
    'sqrt decomposition': '平方根分治',     # 或莫队算法相关
    'heavy-light decomposition': '树链剖分',
    'centroid decomposition': '点分治',

    # 几何
    'geometry': '计算几何',

    # 较冷门但偶尔出现
    'schedules': '调度问题',
    'randomization': '随机化',
    'physics': '物理',                      # 模拟题常见
    'expected value': '期望',
    'linear algebra': '线性代数',
}

def load_problems():
    with open('codeforces_problems.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    problems = load_problems()

    tags_dict = {}
    for prob in problems:
        for tag in prob.get('tags', []):
            if tag not in tags_dict:
                tags_dict[tag] = []
            tags_dict[tag].append(prob)

    selected_tag = request.args.get('tag')
    filtered_problems = tags_dict.get(selected_tag, []) if selected_tag else []

    # 按难度排序
    filtered_problems.sort(key=lambda x: x.get('rating') if isinstance(x.get('rating'), int) else 9999)

    return render_template('index.html',
                         tags=sorted(tags_dict.keys()),
                         selected_tag=selected_tag,
                         problems=filtered_problems,
                         total_count=len(problems),
                         tag_cn=TAG_CN)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
