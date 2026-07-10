from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI(
    title="VORTEX FreeFire Info API",
    description="API اختصاصی VORTEX - دریافت مستقیم از Garena",
    version="3.0"
)

def fetch_from_garena(uid: str):
    url = f"https://ff.garena.com/profile/{uid}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # پیدا کردن اسم
        name_tag = soup.find('h1', class_='profile-name')
        if name_tag:
            nickname = name_tag.text.strip()
        else:
            # روش جایگزین برای پیدا کردن اسم
            name_tag = soup.find('div', class_='profile-name')
            nickname = name_tag.text.strip() if name_tag else "Unknown"
        
        # پیدا کردن سطح
        level_tag = soup.find('div', class_='profile-level')
        if level_tag:
            level_text = level_tag.text.strip().replace('Level', '').strip()
        else:
            level_text = "0"
        
        # پیدا کردن لایک
        likes_tag = soup.find('div', class_='profile-likes')
        if likes_tag:
            likes_text = likes_tag.text.strip().replace('Likes', '').strip()
        else:
            likes_text = "0"
        
        # پیدا کردن رنک
        rank_tag = soup.find('div', class_='profile-rank')
        rank = rank_tag.text.strip() if rank_tag else "Unknown"
        
        return {
            "uid": uid,
            "nickname": nickname,
            "level": level_text,
            "likes": likes_text,
            "rank": rank,
            "source": "Garena Official"
        }
    except Exception as e:
        return None

@app.get("/")
async def root():
    return {
        "api": "VORTEX FreeFire Info",
        "developer": "@XiT_VorteX",
        "channel": "@XiT_VorteX",
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
            "api": "VORTEX",
            "developer": "@XiT_VorteX",
            "data": data
        })
    else:
        return JSONResponse(content={
            "status": "error",
            "message": "امکان دریافت اطلاعات وجود ندارد",
            "developer": "@XiT_VorteX"
        }, status_code=404)
