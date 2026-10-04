# ✨ Zarkdown (v2.0.3)

> [!WARNING]
> TRANSLATED BY DEEPSEEK AI.


> **Keyboard-friendly plain-text markup language** — All symbols are located in the main keyboard area, no Shift key required.

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/yangzizhoudiwuxuande/zarkdown)](https://github.com/yangzizhoudiwuxuande/zarkdown/stargazers)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/yangzizhoudiwuxuande/zarkdown)

Zarkdown is a brand-new plain-text markup language, designed for **fast writing** and **ultimate keyboard efficiency**. It's perfect for notes, technical documentation, blog posts, and can even be used as a configuration file format.

---

## 🎯 Design Philosophy

- **Keyboard-friendly**: All syntax symbols are in the main keyboard area, no need to move your fingers far
- **Intuitive**: `/` for headings (like path hierarchy), `?` for bold (like emphasis)
- **Plain text**: Any text editor can open it, highly human-readable
- **Extensible**: Supports tables, code blocks, footnotes, and other advanced features

---

## 📜 Complete Syntax Reference

| Effect | Syntax | Example | Renders as |
| :--- | :--- | :--- | :--- |
| **Headings 1–4** | `/` `//` `///` `////` + space | `/ Big Title` | `<h1>`~`<h4>` |
| **Bold** | `?text?` | `?important?` | `<strong>` |
| **Italic** | `\text\` | `\italic\` | `<i>` |
| **Strikethrough** | `-text-` | `-deleted-` | `<del>` |
| **Hyperlink** | `*text*(link)` | `*click*(https://x.com)` | `<a>` |
| **Image** | `$name$(link)` | `$logo$(./pic.png)` | `<img>` |
| **Inline code** | `~text~` | `~npm i~` | `<code>` |
| **Multi-line code block** | `~language` + `~` | `~python`...`~` | `<pre><code>` |
| **Unordered list** | `!text` (line start) | `!apple` | `<ul><li>` |
| **Quote** | `\|text` (line start) | `\| quoted text` | `<blockquote>` |
| **Table** | `\| Header \|` + `------` | See example below | `<table>` |
| **Comment** | `<text>` (no URL) | `<note>` | `<!-- -->` |
| **Footnote** | `[number]<text>` | `[1]<explanation>` | `<sup title="">` |
| **Horizontal rule** | `-----` (own line) | | `<hr>` |
| **Escape** | `^` before any symbol | `^/ not a heading` | Output as-is |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yangzizhoudiwuxuande/zarkdown.git
cd zarkdown

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -e .
```

---

## Usage

```bash
# Convert a .zkdn file to .html
zarkdown example.zkdn -o example.html

# Print directly to terminal (no file output)
zarkdown example.zkdn
```

---

## Examples

### Convert to HTML

Create a `hello.zkdn` file:

```zkdn
/ Welcome to Zarkdown

?Congratulations?, your format is working!

Here is a link: *click here*(https://github.com/yangzizhoudiwuxuande)

~python
print("Hello Zarkdown!")
~

```

Then run:

```bash
zarkdown hello.zkdn -w
```

The browser will open automatically and display the rendered HTML page. Edit `hello.zkdn` and save — the page refreshes automatically.

### Convert to Word / LaTeX

Converting to Word or LaTeX requires Pandoc.

```bash
brew install pandoc
```

Convert to Word:

```bash
zarkdown my_note.zkdn -f docx
```

Convert to LaTeX:

```bash
zarkdown my_note.zkdn -f latex
```

---

## Other Installation Methods

### Using a Distribution

Distributions are available in `.pkg`, `.tar.gz`, and `.zip` formats. If you use the `.pkg`, keep clicking "Continue" — the default installation location is your personal folder. The `.tar.gz` and `.zip` are archives. On macOS, you can double-click the archive to open it with Archive Utility and extract it.

### Using Homebrew

`brew install zarkdown` is not yet available, but you can use:

```bash
brew tap yangzizhoudiwuxuande/zarkdown
brew install zarkdown
```

---

## 📸 Preview

[![pm4y4lF.png](https://s41.ax1x.com/2026/08/01/pm4y4lF.png)](https://imgchr.com/i/pm4y4lF)

---

## Contributing

Contributions of any kind are welcome! You can:

- 🐛 Report bugs (describe them in Issues)
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit a Pull Request

---

## 📄 License

This project is released under the **MIT License**. You are free to use, modify, and distribute it.

---

## ❤️ Acknowledgements

Thank you for reading this document! If you find Zarkdown interesting, please give the project a ⭐ star to help more people discover it.

---

## 📝 Changelog

**v2.0.3 (2026-09-25)**
- Added version number flag

**v2.0.2 (2026-08-17)**
- Removed ordered lists
- Fixed several known issues

**v2.0.1 (2026-08-01)**
- **Syntax error checker**
  Automatically scans the entire document before conversion, detecting unclosed paired symbols (`?`, `\`, `-`, `~`, `*`, `$`, `[`, `<`) and precisely reporting line and column numbers to help users locate problems quickly.

- **Bracket pairing check**
  For hyperlinks `*text*(link)` and images `$name$(link)`, it automatically detects missing closing brackets `)` to avoid generating invalid links.

- **Multi-line table support**
  Table cells can now wrap across lines, merged automatically via indented continuation lines and converted to `<br>` tags in the output.

- **Escape character `^`**
  Add `^` before any special symbol to output it as-is without being processed by the parser, e.g. `^/ not a heading`.

- **Smart skip mechanism**
  The error checker automatically skips horizontal rules (lines starting with `-----`), table separator rows, and content inside multi-line code blocks to avoid false positives.

- **Automatic output filename**
  If `-o` is not specified, the output filename is generated automatically from the input filename and format (e.g. `note.html`, `note.pdf`).

**v2.0.0 (2026-07-28)**
- Support for exporting to Word/LaTeX and other formats (requires Pandoc)

**v1.2.2 (2026-07-26)**
- Support for multi-line tables

**v1.2.1 (2026-07-26)**
- Support for nested syntax (italic inside bold, bold inside hyperlinks, etc.)

**v1.2.0 (2026-07-25)**
- Improved the appearance of quotes and tables

**v1.1.0 (2026-07-25)**
- ✨ Added `-w` watch mode — auto-reconvert and refresh on save
- ✨ Automatically open the generated HTML in the browser for live preview
- 🐛 Fixed Chinese encoding issues, compatible with UTF-8 files with BOM
- 🐛 Fixed relative path opening failure on macOS
- 📝 Improved README documentation with a complete syntax table and examples

**v1.0.0 (2026-07-25)**
- 🎉 First release with full Zarkdown syntax support

---

## FAQ

### What's the difference between Zarkdown and Markdown?

All of Zarkdown's syntax symbols are in the main keyboard area, no Shift key required, making writing smoother. Each symbol also has a clear, unique purpose with no ambiguity.

### How do I migrate from Markdown to Zarkdown?

There is no automatic conversion tool yet, but Zarkdown's syntax is simple and intuitive, so manual conversion is low-cost. A conversion tool may be provided in the future.

---

Happy Writing with Zarkdown!

---

## Contact

yangzizhou2026@outlook.com

QQ Group: 1106476845

---

## Zarkdown Viewer

A Zarkdown Viewer app is available in a separate repository called **ZarkdownApp**.
