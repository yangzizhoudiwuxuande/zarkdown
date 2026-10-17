import re


def validate_zarkdown(text):
    """
    检查 Zarkdown 文本中的语法错误：
    1. 未闭合的成对符号（? \\ - ~ * $ _ [ <）
    2. 超链接/图片中缺少闭合括号 )
    自动跳过：
    - 多行代码块（~python ... ~）
    - 分割线/表格分隔符（以 5 个以上 - 开头的行）
    """
    errors = []
    lines = text.split('\n')

    symmetric_pairs = {'?', '\\', '-', '~', '*', '$', '_'}
    asymmetric_pairs = {'[': ']', '<': '>'}

    in_code_block = False

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not in_code_block:
            if re.match(r'^~[a-zA-Z0-9_]+$', stripped):
                in_code_block = True
                continue
        else:
            if stripped == '~':
                in_code_block = False
                continue
            continue

        if re.match(r'^-{5,}', stripped):
            continue

        stack = []
        i = 0
        n = len(line)
        while i < n:
            ch = line[i]

            if ch == '^' and i + 1 < n:
                i += 2
                continue

            if ch in symmetric_pairs:
                if stack and stack[-1][0] == ch:
                    stack.pop()
                else:
                    stack.append((ch, i + 1))
                i += 1
                continue

            if ch in asymmetric_pairs:
                stack.append((ch, i + 1))
                i += 1
                continue

            if ch in asymmetric_pairs.values():
                expected_open = {v: k for k, v in asymmetric_pairs.items()}[ch]
                if stack and stack[-1][0] == expected_open:
                    stack.pop()
                else:
                    errors.append({
                        'line': line_num,
                        'col': i + 1,
                        'symbol': ch,
                        'msg': f"多余的 '{ch}' 结束符，没有对应的起始符"
                    })
                i += 1
                continue

            i += 1

        for sym, col in stack:
            errors.append({
                'line': line_num,
                'col': col,
                'symbol': sym,
                'msg': f"未闭合的 '{sym}' 起始符"
            })

        # 检查超链接/图片的括号
        i = 0
        n = len(line)
        while i < n:
            ch = line[i]

            if ch == '*' and i + 1 < n:
                j = i + 1
                while j < n and line[j] != '*':
                    if line[j] == '^' and j + 1 < n:
                        j += 2
                        continue
                    j += 1
                if j < n and line[j] == '*':
                    if j + 1 < n and line[j + 1] == '(':
                        k = j + 2
                        while k < n and line[k] != ')':
                            k += 1
                        if k >= n:
                            errors.append({
                                'line': line_num,
                                'col': j + 2,
                                'symbol': '(',
                                'msg': "超链接缺少闭合的 ')'"
                            })
                    i = j + 1
                    continue
                else:
                    i += 1
                    continue

            if ch == '$' and i + 1 < n:
                j = i + 1
                while j < n and line[j] != '$':
                    if line[j] == '^' and j + 1 < n:
                        j += 2
                        continue
                    j += 1
                if j < n and line[j] == '$':
                    if j + 1 < n and line[j + 1] == '(':
                        k = j + 2
                        while k < n and line[k] != ')':
                            k += 1
                        if k >= n:
                            errors.append({
                                'line': line_num,
                                'col': j + 2,
                                'symbol': '(',
                                'msg': "图片缺少闭合的 ')'"
                            })
                    i = j + 1
                    continue
                else:
                    i += 1
                    continue

            i += 1

    return errors


def print_errors(errors):
    """友好地打印错误信息"""
    if not errors:
        return
    print("❌ 发现以下语法错误：\n")
    for err in errors:
        print(f"  第 {err['line']} 行，第 {err['col']} 列：{err['msg']} (符号: {err['symbol']})")
    print(f"\n共发现 {len(errors)} 个错误，请修正后再试。")
