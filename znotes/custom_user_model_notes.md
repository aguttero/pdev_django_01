# Custom user model explanation
## part 1 - coding parts
In Django, a custom user model allows you to replace the default username-based authentication with a custom identifier (like an email address) and add custom fields directly to the user record.
Here is exactly how your provided code works and interacts with Django's core authentication system.

1. The Custom User Model (User)

Your User class defines how user data is stored in the database.
• AbstractBaseUser: This provides the core implementation for a user model, including hashed passwords, tokenized resets, and last login tracking. It does not include fields like username, first_name, or last_name, giving you a clean slate.
• PermissionsMixin: This adds the fields and methods necessary to support Django’s built-in permission and group frameworks (is_superuser, groups, user_permissions).
• USERNAME_FIELD = "email": This is the most crucial line. It tells Django to look at the email field instead of a username field when a user attempts to log in. The field used here must have unique=True set.

2. The Model Manager (UserManager)

Django models use a "Manager" class to handle table-level queries (like User.objects.all()). For a custom user model, you must customize the manager to handle user creation properly.
• BaseUserManager: Your class inherits from this to gain access to helper methods like normalize_email (which lowercases the domain part of the email address).
• create_user(): This handles regular user registration. It sanitizes the email, encrypts the password using user.set_password(password), and saves the instance to the database.
• create_superuser(): This wraps around create_user but explicitly flags is_staff=True (allowing Django admin panel login) and is_superuser=True (granting all permissions).

Missing Configuration: Hooking it Together

To make your code functional, Django needs to know that this manager belongs to this model, and your settings need to point to it.

Step 1: Link the Manager to the Model

Inside your User model, you need to explicitly assign your custom manager to the objects attribute:
```python
class User(AbstractBaseUser, PermissionsMixin):
    # ... your fields ...
    
    # Link the custom manager
    objects = UserManager() 
    
    USERNAME_FIELD = "email"
```
Step 2: Update settings.py

Django needs to be told to stop using its default auth model and use yours instead. Add this line to your project's settings file:
```python
# Format: 'app_label.ModelName'
AUTH_USER_MODEL = 'your_app_name.User'
```

Critical Gotcha
If you are implementing this in an existing project where migrations have already been run, switching the AUTH_USER_MODEL can cause database conflicts. It is heavily recommended to set up a custom user model at the very beginning of a Django project.
If you are ready to set this up, let me know:
• Have you already run initial migrations on this project?
• Do you need help writing the Django admin registration code so this model shows up in the admin panel?

## override explanation

Yes, create_user is an override, but with an important distinction: you are overriding a method from BaseUserManager, not the user model itself.
Here is exactly how it fits together:

1. What you are overriding

By default, Django's standard UserManager (the one used for the default username model) inherits from BaseUserManager.
• BaseUserManager provides a skeleton structure, but its native create_user method expects a username field.
• Because you changed USERNAME_FIELD to "email", Django's default user-creation logic would break.
• By writing def create_user(self, email, password=None, **extra_fields):, you are redefining (overriding) the signature and logic to explicitly require an email instead of a username.

2. How Django uses this override

Whenever Django or a third-party package tries to create a user under the hood, it calls User.objects.create_user(...).
Because you hook objects = UserManager() into your model, Django points directly to your overridden method:

When code calls...	It triggers your custom manager logic:
User.objects.create_user()	Validates the email, normalizes it, hashes the password, and saves.
python manage.py createsuperuser	Prompts for email/password, then routes into your overridden create_superuser().


Summary

Your code tells Django: "Forget how you usually create users with a username. From now on, when create_user is called, use this email-first logic instead."
Would you like to see how to write a unit test to verify that your overridden create_user method correctly handles password hashing and email normalization?
