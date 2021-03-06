from docutils import nodes
from docutils.parsers.rst import roles

from sphinx import addnodes
from sphinx.writers.html import Writer, HTMLTranslator as BaseTranslator

def setup(app):
    app.set_translator('html', HTMLTranslator);

    return {'version': 'latest'}


class HTMLWriter(Writer):
    def __init__(self, builder):
        Writer.__init__(self)
        self.builder = builder

class HTMLTranslator(BaseTranslator):
    def __init__(self, builder, *args, **kwds):
        BaseTranslator.__init__(self, builder, *args, **kwds)

    def visit_admonition(self, node, name=''):
        type = 'primary'
        if name == 'note':
            type = 'info'
        elif name == 'warning':
            type = 'warning'
        elif name == 'danger':
            type = 'danger'
        self.body.append(self.starttag(
            node, 'div', CLASS=('card')))
        self.body.append(self.starttag(
            node, 'div', CLASS=('card-header bg-' + type)))

        title = node.traverse(nodes.paragraph)[0];
        self.body.append("<i class='fa fa-exclamation-circle'></i> " + name.title());

        self.body.append("</div>")
        self.body.append(self.starttag(
            node, 'div', CLASS=('card-body')))
        if (len(node.traverse(nodes.paragraph)) > 1):
            node.remove(node.traverse(nodes.paragraph)[0])
            self.body.append(self.starttag(
                node, 'h5', CLASS=('card-title')))
            self.body.append(title.astext());
            self.body.append('</h5>')

    def depart_admonition(self, node=None):
        self.body.append('</div></div>\n')

    def visit_literal_block(self, node):
        if node.rawsource != node.astext():
            # most probably a parsed-literal block -- don't highlight
            return BaseTranslator.visit_literal_block(self, node)
        lang = self.builder.config.highlight_language
        if 'language' in node:
            lang = node['language']
        highlighted = node[0]

        html = '<pre><code class="language-%s">%s</code></pre>' % (lang, highlighted)

        self.body.append(html)

        raise nodes.SkipNode
