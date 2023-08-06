from yafowil.base import factory
from yafowil.utils import entry_point
import os


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')

js = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'widget.js',
    'order': 20,
}]
default_css = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'default/widget.css',
    'order': 20,
}]
bootstrap_css = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'bootstrap/widget.css',
    'order': 20,
}]
plone5_css = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'plone5/widget.css',
    'order': 20,
}]


@entry_point(order=10)
def register():
    import yafowil.widget.dict.widget  # noqa
    factory.register_theme('default', 'yafowil.widget.dict',
                           resourcedir, js=js, css=default_css)
    factory.register_theme('bootstrap', 'yafowil.widget.dict',
                           resourcedir, js=js, css=bootstrap_css)
    factory.register_theme('plone5', 'yafowil.widget.dict',
                           resourcedir, js=js, css=plone5_css)
