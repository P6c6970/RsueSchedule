class Command:
    def __init__(self, text, fun, description=None, is_visible=True):
        self.text = text
        self.fun = fun
        self.description = description
        self.is_visible = is_visible