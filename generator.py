import os
import json
import requests
import random
import yaml
from dotenv import load_dotenv

class AnimalDB:
  def __init__(self, api_headers) -> None:
    url = 'https://parseapi.back4app.com/classes/Animalslist_Animal?limit=600'
    self.data = json.loads(requests.get(url, headers=api_headers).content.decode('utf-8'))

  def randomAnimal(self) -> str:
    animal_num = random.randrange(0,599)
    return(self.data['results'][animal_num]['objectId'])

class Animal:
  def __init__(self, api_headers, objectId) -> None:
    url = 'https://parseapi.back4app.com/classes/Animalslist_Animal/{}'.format(objectId)
    self.data = json.loads(requests.get(url, headers=api_headers).content.decode('utf-8'))

  def name(self) -> str:
    return self.data['name']

class Adjective:
  def __init__(self) -> None:
    with open("adjectives.yaml", "r") as stream:
      try:
          self.data = yaml.safe_load(stream)
      except yaml.YAMLError as exc:
          print(exc)

  def getByLetter(self,letter) -> str:
    adjective_list = set()
    for adjective in self.data['adjectives']:
      if adjective[0] == letter:
        adjective_list.add(adjective)
    random_num = random.randrange(0,len(adjective_list)-1)
    return list(adjective_list)[random_num]

class Main:
  load_dotenv() # Load env
  # define request headers
  backapp_id = os.getenv('BACKAPP_ID')
  backapp_api_key = os.getenv('BACKAPP_API_KEY')
  api_headers = {
      'X-Parse-Application-Id': backapp_id,
      'X-Parse-REST-API-Key': backapp_api_key
  }

  # get animal name
  animal_db = AnimalDB(api_headers)
  animal_object_id = animal_db.randomAnimal()
  animal = Animal(api_headers, animal_object_id)

  # get adjective
  adjective = Adjective().getByLetter(animal.name()[0])

  print("NFT Project Name: {} {}'s".format(adjective,animal.name()))

if __name__ == "__main__":
  Main()