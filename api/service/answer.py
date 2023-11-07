from config.llm_model import LLMModel
from model.query_snippet import QuerySnippet
import re
import os
import google.generativeai as palm


def get_full_query(
    userspace_path: str,
    result_file_name: str,
    num_ref_lines: int,
    query: str,
):
    result_path = f"{userspace_path}/{result_file_name}"

    file_names = os.listdir(userspace_path)
    file_names = [
        file_name for file_name in file_names if file_name != result_file_name
    ]
    if len(file_names) < 0:
        return False, 404, "files not found"

    table_query_snippet = QuerySnippet.retrieve_table_query_snippet()
    if table_query_snippet is None:
        return False, 500, "failed to run query"

    constraint_query_snippet = QuerySnippet.retrieve_constraint_query_snippet()
    if constraint_query_snippet is None:
        return False, 500, "failed to run query"

    full_query = ""
    for file_name in file_names:
        lines = ""
        path = f"{userspace_path}/{file_name}"
        with open(path) as f:
            for _ in range(num_ref_lines):
                lines += f.readline()
            f.close()

        chunk = table_query_snippet.snippet
        chunk = (
            chunk.replace("%file_name%", file_name)
            .replace("%path%", path)
            .replace("%lines%", lines)
        )
        full_query += chunk

    chunk = constraint_query_snippet.snippet
    chunk = (
        chunk.replace("%result_file_name%", result_file_name)
        .replace("%result_path%", result_path)
        .replace("%query%", query)
    )
    full_query += chunk

    return True, 0, full_query


def get_answer(full_query: str):
    completion = palm.generate_text(
        model=LLMModel.model,
        prompt=full_query,
        temperature=0,
        max_output_tokens=800,
    )
    return extract_source(completion.result)


def extract_source(raw: str):
    pattern = re.compile("```python(.*)```", re.DOTALL)
    found = pattern.findall(raw)

    if len(found) > 0:
        return True, found[0]

    return False, ""
