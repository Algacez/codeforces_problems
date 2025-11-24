import requests
import json
import time
from bs4 import BeautifulSoup

def get_problemset():
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data['result'] if data['status'] == 'OK' else None

def get_problem_detail(contest_id, index):
    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    problem_statement = soup.find('div', class_='problem-statement')
    if not problem_statement:
        return None

    detail = {}

    # 题目描述
    desc = problem_statement.find('div', class_='')
    if desc:
        detail['description'] = desc.get_text(strip=True)

    # 输入输出格式
    input_spec = problem_statement.find('div', class_='input-specification')
    if input_spec:
        detail['input'] = input_spec.get_text(strip=True).replace('Input', '', 1).strip()

    output_spec = problem_statement.find('div', class_='output-specification')
    if output_spec:
        detail['output'] = output_spec.get_text(strip=True).replace('Output', '', 1).strip()

    # 样例
    samples = problem_statement.find('div', class_='sample-test')
    if samples:
        inputs = samples.find_all('div', class_='input')
        outputs = samples.find_all('div', class_='output')
        detail['samples'] = [
            {'input': inp.find('pre').get_text(strip=True), 'output': out.find('pre').get_text(strip=True)}
            for inp, out in zip(inputs, outputs) if inp.find('pre') and out.find('pre')
        ]

    return detail

def main():
    print("开始爬取 Codeforces 题库...")
    data = get_problemset()
    if not data:
        print("获取题目列表失败")
        return

    problems = data['problems']
    statistics = data['problemStatistics']

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


    with open('codeforces_problems.json', 'w', encoding='utf-8') as f:
        json.dump(list(problem_dict.values()), f, ensure_ascii=False, indent=2)

    print(f"\n已保存 {len(problem_dict)} 道题目到 codeforces_problems.json")

if __name__ == "__main__":
    main()
