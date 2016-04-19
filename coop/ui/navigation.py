import collections
import json


class Navigation(object):
    """ Repository of the navigation of the coop functions

    The items are stored in a json file so that there can be an unlimited number of branches, where a branch is the
    child selections of an item.
    """

    # Record indices of the items selected in the navigation with newest on the left & oldest on the right
    _bread_crumb = [0]

    def __init__(self):
        """ Load the navigation from the json file & pick the first branch
        """
        self._loadNavigation()

        self._loadSelectedBranch()

    def _loadNavigation(self):
        """ Load the menu selection from json file
        """
        self._tree = json.load(open('ui/navigation.json'), object_pairs_hook=collections.OrderedDict)

    def _loadSelectedBranch(self):
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
            self.moveLeft()

    def atBottomOfBranch(self):
        """ Check to see if ar the bottom of the items in the branch

        :return:
            bool: True if at the bottom, otherwise False
        """
        if len(self._branch) - 1 == self.currentItemIndex():
            return True

        return False

    def atLevel(self):
        """ Get the level in the navigation that we are on.

        :return:
            int: Level (This is NOT zero based, so 1 is the first level.)
        """
        return len(self._bread_crumb)

    def atTopOfBranch(self):
        """ Check to see if ar the top of the items in the branch

        :return:
            bool: True if at the top, otherwise False
        """
        if 0 == self.currentItemIndex():
            return True

        return False

    def currentBranch(self):
        """ Getter for the list of the current items

        :return:
            list: Items in the selected branch
        """
        return self._branch

    def currentItem(self):
        """ Getter for the current items

        :return:
            string: Current item from the branch
        """
        return self._branch[self.currentItemIndex()]

    def currentItemIndex(self):
        """ The first item in the bread crumb

        :return:
            int: The index of the current item (This IS zero based)
        """
        return self._bread_crumb[0]

    def moveDown(self):
        """ Move down in the items in the current branch.

        Update the pointer to the next item down in the branch or if already at the bottom, then back up to the top.
        """
        if not self.atBottomOfBranch():
            self._bread_crumb[0] += 1
        else:
            self._bread_crumb[0] = 0

    def moveLeft(self):
        """ Move back up the navigation to the item that lead into the branch that we are on.
        """
        if 1 < len(self._bread_crumb):
            self._bread_crumb.pop(0)
            self._loadSelectedBranch()

    def moveRight(self):
        """ Dive into the branch for the current item"""
        self._bread_crumb.insert(0, 0)
        self._loadSelectedBranch()

    def moveUp(self):
        """ Move up in the items in the current branch.

        Update the pointer to the previous item up in the branch or if already at the top, then back up to the bottom.
        """
        if not self.atTopOfBranch():
            self._bread_crumb[0] -= 1
        else:
            self._bread_crumb[0] = len(self._branch) - 1

    def reset(self):
        """ Reset the location in the navigation to the first item
        """
        self._bread_crumb = [0]

        self._loadSelectedBranch()
