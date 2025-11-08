from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from nest_py.common import controller, get, post, put, delete, module, injectable
from nest_py.core import NestPyApplicationContext
from fastapi_adapter import FastAPIAdapter


# =========================
# MODELOS
# =========================
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class User(UserBase):
    id: int


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    role: str
    salary: float = Field(..., ge=0)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    role: Optional[str] = None
    salary: Optional[float] = Field(None, ge=0)


class Employee(EmployeeBase):
    id: int


# =========================
# SERVICIOS
# =========================

@injectable()
class UserService:

    def __init__(self):
        # “base de datos” en memoria
        self.users = {
            1: {"username": "alice", "email": "alice@example.com"},
            2: {"username": "bob", "email": "bob@example.com"},
            3: {"username": "charlie", "email": "charlie@example.com"},
        }

    def list_users(self, search: Optional[str] = None):
        result = [User(id=k, **v) for k, v in self.users.items()]
        if search:
            result = [u for u in result if search.lower() in u.username.lower()]
        return result

    def get_user(self, id: int):
        if id not in self.users:
            return None
        return User(id=id, **self.users[id])

    def create_user(self, user: UserCreate):
        if any(u["email"] == user.email for u in self.users.values()):
            raise ValueError("Email already exists")
        new_id = max(self.users.keys(), default=0) + 1
        self.users[new_id] = user.model_dump()
        return User(id=new_id, **self.users[new_id])

    def update_user(self, id: int, user: UserUpdate):
        if id not in self.users:
            raise KeyError("User not found")
        stored = self.users[id]
        update_data = user.dict(exclude_unset=True)
        if "email" in update_data and any(
            u["email"] == update_data["email"] for uid, u in self.users.items() if uid != id
        ):
            raise ValueError("Email already in use")
        stored.update(update_data)
        self.users[id] = stored
        return User(id=id, **stored)

    def delete_user(self, id: int):
        if id not in self.users:
            raise KeyError("User not found")
        del self.users[id]


@injectable()
class EmployeeService:
    def __init__(self):
        self.employees = {
            101: {"name": "John Doe", "role": "Manager", "salary": 55000},
            102: {"name": "Jane Smith", "role": "Developer", "salary": 48000},
            103: {"name": "Mark Lee", "role": "Designer", "salary": 45000},
        }

    def list_employees(self, min_salary: Optional[float] = None):
        result = [Employee(id=k, **v) for k, v in self.employees.items()]
        if min_salary is not None:
            result = [e for e in result if e.salary >= min_salary]
        return result

    def get_employee(self, id: int):
        if id not in self.employees:
            return None
        return Employee(id=id, **self.employees[id])

    def create_employee(self, employee: EmployeeCreate):
        new_id = max(self.employees.keys(), default=100) + 1
        self.employees[new_id] = employee.dict()
        return Employee(id=new_id, **self.employees[new_id])

    def update_employee(self, id: int, employee: EmployeeUpdate):
        if id not in self.employees:
            raise KeyError("Employee not found")
        stored = self.employees[id]
        update_data = employee.dict(exclude_unset=True)
        stored.update(update_data)
        self.employees[id] = stored
        return Employee(id=id, **stored)

    def delete_employee(self, id: int):
        if id not in self.employees:
            raise KeyError("Employee not found")
        del self.employees[id]


# =========================
# CONTROLADORES
# =========================

@controller("/users")
class UserController:
    
    def __init__(self, service: UserService):
        self.service = service

    @get("/")
    async def get_users(self, search: Optional[str] = None):
        return self.service.list_users(search)

    @get("/{id}")
    async def get_user(self, id: int):
        user = self.service.get_user(id)
        if not user:
            return {"error": "User not found"}, 404
        return user

    @post("/")
    async def create_user(self, user: UserCreate):
        try:
            return self.service.create_user(user)
        except ValueError as e:
            return {"error": str(e)}, 400

    @put("/{id}")
    async def update_user(self, id: int, user: UserUpdate):
        try:
            return self.service.update_user(id, user)
        except KeyError:
            return {"error": "User not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400

    @delete("/{id}")
    async def delete_user(self, id: int):
        try:
            self.service.delete_user(id)
            return {"message": "User deleted successfully"}
        except KeyError:
            return {"error": "User not found"}, 404


@controller("/employees")
class EmployeeController:
    
    def __init__(self, service: EmployeeService):
        self.service = service

    @get("/")
    async def get_employees(self, min_salary: Optional[float] = None):
        return self.service.list_employees(min_salary)

    @get("/{id}")
    async def get_employee(self, id: int):
        emp = self.service.get_employee(id)
        if not emp:
            return {"error": "Employee not found"}, 404
        return emp

    @post("/")
    async def create_employee(self, employee: EmployeeCreate):
        return self.service.create_employee(employee)

    @put("/{id}")
    async def update_employee(self, id: int, employee: EmployeeUpdate):
        try:
            return self.service.update_employee(id, employee)
        except KeyError:
            return {"error": "Employee not found"}, 404

    @delete("/{id}")
    async def delete_employee(self, id: int):
        try:
            self.service.delete_employee(id)
            return {"message": "Employee deleted successfully"}
        except KeyError:
            return {"error": "Employee not found"}, 404


@module(
    controllers=[
        "UserController",
        "EmployeeController"
    ],
    providers=[
        "UserService",
        "EmployeeService"
    ],
)
class AppModule:
    pass


nest = NestPyApplicationContext()

app = FastAPIAdapter()
app.conf.set_debug(False)
app.conf.set_description("NestPy Core App")
app.conf.set_title("NestPy")
app.conf.set_version("1.0")
app.conf.set_contact({
    "name": "Brandon Jared Molina Vázquez",
    "email": "jaredbrandon970@gmail.com"
})


for name, params in nest.get_controllers().items():
    app.comp.add_router_group(name, prefix=params.get("params").get("args")[0])

    for k in params.get("routes"):
        app.comp.add_route_in_router_group(
            name,
            endpoint=k.get("handler"),
            tags=[name],
            path=k.get("metadata").get("args")[0],
            **k.get("metadata").get("kwargs")
        )


app.lif.start_server("127.0.0.1", 5000)
