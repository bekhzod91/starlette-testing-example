import databases

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

database = databases.Database("postgresql://postgres:postgres@localhost/test", force_rollback=True)

async def root(request):
    data = await database.execute("select 'Hello World!'")
    return PlainTextResponse(data)

def user_me(request):
    username = "John Doe"
    return PlainTextResponse('Hello, %s!' % username)


routes = [
    Route('/', root),
    Route('/user/me', user_me),
]

app = Starlette(
    debug=True,
    routes=routes,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect]
)

