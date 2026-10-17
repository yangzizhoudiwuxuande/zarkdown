import re
from .escape import escape_text, unescape_text


class _InlineParser:
    """递归解析行内标记，支持嵌套"""

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.n = len(text)

    def parse(self):
        parts = []
        while self.pos < self.n:
            ch = self.text[self.pos]
            if ch == '^':
                self.pos += 1
                if self.pos < self.n:
                    parts.append(self.text[self.pos])
                    self.pos += 1
                continue
            if ch == '?':
                parts.append(self._parse_until('?', '<strong>', '</strong>'))
            elif ch == '\\':
                parts.append(self._parse_until('\\', '<i>', '</i>'))
            elif ch == '-':
                parts.append(self._parse_until('-', '<del>', '</del>'))
            elif ch == '~':
                parts.append(self._parse_until('~', '<code>', '</code>'))
            elif ch == '_':
                parts.append(self._parse_until('_', '<u>', '</u>'))
            elif ch == '*':
                parts.append(self._parse_link())
            else:
                parts.append(ch)
                self.pos += 1
        return ''.join(parts)

    def _parse_until(self, end_char, open_tag, close_tag):
        self.pos += 1
        inner_chars = []
        while self.pos < self.n and self.text[self.pos] != end_char:
            ch = self.text[self.pos]
            if ch == '^':
                self.pos += 1
                if self.pos < self.n:
                    inner_chars.append(self.text[self.pos])
                    self.pos += 1
                continue
            inner_chars.append(ch)
            self.pos += 1
        if self.pos < self.n and self.text[self.pos] == end_char:
            self.pos += 1
        inner_text = ''.join(inner_chars)
        parsed_inner = _InlineParser(inner_text).parse()
        return f'{open_tag}{parsed_inner}{close_tag}'

    def _parse_link(self):
        self.pos += 1
        text_start = self.pos
        while self.pos < self.n and self.text[self.pos] != '*':
            if self.text[self.pos] == '^':
                self.pos += 1
                if self.pos < self.n:
                    self.pos += 1
                continue
            self.pos += 1
        if self.pos >= self.n or self.text[self.pos] != '*':
            return '*' + self.text[text_start:self.pos]
        link_text = self.text[text_start:self.pos]
        self.pos += 1
        if self.pos < self.n and self.text[self.pos] == '(':
            self.pos += 1
            url_start = self.pos
            while self.pos < self.n and self.text[self.pos] != ')':
                self.pos += 1
            if self.pos < self.n and self.text[self.pos] == ')':
                url = self.text[url_start:self.pos]
                self.pos += 1
                parsed_text = _InlineParser(link_text).parse()
                return f'<a href="{url}">{parsed_text}</a>'
            else:
                return '*' + link_text + '*(' + self.text[url_start:self.pos]
        else:
            return '*' + link_text + '*'


def parse_inline(text):
    """行内解析入口，处理注释、脚注、图片，然后交给 _InlineParser"""
    escaped_text = escape_text(text)

    def replace_comment(m):
        if re.search(r'https?://|ftp://|@', m.group(1)):
            return m.group(0)
        return f'<!-- {m.group(1)} -->'

    escaped_text = re.sub(r'<([^>]+)>', replace_comment, escaped_text)
    escaped_text = re.sub(r'\[(\d+)\]<([^>]+)>', r'<sup title="\2">[\1]</sup>', escaped_text)
    escaped_text = re.sub(r'\$(.+?)\$\(([^\)]+)\)', r'<img src="\2" alt="\1">', escaped_text)

    parser = _InlineParser(escaped_text)
    result = parser.parse()
    result = unescape_text(result)
    return result
