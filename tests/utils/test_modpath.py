from inet.utils.modpath import ModulePath


def test_attribute_access():
    package = ModulePath.get_module('package')
    package.module
    package.module.function
    package.module.xclass


def test_generated_path():
    package = ModulePath.get_module('package')
    assert package.module.path == 'package.module'
    assert package.module.function.path == 'package.module.function'
    assert package.module.xclass.path == 'package.module.xclass'
