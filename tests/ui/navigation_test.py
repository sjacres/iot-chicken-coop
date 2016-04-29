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


def test_it_can_be_constructed(navigation):
    assert isinstance(navigation, Navigation)


def test_knows_top_from_bottom(navigation):
    assert navigation.at_top_of_branch()
    assert not navigation.at_bottom_of_branch()

    navigation.move_down()

    assert not navigation.at_top_of_branch()
    assert navigation.at_bottom_of_branch()


def test_top_is_bottom_for_single_node():
    navigation = Navigation({'Single': 'node'})

    assert navigation.at_top_of_branch()
    assert navigation.at_bottom_of_branch()


def test_level_starts_at_1(navigation):
    assert navigation.at_level(1)

    navigation.move_right()

    assert navigation.at_level(2)


def test_moving_up_or_down_does_not_change_level(navigation):
    assert navigation.at_level(1)

    navigation.move_down()

    assert navigation.at_level(1)

    navigation.move_up()

    assert navigation.at_level(1)


def test_level_is_constrained_by_depth_of_nodes(navigation):
    assert navigation.at_level(1)

    navigation.move_left()
    assert navigation.at_level(1)

    navigation.move_right()
    assert navigation.at_level(2)

    navigation.move_right()

    assert navigation.at_level(2)

    navigation.move_left()
    navigation.move_down()
    navigation.move_right()

    assert navigation.at_level(1)


def test_moving_in_a_circle_for_top_or_bottom_node(navigation):
    assert navigation.at_top_of_branch()
    assert not navigation.at_bottom_of_branch()

    navigation.move_down()

    assert not navigation.at_top_of_branch()
    assert navigation.at_bottom_of_branch()

    navigation.move_down()

    assert navigation.at_top_of_branch()
    assert not navigation.at_bottom_of_branch()

    navigation.move_up()

    assert not navigation.at_top_of_branch()
    assert navigation.at_bottom_of_branch()


def test_rest_restarts_the_navigation_at_the_top(navigation):
    navigation.move_right()
    navigation.move_down()

    assert 1 == navigation.current_item_index()
    assert navigation.at_level(2)

    navigation.reset()

    assert 0 == navigation.current_item_index()
    assert navigation.at_level(1)


def test_that_the_expected_item_is_returned(navigation):
    assert "First" == navigation.current_item()

    navigation.move_right()
    navigation.move_down()

    assert "Sub Second" == navigation.current_item()


def test_all_the_items_in_the_branch_can_be_returned_as_a_list_in_expected_order(navigation):
    assert ['First', 'Second'] == navigation.menu()

    navigation.move_right()

    assert ['Sub First', 'Sub Second', 'Sub Third'] == navigation.menu()


def test_it_returns_empty_string_when_no_navigation_items():
    navigation = Navigation({})

    assert "" == navigation.current_item()


def test_expected_default_title():
    navigation = Navigation()

    assert "IOT Chicken Coop\nRight to start->" == navigation.current_item()


def test_that_the_expected_function_is_returned_for_current_item(navigation):
    assert navigation.current_item_function() is None

    navigation.move_right()

    current_function = navigation.current_item_function()

    assert 'some.namespace' == current_function['namespace']
    assert 'Class' == current_function['class']
    assert 'function_to_run' == current_function['function']

    navigation.reset()
    navigation.move_down()

    current_function = navigation.current_item_function()

    assert 'some.namespace' == current_function['namespace']
    assert 'Class' == current_function['class']
    assert 'function_to_run' == current_function['function']
