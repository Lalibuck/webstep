def wsgi_app(env, start_response):
    status = '200 OK'
    headers = [('MIME-type', 'text/plain')]
    start_response(status, headers)
    return '\n'.join(env.get('QUERY-STRING').split('&'))

