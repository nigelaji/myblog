#-*- coding: utf-8 -*
__author__ = 'geebos'
import re
import markdown
from pygments import highlight
from pygments.token import Text, STANDARD_TYPES
from pygments.formatter import Formatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers import guess_lexer


def _get_ttype_class(ttype):
    fname = STANDARD_TYPES.get(ttype)
    if fname:
        return fname
    aname = ''
    while fname is None:
        aname = '-' + ttype[-1] + aname
        ttype = ttype.parent
        fname = STANDARD_TYPES.get(ttype)
    return fname + aname

def _line_num_tag_gen():
    line_num = 0
    def result():
        nonlocal line_num
        line_num += 1
        return f'<div class="line-numbers"><div class="line-num" data-line-num="{line_num}"></div></div>'
    return result

class HtmlLiFormatter(Formatter):
    def __init__(self, **options):
        Formatter.__init__(self, **options)

    def _get_css_class(self, ttype):
        """Return the css class of this token type prefixed with
        the classprefix option."""
        ttypeclass = _get_ttype_class(ttype)
        if ttypeclass:
            return ttypeclass
        return ''

    def html_encode(self, value):
        if '<' in value:
            value = value.replace('<', '&lt;')
        if '>' in value:
            value = value.replace('>', '&gt;')
        return value

    def _get_css_classes(self, ttype):
        """Return the css classes of this token type prefixed with
        the classprefix option."""
        cls = self._get_css_class(ttype)
        while ttype not in STANDARD_TYPES:
            ttype = ttype.parent
            cls = self._get_css_class(ttype) + ' ' + cls
        return cls

    def format(self, tokensource, outfile):
        # lastval is a string we use for caching
        # because it's possible that an lexer yields a number
        # of consecutive tokens with the same token type.
        # to minimize the size of the generated html markup we
        # try to join the values of same-type tokens here

        get_line_num_tag = _line_num_tag_gen()
        line_start_tag = '<li class="line">'
        line_end_tag = '</li>'

        code_tags = ['<ol class="code-container">']
        num_tags = ['<ol class="num-container">']

        line_value = ''

        outfile.write('<div class="code">')

        # 预处理
        temp_tokensource = []
        for ttype, value in tokensource:
            value = value.replace(' ', '&nbsp;')
            if ttype == Text and '\n' in value:
                values = re.findall(pattern='([^\n]*)(\n)([^\n]*)', string=value)

                for i in values:
                    for k in i:
                        if k != '':
                            temp_tokensource.append((ttype, k))
            else:
                temp_tokensource.append((ttype, value))

        for ttype, value in temp_tokensource:
            ttype_class = self._get_css_classes(ttype)

            value = self.html_encode(value)

            if value != '\n':
                line_value += f'<span class="{ttype_class}">{value}</span>'
            else:
                num_tags.append(get_line_num_tag())
                code_tags.append(f'{line_start_tag}<div class="highlight-code"><div class="code-line">{line_value}</div></div>{line_end_tag}\n')

                line_value = ''
        num_tags.append('</ol>')
        code_tags.append('</ol>')

        outfile.write(f'{"".join(num_tags)}{"".join(code_tags)}')
        outfile.write('</div>\n')

def code_to_html(match):
    type_and_content = re.findall(pattern='```(\w*)[\n|\r]([^`]+)```', string=match.group(0))
    formatter = HtmlLiFormatter(linenos=True, style='colorful')

    code_type = type_and_content[0][0]
    code_content = type_and_content[0][1]

    if code_type != '':
        substring = highlight(code=code_content, lexer=get_lexer_by_name(code_type), formatter=formatter)
    else:
        substring = highlight(code=code_content, lexer=guess_lexer(code_content), formatter=formatter)

    return substring


def md_to_html(mdstr):
    sub_string = re.sub(pattern='```([^`]+)```', repl=code_to_html, string=mdstr)

    exts = ['markdown.extensions.extra', 'markdown.extensions.tables']

    html = markdown.markdown(sub_string, extensions=exts)

    return html


