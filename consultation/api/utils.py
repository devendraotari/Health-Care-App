from rest_framework.authtoken.models import Token

from consultation.models import GeneralSymptom


def get_token_key(request):
    token_key = request.headers["Authorization"].split(" ")[1]
    return token_key


def get_request_user(request):
    token_key = get_token_key(request)
    if token_key:
        user = Token.objects.get(key=token_key).user
        return user


def create_or_update_symptoms(id=None, *args, **kwargs) -> GeneralSymptom:
    general_symptom = None
    user = kwargs["user"]
    assigned_doctor = kwargs["assigned_doctor"]
    request = kwargs["request"]
    if id:
        try:
            general_symptom = GeneralSymptom.objects.all().filter(id=id)
        except Exception as e:
            print(str(e))
            return general_symptom
    elif not id:
        general_symptom = GeneralSymptom(patient=user, assigned_doctor=assigned_doctor)
    general_symptom.systolic = request.data.get("systolic", general_symptom.systolic)
    general_symptom.diatolic = request.data.get("diatolic", general_symptom.diatolic)
    general_symptom.blood_glucose = request.data.get(
        "blood_glucose", general_symptom.blood_glucose
    )
    general_symptom.heart_rate = request.data.get(
        "heart_rate", general_symptom.heart_rate
    )
    general_symptom.ecg = request.data.get("ecg", general_symptom.ecg)
    general_symptom.ecg_report = request.data.get(
        "ecg_report", general_symptom.ecg_report
    )
    general_symptom.temp = request.data.get("temp", general_symptom.temp)
    general_symptom.pulse = request.data.get("pulse", general_symptom.pulse)
    general_symptom.spo2 = request.data.get("spo2", general_symptom.spo2)
    general_symptom.weight = request.data.get("weight", general_symptom.weight)
    general_symptom.nutrition = request.data.get("nutrition", general_symptom.nutrition)
    general_symptom.nutrition_report = request.data.get(
        "nutrition_report", general_symptom.nutrition_report
    )
    general_symptom.audiometry = request.data.get(
        "audiometry", general_symptom.audiometry
    )
    general_symptom.audiometry_report = request.data.get(
        "audiometry_report", general_symptom.audiometry_report
    )
    general_symptom.retina_scan = request.data.get(
        "retina_scan", general_symptom.retina_scan
    )
    general_symptom.optometry = request.data.get("optometry", general_symptom.optometry)
    return general_symptom
