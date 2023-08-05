# This file exists within 'config-decorator':
#
#   https://github.com/hotoffthehamster/config-decorator
#
# Copyright © 2019-2020 Landon Bouma. All rights reserved.
#
# Permission is hereby granted,  free of charge,  to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge,  publish,  distribute, sublicense,
# and/or  sell copies  of the Software,  and to permit persons  to whom the
# Software  is  furnished  to do so,  subject  to  the following conditions:
#
# The  above  copyright  notice  and  this  permission  notice  shall  be
# included  in  all  copies  or  substantial  portions  of  the  Software.
#
# THE  SOFTWARE  IS  PROVIDED  "AS IS",  WITHOUT  WARRANTY  OF ANY KIND,
# EXPRESS OR IMPLIED,  INCLUDING  BUT NOT LIMITED  TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE  FOR ANY
# CLAIM,  DAMAGES OR OTHER LIABILITY,  WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE,  ARISING FROM,  OUT OF  OR IN  CONNECTION WITH THE
# SOFTWARE   OR   THE   USE   OR   OTHER   DEALINGS  IN   THE  SOFTWARE.

import pytest

from config_decorator import section
from config_decorator.config_decorator import ConfigDecorator


def generate_config_root():

    @section(None)
    class RootSection(object):
        def inner_function(self):
            return 'foo'

    # ***

    @RootSection.section(None)
    class RootSectionOverlay(object):
        def __init__(self):
            pass

        # ***

        @property
        @RootSection.setting(
            "Hidden test.",
            hidden=True,
        )
        def inner_function(self):
            return RootSection._innerobj.inner_function()

        # ***

        @property
        @RootSection.setting(
            "Hidden test, too.",
            hidden=lambda x: True,
        )
        def callable_hidden_test(self):
            return ''

        # ***

        @property
        @RootSection.setting(
            "Choices test.",
            choices=['', 'one', 'two', 'three'],
        )
        def choices_test(self):
            return ''

        # ***

        @property
        @RootSection.setting(
            "Different Name test.",
            name='real-option-name',
        )
        def real_option_name(self):
            return ''

        # ***

        def some_value_conversation(value):
            if isinstance(value, int):
                return value
            return int(value) + 100

        @property
        @RootSection.setting(
            "Value Type test.",
            conform=some_value_conversation,
        )
        def conform_test(self):
            return '1'

        # ***

        @property
        @RootSection.setting(
            "Allow None test.",
            value_type=bool,
            allow_none=True,
        )
        def allow_none_test(self):
            return None

        # ***

        @property
        @RootSection.setting(
            "Default value None test.",
        )
        def default_value_none_test(self):
            return None

        # ***

        @property
        @RootSection.setting(
            "Default value list test, implicit.",
        )
        def default_value_list_test_implicit(self):
            return [1, 'foo']

        # ***

        @property
        @RootSection.setting(
            "Ephemeral test.",
            ephemeral=True,
        )
        def ephemeral_test(self):
            return 'This will not be saved!'

        # ***

        @property
        @RootSection.setting(
            "Callable Ephemeral test.",
            ephemeral=lambda x: True,
        )
        def callable_ephemeral_test(self):
            return 'Neither will this be saved.'

        # ***

        def must_validate_foo(some_value):
            return some_value

        @property
        @RootSection.setting(
            "Validate pass test.",
            validate=must_validate_foo,
        )
        def pass_validate_test(self):
            return 'This will be validated!'

        # ***

        def validate_true(some_value):
            return True

        @property
        @RootSection.setting(
            "Validate okay test.",
            validate=validate_true,
        )
        def validate_okay_test(self):
            return None

        # ***

        @property
        @RootSection.setting(
            "Validate bool string test, false.",
            value_type=bool,
        )
        def validate_bool_string_false_test(self):
            return 'False'

        @property
        @RootSection.setting(
            "Validate bool string test, true.",
            value_type=bool,
        )
        def validate_bool_string_true_test(self):
            return 'True'

    # ***

    @RootSection.section('level1')
    class RootSectionLevel1(object):
        def __init__(self):
            pass

        @property
        @RootSection.setting(
            "Test sub config setting, level1.foo",
        )
        def foo(self):
            return 'baz'

        @property
        @RootSection.setting(
            "Test same-named settings in separate sections",
        )
        def conflict(self):
            return 'level1'

    # ***

    @RootSectionLevel1.section('level2')
    class RootSectionLevel2(object):
        def __init__(self):
            pass

        @property
        @RootSectionLevel1.setting(
            "Test sub sub config setting, level1.level2.bar",
        )
        def baz(self):
            return 'bat'

        @property
        @RootSectionLevel1.setting(
            "Test same-named settings in separate sections",
        )
        def conflict(self):
            return 'level2'

    # ***

    @RootSection.section('level1.2')
    class RootSectionLevel1dot2TestsDownloadToDictDelConfigSection(object):
        def __init__(self):
            pass

    # ***

    return RootSection


# ***

class TestConfigDecoratorAsDict:
    def test_something(self):
        rootcfg = generate_config_root()
        assert isinstance(rootcfg, ConfigDecorator)
        assert isinstance(rootcfg._innerobj, object)
        _settings = rootcfg.as_dict()  # noqa: F841: var never used


# ***

class TestConfigDecoratorSetDefault:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.setdefault('totally-unknown-key', 123)
        rootcfg.setdefault('totally-unknown-key.subsection.too', False)
        rootcfg.setdefault('level1.foo', 'exercise different branch on known sub key')
        with pytest.raises(TypeError):
            rootcfg.setdefault('missing.value')


# ***

class TestConfigDecoratorKeysValuesItems:
    def test_config_decorator_keys(self):
        rootcfg = generate_config_root()
        _keys = rootcfg.keys()  # noqa: F841: var never used
        # sorted(list(keys)) is the names of the settings tests above, e.g.,
        #   ['allow_none_test', 'choices_test', 'ephemeral_test', etc.]

    def test_config_decorator_values(self):
        rootcfg = generate_config_root()
        _values = rootcfg.values()  # noqa: F841: var never used
        # values is the default values of the settings tests above, e.g.,
        #   ['foo', '', '', 101, None, 'This will not be saved!', etc.]

    def test_config_decorator_items(self):
        rootcfg = generate_config_root()
        _items = rootcfg.items()  # noqa: F841: var never used


# ***

class TestConfigDecoratorAttributeMagic:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.level1.level2.baz.value == 'bat'


class TestConfigDecoratorSubscriptability:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg['level1']['level2']['baz'] == 'bat'


# ***

class TestConfigDecoratorFindAllManyParts:
    def test_something(self):
        rootcfg = generate_config_root()
        settings = rootcfg.find_all(['level1', 'level2', 'baz'])
        assert settings[0].value == 'bat'


class TestConfigDecoratorFindAllNoPartsSelf:
    def test_something(self):
        rootcfg = generate_config_root()
        settings = rootcfg.find_all(parts=[])
        assert settings == [rootcfg]


class TestConfigDecoratorFindSection:
    def test_something(self):
        rootcfg = generate_config_root()
        settings = rootcfg.find_all(parts=['level1', 'level2'])
        assert len(settings) == 1
        assert settings[0] is rootcfg['level1']['level2']


# ***

class TestConfigDecoratorFindRoot:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg['level1'].find_root() is rootcfg
        rootcfg = generate_config_root()
        assert rootcfg['level1'].asobj.foo.find_root() is rootcfg


# ***

class TestConfigDecoratorSectionPath:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.level1.level2._.section_path() == 'level1.level2'
        assert rootcfg.asobj.level1.level2._.section_path('_') == 'level1_level2'


# ***

class TestConfigDecoratorForgetfulWalk:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.forget_config_values()


# ***

class TestConfigDecoratorSetAttributeValueBool:
    def test_one_way(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.validate_bool_string_false_test.value = True

    def test_or_the_other(self):
        rootcfg = generate_config_root()
        rootcfg['validate_bool_string_false_test'] = False


# ***

class TestConfigDecoratorSetAttributeValueString:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg['level1.foo'] = 'zab'


# ***

class TestConfigDecoratorSetAttributeValueList:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg['default_value_list_test_implicit'] = 123
        assert rootcfg['default_value_list_test_implicit'] == [123, ]


# ***

class TestConfigDecoratorSetSubscriptableVague:
    def test_something(self):
        rootcfg = generate_config_root()
        # KeyError: 'More than one config object named: “conflict”'
        with pytest.raises(KeyError):
            rootcfg['conflict'] = 'zab'


# ***

class TestConfigDecoratorGetAttributeError:
    def test_something(self):
        rootcfg = generate_config_root()
        with pytest.raises(AttributeError):
            # AttributeError: 'More than one config object named: “conflict”'
            rootcfg.conflict
        # However, setting an unknown key works just fine.
        rootcfg.conflict = 'zab'
        # FIXME/2019-12-23: (lb): Remove attribute magic, or maybe gait
        # through an intermediate attribute, e.g.,, rootcfg.settings.conflict.


# ***

class TestConfigDecoratorDownloadToDict:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_config = (
            'test: return ckv.value_from_config'
        )
        cfgdict = {}
        rootcfg.apply_items(cfgdict)
        assert cfgdict == rootcfg.as_dict(unmutated=True)


# ***

class TestConfigDecoratorUpdateKnown:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_config = (
            'test: return ckv.value_from_config'
        )
        cfgdict = {
            'level1': {
                'level2': {
                    'baz': 'zab'
                },
                'unknown': 'unconsumed',
            }
        }
        _unconsumed, _errs = rootcfg.update_known(cfgdict)  # noqa: F841: var never used


# ***

class TestConfigDecoratorUpdateGross:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_config = (
            'test: return ckv.value_from_config'
        )
        cfgdict = {
            'level1.level2.baz': 'zab',
            'level1.unknown': 'unconsumed',
        }
        # Alternatively, we can ignore unknown keys.
        rootcfg.update(cfgdict)


# ***

class TestConfigDecoratorFindSettingOkay:
    def test_something(self):
        rootcfg = generate_config_root()
        setting = rootcfg.find_setting(['level1', 'level2', 'baz'])
        assert setting.value == 'bat'


class TestConfigDecoratorFindSettingFailOnePart:
    def test_something(self):
        rootcfg = generate_config_root()
        with pytest.raises(KeyError):
            rootcfg.find_setting(['unknown setting'])


class TestConfigDecoratorFindSettingFailManyParts:
    def test_something(self):
        rootcfg = generate_config_root()
        with pytest.raises(KeyError):
            rootcfg.find_setting(['unknown setting', 'foo'])


class TestConfigDecoratorFindSettingOnePart:
    def test_something(self):
        rootcfg = generate_config_root()
        setting = rootcfg.find_setting(['conflict'])
        assert setting.value == 'level1'


# ***

class TestConfigDecoratorAsobjOkay:
    def test_something(self):
        rootcfg = generate_config_root()
        assert(
            "Test sub sub config setting, level1.level2.bar"
            == rootcfg.asobj.level1.level2.baz.doc
        )


# ***

class TestConfigDecoratorSettingWalk:
    def test_something(self):
        def visitor(section, setting):
            assert section is rootcfg.asobj.level1.level2._
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.walk(visitor)


# ***

class TestConfigDecoratorSettingSetForced:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_forced = 123


# ***

class TestConfigDecoratorSettingSetCliarg:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_cliarg = 123


# ***

class TestSectionSettingValidationOkay:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.validate_okay_test.value = 123


# ***

class TestSectionSettingChoicesOkay:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.choices_test.value = 'one'


class TestSectionSettingChoicesFail:
    def test_something(self):
        rootcfg = generate_config_root()
        with pytest.raises(ValueError):
            rootcfg.asobj.choices_test.value = 'foo'


# ***

class TestSectionSettingFromEnvvar:
    def test_something(self):
        rootcfg = generate_config_root()
        from config_decorator.key_chained_val import KeyChainedValue
        KeyChainedValue._envvar_prefix = 'TEST_'
        environame = 'TEST_LEVEL1_FOO'
        import os
        os.environ[environame] = 'zab'
        assert rootcfg.asobj.level1.foo.value == 'zab'
        del os.environ[environame]


# ***

class TestSectionSettingPrecedence:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.level1.foo.value == 'baz'
        # Note that setting value assumes from config.
        rootcfg.asobj.level1.foo.value = 'bat'
        assert rootcfg.asobj.level1.foo.value_from_config == 'bat'
        assert rootcfg.asobj.level1.foo.value == 'bat'
        #
        from config_decorator.key_chained_val import KeyChainedValue
        KeyChainedValue._envvar_prefix = 'TEST_'
        environame = 'TEST_LEVEL1_FOO'
        import os
        os.environ[environame] = 'zab'
        assert rootcfg.asobj.level1.foo.value == 'zab'
        # Note that int will be converted to setting type, which is string.
        rootcfg.asobj.level1.foo.value_from_cliarg = 123
        assert rootcfg.asobj.level1.foo.value == '123'
        #
        rootcfg.asobj.level1.foo.value_from_forced = 'perfect!'
        assert rootcfg.asobj.level1.foo.value == 'perfect!'

