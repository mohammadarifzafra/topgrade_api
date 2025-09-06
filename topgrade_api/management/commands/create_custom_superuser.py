from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import getpass
import re

User = get_user_model()

class Command(BaseCommand):
    help = "Create a superuser with email or phone number"

    def add_arguments(self, parser):
        parser.add_argument('--email_or_phone', type=str, help='Email or phone number of the superuser')
        parser.add_argument('--noinput', action='store_true', help='Do not prompt for any input')

    def handle(self, *args, **options):
        email_or_phone = options.get('email_or_phone')

        if not email_or_phone and not options.get('noinput'):
            email_or_phone = input('Email or phone number: ')

        if not email_or_phone:
            raise CommandError('Email or phone number is required')

        # Validate input
        if not self.is_valid_email_or_phone(email_or_phone):
            raise CommandError('Please enter a valid email or phone number')

        # Check if user already exists
        if self.user_exists(email_or_phone):
            raise CommandError('User with this email or phone number already exists')

        if not options['noinput']:
            password = getpass.getpass('Password: ')
            password_confirm = getpass.getpass('Password (again): ')

            if password != password_confirm:
                raise CommandError('Passwords do not match')
        else:
            password = None

        try:
            user = User.objects.create_user_with_email_or_phone(
                email_or_phone=email_or_phone,
                password=password,
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser created successfully with {"email" if "@" in email_or_phone else "phone"}: {email_or_phone}')
            )
        except Exception as e:
            raise CommandError(f'Error creating superuser: {str(e)}')

    def is_valid_email_or_phone(self, value):
        try:
            validate_email(value)
            return True
        except ValidationError:
            pass

        # Check if it's a valid phone number
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        cleaned_phone = value.replace(" ", "").replace("-", "")
        return bool(phone_pattern.match(cleaned_phone))
        
    def user_exists(self, email_or_phone):
        if '@' in email_or_phone:
            return User.objects.filter(email=email_or_phone).exists()
        else:
            return User.objects.filter(phone_number=email_or_phone).exists()



          
          
            
            
        