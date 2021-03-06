import collections
import json
import os


class Navigation(object):
    """ Repository of the navigation of the coop functions

    The items are stored in a json file so that there can be an unlimited number of branches, where a branch is the
    child selections of an item.
    """
    def __init__(self, tree=None):
        """ Load the navigation from the json file & pick the first branch
        """

        if tree is None:
            self._load_navigation()
        else:
            self._tree = tree

        # Keep up with the indexes that were selected
        self._bread_crumb = None

        self.reset()

    def _load_navigation(self, navigation=None):
        """ Load the menu selection from json file
        """
        if navigation is None:
            navigation = os.path.dirname(__file__) + '/navigation.json'

        self._tree = json.load(open(navigation), object_pairs_hook=collections.OrderedDict)

    def _load_selected_branch(self):
        """ Make the list of the items in the current branch

        Walk down the bread crumbs to get to the items in the navigation that belong to the previous selection
        """
        # Set the menu to the full tree to start walking down it
        self._branch = self._tree

        # Loop through the menu _bread_crumbs backwards getting each of the values that were selected
        for selected in self._bread_crumb[:0:-1]:
            self._branch = self._branch.values()[selected]

        # Maybe at the end of the line, so there will ont be any children
        try:
            # Get the keys for the level that we ended at
            self._branch = self._branch.keys()
        # Was not, so back up one
        except AttributeError:
            self.move_left()

    def at_bottom_of_branch(self):
        """ Check to see if ar the bottom of the items in the branch

        :return:
            bool: True if at the bottom, otherwise False
        """
        if len(self._branch) - 1 == self.current_item_index():
            return True

        return False

    def at_level(self):
        """ Get the level in the navigation that we are on.

        :return:
            int: Level (This is NOT zero based, so 1 is the first level.)
        """
        return len(self._bread_crumb)

    def at_top_of_branch(self):
        """ Check to see if ar the top of the items in the branch

        :return:
            bool: True if at the top, otherwise False
        """
        if 0 == self.current_item_index():
            return True

        return False

    def current_branch(self):
        """ Getter for the list of the current items

        :return:
            list: Items in the selected branch
        """
        return self._branch

    def current_item(self):
        """ Getter for the current items

        :return:
            string: Current item from the branch
        """
        try:
            return self._branch[self.current_item_index()]
        except IndexError:
            return ""

    def current_item_index(self):
        """ The first item in the bread crumb

        :return:
            int: The index of the current item (This IS zero based)
        """
        return self._bread_crumb[0]

    def move_down(self):
        """ Move down in the items in the current branch.

        Update the pointer to the next item down in the branch or if already at the bottom, then back up to the top.
        """
        if not self.at_bottom_of_branch():
            self._bread_crumb[0] += 1
        else:
            self._bread_crumb[0] = 0

    def move_left(self):
        """ Move back up the navigation to the item that lead into the branch that we are on.
        """
        if 1 < len(self._bread_crumb):
            self._bread_crumb.pop(0)
            self._load_selected_branch()

    def move_right(self):
        """ Dive into the branch for the current item"""
        self._bread_crumb.insert(0, 0)
        self._load_selected_branch()

    def move_up(self):
        """ Move up in the items in the current branch.

        Update the pointer to the previous item up in the branch or if already at the top, then back up to the bottom.
        """
        if not self.at_top_of_branch():
            self._bread_crumb[0] -= 1
        else:
            self._bread_crumb[0] = len(self._branch) - 1

    def reset(self):
        """ Reset the location in the navigation to the first item
        """
        self._bread_crumb = [0]

        self._load_selected_branch()
