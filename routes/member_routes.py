from fastapi import FastAPI, APIRouter, HTTPException
from database.member_db import MemberDB

memberdb = MemberDB()
router = APIRouter()
@router.post("/members")
def create_member(name: str, email: str):
    try:
        member_details=memberdb.create_member({"name": name, "email": email})
        return member_details
    except KeyError:
        raise HTTPException(status_code = 400, detail= "you entered key error in data.")

@router.get("/members")
def get_all_members():
    return memberdb.get_all_members()

@router.get("/members/{id}")
def get_member_by_id(member_id):
    member = memberdb.get_member_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="member not exists.")
    return member

@router.put("/members/{id}")
def update_member(member_id, name, email):
    try:
        member_updated = memberdb.update_member(member_id, {"name": name, "email": email})
        return member_updated
    except KeyError:
        raise HTTPException(status_code = 400, detail= "you entered key error in data.")
    except NameError:
        raise HTTPException(status_code= 404, detail= "member not exists.")

@router.put("/members/{id}/deactivate")
def deactivate_member(member_id):
    try:
        member_updated = memberdb.deactivate_member(member_id)
        return member_updated
    except NameError:
        raise HTTPException(status_code= 404, detail= "member not exists.")

@router.put("/members/{id}/activate")
def activate_member(member_id):
    try:
        member_updated = memberdb.activate_member(member_id)
        return member_updated
    except NameError:
        raise HTTPException(status_code= 404, detail= "member not exists.")