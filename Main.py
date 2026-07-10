from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI(
    title="VORTEX FreeFire Info API",
    description="API اختصاصی VORTEX",
    version="3.0"
)

def fetch_from_garena(uid: str):
    url = f"https://ff.garena.com/profile/?uid={uid}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        name = soup.find('div', class_='profile-name')
        nickname = name.text.strip() if name else "Unknown"
        
        level = soup.find('span', class_='level-num')
        level_text = level.text.strip() if level else "0"
        
        likes = soup.find('span', class_='like-num')
        likes_text = likes.text.strip() if likes else "0"
        
        return {
            "uid": uid,
            "nickname": nickname,
            "level": level_text,
            "likes": likes_text,
            "status": "success"
        }
    except:
        return None

@app.get("/")
async def root():
    return {
        "api": "VORTEX FreeFire Info",
        "developer": "@XiT_VorteX",
        "status": "online"
    }

@app.get("/info")
async def get_info(uid: str = Query(..., description="آیدی عددی بازیکن")):
    if not uid.isdigit():
        raise HTTPException(status_code=400, detail="فرمت آیدی اشتباه است")
    
    data = fetch_from_garena(uid)
    
    if data:
        return JSONResponse(content={
            "status": "success",
            "data": data,
            "developer": "@XiT_VorteX"
        })
    else:
        return JSONResponse(content={
            "status": "error",
            "message": "امکان دریافت اطلاعات وجود ندارد"
        }, status_code=404)
