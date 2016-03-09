from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from claims.models import Claim
from claims.models import ClaimType


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
        Create custom permissions
        """
        content_type = ContentType.objects.get_for_model(Claim)
        try:
            Permission.objects.create(codename='authorise_claim',
                                      name='Can authorise claim',
                                      content_type=content_type)
            self.stdout.write(self.style.SUCCESS('Custom permission added'))
        except IntegrityError:
            pass  # already added
        try:
            Permission.objects.create(codename='senior_authorise_claim',
                                      name='Can senior authorise claim',
                                      content_type=content_type)
            self.stdout.write(self.style.SUCCESS('Custom permission added'))
        except IntegrityError:
            pass  # already added

        """
        Create known about claims
        """
        if options['create_claim']:
            claims = {'Part Time Overtime': False, 'Weekday Overtime': False, 'Sunday Bank Holiday Overtime': False,
                      'Bank Holiday Hours': False, 'Weekday On Call': False, 'On Call Weekend': False, 'On Call Bank'
                                                                                                       'Holiday': False,
                      'Shift A': True, 'Shift B': True, 'Shift C': True, 'Shift D': True, 'Shift E': True,
                      'Shift F': True}
            try:
                for key in claims.keys():
                    c = ClaimType.objects.create_claim_type(name=key, count=claims.get(key))
                    c.save()
            except Exception as e:
                self.stdout.write(self.style.SUCCESS('Opps {}'.format(e)))
            self.stdout.write(self.style.SUCCESS('Claims have been added'))
        self.stdout.write(self.style.SUCCESS('Finished ;)'))
