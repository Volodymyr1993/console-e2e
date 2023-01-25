import os
import re
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

EMAIL_LIST = os.environ.get('EMAIL_LIST')
REPORT_FILE = os.environ.get('REPORT_FILE')
REPORT_URL = "https://gitlab.com/limelight-networks/qa/ltf/ltf-projects/edgio-console-app/-"\
             f"/pipelines/{os.environ.get('CI_PIPELINE_ID')}/test_report"
REPORT_TITLE = f"Edgio Console App Regression (stage): "


EMAIL_TEMPLATE = """<html>
<b>Pipeline results:</b> {run_title}<br>
<hr>
<b>Total:</b> <font color="black">{total}</font><br>
<b>Passed:</b> <font color="green">{passed}</font><br>
<b>Failed:</b> <font color="red">{failed}</font><br>
<b>Blocked:</b> <font color="grey">{blocked}</font><br>
<b>Duration:</b> <font color="black">{duration}</font><br><br>
<a href="{url}">See details here</a><br>
<hr>
</html>
"""


def _send(subj, html_body):
    sender = 'Edgio Console App Regression <norepy@llnw.com>'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subj
    msg['From'] = sender
    msg['To'] = EMAIL_LIST
    html_body = MIMEText(html_body, 'html')
    msg.attach(html_body)
    with smtplib.SMTP('mail.llnw.com', 25) as srv:
        srv.sendmail(sender, EMAIL_LIST.split(','), msg.as_string())


def send_email():
    assert all(
        (REPORT_URL, REPORT_TITLE, REPORT_FILE, EMAIL_LIST)
    ), "Some env vars weren't specified"

    report_data = open(REPORT_FILE).read()

    run_title = REPORT_TITLE
    run_url = REPORT_URL
    broken, failed, blocked, total, duration = re.search(
        r'testsuite name="pytest" errors="(.*?)" failures="(.*?)" skipped="(.*?)" tests="(.*?)" time="(.*?)"',
        report_data).groups()
    passed = int(total) - int(broken) - int(failed) - int(blocked)
    failed = int(broken) + int(failed)
    duration = datetime.timedelta(seconds=float(duration))

    run_title += f'FAILED {failed} of {total}' if failed > 0 else f'PASSED {passed} of {total}'

    _send(
        run_title,
        EMAIL_TEMPLATE.format(
            run_title=run_title,
            total=total,
            passed=passed,
            failed=failed,
            blocked=blocked,
            duration=duration,
            url=run_url
        )
    )


if __name__ == '__main__':
    send_email()
