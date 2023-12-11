from config import redis_connect

# async def list_of_drivers():

# async def list_of_passengers():

# async def list_of_request_book():

# async def cancel_ride():

# async def request_ride():

# async def accept_ride():

# async def cancel_ride():


# async def update_profile():

async def register(id, data):
    user_key = f"user:{id}"
    name = data['name']
    phone = data['contact_info']
    role = data['role']
    redis_connect.hset(user_key, mapping= {
        'id': id,
        "name": name,
        "phone": phone,
        "role": role,
        "status": "not available"
        })
    
# async def getUsersWithActiveStatus():

def update_profile(user_id, data):
        user_key = f"user:{user_id}"
        redis_connect.hset(user_key, "name", data['name'])
        redis_connect.hset(user_key, "role", data['role'])

def get_user_by_id(user_id):
       user_key = f"user:{user_id}"
       user = redis_connect.hgetall(user_key)


       return user 


async def get_all_drivers():
    drivers = []
    all_keys = redis_connect.keys("user:*")
    
    for key in all_keys:
        user_data = redis_connect.hgetall(key)
        if user_data.get("role") == "driver":
            drivers.append(int(user_data["id"]))

    return drivers

