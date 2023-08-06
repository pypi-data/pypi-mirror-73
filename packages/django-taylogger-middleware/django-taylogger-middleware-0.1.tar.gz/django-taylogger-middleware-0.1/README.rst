============================
Taylogger Django Middleware
============================

Taylogger Django Middleware is a middleware that helps
catch Django exceptions and send them to Taylogger to save the
log message of the exception.
Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'taylogger',
    ]

2. Add "polls" to your MIDDLEWARES setting like this::

    MIDDLEWARES = [
        ...
        'taylogger.middleware.ErrorLoggerMiddleware',
    ]


3. Then set the following variables in the settings.py

```python
EXCEPTION_GROUP_ID = "YOUR_EXCEPTION_GROUP_ID"
TAYLOGGER_API_KEY = "YOUR_TAYLOGGER_API_KEY"
```


4. You can now use your app and Taylogger Middleware will catch 
your exceptions and send to Taylogger app
