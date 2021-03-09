from . import session
from app.models.user import User
from app.schemas.user import UserSchema


class CRUD_USER:
    def __init__(self):
        pass


    def get_all(self):
        query = session.query(User).all()
        return query


    async def user_detail(user_id: int):
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return {"user_id": user.id, "user_name": user.name}
        return {"error": "There is no user with this ID"}


    async def user_update(user_id: int, user: UserSchema):
        query = session.query(User).filter(User.id == user_id).first()
        if user:
            for i in session.query(User).all():
                if i.name == user.name and i.id != user_id:
                    return {"error": "A user with this name has already been created"}
                if i.email == user.email and i.id != user_id:
                    return {"error": "A user with this email already been created"}

            query.name = user.name
            query.first_name = user.first_name
            query.last_name = user.last_name
            query.email = user.email
            query.password = user.password
            session.add(query)
            session.commit()
            return {"user_id": query.id, "user_name": query.name}

        return {"error": "There is no user with this ID"}


    async def user_delete(user_id: int):
        user = session.query(User).get(user_id)
        if user:
            session.delete(user)
            session.commit()
            return {"message": "user ({}) delete".format(user.name)}
        else:
            return {"error": "There is no user with this ID"}


