class Command:
    def __init__(self, text, fun, description=None, is_visible=True):
        self.text = text
        self.fun = fun
        self.description = description
        self.is_visible = is_visible

    def __str__(self):  # command text or description if available
        if self.description:
            return self.description
        return self.text