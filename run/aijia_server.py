#!/usr/bin/env python3
# coding=utf-8

import requests,json

aijia_server_login_url = 'https://hsapi.italkdd.com/Aijia.SecondaryFunction/AppInfo/Login/Login'
aijia_server_update_url = 'https://hsapi.italkdd.com/Aijia.SecondaryFunction/AppInfo/AppInfo/UploadAPK'
aijia_server_pwd = 'ai#jia_Italkbb@2019'

class Update_aijia_request_json_model:


    def __init__(self,version,version_code,note_zh,note_en):
        self.appVersionCode = str(version_code)
        self.appVersion = version
        self.updateInfo = note_zh
        self.updateInfoEN = note_en
        self.appName = 'iTalkBB智能家'
        self.appDesc = 'iTalkBB智能家是一款智能家居应用，结合iTalkBB智能眼设备，实时掌握家庭状况，时刻保护您的家庭安全。'
        self.appType = 'iOS'

# AIjia Server
def run_api(request_model:Update_aijia_request_json_model):
    res = mock_login()
    if res == True :
        s_res = update_version_info(request_model)
        if s_res == True :
            print('update aijia app version info success !')
            return True
        else:
            return False
    else :
        return False

def mock_login():
    # mock login first
    res = requests.post(aijia_server_login_url, data={'pwd': aijia_server_pwd})
    if res.status_code == 200:
        parse_data = json.loads(res.content)
        if parse_data['IsSuccess'] == True:
            print('mock aijia server login success .')
            return True
        else:
            print('aijia server mock login failed', parse_data)
            return False
    else:
        print('aijia server mock login failed', res)
        return False

def update_version_info(request_model:Update_aijia_request_json_model):
    # headers = {'Content-Type': 'multipart/form-data','boundary':'<calculated when request is sent>'}
    request_dict = request_model.__dict__
    res = requests.post(aijia_server_update_url, json=request_dict)
    if res.status_code == 200:
        parse_data = json.loads(res.content)
        if parse_data['IsSuccess'] == True:
            print('update server app version info success !')
            return True
        else:
            print('aijia server update version info failed', parse_data)
            return False
    else :
        print('aijia server update version info failed',res)
        return False

if __name__ == '__main__':
    pass