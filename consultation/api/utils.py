from rest_framework.authtoken.models import Token

from consultation.models import GeneralSymptom, SpecialityTag
from covidUsers.models import CustomUser
from consultation.models import FileLabel

def get_token_key(request):
    token_key = request.headers["Authorization"].split(" ")[1]
    return token_key


def get_request_user(request):
    print("**********************&&&&&&")
    token_key = get_token_key(request)
    if token_key:
        user = Token.objects.select_related("user").get(key=token_key).user
        return user


def create_or_update_symptoms(id=None, *args, **kwargs) -> dict:
    """
    this method is used for creating or updating a General symtopms model data
    if id is provided as an argument then update operation is done
    else create operation is done
    kwargs should be in proper formate while calling
    e.g. create_or_update_symptoms(<some_id>, user=user,request=request)
    """
    general_symptom = None
    assigned_doctor = None
    if "user" in kwargs and "request" in kwargs:
        user = kwargs.get("user", None)
        request = kwargs.get("request", None)
        
        assigned_doctor_id = request.data.get("assigned_doctor_id", None)
        if assigned_doctor_id:
            print("FETCHING DOCTOR")
            try:
                assigned_doctor = (
                    CustomUser.objects.all().filter(id=assigned_doctor_id).first()
                )
            except Exception as e:
                return {
                    "Error": str(e),
                    "msg": f"Doctor for given id {assigned_doctor_id} does not exist",
                }
        if id:
            try:
                general_symptom = GeneralSymptom.objects.all().filter(id=id).first()
                general_symptom.assigned_doctor = assigned_doctor
            except Exception as e:
                print(str(e))
                return {
                    "Error": str(e),
                    "msg": f"General Symptoms data for given id {id} does not exist",
                }
        else:
            category = SpecialityTag.objects.all().first()
            general_symptom = GeneralSymptom(
                created_by=user, assigned_doctor=assigned_doctor, category=category
            )

        print(
            f"IN UTIL METHOD {request.data.get('ecg')} type-> {type(request.data.get('ecg'))}"
        )
        general_symptom.systolic = request.data.get(
            "systolic", general_symptom.systolic
        )
        general_symptom.diatolic = request.data.get(
            "diatolic", general_symptom.diatolic
        )
        general_symptom.blood_glucose = request.data.get(
            "blood_glucose", general_symptom.blood_glucose
        )
        general_symptom.heart_rate = request.data.get(
            "heart_rate", general_symptom.heart_rate
        )
        general_symptom.ecg = request.data.get("ecg", general_symptom.ecg)
        general_symptom.temp = request.data.get("temp", general_symptom.temp)
        general_symptom.pulse = request.data.get("pulse", general_symptom.pulse)
        general_symptom.spo2 = request.data.get("spo2", general_symptom.spo2)
        general_symptom.weight = request.data.get("weight", general_symptom.weight)
        general_symptom.nutrition = request.data.get(
            "nutrition", general_symptom.nutrition
        )
        general_symptom.audiometry = request.data.get(
            "audiometry", general_symptom.audiometry
        )
        general_symptom.retina_scan = request.data.get(
            "retina_scan", general_symptom.retina_scan
        )
        general_symptom.optometry = request.data.get(
            "optometry", general_symptom.optometry
        )
        general_symptom.nutrition_report = request.data.get(
            "nutrition_report", general_symptom.nutrition_report
        )
        general_symptom.audiometry_report = request.data.get(
            "audiometry_report", general_symptom.audiometry_report
        )
        general_symptom.ecg_report = request.data.get(
            "ecg_report", general_symptom.ecg_report
        )
        print(
            f"created by name ->{general_symptom.created_by.username} doctorname -> {general_symptom.assigned_doctor.username}"
        )
        return {"general_symptom": general_symptom}
    else:
        return {"Error": "method accepts needs kwargs as user=user and request=request"}
