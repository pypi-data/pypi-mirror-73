===========
Mercury SDK
===========

Mercury SDK can be used in projects that interface with the mercury service
that provides common internal functionality.

Initializing the client
-------------------------------
>>> from mercuryclient import MercuryApi
#Setup connection parameters
>>> conn_params = {'username': 'mercury_username', 'password':'password', 'url':'https://mercury-url.com'}
>>> m = MercuryApi(conn_params)
>>>m.send_mail(['recipent@email.com'],'Test mail', 'Mail body','ses','ses_profile')

Available APIs:
----------------------
- send_mail
