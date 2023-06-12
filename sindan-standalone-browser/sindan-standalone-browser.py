from flask import Flask, render_template
import os
import sys
import json

args = sys.argv

if (len(args) != 2):
    print("python3 sindan-standalone-browser.py linux")
    print("or")
    print("python3 sindan-standalone-browser.py masos")
    exit(1)


app = Flask(__name__)

@app.route('/')
def json_files():
    directory = os.environ['HOME']+'/sindan-client/'+ args[1] +'/log/'
    files = os.listdir(directory)

    keys= ["layer", "log_group", "log_type", "log_campaign_uuid", "result", "target", "detail", "occurred_at"]
    devices = []
    data = {}

    idx_data = 0

    for file in files:
        with open(os.path.join(directory, file), 'r', encoding="utf-8") as f: 

            if (file.find("campaign_") >= 0):
                devices.append(f.read())

            else:
                line = f.read()
                idx_data += 1

                idx_layer = line.find("\"layer\" : ")
                idx_log_group = line.find("\"log_group\" :")
                layer = line[idx_layer + 11 : idx_log_group - 3]
        
                idx_log_type = line.find("\"log_type\" :")
                log_group = line[idx_log_group + 15 : idx_log_type  - 3]
                
                idx_log_campaign_uuid = line.find("\"log_campaign_uuid\" :")
                log_type = line[idx_log_type + 14 : idx_log_campaign_uuid - 3]
                
                idx_result = line.find("\"result\" :")
                log_campaign_uuid = line[idx_log_campaign_uuid + 24 : idx_result - 3]

                idx_target = line.find("\"target\" :")
                result = line[idx_result + 12 : idx_target - 3]

                idx_detail = line.find("\"detail\" :")
                target = line[idx_target + 12 : idx_detail - 3]

                idx_occurred_at = line.find("\"occurred_at\" :")
                detail = line[idx_detail + 12 : idx_occurred_at - 3]
                occurred_at = line[idx_occurred_at + 17 : - 4]

                data[idx_data] = {"occurred_at" : occurred_at, \
                                    "layer" : layer, \
                                    "log_group" : log_group, \
                                    "log_type" : log_type, \
                                    "log_campaign_uuid" : log_campaign_uuid, \
                                    "result" : result, \
                                    "target" : target,\
                                    "detail" : detail
                                }

    sort_data = sorted(data.items(), key=lambda x: x[1]['occurred_at'], reverse=True)

    return render_template('index.html', devices=devices, index=idx_data, data=sort_data)

if __name__ == '__main__':
    app.run(debug=True)
