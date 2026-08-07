# Profile manager
All roles of app we have by a path "`utilities/__init__.py::CATEGORY_STATUS`" 

Every role (exclude the "`BASE`" role):
- have analogous of a name profile by path "`profiles/models/*`".
- managed through the "`UserProfileManagerModel`" from path "`profiles/models/model_user_profile.py::UserProfileManagerModel`"

All works pass through the "`UserProfileManagerModel`". The path to the user pass from the\
  "`UserProfileModel  => profiles.models.model_<client | admin | editor | manager | moderator > => wagtail.users.models.UserProfile => 'persons.models.Users'`"  

## Permissions
The right of managed profile we case by path "`profiles/permissions`"
Note: Every app of this project has it's own permissions. When user pass to the one or other app, he gets under check permissions.

## Tasks 
This task "`profiles/tasks/task_signals`" is working by signal and starting from the tasks list "`persons/views/views_login.py::UserLoginView.run_tasks`"\
Then user do a login event.
