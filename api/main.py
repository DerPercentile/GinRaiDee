# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Query
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

# ── Food Database ──
foods = {
    "morning": [
        {"name": "ข้าวต้มไก่", "emoji": "🍚", "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "180 กิโลแคลอรี่", "desc": "นุ่ม ย่อยง่าย เหมาะกับทุกคน", "tags": ["ย่อยง่าย", "โปรตีนสูง"], "avoid": ["โรคไต"], "p": 22, "c": 25, "f": 4, "good": ["ปวดท้อง", "อ่อนเพลีย"]},
        {"name": "ไข่ต้ม 2 ฟอง", "emoji": "🥚", "image": "https://images.unsplash.com/photo-1587486913049-53fc88980cfc?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "155 กิโลแคลอรี่", "desc": "โปรตีนสูง ไขมันต่ำ บำรุงกล้ามเนื้อ", "tags": ["โปรตีนสูง", "ไขมันต่ำ"], "avoid": [], "p": 13, "c": 1, "f": 10, "good": ["อ่อนเพลีย"]},
        {"name": "โจ๊กปลา", "emoji": "🥣", "image": "https://images.unsplash.com/photo-1594756202469-9ff9799b2e4e?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "165 กิโลแคลอรี่", "desc": "อ่อนนุ่ม เหมาะกับวันที่ไม่สบาย", "tags": ["ย่อยง่าย", "โซเดียมต่ำ"], "avoid": [], "p": 14, "c": 28, "f": 2, "good": ["ปวดท้อง", "กินได้น้อย", "ลำไส้แปรปรวน"]},
        {"name": "สมูทตี้ผักผลไม้", "emoji": "🥤", "image": "https://images.unsplash.com/photo-1553530979-7ee52a2670c4?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "140 กิโลแคลอรี่", "desc": "วิตามินสูง แอนตี้ออกซิแดนต์เต็มแก้ว", "tags": ["วิตามินสูง", "แอนตี้ออกซิแดนต์"], "avoid": ["โรคไต"], "p": 3, "c": 32, "f": 1, "good": []},
        {"name": "ขนมปังธัญพืช", "emoji": "🍞", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "200 กิโลแคลอรี่", "desc": "ใยอาหารสูง ช่วยระบบย่อยอาหาร", "tags": ["ใยอาหารสูง", "ธัญพืช"], "avoid": ["ภูมิแพ้กลูเตน"], "p": 8, "c": 38, "f": 3, "good": []},
        {"name": "ผลไม้รวม", "emoji": "🍇", "image": "https://images.unsplash.com/photo-1619546813926-a78fa6372cd2?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "85 กิโลแคลอรี่", "desc": "วิตามินซีสูง เสริมภูมิคุ้มกัน", "tags": ["วิตามินซี", "คาร์บสูง"], "avoid": ["เบาหวาน"], "p": 1, "c": 22, "f": 0, "good": ["อ่อนเพลีย"]},
    ],
    "noon": [
        {"name": "ปลาอบซีอิ๊ว", "emoji": "🐟", "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "230 กิโลแคลอรี่", "desc": "โปรตีนสูง ไขมันโอเมก้า-3", "tags": ["โอเมก้า-3", "โปรตีนสูง"], "avoid": [], "p": 32, "c": 5, "f": 9, "good": ["อ่อนเพลีย"]},
        {"name": "แกงจืดเต้าหู้", "emoji": "🫕", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "120 กิโลแคลอรี่", "desc": "โซเดียมต่ำ เหมาะผู้ป่วยความดัน", "tags": ["โซเดียมต่ำ", "แแคลเซียม"], "avoid": [], "p": 10, "c": 8, "f": 5, "good": ["ปวดหัว"]},
        {"name": "ข้าวกล้องผัดผัก", "emoji": "🍛", "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "320 กิโลแคลอรี่", "desc": "ใยอาหารสูง น้ำตาลดูดซึมช้า", "tags": ["GI ต่ำ", "ใยอาหารสูง"], "avoid": [], "p": 12, "c": 55, "f": 6, "good": []},
        {"name": "สลัดไก่ย่าง", "emoji": "🥗", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "260 กิโลแคลอรี่", "desc": "โปรตีนสูง คาร์บต่ำ เหมาะผู้ป่วยเบาหวาน", "tags": ["คาร์บต่ำ", "โปรตีนสูง"], "avoid": [], "p": 28, "c": 10, "f": 12, "good": ["กินได้น้อย"]},
        {"name": "ซุปถั่วเลนทิล", "emoji": "🍲", "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "180 กิโลแคลอรี่", "desc": "โปรตีนพืช ธาตุเหล็กสูง", "tags": ["โปรตีนพืช", "ธาตุเหล็ก"], "avoid": ["โรคไต"], "p": 14, "c": 28, "f": 3, "good": ["อ่อนเพลีย"]},
        {"name": "เต้าหู้ผัดน้ำมันหอย", "emoji": "🥢", "image": "https://images.unsplash.com/photo-1582450871972-ab5ca641643d?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "195 กิโลแคลอรี่", "desc": "แคลเซียมสูง โปรตีนครบถ้วน", "tags": ["แคลเซียม", "ไขมันต่ำ"], "avoid": [], "p": 16, "c": 12, "f": 9, "good": []},
    ],
    "evening": [
        {"name": "ไก่นึ่งสมุนไพร", "emoji": "🍗", "image": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "200 กิโลแคลอรี่", "desc": "ไขมันต่ำมาก โปรตีนสูง", "tags": ["ไขมันต่ำ", "โปรตีนสูง"], "avoid": [], "p": 35, "c": 3, "f": 5, "good": ["อ่อนเพลีย", "กินได้น้อย"]},
        {"name": "ต้มยำกุ้ง (น้ำใส)", "emoji": "🍤", "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "170 กิโลแคลอรี่", "desc": "แอนตี้อินแฟลมเมทอรี่จากสมุนไพร", "tags": ["ต้านการอักเสบ", "โปรตีนสูง"], "avoid": ["ความดันโลหิตสูง"], "p": 24, "c": 8, "f": 5, "good": []},
        {"name": "ผัดผักบุ้งน้ำมันหอย", "emoji": "🥬", "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "95 กิโลแคลอรี่", "desc": "วิตามินเอสูง ใยอาหารมาก", "tags": ["วิตามินเอ", "ใยอาหาร"], "avoid": [], "p": 5, "c": 10, "f": 4, "good": []},
        {"name": "ปลาซาบะย่าง", "emoji": "🐠", "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "250 กิโลแคลอรี่", "desc": "DHA และ EPA สูง ดีต่อหัวใจและสมอง", "tags": ["โอเมก้า-3", "สุขภาพหัวใจ"], "avoid": [], "p": 30, "c": 0, "f": 13, "good": ["ปวดหัว"]},
        {"name": "ข้าวกล้องกับแกงเลียง", "emoji": "🫙", "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "290 กิโลแคลอรี่", "desc": "ผักหลายชนิด แคลอรี่ไม่สูง", "tags": ["หลายชนิดผัก", "แคลอรี่ต่ำ"], "avoid": [], "p": 10, "c": 52, "f": 4, "good": []},
        {"name": "ซุปฟักทอง", "emoji": "🎃", "image": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "115 กิโลแคลอรี่", "desc": "เบตาแคโรทีนสูง เสริมภูมิคุ้มกัน", "tags": ["เบตาแคโรทีน", "ย่อยง่าย"], "avoid": [], "p": 4, "c": 22, "f": 2, "good": ["ปวดท้อง", "ลำไส้แปรปรวน"]},
    ],
    "snack": [
        {"name": "ผลไม้สด (ฝรั่ง, ชมพู่, มะละกอ)", "emoji": "🍈", "image": "https://images.unsplash.com/photo-1619546813926-a78fa6372cd2?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "60 - 80 กิโลแคลอรี่", "desc": "มีวิตามินสูง เหมาะกับเบาหวาน ไขมันสูง โรคหัวใจ (ระวังมะละกอในโรคไต)", "tags": ["วิตามินสูง", "ไขมันต่ำ"], "avoid": ["โรคไต"], "p": 1, "c": 18, "f": 0, "good": ["อ่อนเพลีย"]},
        {"name": "ขนมครก (1 คู่)", "emoji": "🥞", "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "100 - 150 กิโลแคลอรี่", "desc": "ทำจากแป้งข้าวเจ้าและกะทิ ปราศจากกลูเตนและนม", "tags": ["คาร์บสูง"], "avoid": ["เบาหวาน", "ไขมันสูง", "โรคหัวใจ"], "p": 1, "c": 18, "f": 5, "good": []},
        {"name": "ชานมไข่มุก (1 แก้ว)", "emoji": "🧋", "image": "https://images.unsplash.com/photo-1541658016709-82535e94bc69?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "350 - 500 กิโลแคลอรี่", "desc": "ชานมไข่มุกยอดนิยม น้ำตาลสูงมาก มีกะทิ/นมวัว", "tags": ["คาร์บสูง"], "avoid": ["เบาหวาน", "ไขมันสูง", "โรคหัวใจ", "แพ้นม"], "p": 2, "c": 80, "f": 11, "good": []},
        {"name": "ขนมปังปิ๊บ / คุกกี้", "emoji": "🍪", "image": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "150 - 200 กิโลแคลอรี่", "desc": "คุกกี้/ขนมปังอบกรอบ มีแป้งสาลีและนมผง", "tags": ["คาร์บสูง"], "avoid": ["ภูมิแพ้กลูเตน", "เบาหวาน", "ไขมันสูง", "แพ้นม"], "p": 3, "c": 26, "f": 7, "good": []},
        {"name": "กล้วยแขก / มันทอด", "emoji": "🍠", "image": "https://images.unsplash.com/photo-1566843972142-a7fcb70de55a?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "250 - 300 กิโลแคลอรี่", "desc": "กล้วยหรือมันชุบแป้งทอดกรอบ อมน้ำมันสูง", "tags": ["คาร์บสูง"], "avoid": ["ไขมันสูง", "โรคหัวใจ", "เบาหวาน"], "p": 2, "c": 40, "f": 12, "good": []},
        {"name": "เฉาก๊วยชากังราว / นมสด", "emoji": "🍧", "image": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "150 - 250 กิโลแคลอรี่", "desc": "เฉาก๊วยหวานเย็น ดับร้อน (ระวังนมสดและน้ำเชื่อม)", "tags": ["ย่อยง่าย"], "avoid": ["เบาหวาน", "แพ้นม"], "p": 1, "c": 40, "f": 4, "good": ["ปวดหัว"]},
        {"name": "ถั่วลิสงต้ม / อัลมอนด์", "emoji": "🥜", "image": "https://images.unsplash.com/photo-1508061253366-f7da158b6d4f?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "150 - 180 กิโลแคลอรี่", "desc": "มีไขมันดีสูง เหมาะกับเบาหวานและไขมันสูง (ระวังฟอสฟอรัสในโรคไต)", "tags": ["ไขมันดี", "โปรตีนสูง"], "avoid": ["โรคไต", "โรคหัวใจ"], "p": 7, "c": 6, "f": 14, "good": ["อ่อนเพลีย"]},
        {"name": "ซาลาเปาหมูสับ (1 ลูก)", "emoji": "🥟", "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "200 - 250 กิโลแคลอรี่", "desc": "ทำจากแป้งสาลี ไส้หมูสับมีโซเดียมและไขมันสูง", "tags": ["โปรตีนสูง"], "avoid": ["ภูมิแพ้กลูเตน", "ไขมันสูง", "โรคไต"], "p": 8, "c": 28, "f": 9, "good": ["กินได้น้อย"]},
        {"name": "ขนมไทยใส่น้ำกะทิ", "emoji": "🥣", "image": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "300 - 400 กิโลแคลอรี่", "desc": "บัวลอยหรือลอดช่องกะทิ แป้งและน้ำตาลสูงมาก", "tags": ["คาร์บสูง"], "avoid": ["เบาหวาน", "ไขมันสูง", "โรคหัวใจ"], "p": 3, "c": 55, "f": 13, "good": []},
        {"name": "โยเกิร์ตรสธรรมชาติ", "emoji": "🫙", "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=400&h=300&q=80", "kcal": "90 - 120 กิโลแคลอรี่", "desc": "แคลเซียมสูง ดีต่อเบาหวาน (รสธรรมชาติ) และไขมันสูง", "tags": ["โปรไบโอติก", "ไขมันต่ำ", "ย่อยง่าย"], "avoid": ["แพ้นม"], "p": 6, "c": 12, "f": 3, "good": ["ลำไส้แปรปรวน"]},
    ],
}


@app.get("/api/foods")
def get_foods(meal: Optional[str] = Query(None, description="Filter by meal type: morning, noon, evening, snack")):
    """Return the food database. Optionally filter by meal type."""
    if meal:
        if meal not in foods:
            return JSONResponse(
                status_code=404,
                content={"error": f"Meal '{meal}' not found. Valid options: morning, noon, evening, snack"}
            )
        return {meal: foods[meal]}
    return foods
