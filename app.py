from fastapi import FastAPI, HTTPException 

from pydantic import BaseModel 

from math import radians, sin, cos, atan2, sqrt 

import numpy as np 

 

app = FastAPI(title="Turbulence Map MVP") 

 

AIRPORTS = { 

    "ARN": {"name": "Stockholm Arlanda", "lat": 59.6519, "lon": 17.9186}, 

    "MMX": {"name": "Malmö", "lat": 55.5363, "lon": 13.3762}, 

    "LPA": {"name": "Gran Canaria", "lat": 27.9319, "lon": -15.3866}, 

} 

 

class AnalyzeReq(BaseModel): 

    origin: str 

    destination: str 

    cruise_fl: int = 360 

    tas_knots: int = 450 

 

def haversine_km(lat1, lon1, lat2, lon2): 

    R = 6371.0 

    p1, p2 = radians(lat1), radians(lat2) 

    dphi = radians(lat2 - lat1) 

    dlambda = radians(lon2 - lon1) 

    a = sin(dphi/2)**2 + cos(p1)*cos(p2)*sin(dlambda/2)**2 

    return 2 * R * atan2(sqrt(a), sqrt(1 - a)) 

 

@app.post("/analyze") 

def analyze(req: AnalyzeReq): 

    orig = AIRPORTS.get(req.origin.upper()) 

    dest = AIRPORTS.get(req.destination.upper()) 

    if not orig or not dest: 

        raise HTTPException(status_code=404, detail="Okänd flygplatskod") 

 

    dist_km = haversine_km(orig["lat"], orig["lon"], dest["lat"], dest["lon"]) 

    eta_min = int(dist_km / ((req.tas_knots * 1.852) / 60)) 

 

    return { 

        "origin": req.origin.upper(), 

        "destination": req.destination.upper(), 

        "distance_km": round(dist_km, 1), 

        "eta_minutes": eta_min, 

        "risk": "medium" 

    } 