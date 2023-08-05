# The circle class accepts two arguments, the radius of the circle and the length of arc between the locations
# which are being assessed.  This generates a representation of the Earth's curvature which will be represented on the
# final graph.  This is important to represent as the curvature of the Earth makes a big difference to whether
# or not, line of sight exists between locations.

import numpy as np


class Circle:

    def __init__(self, radius_of_circle, length_of_arc):
        self.radius = radius_of_circle
        self.arc_length = length_of_arc

    # Define Circle class methods

    # Calculate the central angle, in degrees, by using the arc_length
    # Gives angle in degrees at centre of the circle between the two points (beginning and end points of arc_length)
    # Returns floating point
    def calc_degrees(self):
        return self.calc_radians() * 180 / np.pi

    # Calculate the central angle in radians, between two points on the circle
    # Returns floating point
    def calc_radians(self):  # Where theta is the angle between both points at the centre of the circle
        return self.arc_length / self.radius  # Convert degrees to radians to work with chord_length formula

    # Returns the chord lengths of the arc, taking theta (angle in radians) as it's argument
    # The chord is the horizontal line which separates the arc segment from the rest of the circle
    # Formula for theta (radians) only, not degrees #confirmed using http://www.ambrsoft.com/Trigocalc/Sphere/Arc_.htm
    # Returns floating point
    def calc_chord_length(self):
        return 2 * self.radius * np.sin(self.calc_radians() / 2)

    # Calculates the length of arc, taking theta (angle in radians) as its argument.
    # Confirmed using http://www.ambrsoft.com/Trigocalc/Sphere/Arc_.htm
    # Returns floating point
    def calc_arc_length(self):
        return self.arc_length

    # Calculates the Sagitta of the arc segment.  The Sagitta is the distance from the centre of the arc
    # to the centre of the chord
    # Confirmed correct against online calculator https://www.liutaiomottola.com/formulae/sag.htm
    def calc_sagitta(self):
        return self.radius - (np.sqrt((self.radius ** 2) - ((self.calc_chord_length() / 2) ** 2)))

    # Calculate the distance between the chord of the segment and the centre of the circle
    # Returns floating point
    def calc_arc_apothem(self):
        return round(self.radius - self.calc_sagitta(), 8)

    # Calculate centre point of circle
    # Returns floating point
    def calc_circular_centre_x(self):
        return self.calc_chord_length() / 2

    # Calculate centre point of circle
    # Returns a floating point number
    def calc_circular_centre_y(self):
        return self.calc_sagitta() - self.radius

    # Calculate the diameter of the circle
    # Returns a floating point number which is double the radius.
    def calc_diameter(self):
        return self.radius * 2

    # Returns the starting angle of the circular arc as float in radians
    # Takes two arguments, starting y and x coordinates
    def calc_start_angle(self, start_y, start_x):
        centre_y = self.calc_circular_centre_y()
        centre_x = self.calc_circular_centre_x()
        return np.arctan2(start_y - centre_y, start_x - centre_x)

    # Returns the ending angle of the circular arc as float in radians
    # Takes two arguments, ending y and x coordinates
    def calc_end_angle(self, end_y, end_x):
        centre_y = self.calc_circular_centre_y()
        centre_x = self.calc_circular_centre_x()
        return np.arctan2(end_y - centre_y, end_x - centre_x)

    # Returns a numpy array of y-axis values for mapping on matplotlib graph.  x values list is a list of distances
    # in nautical miles.  Each y-axis value represents the rising and falling of the earth to simulate 'curvature' which
    # effects line of sight visibility.
    def calculate_earth_surface_y_values(self, list_of_x_axis_values, list_of_angles):
        earth_radius = self.radius
        y_values_list = []
        for j in range(len(list_of_x_axis_values)):
            # Calculate the y axis value (height) for the corresponding x value (distance).  Subtract the apothem
            # of the circle to ensure the arc starts at coordinates 0,0 and ends at zero again on the y axis
            y = earth_radius * np.sin(list_of_angles[j]) - self.calc_arc_apothem()
            # Convert nautical miles to meters for elevation, rounding to make it tidier and easier to test
            y = round(y * 1852, 5)
            y_values_list.append(y)
        y_values_np = np.array(y_values_list)

        return y_values_np
