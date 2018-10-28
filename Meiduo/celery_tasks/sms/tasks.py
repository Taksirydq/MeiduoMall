from Meiduo.utils.ytx_sdk.sendSMS import CCP
from celery_tasks.main import app


@app.task(name='send_sms_code')
def send_sms_code(mobile, code, expires, template_id):
    # CCP.sendTemplateSMS(mobile, code, expires, template_id)
    pass
