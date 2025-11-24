import requests
import json
import os

def main():
    json_file = 'codeforces_problems.json'

    # 只获取最新题目检查
    response = requests.get('https://codeforces.com/api/problemset.problems')
    if response.status_code != 200:
        print("获取数据失败")
        return

    data = response.json()
    if data['status'] != 'OK':
        print("API 返回错误")
        return

    latest_problem = data['result']['problems'][0]
    latest_new = f"{latest_problem['contestId']}{latest_problem['index']}"

    # 检查本地最新题目
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            old_data = json.load(f)

        if old_data:
            latest_old = f"{old_data[0]['contestId']}{old_data[0]['index']}"
            if latest_old == latest_new:
                print(f"题库已是最新 (最新题: {latest_new})")
                return

    # 需要更新，获取完整数据
    print(f"发现新题目 {latest_new}，开始更新...")
    problems = data['result']['problems']
    statistics = data['result']['problemStatistics']

    problem_dict = {}
    for prob in problems:
        key = f"{prob['contestId']}{prob['index']}"
        problem_dict[key] = {
            'contestId': prob['contestId'],
            'index': prob['index'],
            'name': prob['name'],
            'type': prob['type'],
            'rating': prob.get('rating', 'N/A'),
            'tags': prob.get('tags', [])
        }

    for stat in statistics:
        key = f"{stat['contestId']}{stat['index']}"
        if key in problem_dict:
            problem_dict[key]['solvedCount'] = stat['solvedCount']

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(list(problem_dict.values()), f, ensure_ascii=False, indent=2)

    print(f"题库已更新: {len(problem_dict)} 题")

if __name__ == "__main__":
    main()
