from fastapi import FastAPI, Body, Depends
from model import PostSchema, UserSchema, UserLoginSchema
from app.views.auth.auth_handler import signJWT
from app.views.auth.auth_bearer import JWTBearer

app = FastAPI()



@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    query = User(name=user.name, first_name=user.first_name, last_name=user.last_name,
                 email=user.email, password=user.password)
    for i in session.query(User).all():
        if i.name == user.name:
            return {"error": "A user with this name has already been created"}
        if i.email == user.email:
            return {"error": "A user with this email has already been created"}

    session.add(query)
    session.commit()

    return signJWT(user.email)


def check_user(data: UserLoginSchema):
    for user in session.query(User).all():
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }


@app.get("/users/", tags=["user"])
async def user_list():
    query = session.query(User).all()
    return query


@app.get("/users/{user_id}", tags=["user"])
async def user_detail(user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        return {"user_id": user.id, "user_name": user.name}
    return {"error": "There is no user with this ID"}


@app.put("/users/{user_id}", tags=["user"])
async def user_update(user_id: int, user: UserSchema):
    query = session.query(User).filter(User.id == user_id).first()
    if user:
        query.name = user.name
        query.first_name = user.first_name
        query.last_name = user.last_name
        query.email = user.email
        query.password = user.password

        session.add(query)
        session.commit()
        return {"user_id": query.id, "user_name": query.name, "status": "success"}

    return {"error": "There is no user with this ID"}


@app.delete("/users/{user_id}", tags=["user"])
async def user_delete(user_id: int):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        return {"message": "user ({}) delete".format(user.name)}
    else:
        return {"error": "There is no user with this ID"}


@app.get("/", tags = ["root"])
async def read_root() -> dict:
    return {"message": "Hello"}


@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    query = session.query(User).all()
    print(query)
    return query


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id>len(posts):
        return {
            "Error": "No such post"
        }
    for post in posts:
        if post["id"] == id:
            return {"data": post}


@app.post("/posts", tags=["posts"], dependencies=[Depends(JWTBearer())])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post_added"
    }

