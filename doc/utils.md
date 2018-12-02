# utils

## search_db
```python
search_db(url)
```

Searches the Request table for the entry that correponds to a given url and returns it.

__Input:__

    - url (str): an url string.

__Output:__

    - the Request table entry corresponding to this url.

## result_from_db
```python
result_from_db(req)
```

Returns the Keywords and the Label associated with a request if it was previously classified as Restricted.
Otherwise, returns that the request was classified as Permitted, with no Keywords and Label associated.

__Input:__

    - req (Request): a Request entry from Request database.

## get_result
```python
get_result(urls, force_calc, callback=None)
```

Returns a tuple containing the urls' labels, the keywords highly correlated to the website's content, the veredict provided by the classification, the process' status, and a boolean indicating if a socket connection should be established with the client.

__Input:__

    - urls (list): list of urls strings to classify.
    - force_calc (boolean): indicates if the veredict from a previous classification should be used (force_calc=False) or not (force_calc=True).
    - callback (str, None): a callback url.


## update_or_create_kws
```python
update_or_create_kws(words, req, db)
```

Creates or updates the keywords in the Keyword table.

__Input:__

    - words (list): a list of strings to be inserted or modified in the Keyword table.
    - req (Request): a Request to be associated with the words.
    - db (database): The app`s database.

## call_cls
```python
call_cls(urls, callback, kws, labels)
```

Provides the communication of the status and results between the classifier process, the main process and the client (when using via web interface).

__Input:__

    - urls (list): a list of urls to be classified.
    - callback(str): the callback url.
    - kws (list): list of pre-defined keywords in the database.
    - labels (list): list of pre-defined labels in the database.

