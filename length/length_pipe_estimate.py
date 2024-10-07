# length/length_pipe_estimate.py

class DistanceCalculator:
    """Class to calculate the distance between two points based on pixel coordinates.

    Attributes:
        coordinates (list): A list of coordinate intervals for reference.
        distance_per_interval (float): The actual distance in meters represented by each pixel interval.
    """

    def __init__(self, coordinates, distance_per_interval):
        """Initializes the DistanceCalculator with coordinates and distance per interval.

        Args:
            coordinates (list): A list of coordinate intervals.
            distance_per_interval (float): The distance that corresponds to each interval in meters.
        """
        self.coordinates = coordinates
        self.distance_per_interval = distance_per_interval

    def calculate_length_between_any_two_points(self, x1, x2):
        """Calculates the total length between two points based on their coordinates.

        Args:
            x1 (int): The pixel coordinate of the first point.
            x2 (int): The pixel coordinate of the second point.

        Returns:
            float or str: The total distance in meters between the two points,
                          or an error message if one or both points are out of range.
        """
        left1, right1 = self.find_interval(x1)
        left2, right2 = self.find_interval(x2)

        if left1 is None or left2 is None:
            return "One or both points are out of range."

        distance1 = self.distance_in_meters(x1, left1, right1)
        distance2 = self.distance_in_meters(x2, left2, right2)

        intervals_between_points = abs(
            self.coordinates.index(right1) - self.coordinates.index(left2)
        ) * self.distance_per_interval
        total_distance = intervals_between_points + distance1 + distance2

        return total_distance

    def find_interval(self, x):
        """Finds the interval in which the given coordinate x lies.

        Args:
            x (int): The pixel coordinate to find the interval for.

        Returns:
            tuple: A tuple containing the left and right bounds of the interval,
                   or (None, None) if the coordinate is out of range.
        """
        for i in range(len(self.coordinates) - 1):
            if self.coordinates[i] <= x <= self.coordinates[i + 1]:
                return self.coordinates[i], self.coordinates[i + 1]
        return None, None

    def distance_in_meters(self, x, left, right):
        """Calculates the distance in meters for a given coordinate within its interval.

        Args:
            x (int): The pixel coordinate to calculate the distance for.
            left (int): The left bound of the interval.
            right (int): The right bound of the interval.

        Returns:
            float: The calculated distance in meters based on the relative position within the interval.
        """
        pixel_distance = abs(right - left)
        if pixel_distance == 0:
            return 0
        relative_position = (x - left) / pixel_distance
        return relative_position * self.distance_per_interval
