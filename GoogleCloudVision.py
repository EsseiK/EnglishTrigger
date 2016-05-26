#!/usr/bin/python
#coding: UTF-8

import base64
import json
import ConfigParser
from requests import Request, Session

class GoogleCloudVision():

    # デフォルト・コンストラクター。
    def __init__(self):
        return
    
    # C画像の分析。
    def ImageDetection(self, str_image_path):
        
    
        # 画像の読み込み。
        bin_image = open(str_image_path, 'rb').read()
        
        # base64エンコード。
        str_encode_file = base64.b64encode(bin_image)
        
        # APIのURL指定。
        str_url = "https://vision.googleapis.com/v1/images:annotate?key="
        
        # Content-Type の設定。
        str_headers = {'Content-Type': 'application/json'}
        
        # ペイロードの設定。
        str_json_data = {
            'requests': [
                {
                    'image': {
                        'content': str_encode_file 
                    },
                    'features': [
                        {
                            'type': "LABEL_DETECTION",
                            'maxResults': 10
                        },
                        {
                            'type': "SAFE_SEARCH_DETECTION",
                            'maxResults': 3
                            
                        }
                    ]
                }
            ]
        }
        
        # API_KEY の取得
        #  API キーは、git 管理外にするため、config ファイルとして外部化している。
        inifile = ConfigParser.SafeConfigParser()
        inifile.read("./config.ini")
        API_KEY = inifile.get("settings", "API_KEY")
        
        # リクエスト送信。
        obj_session = Session()
        obj_request = Request("POST",
                str_url + API_KEY,
                data = json.dumps(str_json_data),
                headers = str_headers
                )
        obj_prepped = obj_session.prepare_request(obj_request)
        obj_response = obj_session.send(obj_prepped, verify=True, timeout = 60) 
        
        # 分析結果の取得
        if obj_response.status_code == 200:
#            print obj_response.text
            return obj_response.text
        else:
            return "error:" + str(obj_response.status_code)
        
class ImageDetectionResult():

    Results = []

    def __init__(self):
        self.Score = 0
        self.Description = ""
        
        return

    def ParseJson(self, target):
        tmpJson = json.loads(target)
        
        # DEBUG
        #print json.dumps(tmpJson, sort_keys=True, indent=4)
        
        tmpList = tmpJson["responses"][0]["labelAnnotations"];
        # DEBUG
        #print tmpList

        # データのクリア。
        self.Results = []
       
        for data in tmpList:
            tmp = ImageDetectionResult()
            tmp.Score = data["score"]
            tmp.Description = data["description"]
            self.Results.append(tmp)
        
        return
        
    def __str__(self):
        return "{0:<20}:{1:<3.1%}".format(self.Description, self.Score)
    