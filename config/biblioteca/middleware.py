from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware simples:
    - Permite acesso apenas ao login, registro e APIs
      quando o usuário NÃO está autenticado.
    """

    PUBLIC_PATHS = [
        "/",            # login
        "/registro/",   # registro
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        # APIs são liberadas
        if path.startswith("/api/") or path.startswith("/dados-livro/"):
            return self.get_response(request)

        # Se rota pública, libera
        if path in self.PUBLIC_PATHS:
            return self.get_response(request)

        # Se usuário não estiver logado, redireciona para login
        if not request.user.is_authenticated:
            return redirect("/")

        # Caso contrário, acesso permitido
        return self.get_response(request)
