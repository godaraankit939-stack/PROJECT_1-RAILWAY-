import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Tera MongoDB URL (RAUSHAN wala)
MONGO_URL = "mongodb+srv://cashoung_db_user:jaihobotki@cluster0.5j4kkiz.mongodb.net/RAUSHAN?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URL)
db = client.RAUSHAN
sessions_col = db.active_sessions  # Jahan login data hai
auth_users_col = db.authorized_users # Jahan authorized users save honge

async def authorize_new_logins():
    print("🚀 Ꭰᥲʀκ Auto-Auth System Live...")
    authorized_list = set()

    # Pehle se authorized users ko load karo
    async for user in auth_users_col.find():
        authorized_list.add(user['user_id'])

    while True:
        # Naye logins check karo
        async for session in sessions_col.find():
            user_id = session.get('user_id')
            
            if user_id and user_id not in authorized_list:
                print(f"✅ New User Detected: {user_id}. Authorizing for Bot Use...")
                
                # Database mein add karo taaki bot ise 'Normal User' pehchane
                await auth_users_col.update_one(
                    {"user_id": user_id},
                    {"$set": {"status": "authorized", "role": "user"}},
                    upsert=True
                )
                authorized_list.add(user_id)
                
        await asyncio.sleep(20) # Har 20 second mein check karega

if __name__ == "__main__":
    asyncio.run(authorize_new_logins())

