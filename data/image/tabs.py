"""A tabs is a widget that creates an array of button that
will change a state."""

from data.api.widget import Widget

from data.image.button import Button
from data.constants import SYSTEM

def set_var(variable, state, act = None):
    """Sets the variable to the state."""
    SYSTEM[variable] = state
    if act is not None:
        act()

class Tabs(Widget):
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
        addition_action (function, optional): Function to call when \
        clicking a button. Defauts to None.
        rows (int, optional): Numbers of formated rows. Defaults to 1.
    """
    def __init__(self, x, y, values, states, variable,\
        image = None, held = None, is_action = False, actions = None,\
        additional_action = None, rows = 1):
        super().__init__(x, y, 0, 0)
        if values is None:
            values = []
        self._values = values
        if states is None:
            states = []
        self._states = states
        self._variable = variable
        self._other_action = additional_action
        self._rows = rows
        if image is None:
            image = SYSTEM["images"]["btn_tab"]
        if held is None:
            held = SYSTEM["images"]["btn_tab_pressed"]
        self._buttons = []
        self._fake_buttons = []
        for i, v in enumerate(values):
            self._buttons.append(Button(image, image,\
                lambda i=i: set_var(self._variable, self._states[i], additional_action)\
                if not is_action else actions[i](),\
                v))
            self._fake_buttons.append(Button(held, held, None, v))
        self.width = sum(b.width for b in self._buttons)
        self.height = max(b.height for b in self._buttons)

    def tick(self):
        """Ticks down the buttons"""
        i = j = dy = dx = ddx = 0
        per_row = len(self._buttons) // self._rows + 1
        for b in self._buttons:
            if i > per_row and i + per_row <= len(self._buttons) and ddx == 0:
                ddx = b.image.width // 2
            dx = j * b.image.width + ddx
            if SYSTEM[self._variable] == self._states[i]:
                self._fake_buttons[i].set(self.x + dx, self.y + dy)\
                    .tick().draw()
            else:
                b.set(self.x + dx, self.y + dy).tick().draw()
            i += 1
            j += 1
            if j >= per_row:
                dy += self._height
                dx = 0
                j = 0

    def set(self, x, y):
        """Sets the tab at the x;y position."""
        super().set(x, y)
        return self
