![pytest](https://github.com/mithem/serverly/workflows/pytest/badge.svg)

# serverly

A really simple-to-use server framework with integrated user management, built on Uvicorn & SQLAlchemy!

## Table of Contents

- [Configuration](#configuration)
- [Custom functions](#custom-dynamic-functions)
- [Methods](#methods)
- [Objects](#objects)
  - [Request](#requests)
  - [Response](#response)
  - [Request & Response](#request--response)
  - [Resource](#resource)
- [serverly.user](#serverlyuser)
- [serverly.statistics](#serverlystatistics)
- [plugins](#plugins)

## Configuration

`address = ('localhost', 8080)` The address used to register the server. Needs to be set before running start()

`name = 'serverly'` The name of the server. Used for logging purposes only.

`logger: fileloghelper.Logger = Logger()` The logger used for logging (surprise!!). See the docs of fileloghelper for reference.

## Custom (dynamic) functions

When you create custom functions you need to tell serverly by either using the `serves(method: str, path: str)` decorator or register it by calling `register_function` (see below). Your function should accept one parameter which is of type Request. You can then process it in whatever way you want.
Your function must return a Response object. See Objects for more info.

## Methods

`static_page(file_path: str, path: str)`
Register a static page where the file is located under `file_path` and will serve `path`

`register_function(method: str, path: str, function)`
Register a dynamic function that will serve `path` via `method`

`unregister(method: str, path: str)`
Unregister any page (static or dynamic). Only affect the `method`-path (GET / POST)

`start(superpath: str='/')`
Start the server after applying all relevant attributes like address. `superpath` will replace every occurence of SUPERPATH/ or /SUPERPATH/ with `superpath`. Especially useful for servers orchestrating other servers.

`register_error_response(code: int, msg_base: str, mode='enumerate')`
Register an error response template for `code` based off the message-stem `msg_base`and accepting \*args as defined by `mode`

`error_template(code: int, *args)`

**Modes:**

- enumerate: append every arg by comma and space to the base
- base: only return the base message

**Example:**

```python
register_error_response(404, 'Page not found.', 'base')
```

You can now get the 404-Response by calling `error_response(404)` -> Response(code=404, body='Page not found.')

Or in enumerate mode:

```python
register_error_response(999, 'I want to buy: ', 'enumerate')
```

`error_response(999, 'apples', 'pineapples', 'bananas')`
-> Response(code=9l9, body='I want to buy: apples, pineapples, bananas')

`error_response(code: int, *args)`
Return Response registered by register_error_response (See above)

## Objects

### Request

<!--- TODO: check if address really looks like this!-->

| Attribute                              | Description                                                                                                                                                                                                                                                 |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| method: str                            | HTTP method (GET, POST, PUT, DELETE)                                                                                                                                                                                                                        |
| path: str                              | Path the request was sent to (e.g. /projects/doorbell)                                                                                                                                                                                                      |
| address: tuple[str, int]               | Address of client as a tuple, i.e. ("localhost": 50760)                                                                                                                                                                                                     |
| authenticated: bool                    | Is user authenticated using the Authorization-Header?                                                                                                                                                                                                       |
| auth_type: str                         | Type of authorization (Authorization-Header). Currently Basic & Bearer supported.                                                                                                                                                                           |
| user_cred: Union[str, tuple[str, str]] | Credentials of the user passed in the Authorization-Header. If `auth_type` is Basic, `user_cred` is a tuple containing username & password. The password is already decrypted from base64. If `auth_type` is Bearer, `user_cred` is the bearer token (str). |

### Response

| Attribute      | Description                                                                                |
| -------------- | ------------------------------------------------------------------------------------------ |
| code: int      | Response code to send to the client                                                        |
| bandwidth: int | Maximum bandwidth used when sending to client (**bytes per sec**). None for no regulation. |

### Request & Response

| Attribute                              | Description                                                                                                                                           |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| headers: dict                          | Headers as a dict[str, Union[str, int]] recieved by the client or yet to return to it                                                                 |
| (set) body: Union[str, dict, list, fb] | set `body` to a str, dict or list. Translating it into JSON, if necessary is handled automatically. Can be set to str, dict, list or file-like object |
| (get) body: str                        | get the JSON representation of the request/response if available, otherwise just the string.                                                          |
| (get) obj: object                      | get the object representation of the request/response. If there is none (body is a non-JSON string for example) it is set to None. NOT SET-able.      |

Due to the properties above the probably best way to use requests/responses is by assigning values like dictionaries to the body attribute of responses and accessing the json of requests by using body (i.e. to store it in a database)

### StaticSite

`StaticSite(path: str, file_path: str)`
A static site using `file_path` for it's data to serve. Will be registered for `path` (if you register it), if not overriden in the process (don't _really_ have to mind). Instead registering it manually, you can call `.use()`.

### Resource

You can subclass `serverly.objects.Resource` to specify your endpoints in an more OO-way.

Example:

```python
class MyAPI(Resource):
  @staticmethod
  @basic_auth
  def info(request: Request):
    # do something and return a Response

  def __init__(self):
    self.__path__ = '/api/'
    self.__map__ = {
      '/overview/?': 'static/json/overview.json', # local filesystem
      '/info/?': self.info,
      '/products/': ProductsAPI
    }
```

where `ProductsAPI` is another Resource subclass:

```python
class ProductsAPI(Resource):
  @staticmethod
  def get_all(request: Request):
    # DB lookup and other stuff
  def __init__(self):
    self.__path__ = '/products/'
    self.__map__ = {
      '/getall': self.get_all,
      '/new': self.new # ...
    }
```

When you call `MyAPI().use()`, the following endpoints will be registered:

| path                 | function                                |
| -------------------- | --------------------------------------- |
| /api/overview/?      |  StaticSite (static/json/overview.json) |
| /info/?              | MyAPI().info                            |
| /api/products/getall | ProductsAPI().get_all                   |
| /api/products/new    | ProductsAPI().new                       |

And yes, it's recursive!!!

### StaticResource

This allows you to serve an entire folder recursively with just one call:

```python
serverly.objects.StaticResource(folder_path: str, endpoint_path: str, file_extensions=True)
```

`file_extensions` specifies whether the endpoints should be include the file_extension of the original file (ex. /folder/hello.py)

## serverly.user

This subpackage allows very easy user-management right through serverly. See [SERVERLY.USER.md](https://github.com/mithem/serverly/blob/master/SERVERLY.USER.md) for more information.

## serverly.statistics

This module is used to save statistics of the server as well as individual endpoints and print them after shutdown as well as saving them to `filename` (defaults to 'statistics.json'). It has the following attributes for holding stats:

```python
overall_performance = {
  'min': 2.7182818284,
  'max': 11.11111,
  'mean': 3.1415926535,
  'len': 42
}
endpoint_performance = {
  'my_endpoint': {
    'min': 3.292932383827,
    'max': 17.223480972,
    'mean': 6.182849,
    'len': 42
  }
}
```

Also, it has the functions `new_statistic(function: str, time: float)` and `print_stats()`, both of which you probably don't need 🧐

## plugins

serverly provides a very basic interface for plugins. The following options are available to you to subclass:

- [HeaderPlugin](#headerplugin)
- [ServerLifespanPlugin](#serverlifespanplugin)

### HeaderPlugin

The `manipulateHeaders(response: Response) -> Response` method gets called of a subclass. It's supposed to alter the headers of the Response just before getting sent to the client. The default implementation raises a NotImplemtedError. The default constructor takes an array of regex patterns, as `str`s, used as exceptions where the plugin will NOT do it's work. There are a few implementations of common `HeaderPlugin`s:

- `Content_Security_PolicyHeaderPlugin(policy: str, exceptions=[])`
- `X_Frame_OptionsHeaderPlugin(policy: str, exceptions=[])`
- `X_Content_TypeOptionsHeaderPlugin(policy: str, exceptions=[])`

### ServerLifespanPlugin

The methods of this plugin get called with the lifecycle of the (main) server. Available are:

- `onServerStart()`
- `onServerShutdown()`
