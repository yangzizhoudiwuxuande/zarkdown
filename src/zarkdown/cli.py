import argparse
import os
import sys
import time
import webbrowser

from ._version import __version__
from .renderer import zarkdown_to_html
from .validator import validate_zarkdown, print_errors

try:
    import pypandoc
except ImportError:
    pypandoc = None


def _default_output(input_path, fmt):
    base = input_path.rsplit('.', 1)[0]
    ext = {'html': '.html', 'pdf': '.pdf', 'docx': '.docx', 'latex': '.tex'}
    return base + ext.get(fmt, '.html')


def main():
    parser = argparse.ArgumentParser(
        description="将 Zarkdown 文件转为 HTML/PDF/DOCX/LaTeX",
        epilog="示例: zarkdown input.zkdn -o output.html"
    )
    parser.add_argument("input", nargs="?", help="输入的 .zkdn 文件路径")
    parser.add_argument("-o", "--output", default=None,
                        help="输出文件路径（默认：根据输入文件名和格式自动生成）")
    parser.add_argument("-w", "--watch", action="store_true",
                        help="监听文件变化，自动重新转换并刷新浏览器（仅 HTML 格式）")
    parser.add_argument("-f", "--format",
                        choices=['html', 'pdf', 'docx', 'latex'],
                        default='html',
                        help="输出格式 (默认: html)")
    parser.add_argument("--no-check", action="store_true",
                        help="跳过语法错误检查（不推荐）")
    parser.add_argument("-v", "--version", action="version",
                        version=f"Zarkdown {__version__}",
                        help="显示版本号并退出")
    args = parser.parse_args()

    if args.input is None:
        parser.print_help()
        sys.exit(0)

    if args.output is None:
        args.output = _default_output(args.input, args.format)

    def convert():
        try:
            with open(args.input, 'r', encoding='utf-8-sig') as f:
                content = f.read()

            if not args.no_check:
                errors = validate_zarkdown(content)
                if errors:
                    print_errors(errors)
                    return

            html = zarkdown_to_html(content)

            if args.format == 'html':
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"✅ {args.input} -> {args.output}  ({time.strftime('%H:%M:%S')})")
                if args.watch:
                    webbrowser.open('file://' + os.path.abspath(args.output))
            else:
                if pypandoc is None:
                    print("❌ 导出 PDF/DOCX/LaTeX 需要安装 pypandoc 和 pandoc 工具。")
                    print("   pip install pypandoc")
                    print("   https://pandoc.org/installing.html")
                    return
                extra_args = ['--pdf-engine=xelatex'] if args.format == 'pdf' else []
                try:
                    pypandoc.convert_text(
                        html, to=args.format, format='html',
                        outputfile=args.output, extra_args=extra_args
                    )
                    print(f"✅ {args.input} -> {args.output} ({args.format})  ({time.strftime('%H:%M:%S')})")
                except Exception as e:
                    print(f"❌ 导出 {args.format} 失败: {e}")
                    print("   请确认 pandoc 已正确安装，PDF 导出需要 LaTeX 引擎 (如 xelatex)")
        except FileNotFoundError:
            print(f"❌ 错误：找不到文件 {args.input}")
        except Exception as e:
            print(f"❌ 转换出错: {e}")

    convert()

    if args.watch and args.format == 'html':
        print(f"👀 正在监听 {args.input} 的变化（按 Ctrl+C 停止）...")
        try:
            last_mtime = os.path.getmtime(args.input)
            while True:
                current_mtime = os.path.getmtime(args.input)
                if current_mtime > last_mtime:
                    last_mtime = current_mtime
                    convert()
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n👋 停止监听")
    elif args.watch and args.format != 'html':
        print("⚠️ 监听模式仅支持 HTML 格式。请使用 -f html 或移除 -w 参数。")
