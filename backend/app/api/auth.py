from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    """用户登录"""
    return {"message": "登录成功", "data": {"token": "xxx"}}

@router.post("/register")
async def register():
    """用户注册"""
    return {"message": "注册成功"}

@router.get("/me")
async def get_current_user():
    """获取当前用户信息"""
    return {"message": "获取用户信息", "data": {"id": 1, "username": "admin"}}