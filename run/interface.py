# coding=utf-8

from enum import IntEnum

class CompareResult(IntEnum):
    Equal = 1
    Greater = 2
    Less = 3

class base_json_model:
    def __init__(self, d):
        self.__dict__.update(d)


class run_json_model():
    smtp_user = ''
    smtp_to_user_list = ''
    smtp_host = ''
    smtp_port = 25
    smtp_password = ''
    app_release_note = ''
    latest_app_version = ''
    app_id = ''
    app_name = ''
    appstore_info_url = ''
    smtp_user_nickname = ''

class appstore_result_json_model(base_json_model):

    appletvScreenshotUrls = []
    screenshotUrls = []
    ipadScreenshotUrls = []
    artworkUrl512 = ''
    artistViewUrl = ''
    artworkUrl60 = ''
    artworkUrl100 = ''
    supportedDevices = []
    advisories = []
    isGameCenterEnabled = False
    features = []
    kind = ''
    languageCodesISO2A = []  # [ZH,EN,KO]
    fileSizeBytes = ''
    averageUserRatingForCurrentVersion = 0
    userRatingCountForCurrentVersion = 0
    trackContentRating = ''  # 4+
    trackCensoredName = ''  # iTalkBB AIjia
    trackViewUrl = ''  # view url: https://apps.apple.com/us/app/italkbb-aijia/id1261293132?uo=4
    contentAdvisoryRating = ''  # 4+
    averageUserRating = 0  # 4.35
    trackId = 0  # app_id : 1261293132
    trackName = ''  # iTalkBB AIjia 😃
    primaryGenreId = 0  # 6002
    releaseDate = ''  # 2019-09-09T07:00:00Z
    genreIds = []
    formattedPrice = ''
    primaryGenreName = ''
    isVppDeviceBasedLicensingEnabled = True
    minimumOsVersion = ''  # 11.0
    currentVersionReleaseDate = ''  # 2020-04-03T06:37:59Z 😃
    releaseNotes = ''  # update note 😃
    sellerName = ''  # iTalk Global Communications
    currency = ''  # USD
    description = ''  # app-description 😃
    artistId = 0  # 400404637
    artistName = ''  # iTalk Global Communications, Inc.
    genres = []
    price = 0.0
    bundleId = ''  # com.italkbb.arm 😃
    version = ''  # 1.7.0 😃
    wrapperType = ''  # software
    userRatingCount = 0  # 8

def compare(a, b) -> CompareResult:
    la = a.split('.')
    lb = b.split('.')
    f = 0
    if len(la) > len(lb):
        f = len(la)
    else:
        f = len(lb)
    for i in range(f):
        try:
            if int(la[i]) > int(lb[i]):
                print(a + '>' + b)
                return CompareResult.Greater
            elif int(la[i]) == int(lb[i]):
                continue
            else:
                print(a + '<' + b)
                return CompareResult.Less
        except IndexError as e:
            if len(la) > len(lb):
                print(a + '>' + b)
                return CompareResult.Greater
            else:
                print(a + '<' + b)
                return CompareResult.Less
    print(a + '==' + b)
    return CompareResult.Equal

def run():
    pass


if __name__ == '__main__':
    run()
