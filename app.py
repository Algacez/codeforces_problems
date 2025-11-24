from flask import Flask, render_template, request
import json

app = Flask(__name__)

TAG_CN = {
    'implementation': '实现', 'math': '数学', 'greedy': '贪心', 'dp': '动态规划',
    'data structures': '数据结构', 'brute force': '暴力', 'constructive algorithms': '构造',
    'graphs': '图论', 'sortings': '排序', 'binary search': '二分', 'dfs and similar': 'DFS',
    'trees': '树', 'strings': '字符串', 'number theory': '数论', 'combinatorics': '组合数学',
    'geometry': '几何', 'bitmasks': '位运算', 'two pointers': '双指针', 'dsu': '并查集',
    'shortest paths': '最短路', 'probabilities': '概率', 'divide and conquer': '分治',
    'hashing': '哈希', 'games': '博弈', 'flows': '网络流', 'interactive': '交互',
    'matrices': '矩阵', 'string suffix structures': '后缀结构', 'fft': 'FFT',
    'graph matchings': '图匹配', 'ternary search': '三分', 'expression parsing': '表达式解析',
    'meet-in-the-middle': '折半搜索', '2-sat': '2-SAT', 'chinese remainder theorem': '中国剩余定理',
    'schedules': '调度'
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
    app.run(debug=True)
