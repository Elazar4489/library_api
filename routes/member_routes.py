from fastapi import FastAPI, APIRouter, HTTPException
from database.member_db import MemberDB, EmailError
import main
import logging
logger = logging.getLogger()
memberdb = MemberDB()
router = APIRouter(prefix= "/members", tags=["members"])
@router.post("")
def create_member(name: str, email: str):
    logger.info("POST /members called")
    try:
        logger.info("Attempting to create a new member")
        member_details=memberdb.create_member({"name": name, "email": email})
        logger.info("New member added successfully")
        return member_details
    except EmailError:
        logger.error("the email is already exists in the table.")
        raise HTTPException(status_code = 400, detail= "your email is already exists in the table.")

@router.get("")
def get_all_members():
    logger.info("GET /members called")
    logger.info("The request 'get all members' was successfully received")
    return memberdb.get_all_members()

@router.get("/{member_id}")
def get_member_by_id(member_id):
    logger.info("GET /members/{id} called")
    member = memberdb.get_member_by_id(member_id)
    logger.info(f"Attempting a 'get member by id', id: {member_id} request")
    if not member:
        logger.error(f"member {member_id} not exists")
        raise HTTPException(status_code=404, detail=f"member {member_id} not exists.")
    logger.info(f"The request 'get member by id', id: {member_id} was successfully received")
    return member

@router.put("/{member_id}")
def update_member(member_id, name, email):
    logger.info("PUT /members called")
    try:
        logger.info(f"Attempting a 'update member', id: {member_id} request")
        member_updated = memberdb.update_member(member_id, {"name": name, "email": email})
        logger.info(f"The request 'update member', id: {member_id} was successfully received")
        return member_updated
    except EmailError:
        logger.error("the email is already exists in the table.")
        raise HTTPException(status_code=400, detail="your email is already exists in the table.")
    except main.IDNotFound:
        logger.error(f"member {member_id} not exists.")
        raise HTTPException(status_code= 404, detail= f"member {member_id} not exists.")

@router.put("/{member_id}/deactivate")
def deactivate_member(member_id):
    logger.info("PUT /members/{id}/deactivate called")
    try:
        logger.info(f"Attempting a 'deactivate member', id: {member_id} request")
        member_updated = memberdb.deactivate_member(member_id)
        logger.info(f"The request 'deactivate member', id: {member_id} was successfully received")
        return member_updated
    except main.IDNotFound:
        logger.error(f"member {member_id} not exists.")
        raise HTTPException(status_code= 404, detail= f"member {member_id} not exists.")

@router.put("/{member_id}/activate")
def activate_member(member_id):
    logger.info("PUT /members/{id}/activate called")
    try:
        logger.info(f"Attempting a 'activate member', id: {member_id} request")
        member_updated = memberdb.activate_member(member_id)
        logger.info(f"The request 'activate member', id: {member_id} was successfully received")
        return member_updated
    except main.IDNotFound:
        logger.error(f"member {member_id} not exists.")
        raise HTTPException(status_code= 404, detail= f"member {member_id} not exists.")