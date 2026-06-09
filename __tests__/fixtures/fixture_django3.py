#
# def pytest_generate_tests(metafunc):
#     generate_regisration(metafunc)
#
# def generate_regisration(metafunc):
#     if "user_registrate_playwright" in metafunc.fixturenames:

TEST_FORM_DATA = [
    # ========== HAPPY PATH TESTS ==========
    {
        "id": "1",
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
        "expected": { # It and similar code below don't using.
            "valid": True,
            "category": "ADMIN",
            "is_staff": True,
            "is_verified": False,
            "is_sent": False
        }
    },
    {
        "id": "2",
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
            "category": "CLIENT",
            "is_staff": False,
            "is_verified": False,
            "is_sent": False
        }
    },
    {
        "id": "3",
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
            "category": "MODERATOR",
            "is_staff": False
        }
    },

    # ========== USERNAME VALIDATION TESTS ==========
    {
        "id": "4",
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
            "valid": False,
            "error_field": "username",
            "error_message": "Username must be at least 3 characters"
        }
    },
    {
        "id": "5",
        "name": "username_too_long",
        "data": {
            "username": "a" * 151,  # Exceeds max length
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
            "valid": False,
            "error_field": "username",
            "error_message": "Username cannot exceed 150 characters"
        }
    },
    {
        "id": "6",
        "name": "username_with_special_chars",
        "data": {
            "username": "user@#$%^&*()",
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
            "valid": False,
            "error_field": "username",
            "error_message": "Username contains invalid characters"
        }
    },
    {
        "id": "7",
        "name": "username_duplicate",
        "data": {
            "username": "admin_super",  # Already exists
            "first_name": "Duplicate",
            "last_name": "User",
            "email": "duplicate@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "username",
            "error_message": "Username already exists"
        }
    },
    {
        "id": "8",
        "name": "username_missing_required",
        "data": {
            "username": "",
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
            "valid": False,
            "error_field": "username",
            "error_message": "Username is required"
        }
    },

    # ========== EMAIL VALIDATION TESTS ==========
    {
        "id": "9",
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
        "id": "0",
        "name": "email_too_long",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": f"{'a' * 300}@example.com",  # Exceeds 320 chars
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
        "id": "11",
        "name": "email_duplicate",
        "data": {
            "username": "different_user",
            "first_name": "Different",
            "last_name": "User",
            "email": "admin@example.com",  # Already exists
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
        "id": "12",
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
            "email": "test@example.com",
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
    },
    {
        "id": "14",
        "name": "passwords_do_not_match",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
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
        "id": "15",
        "name": "password_missing",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
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
            "email": "test@example.com",
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
            "email": "test@example.com",
            "is_staff": False,
            "category": "INVALID_CATEGORY",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "category",
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
            "category": "CLIENT",  # Staff but not admin
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "is_staff",
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
            "check_user": "off",  # Checkbox not checked
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "check_user",
            "error_message": "You must confirm user verification"
        }
    },

    # ========== FIELD LENGTH BOUNDARY TESTS ==========
    {
        "id": "20",
        "name": "first_name_max_length",
        "data": {
            "username": "testuser",
            "first_name": "A" * 150,
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
            "first_name_length": 150
        }
    },
    {
        "id": "21",
        "name": "first_name_exceeds_max",
        "data": {
            "username": "testuser",
            "first_name": "A" * 151,
            "last_name": "User",
            "email": "test@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "error_field": "first_name",
            "error_message": "First name cannot exceed 150 characters"
        }
    },
    {
        "id": "22",
        "name": "last_name_max_length",
        "data": {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "B" * 150,
            "email": "test@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": True,
            "last_name_length": 150
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
            "valid": True,
            "email_format": "valid_with_plus"
        }
    },

    # ========== SECURITY TESTS ==========
    {
        "id": "25",
        "name": "sql_injection_attempt",
        "data": {
            "username": "'; DROP TABLE users; --",
            "first_name": "'; DELETE FROM auth_user; --",
            "last_name": "'; DROP TABLE; --",
            "email": "test@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "should_be_sanitized": True
        }
    },
    {
        "id": "26",
        "name": "xss_attempt",
        "data": {
            "username": "<script>alert('XSS')</script>",
            "first_name": "<img src=x onerror=alert('XSS')>",
            "last_name": "User",
            "email": "test@example.com",
            "is_staff": False,
            "category": "CLIENT",
            "check_user": "on",
            "password1": "ValidPass123!",
            "password2": "ValidPass123!",
        },
        "expected": {
            "valid": False,
            "should_escape_html": True
        }
    },
]
        # metafunc.parametrize(
        #     "user_registrate_playwright",
        #     TEST_FORM_DATA,
        #     ids=[s['id'] for s in TEST_FORM_DATA]
        # )
