def add_pad(serial_no):
    serial = str(serial_no)
    ln = len(serial)
    
    if ln == 1:
        serial = '00' + serial
    elif ln == 2:
        serial= '0' + serial

    return serial

def generate_appointments_id(date_obj, serial_no):
    date = ('').join(str(date_obj).split('-'))
    serial = add_pad(serial_no)

    return date+serial