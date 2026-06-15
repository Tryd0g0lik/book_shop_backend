[Note: Below ](persons/views/views_register.py:263) is the line that defines which is used to define what's in front of you. In this case, it refers back to `role` and so on for all other lines where there are references like "person.role" or something similar.the 'category' we will be caching.\
User will get own role/category when pass a verification.

[We can have a (count)](persons/views/views_register.py:270):
- Superadmin before 1;
- Admin ... 1;
- Manager ... 0-3;
- Client more.

## Celery + Redis
- [Beginning to caching](persons/views/views_register.py:305) First task for a cache.\
There we only send data in the cache.
- [Second the celery task](persons/views/views_register.py:311) Here we start mailing.


## **....**


### Login
- [Logic for verification](persons/views/views_register.py:316). HEre is we receiving our token via user's email.\
If user passed verification hi get redirect to login page (app hase two login page. One for [admins to the](project/urls.py:57) "`/admin/login/`" and [next to the](persons/urls.py:25) "`/person/login/`" ).

