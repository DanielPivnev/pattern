from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, content, folder='templates'):
    """
    :param folder:
    :param template_name: имя шаблона
    :param content: параметр для передачи в шаблон
    :return:
    """
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)

    return template.render(**content)


def check_view(page, path):
    if path.lower() == '/' + page.path or path.lower() + '/' == '/' + page.path:
        return True
    else:
        return False
