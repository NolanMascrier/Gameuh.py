"""A tabs is a widget that creates an array of button that
will change a state."""

from data.image.button import Button
from data.constants import SYSTEM

def set_var(variable, state):
    """Sets the variable to the state."""
    SYSTEM[variable] = state

class Tabs:
    """Define a tab.
    
    Args:
        x (int): x position of the first element of the tab.
        y (int): y position of the first element of the tab.
        values (list[str]): list of name for the buttons.
        states (list[str]): list of states value.
        variable (str): which variable will be changed.
        image (Image, optional): Image for the buttons.
        held (Image, optional): Image for the held buttons.
        is_action (bool, False): Whether or not a click should
        call an action rather than merely changing a state. Defaults\
        to `False`.
        actions (list, optional): List of function calls to use with\
        the previous option. Defaults to None. 
    """
    def __init__(self, x, y, values, states, variable,\
        image = None, held = None, is_action = False, actions = None):
        self._x = x
        self._y = y
        if values is None:
            values = []
        self._values = values
        if states is None:
            states = []
        self._states = states
        self._variable = variable
        if image is None:
            image = SYSTEM["images"]["btn_tab"]
        if held is None:
            held = SYSTEM["images"]["btn_tab_pressed"]
        self._buttons = []
        self._fake_buttons = []
        for i, v in enumerate(values):
            self._buttons.append(Button(image, image,\
                lambda i=i: set_var(self._variable, self._states[i])\
                if not is_action else actions[i](),\
                v))
            self._fake_buttons.append(Button(held, held, None, v))

    def tick(self):
        """Ticks down the buttons"""
        i = 0
        for b in self._buttons:
            if SYSTEM[self._variable] == self._states[i]:
                self._fake_buttons[i].set(self._x + i * b.image.width, self._y)\
                    .tick().draw(SYSTEM["windows"])
            else:
                b.set(self._x + i * b.image.width, self._y).tick().draw(SYSTEM["windows"])
            i += 1
