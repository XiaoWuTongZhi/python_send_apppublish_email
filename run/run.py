#!/usr/bin/env python3
# coding=utf-8
import smtplib, requests, json, os, time
import pandas as pd
from interface import appstore_result_json_model, run_json_model, compare, CompareResult

from email.mime.text import MIMEText
from email.header import Header

lastest_app_version = ''

run_info = run_json_model()

def auto_send_email(json_model:appstore_result_json_model):

    if compare(lastest_app_version, run_info.latest_app_version) == CompareResult.Greater:

        print('\033[1;32m 😁 needs to send email to everybody !\033[0m')

        write_excel(6, 1, lastest_app_version)
        time.sleep(2)
        os.system('git add *')
        # git_commit = "git commit - m 'update latest version to %s'"%lastest_app_version
        os.system("git commit -m 'update latest version to %s'" % lastest_app_version)
        res = os.system('git push origin')

        if res != 0:
            print('\033[0;31m git push origin failed ! \033[0m')
            os._exit(-1)
        else:
            os.system('git tag %s' % lastest_app_version)
            os.system('git push origin --tags')
            send_email_to_everybody()

    else:
        print("\033[1;33m 😿 it doesn't need to send update-email. \033[0m")



def check_appstore_version() -> appstore_result_json_model:
    global lastest_app_version

    res = requests.get(url=run_info.appstore_info_url, params={'id': run_info.app_id})
    dict = json.loads(res.content)
    print('AppStore response json data is', dict)
    json_model = appstore_result_json_model(dict['results'][0])  # parse json model
    lastest_app_version = json_model.version
    run_info.app_release_note = run_info.app_release_note + '\n\n' + json_model.releaseNotes
    run_info.app_name = json_model.trackName
    print('===============================')
    print('appstore version is %s\nlocal lastest version is %s' % (lastest_app_version, run_info.latest_app_version))
    return json_model

# SMTP email
def send_email_to_everybody():

    server = smtplib.SMTP(host=run_info.smtp_host, port=run_info.smtp_port)
    server.login(user=run_info.smtp_user, password=run_info.smtp_password)
    server.set_debuglevel(1)

    msg = MIMEText(run_info.app_release_note, 'plain', 'utf-8')
    msg['From'] = '"%s"<%s>'%(run_info.smtp_user_nickname,run_info.smtp_user)
    msg['To'] = str(run_info.smtp_to_user_list)
    msg['Subject'] = Header('%s %s iOS 上线通知' %(run_info.app_name,lastest_app_version), 'utf-8')
    try:
        server.sendmail(from_addr=run_info.smtp_user, to_addrs=run_info.smtp_to_user_list, msg=msg.as_string())
        print('\033[0;32m smtp send success ‍\033[0m')
        return True
    except smtplib.SMTPException as exp:
        print('\033[0;31m smtp send failed \033[0m', exp)
        return False


# Excel
def read_excel():
    filename = os.path.join('run', 'input.xlsx')
    df = pd.read_excel(filename)
    print('read excel:' + str(df.values) + '\n==========================')
    update_run_information(df)


def write_excel(row, colum, value):
    filename = os.path.join('run', 'input.xlsx')
    df = pd.read_excel(filename)
    df.iloc[row][colum] = value
    df.to_excel(filename, index=False, header=True)
    print('write excel complete')



# Private
def update_run_information(df):
    run_info.smtp_user = df.iloc[0][1]
    run_info.smtp_to_user_list = df.iloc[1][1]
    run_info.smtp_host = df.iloc[2][1]
    run_info.smtp_port = df.iloc[3][1]
    run_info.smtp_password = df.iloc[4][1]
    run_info.app_release_note = df.iloc[5][1]
    run_info.latest_app_version = df.iloc[6][1]
    run_info.app_id = df.iloc[7][1]
    run_info.appstore_info_url = df.iloc[8][1]
    run_info.smtp_user_nickname = df.iloc[9][1]

def run():
    read_excel()
    json_model = check_appstore_version()
    auto_send_email(json_model)


if __name__ == '__main__':
    run()
