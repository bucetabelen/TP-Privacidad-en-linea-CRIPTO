import random
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Cookie Tracker API",
)

# Configura la middleware de CORS para permitir solicitudes desde http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://localhost:8082"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

car_ads = [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSszaJ1DcpEbAi_LVi0IpwIF2lHNsP-PQFX7mdprRZ0zaDXQP4ug6vFxq-GBy8LieHQvfA&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYtHOqyrCEaGttLg00eWnOz-gfMn7EGMirw2enFl9CkBCZb37K3FmPE7Ra7gxiYmkp4LQ&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0QK9VsvA5_ZoF-cZA7z4Y5p8i-oU4SGx3fw&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTiaLTHguHGVrgZOq7fMGDEnyEDlFr1x72m93fi7B9qEpk1TFpYFv8P820iIOBpSKM31o&usqp=CAU",

]
cat_ads = [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTewDK7gZnXaIup2LdpsPGh4QVF2P-X9PVwnScD0BLL9xBL5cRAxw1fkfQy_8qFbqYLDqM&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5G9UnH-o4ZkRPwv2LEFv8fUp1fFTumgqisnfFGtQLUZTj-fc4NaArxHyH5K1gB7UJ6tc&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjufWbjtU2vq3jTBMyY2ZdYqTEQGrnue19UyZIV5reqjTKuvMLzTwrnLoyW6xIIQbTxy4&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSq4700miM07HzEBq_RHtw8hQfxvNmjKpf6LA&usqp=CAU",
]


@app.get("/")
async def root():
    return {"message": "Hello from Cookie Tracker API"}

tracked_users = {}


@app.get("/ad", response_class=HTMLResponse)
async def ad(request: Request, url: str):
    cookie = request.cookies.get("tracking-cookie")
    print("Visitor from: ", url)
    if not cookie:
        print("No cookie found, generating new user id")
        user_id = len(tracked_users) + 1
        tracked_users[user_id] = [url]
    else:
        print("Cookie received: ", cookie, "from url: ", url)
        print("Cookie found. user id : ", cookie)
        user_id = int(cookie)
        if user_id not in tracked_users:
            tracked_users[user_id] = []
        tracked_users[user_id].append(url)
        print("User has visited: ", tracked_users[user_id])
    ad = generate_ad(user_id)
    response = HTMLResponse(content=ad, status_code=200)
    if not cookie:
        response.set_cookie(key="tracking-cookie", value=str(user_id))
    return response


@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    cookie = request.cookies.get("tracking-cookie")
    content = "<h1>Te estamos observando...</h1>"
    if cookie and int(cookie) in tracked_users:
        user_id = int(cookie)
        print("Cookie found. user id : ", user_id)

        if user_id in tracked_users:
            content += "<h2>Este es tu historial de navegación:</h2>"
            content += "<ul>"
            for site in tracked_users[user_id]:
                content += "<li>" + site + "</li>"
            content += "</ul>"
    response = HTMLResponse(content, status_code=200)
    return response


def generate_ad(user_id):
    ad = "<h1>Este es un buen espacio para una publicidad...</h1> <h2>Si tan solo supieramos algo más de tus gustos... >:c</h2>"
    if user_id in tracked_users:
        counters = {
            "car": 0,
            "cat": 0
        }
        for site in tracked_users[user_id][-6:]:
            if "autosRapidosPuntoCom" in site:
                counters["car"] += 1
            elif "gatitosAdorablesPuntoCom" in site:
                counters["cat"] += 1

        if counters["car"] >= counters["cat"] and counters["car"] > 2:
            ad = "<img width=100% height=100% src='" + random.choice(car_ads) + "'/>"
        elif counters["cat"] > counters["car"] and counters["cat"] > 2:
            ad = "<img width=100% height=100% src='" + random.choice(cat_ads) + "'/>"
    return ad
