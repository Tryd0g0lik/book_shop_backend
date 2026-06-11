#
# def pytest_generate_tests(metafunc):
#     generate_regisration(metafunc)
#
# def generate_regisration(metafunc):
#     if "user_registrate_playwright" in metafunc.fixturenames:
from project.settings_conf.settings_env import APP_MINIMUM_PASSWORD_LENGTH

TEST_FORM_DATA = [
    # ========== HAPPY PATH TESTS ==========
    {

        "name": "valid_admin_user",
        "data": {
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
        "expected": {
            "valid": True,
            "error_field": None,
        }
    },
    {

        "name": "valid_client_user",
        "data": {
            "username": "client_john",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        },
        "expected": {
            "valid": True,
            "error_field": None,
        }
    },
    {

        "name": "valid_moderator_user",
        "data": {
            "username": "moderator_anna",
            "first_name": "Anna",
            "last_name": "Smith",
            "email": "anna.smith@example.com",
            "is_staff": False,
            "category": "MODERATOR",
            "check_user": "on",
            "password1": "ModPass456!",
            "password2": "ModPass456!",
        },
        "expected": {
            "valid": True,
            "error_field": None,
        }
    },

    # ========== USERNAME VALIDATION TESTS ==========
    {

        "name": "username_too_short",
        "data": {
            "username": "ab",  # Less than minimum length
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": True,
            "error_field": "username",
        }
    },{

        "name": "username_too_short",
        "data": {
            "username": "ab@+-_00",  # Available symbols
            "first_name": "Test",
            "last_name": "User",
            "email": "test7@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": True,
            "error_field": "username",
        }
    },
    {

        "name": "username_too_long",
        "data": {
            "username": "a" * 50,  # It accessible max length
            "first_name": "Test",
            "last_name": "User",
            "email": "test1@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": True,
            "error_field": None,
        }
    },
{

        "name": "username_duplicate",
        "data": {
            "username": "admin_super",  # Already exists. It is a doublicate email
            "first_name": "Duplicate",
            "last_name": "User",
            "email": "test2@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "email",
            "error_message": "Username already exists"
        }
    },
    # ========== USERNAME INVALID TESTS ==========
    {

        "name": "username_too_long",
        "data": {
            "username": "a" * 51,  # Exceeds max length
            "first_name": "Test",
            "last_name": "User",
            "email": "test3@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": None,
        }
    },
{

        "name": "username_too_short",
        "data": {
            "username": "ab$",  # In symbol $
            "first_name": "Test",
            "last_name": "User",
            "email": "test4@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "username",
        }
    },
    {

        "name": "username_too_short",
        "data": {
            "username": "ab@+- _00",  # Invalid symbol  " "
            "first_name": "Test",
            "last_name": "User",
            "email": "test5@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "username",
        }
    },
    {

        "name": "username_too_short",
        "data": {
            "username": "ab@+-%_00",  # Invalid symbol %
            "first_name": "Test",
            "last_name": "User",
            "email": "test6@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "username",
        }
    },
    {

        "name": "username_with_special_chars",
        "data": {
            "username": "user@#$%^&*()",
            "first_name": "Test",
            "last_name": "User",
            "email": "test8@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "username",
        }
    },

    {

        "name": "username_missing_required",
        "data": {
            "username": "",
            "first_name": "Test",
            "last_name": "User",
            "email": "test9@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "username",
        }
    },

    # ========== EMAIL VALIDATION TESTS ==========
    {

        "name": "invalid_email_format",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "invalid-email",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "email",
            "error_message": "Enter a valid email address"
        }
    },
    {

        "name": "email_too_long",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": f"{'a' * 51}@example.com",  # Exceeds 320 chars
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "email",
            "error_message": "Email cannot exceed 320 characters"
        }
    },
    {

        "name": "email_duplicate",
        "data": {
            "username": "different_user",
            "first_name": "Different",
            "last_name": "User",
            "email": f"{"a" * 50}@example.com",  # Already exists
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "email",
            "error_message": "Email already registered"
        }
    },
{

        "name": "email_duplicate",
        "data": {
            "username": "different_user",
            "first_name": "Different",
            "last_name": "User",
            "email": f"{"a" * 50}@example.com",  # Already exists
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "email",
            "error_message": "Email already registered"
        }
    },
    {

        "name": "email_missing",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "email",
            "error_message": "Email is required"
        }
    },
{
        "id": "12A",
        "name": "email_missing",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "email",
            "error_message": "Email is required"
        }
    },

    # ========== PASSWORD VALIDATION TESTS ==========
    {
        "id": "13",
        "name": "password_too_short",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test10@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "12",  # Less than minimum length
            "password2": "12",
        },
        "expected": {
            "valid": False,
            "error_field": "password1",
            "error_message": "Password must be at least 3 characters"
        }
    },{
        "id": "13A",
        "name": "password_too_short",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test11@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": f"{"a" * 255}",  # Less than max length
            "password2": f"{"a" * 255}",
        },
        "expected": {
            "valid": False,
            "error_field": "password1",
            "error_message": "Password must be at least 3 characters"
        }
    },{
        "id": "13B",
        "name": "password_too_short",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test12@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": f"{"a" * APP_MINIMUM_PASSWORD_LENGTH}"[:-1],  # Less than minimum length invalid
            "password2": f"{"a" * APP_MINIMUM_PASSWORD_LENGTH}"[:-1],
        },
        "expected": {
            "valid": True,
            "error_field": "password1",
            "error_message": "Password must be at least 3 characters"
        }
    },{
        "id": "13C",
        "name": "password_too_short",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test13@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": f"{"a" * 256}",  # Less than max length invalid
            "password2": f"{"a" * 256}",
        },
        "expected": {
            "valid": False,
            "error_field": "password1",
            "error_message": "Password must be at least 3 characters"
        }
    },
    {
        "id": "14",
        "name": "passwords_do_not_match",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test14@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "Password123!",
            "password2": "DifferentPassword456!",
        },
        "expected": {
            "valid": False,
            "error_field": "password2",
            "error_message": "Passwords do not match"
        }
    },
    {
        "id": "14A",
        "name": "password_missing",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test15@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "",
            "password2": "",
        },
        "expected": {
            "valid": False,
            "error_field": "password1",
            "error_message": "Password is required"
        }
    },
    {
        "id": "16",
        "name": "password_too_weak_common",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test16@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "password123",
            "password2": "password123",
        },
        "expected": {
            "valid": False,
            "error_field": "password1",
            "error_message": "Password is too common"
        }
    },

    # ========== CATEGORY AND PERMISSIONS TESTS ==========
    {
        "id": "17",
        "name": "invalid_category",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test17@example.com",
            "is_staff": False,
            "category": "INVALID_CATEGORY",
            "check_user": "on", # Is valid
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": True,
            "error_field": None,
            "error_message": "Select a valid choice"
        }
    },
    {
        "id": "18",
        "name": "staff_without_admin_category",
        "data": {
            "username": "staff_user",
            "first_name": "Staff",
            "last_name": "User",
            "email": "staff@example.com",
            "is_staff": True,
            "category": "CLIENT",
            "check_user": "", # Checkbox not checked / Is invalid
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "check_user",
            "error_message": "Staff status requires ADMIN category"
        }
    },
    {
        "id": "19",
        "name": "admin_without_check_user",
        "data": {
            "username": "admin_no_check",
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin2@example.com",
            "is_staff": True,
            "category": "ADMIN",
            "check_user": "off",  # Checkbox not checked / Is invalid
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "check_user",
            "error_message": "You must confirm user verification"
        }
    },


    # ========== SPECIAL CHARACTER AND UNICODE TESTS ==========
    {
        "id": "23",
        "name": "unicode_characters_in_names",
        "data": {
            "username": "ユーザー名",
            "first_name": "José",
            "last_name": "García",
            "email": "unicode@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": True,
            "supports_unicode": True
        }
    },
    {
        "id": "24",
        "name": "email_with_plus_sign",
        "data": {
            "username": "email_plus",
            "first_name": "Test",
            "last_name": "User",
            "email": "test+alias@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "email"
        }
    },

    # ========== SECURITY TESTS ==========

    {
        "id": "26",
        "name": "xss_attempt",
        "data": {
            "username": "<script>alert('XSS')</script>",
            "first_name": "<img src=x onerror=alert('XSS')>",
            "last_name": "User",
            "email": "test18@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "username"
        }
    },
]
        # metafunc.parametrize(
        #     "user_registrate_playwright",
        #     TEST_FORM_DATA,
        #     ids=[s['id'] for s in TEST_FORM_DATA]
        # )
