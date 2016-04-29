import collections
from coop.ui.navigation import Navigation
import pytest


@pytest.fixture()
def navigation(request):
    tree = collections.OrderedDict()
    node1 = collections.OrderedDict()
    function = collections.OrderedDict()

    function['namespace'] = 'some.namespace'
    function['class'] = 'Class'
    function['function'] = 'function_to_run'

    node1['Sub First'] = function
    node1['Sub Second'] = function
    node1['Sub Third'] = function

    tree['First'] = node1
    tree['Second'] = function

    return Navigation(tree)


def test_knows_top_from_bottom(navigation):
    assert True == navigation.at_top_of_branch()
    assert False == navigation.at_bottom_of_branch()

    navigation.move_down()

    assert False == navigation.at_top_of_branch()
    assert True == navigation.at_bottom_of_branch()


def test_top_is_bottom_for_single_node():
    navigation = Navigation({'Single': 'node'})

    assert True == navigation.at_top_of_branch()
    assert True == navigation.at_bottom_of_branch()


def test_level_starts_at_1(navigation):
    assert 1 == navigation.at_level()

    navigation.move_right()

    assert 2 == navigation.at_level()


def test_moving_up_or_down_does_not_change_level(navigation):
    assert 1 == navigation.at_level()

    navigation.move_down()

    assert 1 == navigation.at_level()

    navigation.move_up()

    assert 1 == navigation.at_level()


def test_level_is_constrained_by_depth_of_nodes(navigation):
    assert 1 == navigation.at_level()

    navigation.move_left()
    assert 1 == navigation.at_level()

    navigation.move_right()
    assert 2 == navigation.at_level()

    navigation.move_right()

    assert 2 == navigation.at_level()

    navigation.move_left()
    navigation.move_down()
    navigation.move_right()

    assert 1 == navigation.at_level()


def test_moving_in_a_circle_for_top_or_bottom_node(navigation):
    assert True == navigation.at_top_of_branch()
    assert False == navigation.at_bottom_of_branch()

    navigation.move_down()

    assert False == navigation.at_top_of_branch()
    assert True == navigation.at_bottom_of_branch()

    navigation.move_down()

    assert True == navigation.at_top_of_branch()
    assert False == navigation.at_bottom_of_branch()

    navigation.move_up()

    assert False == navigation.at_top_of_branch()
    assert True == navigation.at_bottom_of_branch()


def test_rest_restarts_the_navigation_at_the_top(navigation):
    navigation.move_right()
    navigation.move_down()

    assert 1 == navigation.current_item_index()
    assert 2 == navigation.at_level()

    navigation.reset()

    assert 0 == navigation.current_item_index()
    assert 1 == navigation.at_level()


def test_that_the_expected_item_is_returned(navigation):
    assert "First" == navigation.current_item()

    navigation.move_right()
    navigation.move_down()

    assert "Sub Second" == navigation.current_item()


def test_all_the_items_in_the_branch_can_be_returned_as_a_list_in_expected_order(navigation):
    assert ['First', 'Second'] == navigation.current_branch()

    navigation.move_right()

    assert ['Sub First', 'Sub Second', 'Sub Third'] == navigation.current_branch()


def test_it_returns_empty_string_when_no_navigation_items():
    navigation = Navigation({})

    assert "" == navigation.current_item()


def test_expected_default_title():
    navigation = Navigation()

    assert "IOT Chicken Coop\nRight to start->" == navigation.current_item()

# def test_that_the_expected_function_is_returned(navigation):
#     navigation.move_right()
#
#     assert {'child.class': 'func_a'} == navigation.current_function()
