def is_active_page(func):
    def wrapper(self, *args, **kwargs):
        if getattr(self.app, "current_page", None) != self:
            return
        return func(self, *args, **kwargs)
    return wrapper
