import socketio


sio = socketio.Client()

# sio.connect('http://192.168.43.153:3000')
sio.connect('http://192.168.0.165:3000')

sio.emit('join', 'psi01')

@sio.event
def sendData(data):
    sio.emit('data', data)


# data = { 'temp1' : 23.12, 'temp2' : 23.5}

# sendData(data)
# sendData(data)



# sendData(data)
# sendData(data)
# sendData(data)

# sio.wait()
