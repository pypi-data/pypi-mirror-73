from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        cls_user = get_user_model()
        with open('users.csv', 'w') as csv:
            csv.write('Username, Last Name, First Name, Email\n')
            for user in cls_user.objects.all():
                d = '%s, %s, %s, %s\n' % (user.username, user.last_name, user.first_name, user.email)
                csv.write(d)
