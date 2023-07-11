import time
from rplidar import RPLidar
import PyCmdMessenger

PORT_NAME = 'COM4' # this is for the Lidar
myarduino = PyCmdMessenger.ArduinoBoard("COM13",baud_rate=9600)

commands = [["motor_control", "iiiii"]]

c = PyCmdMessenger.CmdMessenger(myarduino,commands)

# Define some constants for your rover
MIN_DISTANCE = 0.3  # Minimum distance to an obstacle (in meters)
FORWARD_SPEED = 255  # Rover forward speed
TURN_SPEED = 255  # Rover turn speed
SLEEP_TIME = 0.1  # Time between control updates (in seconds)


class Vehicle:
    def __init__(self):
        self.left_wheel_speed = 0
        self.left_wheel_direction = True
        self.right_wheel_speed = 0
        self.right_wheel_direction = True
        self.movement_enabled = True

    def set_left_wheel_speed(self, speed, direction):
        self.left_wheel_speed = speed
        self.left_wheel_direction = direction

    def set_right_wheel_speed(self, speed, direction):
        self.right_wheel_speed = speed
        self.right_wheel_direction = direction

    def stop_movement(self):
        self.movement_enabled = False

    def start_movement(self):
        self.movement_enabled = True

    def update(self):
        # Update the rover's wheels based on the current speed and direction
        pass

def get_lidar_data(lidar):
    # Get the angle and distance to the nearest detected object
    global stop
    print('Recording measurements... Press Crl+C to stop.')
    for measurment in lidar.iter_measurments():
        if stop == True:
            lidar.stop()
            lidar.stop_motor()
            c.send("motor_control",0,0,0,0,0)  # turn off wheel motors
            lidar.disconnect()
            break
        return measurment[1], measurment[2]


def main():
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    lidar.start_motor()
    time.sleep(1)
    info = lidar.get_info()
    print(info)
    rover = Vehicle()

    while True:
        angle, distance = get_lidar_data(lidar)

        if distance < MIN_DISTANCE:
            rover.stop_movement()
            if angle < 180:
                # Turn right
                rover.set_left_wheel_speed(TURN_SPEED, True)
                rover.set_right_wheel_speed(TURN_SPEED, False)
            else:
                # Turn left
                rover.set_left_wheel_speed(TURN_SPEED, False)
                rover.set_right_wheel_speed(TURN_SPEED, True)
            rover.start_movement()

        else:
            rover.set_left_wheel_speed(FORWARD_SPEED, True)
            rover.set_right_wheel_speed(FORWARD_SPEED, True)

        # Update the rover's wheels and sleep
        rover.update()
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()