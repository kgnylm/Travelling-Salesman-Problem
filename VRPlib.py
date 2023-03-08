import matplotlib.pyplot as plt


def plot_routes(routes, distance_matrix,title):

    # Plot the routes
    plt.figure(figsize=(20, 5))
    plt.suptitle(title)
    plt.subplot(1, 3, 1)
    for j in range(len(routes[0])):
        # Get the next location in the route
        if j == len(routes[0]) - 1:
            k = 0
        else:
            k = j + 1
        # Get the current and next location
        loc1 = routes[0][j]
        loc2 = routes[0][k]
        # Get the x and y values
        x1 = distance_matrix[loc1][0]
        y1 = distance_matrix[loc1][1]
        x2 = distance_matrix[loc2][0]
        y2 = distance_matrix[loc2][1]
        # Plot the locations
        plt.plot([x1, x2], [y1, y2], color='r')
        plt.scatter(x1, y1, color='g')
        plt.scatter(x2, y2, color='b')
    plt.title("Route 1")
    plt.subplot(1, 3, 2)
    for j in range(len(routes[1])):
        # Get the next location in the route
        if j == len(routes[1]) - 1:
            k = 0
        else:
            k = j + 1
        # Get the current and next location
        loc1 = routes[1][j]
        loc2 = routes[1][k]
        # Get the x and y values
        x1 = distance_matrix[loc1][0]
        y1 = distance_matrix[loc1][1]
        x2 = distance_matrix[loc2][0]
        y2 = distance_matrix[loc2][1]
        # Plot the locations
        plt.plot([x1, x2], [y1, y2], color='m')
        plt.scatter(x1, y1, color='g')
        plt.scatter(x2, y2, color='b')
    plt.title("Route 2")
    plt.subplot(1, 3, 3)
    for j in range(len(routes[2])):
        # Get the next location in the route
        if j == len(routes[2]) - 1:
            k = 0
        else:
            k = j + 1
        # Get the current and next location
        loc1 = routes[2][j]
        loc2 = routes[2][k]
        # Get the x and y values
        x1 = distance_matrix[loc1][0]
        y1 = distance_matrix[loc1][1]
        x2 = distance_matrix[loc2][0]
        y2 = distance_matrix[loc2][1]
        # Plot the locations
        plt.plot([x1, x2], [y1, y2], color='y')
        plt.scatter(x1, y1, color='g')
        plt.scatter(x2, y2, color='b')
    plt.title("Route 3")
    plt.show()


def calculateSavings(distanceMatrix):
    n = len(distanceMatrix)
    savings = {}
    # Calculate savings for each pair of locations
    for i in range(n):
        for j in range(i+1, n):
            savings[(i, j)] = distanceMatrix[0][i] + \
                distanceMatrix[0][j] - distanceMatrix[i][j]
    return savings


def selectBestPair(savings, unassignedLocations):
    bestPair = None
    maxSavings = -float("inf")
    # Find pair of locations with highest savings
    for pair, s in savings.items():
        if s > maxSavings and all(x in unassignedLocations for x in pair):
            bestPair = pair
            maxSavings = s
    if bestPair == None:
        return (-1, -1)
    return bestPair


def selectBestLocation(savings, route, unassignedLocations, capacity, demand):
    bestLocation = None
    maxSavings = -float("inf")
    # Find location that results in highest savings
    for i in range(len(route)):
        for j in unassignedLocations:
            if (route[i], j) in savings and savings[(route[i], j)] > maxSavings and capacity - demand >= 0:
                bestLocation = j
                maxSavings = savings[(route[i], j)]
    return bestLocation


def savingsAlgorithm(distance_Matrix, capacity, customers, nodes, demand=10):
    #global selectBestPair
    # Initialize variables
    routes = []
    unassignedLocations = set(nodes)
    savings = {(i, j): round(distance_Matrix[i][0] + distance_Matrix[0][j] - distance_Matrix[i][j], 2)
               for i in customers for j in customers if j != i}
    # Iteratively construct routes
    while unassignedLocations != []:
        # Select pair of locations with highest savings
        a, b = selectBestPair(savings, unassignedLocations)
        if (a, b) == (-1, -1):
            break
        # Create new route with locations a and b
        route = [a, b]
        unassignedLocations.remove(a)
        unassignedLocations.remove(b)
        # Iteratively add locations to the route until capacity or time limit is reached
        while len(route)*demand < capacity:
            # Select the location that results in the highest savings
            best_loc = selectBestLocation(
                savings, route, unassignedLocations, capacity, demand)
            if best_loc == None:
                break
            route.append(best_loc)
            unassignedLocations.remove(best_loc)
        routes.append(route)
    return routes


def routeDistance(distance_matrix, route):

    # Initialize distance to default 0 to somewhere and return 0
    distance = distance_matrix[0][route[0]]+distance_matrix[route[-1]][0]

    # Iterate over the locations in the route and calculate the distance between each pair of locations
    for i in range(len(route) - 1):
        distance += distance_matrix[route[i]][route[i+1]]

    return distance


def two_opt(tour, tour_length, distanceMatrix):

    current_tour, current_tour_length = tour, tour_length
    best_tour, best_tour_length = current_tour, current_tour_length
    solution_improved = True

    while solution_improved:
        print()
        print('Attempting to improve the tour', current_tour,
              'with length', current_tour_length)
        solution_improved = False

        for i in range(1, len(current_tour)-2):
            for j in range(i+1, len(current_tour)-1):
                difference = round((distanceMatrix[current_tour[i-1]][current_tour[j]]
                                    + distanceMatrix[current_tour[i]][current_tour[j+1]]
                                    - distanceMatrix[current_tour[i-1]][current_tour[i]]
                                    - distanceMatrix[current_tour[j]][current_tour[j+1]]), 2)

                print('Cost difference due to swapping', current_tour[i], 'and',
                      current_tour[j], 'is:', difference)

                if current_tour_length + difference < best_tour_length:
                    print('Found an improving move! Updating the best tour...')

                    best_tour = current_tour[:i] + \
                        list(
                            reversed(current_tour[i:j+1])) + current_tour[j+1:]
                    best_tour_length = round(
                        current_tour_length + difference, 2)

                    print('Improved tour is:', best_tour, 'with length',
                          best_tour_length)

                    solution_improved = True

        current_tour, current_tour_length = best_tour, best_tour_length

    # Return the resulting tour and its length as a tuple
    return best_tour, best_tour_length


def twoExchange(distance_matrix, routes, r1_index, r2_index, demand, capacity=120):
    # Select the routes to be optimized
    r1 = routes[r1_index]
    r2 = routes[r2_index]

    # Initialize the best routes and best increase in distance to the original routes and 0
    best_routes = [r1, r2]
    best_increase = 0

    # Iterate over each pair of locations in r1 and r2
    for i in range(len(r1)):
        for j in range(len(r2)):
            # Create a copy of the routes
            new_routes = [r1.copy(), r2.copy()]
            # Replace the locations in the copy of the routes
            new_routes[0][i] = r2[j]
            new_routes[1][j] = r1[i]
            # Calculate the increase in distance
            increase = routeDistance(
                distance_matrix, new_routes[0]) + routeDistance(distance_matrix, new_routes[1])
            - routeDistance(distance_matrix, r1) - \
                routeDistance(distance_matrix, r2)
            # If the increase is smaller than the best increase and the routes are feasible, update the best routes and best increase
            if increase < best_increase:
                best_routes = new_routes
                best_increase = increase

    # Return the best routes
    return best_routes
