# encoding: utf-8
from __future__ import annotations

from typing import Any, Callable

import click
import ckan.plugins as p


@click.command(
    name=u'plugin-info',
    short_help=u'Provide info on installed plugins.'
)
def plugin_info():
    u''' print info about current plugins from the .ini file'''
    import ckan.plugins as p
    interfaces = {}
    plugins = {}
    for name in dir(p):
        item = getattr(p, name)
        try:
            if issubclass(item, p.Interface):
                interfaces[item] = {u'class': item}
        except TypeError:
            pass

    for interface in interfaces:
        for plugin in p.PluginImplementations(interface):
            name = plugin.name
            if name not in plugins:
                plugins[name] = {
                    u'doc': plugin.__doc__,
                    u'class': plugin,
                    u'implements': []
                }
            plugins[name][u'implements'].append(interface.__name__)

    for plugin in plugins:
        p = plugins[plugin]
        click.echo(plugin + u':')
        click.echo(u'-' * (len(plugin) + 1))
        if p[u'doc']:
            click.echo(p[u'doc'])
        click.echo(u'Implements:')
        for i in p[u'implements']:
            extra = None
            if i == u'ITemplateHelpers':
                extra = _template_helpers(p[u'class'])
            if i == u'IActions':
                extra = _actions(p[u'class'])
            click.echo(u'    {i}'.format(i=i))
            if extra:
                click.echo(extra)
        click.echo()


def _template_helpers(plugin_class: p.ITemplateHelpers):
    u''' Return readable helper function info. '''
    helpers = plugin_class.get_helpers()
    return _function_info(helpers)


def _actions(plugin_class: p.IActions):
    u''' Return readable action function info. '''
    actions = plugin_class.get_actions()
    return _function_info(actions)


def _function_info(functions: dict[str, Callable[..., Any]]):
    u''' Take a dict of functions and output readable info '''
    import inspect
    output = []
    for function_name in functions:
        fn = functions[function_name]
        params = []
        star_added = False
        for name, parameter in inspect.signature(fn).parameters.items():
            if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
                star_added = True
                params.append(u'*' + name)
            elif parameter.kind is inspect.Parameter.VAR_KEYWORD:
                params.append(u'**' + name)
            else:
                if parameter.kind is inspect.Parameter.KEYWORD_ONLY and not star_added:
                    params.append(u'*')
                    star_added = True
                if parameter.default is inspect.Parameter.empty:
                    params.append(name)
                else:
                    params.append(u'{0}={1!r}'.format(name, parameter.default))
        params = u', '.join(params)
        output.append(u'        {function_name}({params})'.format(
            function_name=function_name, params=params))
        # doc string
        if fn.__doc__:
            bits = fn.__doc__.split(u'\n')
            for bit in bits:
                output.append(u'            {bit}'.format(bit=bit))
    return (u'\n').join(output)
