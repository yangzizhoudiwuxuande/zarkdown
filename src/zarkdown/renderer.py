import re
from .escape import escape_text
from .inline import parse_inline


HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zarkdown 输出</title>
    <style>
        body {{
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #1e1e2f;
            background-color: #fafafa;
        }}
        h1, h2, h3, h4 {{ color: #1e1e2f; margin-top: 1.5em; }}
        h1 {{ border-bottom: 2px solid #eee; padding-bottom: 0.3em; }}
        blockquote {{
            margin: 1.2em 0;
            padding: 0.8em 1.2em;
            border-left: 4px solid #4a90d9;
            background-color: #f0f4ff;
            border-radius: 0 4px 4px 0;
            color: #2c3e50;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            font-size: 0.95em;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
            vertical-align: top;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: 600;
        }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        pre {{
            background: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
        }}
        code {{
            font-family: "SF Mono", "Fira Code", monospace;
            font-size: 0.9em;
        }}
        hr {{
            border: none;
            border-top: 2px dashed #ccc;
            margin: 2em 0;
        }}
        sup {{
            background: #eee;
            padding: 0.1em 0.4em;
            border-radius: 4px;
            font-size: 0.75em;
            cursor: help;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>'''


def _render_table(lines, i, escaped_line):
    """解析表格，返回 (html_string, next_index)"""
    next_esc = escape_text(lines[i + 1])
    after_esc = escape_text(lines[i + 2]) if i + 2 < len(lines) else ''
    if not (re.match(r'^-{5,}$', next_esc.strip()) and re.match(r'^\|.*\|$', after_esc)):
        return None, i

    headers = [h.strip() for h in escaped_line.split('|')[1:-1]]
    html = ['<table><thead><tr>']
    for h in headers:
        html.append(f'<th>{parse_inline(h)}</th>')
    html.append('</tr></thead><tbody>')

    j = i + 2
    current_cells = None
    in_data_row = False
    while j < len(lines):
        cur_raw = lines[j]
        cur_esc = escape_text(cur_raw)
        trimmed = cur_esc.strip()
        if re.match(r'^-{5,}$', trimmed):
            j += 1
            continue
        if re.match(r'^\|.*\|$', cur_esc):
            if in_data_row and current_cells is not None:
                html.append('<tr>')
                for cell in current_cells:
                    html.append(f'<td>{parse_inline(cell)}</td>')
                html.append('</tr>')
                current_cells = None
                in_data_row = False
            cells = [c.strip() for c in cur_esc.split('|')[1:-1]]
            while len(cells) < len(headers):
                cells.append('')
            current_cells = cells
            in_data_row = True
            j += 1
            continue
        elif in_data_row and cur_raw.startswith('  '):
            if current_cells and len(current_cells) > 0:
                content = cur_raw.lstrip()
                current_cells[-1] = current_cells[-1] + '[Z_BR]' + content
            j += 1
            continue
        else:
            break

    if in_data_row and current_cells is not None:
        html.append('<tr>')
        for cell in current_cells:
            html.append(f'<td>{parse_inline(cell)}</td>')
        html.append('</tr>')
    html.append('</tbody></table>')
    return ''.join(html), j


def _render_code_block(lines, i):
    """解析多行代码块，返回 (html_string, next_index)"""
    raw_line = lines[i]
    lang = raw_line.strip()[1:]
    code_lines = []
    j = i + 1
    while j < len(lines) and lines[j].strip() != '~':
        code_lines.append(lines[j])
        j += 1
    if j < len(lines) and lines[j].strip() == '~':
        j += 1
    html = f'<pre><code class="language-{lang}">{"\n".join(code_lines)}</code></pre>'
    return html, j


def _render_list(lines, i, marker='!'):
    """解析无序列表，返回 (html_string, next_index)"""
    items = []
    while i < len(lines) and escape_text(lines[i]).startswith(marker):
        items.append(f'<li>{parse_inline(escape_text(lines[i])[1:].strip())}</li>')
        i += 1
    return f'<ul>{"".join(items)}</ul>', i


def zarkdown_to_html(text):
    """将 Zarkdown 文本转换为完整的 HTML 页面"""
    lines = text.split('\n')
    result = []
    i = 0

    while i < len(lines):
        raw_line = lines[i]
        escaped_line = escape_text(raw_line)

        # 多行代码块
        if re.match(r'^~[a-zA-Z0-9_]+$', raw_line.strip()):
            html, i = _render_code_block(lines, i)
            result.append(html)
            continue

        # 表格
        if re.match(r'^\|.*\|$', escaped_line) and i + 2 < len(lines):
            html, new_i = _render_table(lines, i, escaped_line)
            if html is not None:
                result.append(html)
                i = new_i
                continue

        # 标题
        if re.match(r'^//// ', escaped_line):
            result.append(f'<h4>{parse_inline(escaped_line[5:])}</h4>')
        elif re.match(r'^/// ', escaped_line):
            result.append(f'<h3>{parse_inline(escaped_line[4:])}</h3>')
        elif re.match(r'^// ', escaped_line):
            result.append(f'<h2>{parse_inline(escaped_line[3:])}</h2>')
        elif re.match(r'^/ ', escaped_line):
            result.append(f'<h1>{parse_inline(escaped_line[2:])}</h1>')

        # 无序列表
        elif escaped_line.startswith('!'):
            html, i = _render_list(lines, i, '!')
            result.append(html)
            continue

        # 引用
        elif escaped_line.startswith('|'):
            result.append(f'<blockquote>{parse_inline(escaped_line[1:].strip())}</blockquote>')

        # 分割线
        elif re.match(r'^-{5,}$', escaped_line.strip()):
            result.append('<hr>')

        # 普通段落
        else:
            if raw_line.strip():
                result.append(f'<p>{parse_inline(escaped_line)}</p>')
            else:
                result.append('')

        i += 1

    html_content = '\n'.join(result)
    html_content = html_content.replace('[Z_BR]', '<br>')
    return HTML_TEMPLATE.format(content=html_content)
