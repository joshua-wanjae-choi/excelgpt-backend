from api.secret import Secret
import google.generativeai as palm
import re


def write_source(source: str):
    path = "expt_source.py"
    with open(path, "w") as f:
        f.write(source)


def extract_source(raw: str):
    pattern = re.compile("```python(.*)```", re.DOTALL)
    found = pattern.findall(raw)

    if len(found) > 0:
        write_source(found[0])


if __name__ == "__main__":
    palm.configure(api_key=Secret.API_KEY)
    models = [
        m
        for m in palm.list_models()
        if "generateText" in m.supported_generation_methods
    ]
    print(f"${models=}")

    model = models[0].name

    prompt_1 = """
    Table name = AB
    Columns = ['col1', 'col2', 'col3']
    CSV data = `
    1, 2, 3
    4, 5, 6
    7, 8, 9
    `
    request below.
    add 1 to col names 'col3' using python, pandas.
    """

    prompt_2 = """
    Table name is AAA.
    file name is AAA.csv.
    AAA CSV data = `
    col1, col2, col3
    김, 2, 3
    이, 5, 6
    박, 8, 9
    `.
    first line of AAA.csv is header.
    
    Table name is BBB.
    file name is BBB.csv.
    BBB CSV data = `
    col4
    김
    `.
    first line of BBB.csv is header.
    
    result file name is update.csv
    
    request below.
    AAA.col1 과 BBB.col4 값이 같다면 BBB에 col5를 새로 만들고 AAA.col2값을 BBB.col5에 대입하라.
    AAA.col1.과 BBB.col4 값이 다르다면 BBB.col5에 -1을 대입하라.
    결과 테이블에 BBB.col4의 모든 값을 반드시 포함시켜라.
    Extract only existing BBB table columns and newly added columns from update.csv.
    
    
    constraints below.
    using python, pandas and do not print results.
    if you would use pd.merge, you must use left_on, right_on.
    """

    prompt_3 = """
    dataframe name is AAA.
    file name is AAA.csv.
    AAA CSV data = `
    col1, col2, col3
    김, 2, 3
    이, 5, 6
    박, 8, 9
    `.
    first line of AAA.csv is header.
    
    dataframe name is BBB.
    file name is BBB.csv.
    BBB CSV data = `
    col4
    김
    `.
    first line of BBB.csv is header.
    
    result dataframe is named update.
    result file name is update.csv.
    
    request below.
    기준 컬럼은 AAA.col1, BBB.col4으로 AAA와 BBB를 left join 실행.
    col4 값이 없는 경우 -1을 값으로 할당하라.
    Extract only existing columns of BBB.csv.
    
    
    constraints below.
    using python, pandas and do not print results.
    if you would use pd.merge, you must use left_on, right_on.
    """
    prompt = prompt_3

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=800,
    )
    print(f"${completion.result=}")
    extract_source(completion.result)
