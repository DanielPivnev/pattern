from page_contr_path import page


def application(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    """
    if environ['PATH_INFO'].lower() == '/' + page['path'] \
            or environ['PATH_INFO'].lower() + '/' == '/' + page['path']:
        # сначала в функцию start_response передаем код ответа и заголовки
        start_response('200 OK', [('Content-Type', 'text/html')])

        # возвращаем тело ответа в виде списка из byte
        page_content = page['view']()
        page_content = page_content.encode()

        return [page_content]
    else:
        # сначала в функцию start_response передаем код ответа и заголовки
        start_response('404 Page Not Found', [('Content-Type', 'text/html')])

        # возвращаем тело ответа в виде списка из byte
        return [b'<h1>Page Not Found. Error 404</h1>']
