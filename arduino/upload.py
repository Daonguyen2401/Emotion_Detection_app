import pyduinocli
import os



def upload_play_song():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        arduino = pyduinocli.Arduino("./arduino-cli")
        brds = arduino.board.list()
        # assuming we are using the first board listed
        #print(port = brds['result'][0]["detected_ports"]['port']['address'])
        
        port = brds['result']["detected_ports"][0]["port"]["address"]
        fqbn = brds['result']["detected_ports"][0]['matching_boards'][0]['fqbn']
        arduino.compile(fqbn=fqbn, sketch="code")
        arduino.upload(fqbn=fqbn, sketch="code", port=port)
        return True, "Successfully uploaded and played the song"
    except Exception as e:
        print(e)
        return False, str(e)

def upload_empty_code():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        arduino = pyduinocli.Arduino("./arduino-cli")
        brds = arduino.board.list()
        # assuming we are using the first board listed
        #print(port = brds['result'][0]["detected_ports"]['port']['address'])
        port = brds['result']["detected_ports"][0]["port"]["address"]
        fqbn = brds['result']["detected_ports"][0]['matching_boards'][0]['fqbn']
        arduino.compile(fqbn=fqbn, sketch="pause")
        arduino.upload(fqbn=fqbn, sketch="pause", port=port)
        return True, "Successfully uploaded and played the song"
    except Exception as e:
        print("This is errror")
        print(e)
        return False, str(e)
    
if __name__ == "__main__":
    #success, message = upload_play_song()
    # print(message)
    success, message = upload_empty_code()
    print(message)
        