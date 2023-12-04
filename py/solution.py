from typing import Dict, List, Tuple
import math, numpy
from util import Color, Sat, User, Vector3

def solve(users: Dict[User, Vector3], sats: Dict[Sat, Vector3]) -> Dict[User, Tuple[Sat, Color]]:
    solution = {}

    # Calculate the maximum number of users a satellite can serve
    max_users_per_satellite = 32

    # Initialize a dictionary to keep track of the used colors for each satellite
    used_colors = {sat: set() for sat in sats}

    # Helper function to calculate the angle between two vectors
    def angle_between(v1: Vector3, v2: Vector3) -> float:
        #return math.degrees(math.acos(v1.dot(v2-v1) / (v1.mag() * (v2-v1).mag())))
        return math.degrees(math.acos(v1.unit().dot(v2.unit())))

    # Sort users by latitude to serve users near the equator first
    sorted_users = sorted(users.items(), key=lambda x: abs(x[1].y))

    # Iterate through each user and assign them to a satellite and color
    for user, user_position in sorted_users:
        best_satellite = None
        best_color = None
        best_score = float('-inf')

        for sat, sat_position in sats.items():
            # Calculate the angle between user and satellite
            angle = angle_between(user_position, sat_position - user_position)
            #print(angle)

            # Calculate the satellite_beam vector
            satellite_beam = sat_position - user_position
            for color in Color:
                # Check if the angle is within 45 degrees
                if angle <= 45 and color not in used_colors[sat]:
                    # Calculate the score based on user density around the satellite
                    score = sum(
                        1 for u, _ in solution.values() if _ == sat and 
                        angle_between(satellite_beam, sat_position - users[u]) >= 10)
                        #print(score)
                    if score > best_score:
                        best_satellite = sat
                        best_color = color
                        best_score = score
                    best_satellite = sat
                    best_color = color
        if best_satellite is not None:
            solution[user] = (best_satellite, best_color)
            used_colors[best_satellite].add(best_color)

            # Check if the maximum number of users per satellite is reached
            if len(solution) >= max_users_per_satellite * len(sats):
                break

    return solution
# Test case 1
if __name__ == '__main__':
    users = {
        User(0): Vector3(-6370.9384, 24.2156, -14.0911),
        User(1): Vector3(6372, 0, 0),
    }

    sats = {
        Sat(0): Vector3(-5059.9798, 4721.9536, 0.0000),
    }

    result = solve(users, sats)

    print(result)
