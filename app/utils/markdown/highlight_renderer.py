import houdini
import misaka
from pygments               import highlight
from pygments.formatters    import HtmlFormatter, ClassNotFound
from pygments.lexers        import get_lexer_by_name

class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        # default
        return '\n<pre><code>{}</code></pre>\n'.format(
                            houdini.escape_html(text.strip()))