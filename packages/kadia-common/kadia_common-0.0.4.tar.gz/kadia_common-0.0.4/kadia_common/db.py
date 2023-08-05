import pymongo
from .types import *

class SkillNotFound(Exception):
    def __init__(self, skill_id):
        self.skill_id = skill_id

    def __str__(self):
        return f"Skill {self.skill_id} not found"

class MongoDB:
    def __init__(self, url: str):
        self.client = pymongo.MongoClient(url)
        self.kadia_db = self.client.kadia_db
        self.users = self.kadia_db.users
        self.history = self.kadia_db.history
        self.skills = self.kadia_db.skills
        self.instances = self.kadia_db.instances

    def fetch_telegram_user(self, telegram_id: int):
        user = self.users.find_one({"telegram_id": telegram_id})
        if user is None:
            user = User(telegram_id=token)
            user._id = self.users.insert_one(user.as_dict()).inserted_id
        else:
            user = User(**user)
        return user

    def add_replic_to_history(self, replic: Replic):
        self.history.insert_one(replic)

    def change_user_waiting_status(self, user: User, status: bool):
        self.users.update_one({'_id': user._id}, {
            '$set': {
                'state.is_waiting': status
            }
        })

    def fetch_skill(self, skill_id):
        skill = self.skills.find_one({'_id': skill_id})
        if skill is None:
            raise SkillNotFound(skill_id)
        return Skill(**skill)

    def update_instance(instance: SkillInstance, local_state: str, global_state: str):
        self.instances.update_one({'_id': instance._id}, {'$set': {'local_state': local_state,
                                                                   'global_state': global_state}})
