# __init__

## ConfigDev
```python
ConfigDev(self, /, *args, **kwargs)
```

Sets app's development configuration.

### SQLALCHEMY_DATABASE_URI
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
### SQLALCHEMY_TRACK_MODIFICATIONS
bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.
## create_app
```python
create_app(Config)
```

Creates the website's pages behavior and the app's database. Returns app object and database object.

### index 
``` python
index()
```

Creates and desplays the main page (index). Returns the rendered webpage.

### prepare
``` python
prepare()
```      

Creates an intermediate page that prepares the classification answer to be presented. Returns an redirection to the main page.

### send_data
``` python
send_data()
```      

Establishes a socjet connection with the server to receive status from classification and redirects to prepare page when the result is received.
