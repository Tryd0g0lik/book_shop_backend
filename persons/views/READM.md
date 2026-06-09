
## Регистрация
- '`project/celery.py`'.

### The form of registration

This form contains 6 fields and one checkbox.
- '`email`' - This is unique field. User can't change after registration. Min. 5 characters, max 50 characters.
    It is required to fill in.
- '`username`'- This is not unique & not required field. This field will be used only '`A-Za-z_0-9`' characters.
- '`first_name`'- This is field almost repeat a '`username`'. The difference between them is that - he does not must contain the characters '`0-9`'. 
- '`password1`', '`password2`' - These are required fields to be filled. Min 8 chars.
- '`catergory`" For everyone, this field has a default value (at the beginning) it is "`BASE`". Then we look - "From where user comes here." and change it a status. Of course if he - has passed authentication.
- '`checbox`' - This is required field. Here, user is sending us that he - consent to data processing.

### First letter
After pressing button `Register`, data of form passes through all checks on validation checks and then send to the server. The task under name "`task_set_cache`" makes this the first cache.
Everything is stored in the relational database and part of the cache server under key "`user:pending:%s`". \
Example. If user has email username25@mail.ru, so this would be the key "`user:pending:username25mailru`". \
This key saves data for a first letter "`persons/templates/account/email/email_confirmation_subject.txt`"

