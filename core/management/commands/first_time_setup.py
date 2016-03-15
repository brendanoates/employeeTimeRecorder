from datetime import datetime

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from claims.models import Claim
from claims.models import ClaimType
from core.management.commands import PASSWORD
from profiles.models import EmployeeTimeRecorderUser


class Command(BaseCommand):
    help = 'Sets up a number of objects required by the application for a new installation of the application'

    def add_arguments(self, parser):
        # Positional arguments

        # Named (optional) arguments
        parser.add_argument('--create_claim',
                            action='store_true',
                            dest='create_claim',
                            default=False,
                            help='Create claim objects')

    def handle(self, *args, **options):
        """
        Populate the test database with the test data
        """
        content_type = ContentType.objects.get_for_model(Claim)
        try:
            auth_claim = Permission.objects.create(codename='authorise_claim',
                                      name='Can authorise claim',
                                      content_type=content_type)
        except IntegrityError:
            pass  # already added
        try:
            senior_auth_claim = Permission.objects.create(codename='senior_authorise_claim',
                                      name='Can senior authorise claim',
                                      content_type=content_type)
        except IntegrityError:
            pass  # already added

        """
        Create known about claim types
        """
        claims = {'Part Time Overtime': False, 'Weekday Overtime': False, 'Sunday Bank Holiday Overtime': False,
                  'Bank Holiday Hours': False, 'Weekday On Call': False, 'On Call Weekend': False, 'On Call Bank'
                                                                                                   'Holiday': False,
                  'Shift A': True, 'Shift B': True, 'Shift C': True, 'Shift D': True, 'Shift E': True,
                  'Shift F': True}
        for key in claims.keys():
            c = ClaimType.objects.create_claim_type(name=key, count=claims.get(key))
            c.save()

        """
        Create Groups
        """
        perm = Permission.objects.get(name='Can change claim type')
        hr_group = Group.objects.create(name='Human Resources')
        hr_group.permissions.add(perm)
        hr_group.save()

        manager_group = Group.objects.create(name='Managers')
        manager_group.permissions.add(auth_claim)
        manager_group.save()

        senior_manager_group = Group.objects.create(name='Senior Managers')
        senior_manager_group.permissions.add(senior_auth_claim)
        senior_manager_group.permissions.add(auth_claim)
        senior_manager_group.save()

        """
        Create Test Users
        """

        user = EmployeeTimeRecorderUser.objects.create_superuser(username='Super.user', email='test@email.com',
                                                                 password=PASSWORD)
        user.set_password(PASSWORD)
        user.save()

        user = EmployeeTimeRecorderUser.objects.create(username='HR', email='test@email.com')
        user.groups.add(hr_group)
        user.is_staff = True
        user.set_password(PASSWORD)
        user.save()

        manager1 = EmployeeTimeRecorderUser.objects.create(username='Manager1', email='test@email.com')
        manager1.set_password(PASSWORD)
        manager1.groups.add(manager_group)
        manager1.save()

        user = EmployeeTimeRecorderUser.objects.create(username='Manager2', email='test@email.com')
        user.set_password(PASSWORD)
        user.groups.add(manager_group)
        user.save()

        user = EmployeeTimeRecorderUser.objects.create(username='Manager3', email='test@email.com')
        user.set_password(PASSWORD)
        user.groups.add(manager_group)
        user.save()


        user = EmployeeTimeRecorderUser.objects.create(username='Senior.manager1', email='test@email.com')
        user.set_password(PASSWORD)
        user.groups.add(senior_manager_group)
        user.save()

        user = EmployeeTimeRecorderUser.objects.create(username='Senior.manager2', email='test@email.com')
        user.set_password(PASSWORD)
        user.groups.add(senior_manager_group)
        user.save()

        user = EmployeeTimeRecorderUser.objects.create(username='Senior.manager3', email='test@email.com')
        user.set_password(PASSWORD)
        user.groups.add(senior_manager_group)
        user.save()

        normal_user1 = EmployeeTimeRecorderUser.objects.create(username='Normal.user1', email='test@email.com')
        normal_user1.set_password(PASSWORD)
        normal_user1.manager_email = manager1.username
        normal_user1.save()

        user = EmployeeTimeRecorderUser.objects.create(username='Normal.user2', email='test@email.com')
        user.set_password(PASSWORD)
        user.save()

        user = EmployeeTimeRecorderUser.objects.create(username='Normal.user3', email='test@email.com')
        user.set_password(PASSWORD)
        user.save()

        for x in range(1,21):
            claim = Claim(type= ClaimType.objects.all()[0], owner= normal_user1, authorising_manager=manager1,
                          date= datetime(2016,1,x), value=1)
            claim.save()

