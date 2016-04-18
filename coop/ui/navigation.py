import collections
import json


class Navigation(object):
    _bread_crumb = [0]

    def __init__(self):
        self._loadNavigation()

        self._loadSelectedBranch()

    def _loadNavigation(self):
        # Load the menu selection from json file
        self._tree = json.load(open('ui/navigation.json'), object_pairs_hook=collections.OrderedDict)

    def _loadSelectedBranch(self):
        # Set the menu to the full tree to start walking down it
        self._branch = self._tree

        # Loop through the menu _bread_crumbs backwards getting each of the values that were selected
        for selected in self._bread_crumb[:0:-1]:
            self._branch = self._branch.values()[selected]

        try:
            # Get the keys for the level that we ended at
            self._branch = self._branch.keys()
        except AttributeError:
            self.moveLeft()

    def atBottomOfBranch(self):
        if len(self._branch) - 1 == self.currentItemIndex():
            return True

        return False

    def atLevel(self):
        return len(self._bread_crumb)

    def atTopOfBranch(self):
        if 0 == self.currentItemIndex():
            return True

        return False

    def currentBranch(self):
        return self._branch

    def currentItem(self):
        return self._branch[self.currentItemIndex()]

    def currentItemIndex(self):
        return self._bread_crumb[0]

    def items(self):
        return self._branch

    def moveDown(self):
        # Any menu _branch above?
        if not self.atBottomOfBranch():
            self._bread_crumb[0] += 1
        # Wrap to the top if on the bottom
        else:
            self._bread_crumb[0] = 0

    def moveLeft(self):
        if 1 < len(self._bread_crumb):
            self._bread_crumb.pop(0)
            self._loadSelectedBranch()

    def moveRight(self):
        self._bread_crumb.insert(0, 0)
        self._loadSelectedBranch()

    def moveUp(self):
        # Any menu _branch below?
        if not self.atTopOfBranch():
            self._bread_crumb[0] -= 1
        # Wrap around to the bottom if on the top
        else:
            self._bread_crumb[0] = len(self._branch) - 1

    def reset(self):
        self._bread_crumb = [0]

        self._loadSelectedBranch()

