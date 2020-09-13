from django.core.management.base import BaseCommand
from covidUsers.models import ROLE_CHOICES, Role,CustomUser


class Command(BaseCommand):
    help = """ By default creates 20 users with 15 patients and 5 doctors
                you can provide no. of patients and doctors 
                as string argument separated by space
            """
    

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            help='''takes no arguement creates 20 users 10 doctors and 10 patients
                    '''
        )

    def create_users(self):
        role_p = Role.objects.all().filter(role=ROLE_CHOICES[2][0]).first()
        rd = Role.objects.all().filter(role=ROLE_CHOICES[0][0]).first()
        cp1 = CustomUser(user_role=role_p,phone='9876543210',email="dummy1@dummy.com",username="dummy_patient_1",password='dummy123')
        cp1.save()
        cp2 = CustomUser(user_role=role_p,phone='9876543211',email="dummy2@dummy.com",username="dummy_patient_2",password='dummy123')
        cp2.save()
        cp3 = CustomUser(user_role=role_p,phone='9876543212',email="dummy3@dummy.com",username="dummy_patient_3",password='dummy123')
        cp3.save()
        cp4 = CustomUser(user_role=role_p,phone='9876543213',email="dummy4@dummy.com",username="dummy_patient_4",password='dummy123')
        cp4.save()
        cp5 = CustomUser(user_role=role_p,phone='9876543214',email="dummy5@dummy.com",username="dummy_patient_5",password='dummy123')
        cp5.save()
        cp6 = CustomUser(user_role=role_p,phone='9876543215',email="dummy6@dummy.com",username="dummy_patient_6",password='dummy123')
        cp6.save()
        cp7 = CustomUser(user_role=role_p,phone='9876543216',email="dummy7@dummy.com",username="dummy_patient_7",password='dummy123')
        cp7.save()
        cp8 = CustomUser(user_role=role_p,phone='9876543217',email="dummy8@dummy.com",username="dummy_patient_8",password='dummy123')
        cp8.save()
        cp9 = CustomUser(user_role=role_p,phone='9876543218',email="dummy9@dummy.com",username="dummy_patient_9",password='dummy123')
        cp9.save()
        cp10 = CustomUser(user_role=role_p,phone='9876543219',email="dummy10@dummy.com",username="dummy_patient_10",password='dummy123')
        cp10.save()
        
        cd1 = CustomUser(user_role=rd,phone='9876543210',email="dummy11@dummy.com",username="dummy_doc_1",password='dummy123')
        cd1.save()
        cd2 = CustomUser(user_role=rd,phone='9876543220',email="dummy12@dummy.com",username="dummy_doc_2",password='dummy123')
        cd2.save()
        cd3 = CustomUser(user_role=rd,phone='9876543230',email="dummy13@dummy.com",username="dummy_doc_3",password='dummy123')
        cd3.save()
        cd4 = CustomUser(user_role=rd,phone='9876543240',email="dummy14@dummy.com",username="dummy_doc_4",password='dummy123')
        cd4.save()
        cd5 = CustomUser(user_role=rd,phone='9876543250',email="dummy15@dummy.com",username="dummy_doc_5",password='dummy123')
        cd5.save()
        cd6 = CustomUser(user_role=rd,phone='9876543260',email="dummy16@dummy.com",username="dummy_doc_6",password='dummy123')
        cd6.save()
        cd7 = CustomUser(user_role=rd,phone='9876543270',email="dummy17@dummy.com",username="dummy_doc_7",password='dummy123')
        cd7.save()
        cd8 = CustomUser(user_role=rd,phone='9876543280',email="dummy18@dummy.com",username="dummy_doc_8",password='dummy123')
        cd8.save()
        cd9 = CustomUser(user_role=rd,phone='9876543290',email="dummy19@dummy.com",username="dummy_doc_9",password='dummy123')
        cd9.save()
        cd10 = CustomUser(user_role=rd,phone='9876543200',email="dummy20@dummy.com",username="dummy_doc_10",password='dummy123')
        cd10.save()
    def handle(self, *args, **kwargs):
        self.create_users()
