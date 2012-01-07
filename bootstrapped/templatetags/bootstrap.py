from django import template
from django.conf import settings

register = template.Library()

SCRIPT_TAG = '<script src="%sbootstrap/js/bootstrap-%s.js" type="text/javascript"></script>'

class BootstrapJSNode(template.Node):

    def __init__(self, args):
        self.args = set(args)

    def render_all_scripts(self):
        results = [
            SCRIPT_TAG % (settings.STATIC_URL, 'alerts'),
            SCRIPT_TAG % (settings.STATIC_URL, 'buttons'),
            SCRIPT_TAG % (settings.STATIC_URL, 'dropdown'),
            SCRIPT_TAG % (settings.STATIC_URL, 'modal'),
            SCRIPT_TAG % (settings.STATIC_URL, 'popover'),
            SCRIPT_TAG % (settings.STATIC_URL, 'scrollspy'),
            SCRIPT_TAG % (settings.STATIC_URL, 'tabs'),
            SCRIPT_TAG % (settings.STATIC_URL, 'twipsy'),
        ]
        return '\n'.join(results)

    def render(self, context):
        if 'all' in self.args:
            return self.render_all_scripts()
        else:
            # popover requires twipsy
            if 'popover' in self.args:
                self.args.add('twipsy')
            tags = [SCRIPT_TAG % (settings.STATIC_URL,tag) for tag in self.args]
            return '\n'.join(tags)

@register.simple_tag
def bootstrap_custom_less(less):
    output=[
            '<link rel="stylesheet/less" type="text/css" href="%sbootstrap/%s" media="all">' % (settings.STATIC_URL, less),
            '<script src="%sbootstrap/js/less-1.1.5.min.js" type="text/javascript"></script>' % settings.STATIC_URL,
        ]
    return '\n'.join(output)

@register.simple_tag
def bootstrap_css():
    if settings.TEMPLATE_DEBUG:
        return '<link rel="stylesheet" type="text/css" href="%sbootstrap/bootstrap.css">' % settings.STATIC_URL
    else:
        return '<link rel="stylesheet" type="text/css" href="%sbootstrap/bootstrap.min.css">' % settings.STATIC_URL

@register.simple_tag
def bootstrap_less():
    output=[
            '<link rel="stylesheet/less" type="text/css" href="%sbootstrap/lib/bootstrap.less">' % settings.STATIC_URL,
            '<script src="%sbootstrap/less.js" type="text/javascript"></script>' % settings.STATIC_URL,
        ]
    return '\n'.join(output)

@register.tag(name='bootstrap_js')
def do_bootstrap_js(parser, token):
    print '\n'.join(token.split_contents())
    return BootstrapJSNode(token.split_contents()[1:])