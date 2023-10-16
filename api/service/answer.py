from config.llm_model import LLMModel
import google.generativeai as palm
import re


def get_answer(query: str):
    prompt = f"""
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
    {query}
    Extract only existing columns of BBB.csv.
    
    
    constraints below.
    using python, pandas and do not print results.
    if you would use pd.merge, you must use left_on, right_on.
    """

    completion = palm.generate_text(
        model=LLMModel.Model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=800,
    )
    answer = _extract_source(completion.result)

    return answer


def _extract_source(raw: str):
    pattern = re.compile("```python(.*)```", re.DOTALL)
    found = pattern.findall(raw)

    if len(found) > 0:
        return found[0]

    return ""
