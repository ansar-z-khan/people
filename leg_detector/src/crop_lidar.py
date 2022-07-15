import rospy
from sensor_msgs.msg import LaserScan
import math

SCAN_TOPIC = "/scan"
OUTPUT_TOPIC = "/forward_scan"


pub = None

def scan_cb(data):
    global pub
    MIN_ANGLE = -5*math.pi/8
    MAX_ANGLE = -3*math.pi/8
    actual_min = data.angle_min
    actual_max = data.angle_max
    filtered_data = data
    new_ranges = []
    current_angle = actual_min
    i = 0
    while i < len(data.ranges):
        if current_angle > MIN_ANGLE and current_angle < MAX_ANGLE:
            new_ranges.append(data.ranges[i])
        if current_angle > MAX_ANGLE:
            break
        i += 1
        current_angle += data.angle_increment
        
    filtered_data.ranges = new_ranges
    filtered_data.angle_min = MIN_ANGLE
    filtered_data.angle_max = MAX_ANGLE
    filtered_data.intensities = [data.intensities[0]]*len(new_ranges)
    pub.publish(filtered_data)


def main():
    global pub
    rospy.init_node("LidarCropper")
    rospy.Subscriber(SCAN_TOPIC, LaserScan, scan_cb)
    pub = rospy.Publisher(OUTPUT_TOPIC, LaserScan, queue_size=10)
    rospy.spin()

if __name__ == "__main__":
    main()