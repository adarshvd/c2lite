import db

# to handle right click fucntions
def handle_right_clicked_feature(data):
    print("things will be handled")
    if data['choice']=="Online" or data['choice']=="Offline":
        db.put_data(f"UPDATE csl.devices SET dev_status = '{data['choice']}' where id = {data['id']}")
    else:
        print("other logics")




#     UPDATE csl.devices
# SET dev_status = 'new_status'
# WHERE dev_name = 'device_name';