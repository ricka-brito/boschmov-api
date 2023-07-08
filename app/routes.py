import requests
import os
import mysql.connector
from app.infos import SECRET_KEY, DATABASE_URL

from app import SessionLocal, crud
from app.crud import get_bustops_by_adress
from models.models import Adress


def closestpoints(db : SessionLocal, initial: str):
    bustopsdistances = {}


    points = crud.get_adresses(db)

    for i in points:

        body = {
          "origins": [
              {
              "waypoint": {
                "address": initial
                          }
              }
          ],
      "destinations": [
          {
          "waypoint": {
            "address": f"{i.street} {i.houseNumber} {i.neighborhood} {i.city} SP {i.cep}"
                      }
          }
      ]
    }
        response = requests.post('https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix', json=body, headers={"X-Goog-Api-Key": "AIzaSyAFP6mWjy3pM5g0Lm4ZyHcQKEvRxAgPw0c", "X-Goog-FieldMask": "distanceMeters"})
        bustopsdistances[response.json()[0]["distanceMeters"]] = {"Adress": i, "distance": response.json()[0]["distanceMeters"]}

    return {
        "closest_route": {"distance" : bustopsdistances[min(bustopsdistances)]["distance"], "bustops": get_bustops_by_adress(db, bustopsdistances[min(bustopsdistances)]["Adress"])}
    }


