import db
import utils_streaming

# to handle right click fucntions
def handle_right_clicked_feature(data):
    # print("things will be handled")

    #camera
    if data['dev_type']=="camera":
        if data['choice']=="Status":
            print("status logic")
        elif data['choice']=="Stream"and data['dev_status']=="Online":
            print("stream based on camera rtspid")
            try:
                utils_streaming.cam_popup(data['dev_rtsp'])
            except:
                print(f"error opening camera {data['dev_id']}")
        else:
            print("other camera logics")


    # espf
    if data['dev_type']=="espf":
        if data['choice']=="Status":
            print("status logic")
        elif data['choice']=="On":
            db.put_data(f"UPDATE csl.devices SET dev_status = 'Online' where dev_id = {data['dev_id']}")
        elif data['choice']=="Off":
            db.put_data(f"UPDATE csl.devices SET dev_status = 'Offline' where dev_id = {data['dev_id']}")
        else:
            print("other espf logics")




#     UPDATE csl.devices
# SET dev_status = 'new_status'
# WHERE dev_name = 'device_name';