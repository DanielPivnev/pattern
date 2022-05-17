class NoTemplate(Exception):
    def __str__(self):
        return 'A BaseView must have a template!'
