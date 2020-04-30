#!/usr/bin/env python3
# coding=utf-8
import smtplib, requests, json, os, time
import pandas as pd
from interface import appstore_result_json_model, run_json_model, compare, CompareResult
from email.mime.text import MIMEText
from email.header import Header
import aijia_server



lastest_app_version = ''

run_info = run_json_model()

# Output file
def output_txt(tip:str):
    print('output result.txt :',tip)
    with open('result.txt','w',encoding='utf-8') as f:
        f.write(tip)

# Check AppStore Version
def check_appstore_version() -> appstore_result_json_model:
    global lastest_app_version

    res = requests.post(url=run_info.appstore_info_url, params={'id': run_info.app_id})
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

    release_note = run_info.app_release_note % lastest_app_version

    msg = MIMEText(release_note, 'plain', 'utf-8')
    msg['From'] = '"%s"<%s>' % (run_info.smtp_user_nickname, run_info.smtp_user)
    to_emails_str = ','.join(run_info.smtp_to_user_list)
    msg['To'] = to_emails_str
    msg['Subject'] = Header('%s %s iOS 上线通知' % (run_info.app_name, lastest_app_version), 'utf-8')
    try:
        server.sendmail(from_addr=run_info.smtp_user, to_addrs=run_info.smtp_to_user_list, msg=msg.as_string())
        print('\033[0;32m smtp send success ‍\033[0m')
        return True
    except smtplib.SMTPException as exp:
        print('\033[0;31m smtp send failed \033[0m', exp)
        return False


# Excel
def read_excel():
    # filename = os.path.join('run', 'input.xlsx')
    filename = 'input.xlsx'
    df = pd.read_excel(filename)
    print('read excel:' + str(df.values) + '\n==========================')
    update_run_information(df)


def write_excel(row, colum, value):
    # filename = os.path.join('run', 'input.xlsx')
    filename = 'input.xlsx'
    df = pd.read_excel(filename)
    df.iloc[row][colum] = value
    df.to_excel(filename, index=False, header=True)
    print('write excel complete')

def remove_txt_if_needs():
    filename = 'result.txt'
    if os.path.exists(filename):
        print('Find result.txt exist, will delete it first ...')
        os.remove(filename)

# Private
def update_run_information(df):
    run_info.smtp_user = df.iloc[0][1]
    run_info.smtp_to_user_list = str(df.iloc[1][1]).split(',')
    run_info.smtp_host = df.iloc[2][1]
    run_info.smtp_port = df.iloc[3][1]
    run_info.smtp_password = df.iloc[4][1]
    run_info.app_release_note = df.iloc[5][1]
    run_info.latest_app_version = df.iloc[6][1]
    run_info.app_id = df.iloc[7][1]
    run_info.appstore_info_url = df.iloc[8][1]
    run_info.smtp_user_nickname = df.iloc[9][1]

def system(cmd:str):
    print(cmd)
    res = os.system(cmd)
    return res

# Final step
def auto_send_email(json_model: appstore_result_json_model):
    if compare(lastest_app_version, run_info.latest_app_version) == CompareResult.Greater:

        print('\033[1;32m 😁 needs to send email to everybody !\033[0m')

        write_excel(6, 1, lastest_app_version)
        time.sleep(2)

        git_add = 'git add .'
        system(git_add)

        # git_commit = "git commit - m 'update latest version to %s'"%lastest_app_version
        git_commit = "git commit -m 'update latest version to %s'" % lastest_app_version
        system(git_commit)

        git_push = 'git push origin'
        res = system(git_push)

        if res != 0:
            print('\033[0;31m git push origin failed ! \033[0m')
            os._exit(-1)
            output_txt('appstore updated, but push git push origin failed')
        else:
            git_tag = 'git tag %s' % lastest_app_version
            system(git_tag)

            git_tag_push = 'git push origin --tags'
            system(git_tag_push)

            res = send_email_to_everybody()
            output_txt('appstore updated, send email suc !' if (res==True) else 'appstore updated, but send email failed')

    else:
        print("\033[1;33m 😿 it doesn't need to send update-email. \033[0m")

def run():
    remove_txt_if_needs()
    read_excel()
    json_model = check_appstore_version()
    auto_send_email(json_model)
    # json_model = aijia_server.Update_aijia_request_json_model(version=lastest_app_version,version_code=2415,note_zh=run_info.app_release_note,note_en=run_info.app_release_note)
    # aijia_server.run_api(json_model)

if __name__ == '__main__':
    run()
