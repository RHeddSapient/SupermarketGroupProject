
def prod_coords(dimensions, obstacles):

    store_map = [[0]*dimensions[1] for _ in range(dimensions[0])]

    products = []
    for obstacle in obstacles:
        store_map[obstacle[1]][obstacle[0]] = 1

    for obstacle in obstacles:
        
        if store_map[obstacle[1]+1][obstacle[0]+1] != 1:
            store_map[obstacle[1]+1][obstacle[0]+1] = 2
            products.append([obstacle[1]+1,obstacle[0]+1])

        if store_map[obstacle[1]+1][obstacle[0]] != 1:
            store_map[obstacle[1]+1][obstacle[0]] = 2
            products.append([obstacle[1]+1,obstacle[0]])

        if store_map[obstacle[1]+1][obstacle[0]-1] != 1:
            store_map[obstacle[1]+1][obstacle[0]-1] = 2
            products.append([obstacle[1]+1,obstacle[0]-1])

        if store_map[obstacle[1]][obstacle[0]+1] != 1:
            store_map[obstacle[1]][obstacle[0]+1] = 2
            products.append([obstacle[1],obstacle[0]+1])

        if store_map[obstacle[1]][obstacle[0]-1] != 1:
            store_map[obstacle[1]][obstacle[0]-1] = 2
            products.append([obstacle[1],obstacle[0]-1])

        if store_map[obstacle[1]-1][obstacle[0]+1] != 1:
            store_map[obstacle[1]-1][obstacle[0]+1] = 2
            products.append([obstacle[1]-1,obstacle[0]+1])

        if store_map[obstacle[1]-1][obstacle[0]] != 1:
            store_map[obstacle[1]-1][obstacle[0]] = 2
            products.append([obstacle[1]-1,obstacle[0]])

        if store_map[obstacle[1]-1][obstacle[0]-1] != 1:
            store_map[obstacle[1]-1][obstacle[0]-1] = 2
            products.append([obstacle[1]-1,obstacle[0]-1])
            

    return products

