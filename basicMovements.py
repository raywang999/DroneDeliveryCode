from djitellopy import tello

drone = tello.Tello()

# connect to drone
drone.connect()
print("Battery Level: ", drone.get_battery())
# drone.takeoff()
# drone.rotate_counter_clockwise(90)
# drone.move_forward(100)

# drone.land()