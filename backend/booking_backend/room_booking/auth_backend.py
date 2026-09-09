"""Authentication design notes.

This module is intentionally not a custom Django authentication backend.
The app uses Django's built-in ModelBackend for username/password login and
Django REST Framework TokenAuthentication for API requests.
"""
