import ast
import io
import re
import sys
import tokenize

import nbformat

HEADING_PATTERN = re.compile(r"^### 3\.\d+ Resolvendo")


def has_comment(source):
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return any(token.type == tokenize.COMMENT for token in tokens)


def has_docstring(source):
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            first = node.body[0] if node.body else None
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                return True
    return False


def code_problems(index, source):
    problems = []
    try:
        if has_comment(source):
            problems.append(f"célula {index}: comentário no código")
        if has_docstring(source):
            problems.append(f"célula {index}: docstring no código")
    except (SyntaxError, tokenize.TokenError) as error:
        problems.append(f"célula {index}: código inválido ({error})")
    return problems


def triad_problems(cells, index):
    follow_up = cells[index + 1 : index + 4]
    expected = ["code", "code", "markdown"]
    title = cells[index].source.strip()
    if len(title.splitlines()) != 1:
        return [f"célula {index}: o título de problema deve ter uma única linha"]
    if [cell.cell_type for cell in follow_up] != expected:
        return [f"célula {index}: '{title}' deve ser seguido de duas células de código e depois de Markdown"]
    return []


def check_notebook(path):
    cells = nbformat.read(path, as_version=4).cells
    problems = []
    for index, cell in enumerate(cells):
        if cell.cell_type == "code" and cell.source.strip():
            problems.extend(code_problems(index, cell.source))
            if cell.execution_count is None:
                problems.append(f"célula {index}: não executada")
            if any(output.output_type == "error" for output in cell.get("outputs", [])):
                problems.append(f"célula {index}: saída com erro")
        if cell.cell_type == "markdown":
            if "<<" in cell.source:
                problems.append(f"célula {index}: marcador '<<' pendente")
            if HEADING_PATTERN.match(cell.source.strip()):
                problems.extend(triad_problems(cells, index))
    return problems


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    problems = check_notebook(sys.argv[1])
    for problem in problems:
        print(problem)
    print(f"{len(problems)} problema(s) encontrado(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
