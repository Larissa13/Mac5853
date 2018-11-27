[nltk_data] Downloading package stopwords to
[nltk_data]     /home/larissa/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
[nltk_data] Downloading package rslp to /home/larissa/nltk_data...
[nltk_data]   Package rslp is already up-to-date!
[nltk_data] Downloading package punkt to /home/larissa/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
loading w2v
finished loading
loading w2v
finished loading
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

    req (Request): a Request entry from Request database.

## get_result
```python
get_result(urls, force_calc, callback=None)
```



## update_or_create_kws
```python
update_or_create_kws(words, req, db)
```

Creates or updates the keywords in the Keyword table.

__Input:__

    - words (list): a list of strings to be inserted or modified in the Keyword table.
    - req (Request): a Request to be associated with the words.
    - db (database): The app`s database.

