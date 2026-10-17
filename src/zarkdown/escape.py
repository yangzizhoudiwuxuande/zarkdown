import re


def escape_text(text):
    """将 ^符号 替换为不可打印占位符"""
    def repl(m):
        return f'\x00ESC_{ord(m.group(1))}\x00'
    return re.sub(r'\^([/\\?~\-*$•|!<\[\]_])', repl, text)


def unescape_text(text):
    """恢复占位符为原字符"""
    return re.sub(r'\x00ESC_(\d+)\x00', lambda m: chr(int(m.group(1))), text)
