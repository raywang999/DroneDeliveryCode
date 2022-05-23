from djitellopy import tello

drone = tello.Tello()

# connect to drone
drone.connect()
print("Battery Level: ", drone.get_battery())
drone.takeoff()
drone.move_forward(100)
drone.rotate_clockwise(90)
drone.flip_left()
drone.move_forward(200)

drone.land()