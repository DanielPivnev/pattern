from jinja2 import Template


def render(template_name, content):
    """
    :param template_name: имя шаблона
    :param content: параметр для передачи в шаблон
    :return:
    """
    with open(template_name, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**content)


def check_view(view, path):
    if path.lower() == '/' + view.path or path.lower() + '/' == '/' + view.path:
        return True
    else:
        return False
