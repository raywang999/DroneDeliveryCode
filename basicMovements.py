from djitellopy import tello

drone = tello.Tello()

# connect to drone
drone.connect()
print("Battery Level: ", drone.get_battery())
drone.takeoff()
# drone.move_forward(547)
# drone.move_forward(547)
drone.move_forward(400)

drone.land()