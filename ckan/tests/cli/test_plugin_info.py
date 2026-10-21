# -*- coding: utf-8 -*-

import pytest

import ckan.plugins as p

from ckan.cli.cli import ckan


class KeywordOnlyActionPlugin(p.SingletonPlugin, p.IActions):
    """Plugin exposing an action with a keyword-only argument."""

    def get_actions(self):
        def test_action(context, data_dict, *, flag=True):
            """Action with a keyword-only argument."""
            return {}

        return {u"test_action": test_action}


@pytest.mark.provide_plugin(u"KeywordOnlyActionPlugin", KeywordOnlyActionPlugin)
@pytest.mark.ckan_config(u"ckan.plugins", u"KeywordOnlyActionPlugin")
@pytest.mark.usefixtures(u"with_plugins", u"with_extended_cli")
def test_plugin_info_with_keyword_only_action(cli):
    """``plugin-info`` must not crash on actions with keyword-only args."""
    result = cli.invoke(ckan, [u"plugin-info"])

    assert not result.exit_code, result.output
    assert u"test_action(context, data_dict, *, flag=True)" in result.output
