.. _usage:

Usage
=====

Quickstart
----------

.. note::
    Using strict=True need only for marshmallow < 3.0.0

.. code-block:: python

    from aiohttp_apispec import (docs,
                                 request_schema,
                                 response_schema,
                                 setup_aiohttp_apispec)
    from aiohttp import web
    from marshmallow import Schema, fields


    class RequestSchema(Schema):
        id = fields.Int()
        name = fields.Str(description='name')
        bool_field = fields.Bool()


    class ResponseSchema(Schema):
        msg = fields.Str()
        data = fields.Dict()


    @docs(tags=['mytag'],
          summary='Test method summary',
          description='Test method description')
    @request_schema(RequestSchema(strict=True))
    @response_schema(ResponseSchema(), 200)
    async def index(request):
        return web.json_response({'msg': 'done',
                                  'data': {}})

    # Class based views are also supported:
    class TheView(web.View):
        @docs(
            tags=['mytag'],
            summary='View method summary',
            description='View method description',
        )
        @request_schema(RequestSchema(strict=True))
        def delete(self):
            return web.json_response({
                'msg': 'done',
                'data': {'name': self.request['data']['name']},
            })


    app = web.Application()
    app.router.add_post('/v1/test', index)
    app.router.add_view('/v1/view', TheView)

    # init docs with all parameters, usual for ApiSpec
    setup_aiohttp_apispec(app=app, title="My Documentation", version="v1")


    # find it on 'http://localhost:8080/api/docs/api-docs'
    web.run_app(app)

Adding validation middleware
----------------------------

.. code-block:: python

    from aiohttp_apispec import validation_middleware

    ...

    app.middlewares.append(validation_middleware)

Now you can access all validated data in route from ``request['data']`` like so:

.. code-block:: python

    @docs(tags=['mytag'],
          summary='Test method summary',
          description='Test method description')
    @request_schema(RequestSchema(strict=True))
    @response_schema(ResponseSchema(), 200)
    async def index(request):
        uid = request['data']['id']
        name = request['data']['name']
        return web.json_response(
            {'msg': 'done',
             'data': {'info': f'name - {name}, id - {uid}'}}
         )

You can change ``Request``'s ``'data'`` param to another
with ``request_data_name`` argument of ``setup_aiohttp_apispec`` function:

.. code-block:: python

    setup_aiohttp_apispec(app=app,
                          request_data_name='validated_data',
                          title='My Documentation',
                          version='v1',
                          url='/api/docs/api-docs')

    ...

    @request_schema(RequestSchema(strict=True))
    async def index(request):
        uid = request['validated_data']['id']
        ...

More decorators
---------------

Starting from version 2.0 you can use shortenings for documenting and validating
specific request parts like cookies, headers etc using those decorators:

================== =======================
  Decorator name    Default put_into param
================== =======================
match_info_schema  match_info
querystring_schema querystring
form_schema        form
json_schema        json
headers_schema     headers
cookies_schema     cookies
================== =======================

And example:

.. code-block:: python

    @docs(
        tags=["users"],
        summary="Create new user",
        description="Add new user to our toy database",
        responses={
            200: {"description": "Ok. User created", "schema": OkResponse},
            401: {"description": "Unauthorized"},
            422: {"description": "Validation error"},
            500: {"description": "Server error"},
        },
    )
    @headers_schema(AuthHeaders)
    @json_schema(UserMeta)
    @querystring_schema(UserParams)
    async def create_user(request: web.Request):
        headers = request["headers"]  # <- validated headers!
        json_data = request["json"]  # <- validated json!
        query_params = request["querystring"]  # <- validated querystring!
        ...


Custom error handling
---------------------

If you want to catch validation errors by yourself you
could use ``error_callback`` parameter and create your custom error handler. Note that
it can be one of coroutine or callable and it should
have interface exactly like in examples below:

.. code-block:: python

    from marshmallow import ValidationError, Schema
    from aiohttp import web
    from typing import Optional, Mapping, NoReturn


    def my_error_handler(
        error: ValidationError,
        req: web.Request,
        schema: Schema,
        error_status_code: Optional[int] = None,
        error_headers: Optional[Mapping[str, str]] = None,
    ) -> NoReturn:
        raise web.HTTPBadRequest(
                body=json.dumps(error.messages),
                headers=error_headers,
                content_type="application/json",
            )

    setup_aiohttp_apispec(app, error_callback=my_error_handler)

Also you can create your own exceptions and create
regular Request in middleware like so:

.. code-block:: python

    class MyException(Exception):
        def __init__(self, message):
            self.message = message

    # It can be coroutine as well:
    async def my_error_handler(
        error: ValidationError,
        req: web.Request,
        schema: Schema,
        error_status_code: Optional[int] = None,
        error_headers: Optional[Mapping[str, str]] = None,
    ) -> NoReturn:
        await req.app["db"].do_smth()  # So you can use some async stuff
        raise MyException({"errors": error.messages, "text": "Oops"})

    # This middleware will handle your own exceptions:
    @web.middleware
    async def intercept_error(request, handler):
        try:
            return await handler(request)
        except MyException as e:
            return web.json_response(e.message, status=400)


    setup_aiohttp_apispec(app, error_callback=my_error_handler)

    # Do not forget to add your own middleware before validation_middleware
    app.middlewares.extend([intercept_error, validation_middleware])

Named routes
------------

Routes for the Swagger UI and to the swagger specification file `swagger.json`
are registered as `named resources <https://docs.aiohttp.org/en/stable/web_quickstart.html#reverse-url-constructing-using-named-resources`_
with the `swagger.docs` and `swagger.spec` names respectively. The
corresponding routes are therefore avaialble un the value returned by the
application's router `named_resources()` call.


Build swagger web client
------------------------

3.X SwaggerUI version
*********************


Just add ``swagger_path`` parameter to ``setup_aiohttp_apispec`` function.

For example:

.. code-block:: python
    setup_aiohttp_apispec(app, swagger_path="/docs")

Then go to ``/docs`` and see awesome SwaggerUI

2.X SwaggerUI version
*********************

``aiohttp-apispec`` adds ``swagger_dict`` parameter to aiohttp
web application after initialization (with ``setup_aiohttp_apispec`` function).
So you can use it easily with ``aiohttp_swagger`` library:

.. code-block:: python

    from aiohttp_apispec import setup_aiohttp_apispec
    from aiohttp_swagger import setup_swagger


    def create_app(app):
        setup_aiohttp_apispec(app)

        async def swagger(app):
            setup_swagger(
                app=app, swagger_url='/api/doc', swagger_info=app['swagger_dict']
            )
        app.on_startup.append(swagger)
        # now we can access swagger client on '/api/doc' url
        ...
        return app

Now we can access swagger client on ``/api/doc`` url
