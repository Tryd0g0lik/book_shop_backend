# ELSE
def pytest_generate_tests(metafunc):
    if "new_users_registration" in metafunc.fixturenames:
        generate_regisration(metafunc)


def generate_regisration(metafunc):
    if "new_users_registration" in metafunc.fixturenames:

        users = [
            {
                "is_superuser": True,
                "username": "admin_super",
                "first_name": "Admin",
                "last_name": "Supervisor",
                "email": "admin@example.com",
                "is_staff": True,
                "category": "ADMIN",
                "check_user": "on",
                "password1": "pbkdf2_sha256$hash_admin_1",
                "password2": "pbkdf2_sha256$hash_admin_1",
            },
            {
                "is_superuser": False,
                "username": "staff_moderator",
                "first_name": "Moderator",
                "last_name": "Staff",
                "email": "moderator@example.com",
                "is_staff": True,
                "category": "MODERATORS",
                "check_user": "on",
                "password1": "pbkdf2_sha256$hash_staff_2",
                "password2": "pbkdf2_sha256$hash_staff_2",
            },
            {
                "is_superuser": False,
                "username": "Client_name",
                "first_name": "Client",
                "last_name": "Client",
                "email": "client@example.com",
                "is_staff": False,
                "category": "CLIENT",
                "check_user": "on",
                "password1": "pbkdf2_sha256$hash_staff_2",
                "password2": "pbkdf2_sha256$hash_staff_2",
            },
            {
                "is_superuser": False,
                "username": "Editor_name",
                "first_name": "Editor",
                "last_name": "Editor",
                "email": "editor@example.com",
                "is_staff": True,
                "category": "EDITORS",
                "check_user": "on",
                "password1": "pbkdf2_sha256$hash_staff_2",
                "password2": "pbkdf2_sha256$hash_staff_2",
            },
            {
                "is_superuser": False,
                "username": "Manager_name",
                "first_name": "Manager",
                "last_name": "Manager",
                "email": "manager@example.com",
                "is_staff": True,
                "category": "MANAGER",
                "check_user": "on",
                "password1": "pbkdf2_sha256$hash_staff_2",
                "password2": "pbkdf2_sha256$hash_staff_2",
            },
        ]
        metafunc.parametrize(
            "new_users_registration", users, ids=[s["email"] for s in users]
        )
