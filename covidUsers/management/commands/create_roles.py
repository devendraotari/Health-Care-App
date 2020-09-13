from django.core.management.base import BaseCommand
from covidUsers.models import ROLE_CHOICES,Role

class Command(BaseCommand):
    help = '''Creates Four roles Doctor, Patient, Counsellor and Other 
            these roles will be used while creating CustomUsers'''
    
    def add_arguments(self, parser):
        parser.add_argument('--all',
            help='Takes no argument creates all roles by default')
        
    def handle(self,*args, **kwargs):
        if Role.objects.all():
            self.stdout.write(self.style.SUCCESS('Roles were already present'))
        else:        
            for role in ROLE_CHOICES:
                roleObj = Role(role=role[0])
                roleObj.save()
            self.stdout.write(self.style.SUCCESS('All roles are created and saved successfully.'))