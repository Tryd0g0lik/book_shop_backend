# ELSE
def pytest_generate_tests_regisration(metafunc):
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
                "category": "STAFF",
                "check_user": "on",
                "password1": "pbkdf2_sha256$hash_staff_2",
                "password2": "pbkdf2_sha256$hash_staff_2",
            },
        ]
        metafunc.parametrize(
            "new_users_registration",
            users,
            ids=[s['email'] for s in users]
        )
