import collections
from coop.ui.navigation import Navigation
import pytest

@pytest.fixture()
def navigation(request):
    tree = collections.OrderedDict()
    node1 = collections.OrderedDict()

    node1['Sub First'] = 'child a'
    node1['Sub Second'] = 'child b'
    node1['Sub Third'] = 'child c'

    tree['First'] = node1
    tree['Second'] = 'node 2'

    return Navigation(tree)

def test_knows_top_from_bottom(navigation):
    assert True == navigation.atTopOfBranch()
    assert False == navigation.atBottomOfBranch()

    navigation.moveDown()

    assert False == navigation.atTopOfBranch()
    assert True == navigation.atBottomOfBranch()

def test_top_is_bottom_for_single_node():
    navigation = Navigation({'Single': 'node'})

    assert True == navigation.atTopOfBranch()
    assert True == navigation.atBottomOfBranch()

def test_level_starts_at_1(navigation):
    assert 1 == navigation.atLevel()

    navigation.moveRight()

    assert 2 == navigation.atLevel()

def test_moving_up_or_down_does_not_change_level(navigation):
    assert 1 == navigation.atLevel()

    navigation.moveDown()

    assert 1 == navigation.atLevel()

    navigation.moveUp()

    assert 1 == navigation.atLevel()

def test_level_is_constrained_by_depth_of_nodes(navigation):
    assert 1 == navigation.atLevel()

    navigation.moveLeft()

    assert 1 == navigation.atLevel()

    navigation.moveRight()

    assert 2 == navigation.atLevel()

    navigation.moveRight()

    assert 2 == navigation.atLevel()

    navigation.moveLeft()
    navigation.moveDown()
    navigation.moveRight()

    assert 1 == navigation.atLevel()

def test_moving_in_a_circle_for_top_or_bottom_node(navigation):
    assert True == navigation.atTopOfBranch()
    assert False == navigation.atBottomOfBranch()

    navigation.moveDown()

    assert False == navigation.atTopOfBranch()
    assert True == navigation.atBottomOfBranch()

    navigation.moveDown()

    assert True == navigation.atTopOfBranch()
    assert False == navigation.atBottomOfBranch()

    navigation.moveUp()

    assert False == navigation.atTopOfBranch()
    assert True == navigation.atBottomOfBranch()

def test_rest_restarts_the_navgation_at_the_top(navigation):
    navigation.moveRight()
    navigation.moveDown()

    assert 1 == navigation.currentItemIndex()
    assert 2 == navigation.atLevel()

    navigation.reset()

    assert 0 == navigation.currentItemIndex()
    assert 1 == navigation.atLevel()

def test_that_the_expected_item_is_returned(navigation):
    assert "First" == navigation.currentItem()

    navigation.moveRight()
    navigation.moveDown()

    assert "Sub Second" == navigation.currentItem()

def test_all_the_items_in_the_branch_can_be_returned_as_a_list_in_expected_order(navigation):
    assert ['First', 'Second'] == navigation.currentBranch()

    navigation.moveRight()

    assert ['Sub First', 'Sub Second', 'Sub Third'] == navigation.currentBranch()

def test_it_returns_empty_string_when_no_navigation_items():
    navigation = Navigation({})

    assert "" == navigation.currentItem()

def test_expected_default_title():
    navigation = Navigation()

    assert "IOT Chicken Coop\nRight to start->" == navigation.currentItem()