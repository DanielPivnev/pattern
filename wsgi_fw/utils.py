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


def check_view(page, path):
    if path.lower() == '/' + page.path or path.lower() + '/' == '/' + page.path:
        return True
    else:
        return False
