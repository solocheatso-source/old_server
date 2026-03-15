#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Коллекция предметов из базы данных v2
Всего предметов: 227
"""

import json

# Полная коллекция предметов
ITEMS_DATA = [
  {
    "_id": "301",
    "Id": 301,
    "DisplayName": "Origin Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "302",
    "Id": 302,
    "DisplayName": "Furious Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "303",
    "Id": 303,
    "DisplayName": "Rival Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "304",
    "Id": 304,
    "DisplayName": "Fable Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "305",
    "Id": 305,
    "DisplayName": "Scorpion Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "306",
    "Id": 306,
    "DisplayName": "Empire Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "307",
    "Id": 307,
    "DisplayName": "Sharp Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "308",
    "Id": 308,
    "DisplayName": "Revenge Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "309",
    "Id": 309,
    "DisplayName": "Fun And Sun Weapon Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "310",
    "Id": 310,
    "DisplayName": "Fun And Sun Knife Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "311",
    "Id": 311,
    "DisplayName": "Chameleon Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "318",
    "Id": 318,
    "DisplayName": "Reforged Arcane Case",
    "Type": "case",
    "Rarity": "Arcane",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "5",
      "collection": "Reforged",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "319",
    "Id": 319,
    "DisplayName": "Reforged Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Reforged",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "321",
    "Id": 321,
    "DisplayName": "Nightmare Arcane Case",
    "Type": "case",
    "Rarity": "Arcane",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "5",
      "collection": "Nightmare",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "329",
    "Id": 329,
    "DisplayName": "Nightmare Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Nightmare",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "347",
    "Id": 347,
    "DisplayName": "Kitsune Dreams Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "KitsuneDreams",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "348",
    "Id": 348,
    "DisplayName": "Kitsune Dreams Arcane Case",
    "Type": "case",
    "Rarity": "Arcane",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "5",
      "collection": "KitsuneDreams",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "350",
    "Id": 350,
    "DisplayName": "Custom Case",
    "Type": "case",
    "Rarity": "Rare",
    "BuyPrice": {
      "102": 150
    },
    "SellPrice": {
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "401",
    "Id": 401,
    "DisplayName": "Origin Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "402",
    "Id": 402,
    "DisplayName": "Furious Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "403",
    "Id": 403,
    "DisplayName": "Rival Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "404",
    "Id": 404,
    "DisplayName": "Fable Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "405",
    "Id": 405,
    "DisplayName": "Scorpion Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "406",
    "Id": 406,
    "DisplayName": "Empire Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "407",
    "Id": 407,
    "DisplayName": "Sharp Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "408",
    "Id": 408,
    "DisplayName": "Revenge Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "411",
    "Id": 411,
    "DisplayName": "Chameleon Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "320",
    "Id": 320,
    "DisplayName": "Reforged Box",
    "Type": "box",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 2500
    },
    "SellPrice": {
      "101": 1250
    },
    "Properties": {
      "value": "2",
      "collection": "Reforged",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "15003",
    "Id": 15003,
    "DisplayName": "Deagle Predator",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "45002",
    "Id": 45002,
    "DisplayName": "AKR12 Pixel Camouflage",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "51002",
    "Id": 51002,
    "DisplayName": "AWM Phoenix",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "62002",
    "Id": 62002,
    "DisplayName": "SM1014 Pathfinder",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "13001",
    "Id": 13001,
    "DisplayName": "P350 Cyber",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "32001",
    "Id": 32001,
    "DisplayName": "UMP45 Cyberpunk",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "35002",
    "Id": 35002,
    "DisplayName": "P90 Ghoul",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "45001",
    "Id": 45001,
    "DisplayName": "AKR12 Railgun",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "46002",
    "Id": 46002,
    "DisplayName": "M4 Necromancer",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "47002",
    "Id": 47002,
    "DisplayName": "M16 Winged",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "11002",
    "Id": 11002,
    "DisplayName": "G22 Nest",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "44002",
    "Id": 44002,
    "DisplayName": "AKR Treasure Hunter",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "71002",
    "Id": 71002,
    "DisplayName": "M9 Bayonet Ancient",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "71003",
    "Id": 71003,
    "DisplayName": "M9 Bayonet Scratch",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "71004",
    "Id": 71004,
    "DisplayName": "M9 Bayonet Universe",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "71005",
    "Id": 71005,
    "DisplayName": "M9 Bayonet Dragon Glass",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Origin",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "15002",
    "Id": 15002,
    "DisplayName": "Deagle Blood",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "46006",
    "Id": 46006,
    "DisplayName": "M4 Pro",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "51004",
    "Id": 51004,
    "DisplayName": "AWM Scratch",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "32003",
    "Id": 32003,
    "DisplayName": "UMP45 Shark",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "48001",
    "Id": 48001,
    "DisplayName": "Famas Beagle",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "44004",
    "Id": 44004,
    "DisplayName": "AKR Sport",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "52001",
    "Id": 52001,
    "DisplayName": "M40 Quake",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "51003",
    "Id": 51003,
    "DisplayName": "AWM Gear",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "32004",
    "Id": 32004,
    "DisplayName": "UMP45 Winged",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "13003",
    "Id": 13003,
    "DisplayName": "P350 Forest Spirit",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "48002",
    "Id": 48002,
    "DisplayName": "Famas Fury",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "72002",
    "Id": 72002,
    "DisplayName": "Karambit Claw",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "72006",
    "Id": 72006,
    "DisplayName": "Karambit Scratch",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "72004",
    "Id": 72004,
    "DisplayName": "Karambit Ice Dragon",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "72007",
    "Id": 72007,
    "DisplayName": "Karambit Universe",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Furious",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "13004",
    "Id": 13004,
    "DisplayName": "P350 Rally",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "44006",
    "Id": 44006,
    "DisplayName": "AKR Carbon",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "48003",
    "Id": 48003,
    "DisplayName": "Famas Hull",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "52003",
    "Id": 52003,
    "DisplayName": "M40 Beagle",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "15006",
    "Id": 15006,
    "DisplayName": "Deagle Dragon Glass",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "34001",
    "Id": 34001,
    "DisplayName": "MP7 Offroad",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "46007",
    "Id": 46007,
    "DisplayName": "M4 Grand Prix",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "11008",
    "Id": 11008,
    "DisplayName": "G22 Frost Wyrm",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "34002",
    "Id": 34002,
    "DisplayName": "MP7 Arcade",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "44005",
    "Id": 44005,
    "DisplayName": "AKR Necromancer",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "32005",
    "Id": 32005,
    "DisplayName": "UMP45 Beast",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "51007",
    "Id": 51007,
    "DisplayName": "AWM Genesis",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "73002",
    "Id": 73002,
    "DisplayName": "jKommando Ancient",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "73003",
    "Id": 73003,
    "DisplayName": "jKommando Reaper",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "73004",
    "Id": 73004,
    "DisplayName": "jKommando Floral",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "73006",
    "Id": 73006,
    "DisplayName": "jKommando Luxury",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Rival",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "41102",
    "Id": 41102,
    "DisplayName": "G22 Starfall",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "41502",
    "Id": 41502,
    "DisplayName": "Deagle Ace",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "41703",
    "Id": 41703,
    "DisplayName": "FiveSeven Tactical",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "41212",
    "Id": 41212,
    "DisplayName": "USP Pisces",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "43202",
    "Id": 43202,
    "DisplayName": "UMP45 Cerberus",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "44903",
    "Id": 44903,
    "DisplayName": "FnFAL Tactical",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "41605",
    "Id": 41605,
    "DisplayName": "Tec9 Fable",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "43402",
    "Id": 43402,
    "DisplayName": "MP7 Lich",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "44601",
    "Id": 44601,
    "DisplayName": "M4 Lizard",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "41701",
    "Id": 41701,
    "DisplayName": "FiveSeven Venom",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "44603",
    "Id": 44603,
    "DisplayName": "M4 Samurai",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "47504",
    "Id": 47504,
    "DisplayName": "Butterfly Red",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "47502",
    "Id": 47502,
    "DisplayName": "Butterfly Gold",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "47503",
    "Id": 47503,
    "DisplayName": "Butterfly Dragon Glass",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "47505",
    "Id": 47505,
    "DisplayName": "Butterfly Starfall",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Fable",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "81107",
    "Id": 81107,
    "DisplayName": "G22 Carbon",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "83411",
    "Id": 83411,
    "DisplayName": "MP7 Banana",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "84403",
    "Id": 84403,
    "DisplayName": "AKR Nano",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "86216",
    "Id": 86216,
    "DisplayName": "SM1014 Wave",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "84500",
    "Id": 84500,
    "DisplayName": "AKR12 Carbon",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "44902",
    "Id": 44902,
    "DisplayName": "FnFAL Parrot",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "81726",
    "Id": 81726,
    "DisplayName": "FiveSeven Wraith",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "83410",
    "Id": 83410,
    "DisplayName": "MP7 Graffity",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "46009",
    "Id": 46009,
    "DisplayName": "M4 Night Wolf",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "85127",
    "Id": 85127,
    "DisplayName": "AWM Dragon",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "71306",
    "Id": 71306,
    "DisplayName": "P350 Samurai",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "84402",
    "Id": 84402,
    "DisplayName": "AKR Dragon",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "87919",
    "Id": 87919,
    "DisplayName": "Scorpion Veil",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "87920",
    "Id": 87920,
    "DisplayName": "Scorpion Sea Eye",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "87921",
    "Id": 87921,
    "DisplayName": "Scorpion Scratch",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "87922",
    "Id": 87922,
    "DisplayName": "Scorpion Starfall",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Scorpion",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "81300",
    "Id": 81300,
    "DisplayName": "P350 Oni",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "121600",
    "Id": 121600,
    "DisplayName": "Tec9 Tropic",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "124300",
    "Id": 124300,
    "DisplayName": "M4A1 Kitsune",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "84600",
    "Id": 84600,
    "DisplayName": "M4 Demon",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "83512",
    "Id": 83512,
    "DisplayName": "MP7 Palace",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "84800",
    "Id": 84800,
    "DisplayName": "FAMAS Anger",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "165200",
    "Id": 165200,
    "DisplayName": "M60 Steam Beast",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "121200",
    "Id": 121200,
    "DisplayName": "USP Chameleon",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "15001",
    "Id": 15001,
    "DisplayName": "Desert Eagle Orochi",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "165100",
    "Id": 165100,
    "DisplayName": "M60 Grunge",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "124301",
    "Id": 124301,
    "DisplayName": "M4A1 Bubblegum",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "1125100",
    "Id": 1125100,
    "DisplayName": "AWM BOOM",
    "Type": "weapon",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Empire",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3004",
    "Id": 3004,
    "DisplayName": "Gloves Living Flame",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3007",
    "Id": 3007,
    "DisplayName": "Gloves Punk",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3008",
    "Id": 3008,
    "DisplayName": "Gloves Champion",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3009",
    "Id": 3009,
    "DisplayName": "Gloves Steam Rider",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170010",
    "Id": 170010,
    "DisplayName": "M16 Needle",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170011",
    "Id": 170011,
    "DisplayName": "M40 Grip",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170019",
    "Id": 170019,
    "DisplayName": "TEC9 Needle",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170020",
    "Id": 170020,
    "DisplayName": "USP Purple Camo",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170002",
    "Id": 170002,
    "DisplayName": "AKR12 Stream Beast",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170003",
    "Id": 170003,
    "DisplayName": "Desert Eagle Pirahna",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "210007",
    "Id": 210007,
    "DisplayName": "M4A1 Sour",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170008",
    "Id": 170008,
    "DisplayName": "G22 Casual",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170017",
    "Id": 170017,
    "DisplayName": "P90 Oops",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170018",
    "Id": 170018,
    "DisplayName": "P350 Tag King",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170001",
    "Id": 170001,
    "DisplayName": "AKR Tag King",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "154800",
    "Id": 154800,
    "DisplayName": "FnFAL BOOM",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170021",
    "Id": 170021,
    "DisplayName": "Dual Daggers Acid",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170022",
    "Id": 170022,
    "DisplayName": "Dual Daggers Demonic Steel",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170023",
    "Id": 170023,
    "DisplayName": "Dual Daggers Grunge",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "170024",
    "Id": 170024,
    "DisplayName": "Dual Daggers Molten",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Sharp",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220003",
    "Id": 220003,
    "DisplayName": "M40 Impale",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220004",
    "Id": 220004,
    "DisplayName": "M110 Tech Shard",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220006",
    "Id": 220006,
    "DisplayName": "FnFal Red Hot",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220007",
    "Id": 220007,
    "DisplayName": "P350 Rhino",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220008",
    "Id": 220008,
    "DisplayName": "M4 Powergame",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220009",
    "Id": 220009,
    "DisplayName": "USP Ignite",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220010",
    "Id": 220010,
    "DisplayName": "MP7 Precision",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "250001",
    "Id": 250001,
    "DisplayName": "MAC10 Noxious",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220011",
    "Id": 220011,
    "DisplayName": "AKR Evolution",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220012",
    "Id": 220012,
    "DisplayName": "AWM Kings",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220013",
    "Id": 220013,
    "DisplayName": "Tec9 Tie Dye",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220014",
    "Id": 220014,
    "DisplayName": "MAC10 Shogun Stripes",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220021",
    "Id": 220021,
    "DisplayName": "Knife Stilet Soul Devourer",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220022",
    "Id": 220022,
    "DisplayName": "Knife Stilet Viper",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220023",
    "Id": 220023,
    "DisplayName": "Knife Stilet Tie Dye",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "220024",
    "Id": 220024,
    "DisplayName": "Knife Stilet Damascus",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Revenge",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "121100",
    "Id": 121100,
    "DisplayName": "G22 Scale",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "126201",
    "Id": 126201,
    "DisplayName": "SM1014 Tropic",
    "Type": "weapon",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "121300",
    "Id": 121300,
    "DisplayName": "P350 Oni",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "123200",
    "Id": 123200,
    "DisplayName": "UMP45 Peaceful Dream",
    "Type": "weapon",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "121500",
    "Id": 121500,
    "DisplayName": "Deagle Orochi",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "123400",
    "Id": 123400,
    "DisplayName": "MP7 Empire",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "124600",
    "Id": 124600,
    "DisplayName": "M4 Demon",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "125200",
    "Id": 125200,
    "DisplayName": "M40 Cursed Fire",
    "Type": "weapon",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "157100",
    "Id": 157100,
    "DisplayName": "M9 Bayonet Kumo",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "157200",
    "Id": 157200,
    "DisplayName": "Karambit Year Of The Tiger",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "157500",
    "Id": 157500,
    "DisplayName": "Butterfly Kumo",
    "Type": "knife",
    "Rarity": "Arcane",
    "BuyPrice": {
      "101": 50000,
      "102": 5000
    },
    "SellPrice": {
      "101": 25000,
      "102": 2500
    },
    "Properties": {
      "value": "5",
      "collection": "Chameleon",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "501",
    "Id": 501,
    "DisplayName": "Gift New Year 2019",
    "Type": "gift",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "601",
    "Id": 601,
    "DisplayName": "Two Years Event Gold Pass",
    "Type": "pass",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "1100",
    "Id": 1100,
    "DisplayName": "Fashist",
    "Type": "special",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "1101",
    "Id": 1101,
    "DisplayName": "Gold Skull",
    "Type": "special",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3000",
    "Id": 3000,
    "DisplayName": "Gloves Phoenix",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3001",
    "Id": 3001,
    "DisplayName": "Gloves Autumn",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3002",
    "Id": 3002,
    "DisplayName": "Gloves Geometric",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3003",
    "Id": 3003,
    "DisplayName": "Gloves RetroWave",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3005",
    "Id": 3005,
    "DisplayName": "Gloves Neutro",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3006",
    "Id": 3006,
    "DisplayName": "Gloves Burning Fists",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3010",
    "Id": 3010,
    "DisplayName": "Gloves Year Of The Tiger",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3011",
    "Id": 3011,
    "DisplayName": "Gloves Acid",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3012",
    "Id": 3012,
    "DisplayName": "Gloves Thug",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3013",
    "Id": 3013,
    "DisplayName": "Gloves Fossil",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3014",
    "Id": 3014,
    "DisplayName": "Gloves Handcraft",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3015",
    "Id": 3015,
    "DisplayName": "Gloves Raider",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3016",
    "Id": 3016,
    "DisplayName": "Gloves Camo",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3030",
    "Id": 3030,
    "DisplayName": "Gloves Stream",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3031",
    "Id": 3031,
    "DisplayName": "Gloves Artificer",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3032",
    "Id": 3032,
    "DisplayName": "Gloves Dragon Glass",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3033",
    "Id": 3033,
    "DisplayName": "Gloves Mimicry",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3034",
    "Id": 3034,
    "DisplayName": "Gloves Rebellion",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3035",
    "Id": 3035,
    "DisplayName": "Gloves Utility",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3036",
    "Id": 3036,
    "DisplayName": "Gloves Ironclad",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3037",
    "Id": 3037,
    "DisplayName": "Gloves Spectral",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3038",
    "Id": 3038,
    "DisplayName": "Gloves Gangster",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3039",
    "Id": 3039,
    "DisplayName": "Gloves Polymer",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3040",
    "Id": 3040,
    "DisplayName": "Gloves Acid Veil",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3041",
    "Id": 3041,
    "DisplayName": "Gloves Flux",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3042",
    "Id": 3042,
    "DisplayName": "Gloves Haunt",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3043",
    "Id": 3043,
    "DisplayName": "Gloves Immolation",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3044",
    "Id": 3044,
    "DisplayName": "Gloves Plague",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3045",
    "Id": 3045,
    "DisplayName": "Gloves Shatter",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "3046",
    "Id": 3046,
    "DisplayName": "Gloves Hanami",
    "Type": "gloves",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "7001",
    "Id": 7001,
    "DisplayName": "Avatar Frame Tier Bronze 1",
    "Type": "avatar_frame",
    "Rarity": "Common",
    "BuyPrice": {
      "101": 100,
      "102": 10
    },
    "SellPrice": {
      "101": 50,
      "102": 5
    },
    "Properties": {
      "value": "0",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "100",
    "Id": 100,
    "DisplayName": "Medal Assistance Bronze",
    "Type": "medal",
    "Rarity": "Common",
    "BuyPrice": {
      "101": 100,
      "102": 10
    },
    "SellPrice": {
      "101": 50,
      "102": 5
    },
    "Properties": {
      "value": "0",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "101",
    "Id": 101,
    "DisplayName": "Medal Assistance Silver",
    "Type": "medal",
    "Rarity": "Uncommon",
    "BuyPrice": {
      "101": 500,
      "102": 50
    },
    "SellPrice": {
      "101": 250,
      "102": 25
    },
    "Properties": {
      "value": "1",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "102",
    "Id": 102,
    "DisplayName": "Medal Assistance Gold",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "103",
    "Id": 103,
    "DisplayName": "Medal Assistance Platinum",
    "Type": "medal",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "104",
    "Id": 104,
    "DisplayName": "Medal Assistance Brilliant",
    "Type": "medal",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "105",
    "Id": 105,
    "DisplayName": "Medal Veteran 2018 Bronze",
    "Type": "medal",
    "Rarity": "Common",
    "BuyPrice": {
      "101": 100,
      "102": 10
    },
    "SellPrice": {
      "101": 50,
      "102": 5
    },
    "Properties": {
      "value": "0",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "106",
    "Id": 106,
    "DisplayName": "Medal Veteran 2018 Silver",
    "Type": "medal",
    "Rarity": "Uncommon",
    "BuyPrice": {
      "101": 500,
      "102": 50
    },
    "SellPrice": {
      "101": 250,
      "102": 25
    },
    "Properties": {
      "value": "1",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "107",
    "Id": 107,
    "DisplayName": "Medal Veteran 2018 Gold",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "108",
    "Id": 108,
    "DisplayName": "Medal Veteran 2018 Platinum",
    "Type": "medal",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "109",
    "Id": 109,
    "DisplayName": "Medal Veteran 2019 Bronze",
    "Type": "medal",
    "Rarity": "Common",
    "BuyPrice": {
      "101": 100,
      "102": 10
    },
    "SellPrice": {
      "101": 50,
      "102": 5
    },
    "Properties": {
      "value": "0",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "110",
    "Id": 110,
    "DisplayName": "Medal Veteran 2019 Silver",
    "Type": "medal",
    "Rarity": "Uncommon",
    "BuyPrice": {
      "101": 500,
      "102": 50
    },
    "SellPrice": {
      "101": 250,
      "102": 25
    },
    "Properties": {
      "value": "1",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "111",
    "Id": 111,
    "DisplayName": "Medal Veteran 2019 Gold",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "112",
    "Id": 112,
    "DisplayName": "Medal Veteran 2019 Platinum",
    "Type": "medal",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "113",
    "Id": 113,
    "DisplayName": "Medal 2 Years Silver",
    "Type": "medal",
    "Rarity": "Uncommon",
    "BuyPrice": {
      "101": 500,
      "102": 50
    },
    "SellPrice": {
      "101": 250,
      "102": 25
    },
    "Properties": {
      "value": "1",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "114",
    "Id": 114,
    "DisplayName": "Medal 2 Years Gold",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "115",
    "Id": 115,
    "DisplayName": "Medal NC Bronze",
    "Type": "medal",
    "Rarity": "Common",
    "BuyPrice": {
      "101": 100,
      "102": 10
    },
    "SellPrice": {
      "101": 50,
      "102": 5
    },
    "Properties": {
      "value": "0",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "116",
    "Id": 116,
    "DisplayName": "Medal NC Silver",
    "Type": "medal",
    "Rarity": "Uncommon",
    "BuyPrice": {
      "101": 500,
      "102": 50
    },
    "SellPrice": {
      "101": 250,
      "102": 25
    },
    "Properties": {
      "value": "1",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "117",
    "Id": 117,
    "DisplayName": "Medal NC Gold",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "118",
    "Id": 118,
    "DisplayName": "Medal NC Platinum",
    "Type": "medal",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "119",
    "Id": 119,
    "DisplayName": "Medal NC Brilliant",
    "Type": "medal",
    "Rarity": "Legendary",
    "BuyPrice": {
      "101": 15000,
      "102": 1500
    },
    "SellPrice": {
      "101": 7500,
      "102": 750
    },
    "Properties": {
      "value": "4",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "160",
    "Id": 160,
    "DisplayName": "Medal NY 2023 NC",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "194",
    "Id": 194,
    "DisplayName": "Medal New 2B",
    "Type": "medal",
    "Rarity": "Common",
    "BuyPrice": {
      "101": 100,
      "102": 10
    },
    "SellPrice": {
      "101": 50,
      "102": 5
    },
    "Properties": {
      "value": "0",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "195",
    "Id": 195,
    "DisplayName": "Medal New 2S",
    "Type": "medal",
    "Rarity": "Uncommon",
    "BuyPrice": {
      "101": 500,
      "102": 50
    },
    "SellPrice": {
      "101": 250,
      "102": 25
    },
    "Properties": {
      "value": "1",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "196",
    "Id": 196,
    "DisplayName": "Medal New 2G",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "197",
    "Id": 197,
    "DisplayName": "Medal New 2P",
    "Type": "medal",
    "Rarity": "Epic",
    "BuyPrice": {
      "101": 5000,
      "102": 500
    },
    "SellPrice": {
      "101": 2500,
      "102": 250
    },
    "Properties": {
      "value": "3",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "198",
    "Id": 198,
    "DisplayName": "Medal New 2",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  },
  {
    "_id": "199",
    "Id": 199,
    "DisplayName": "Medal New 1",
    "Type": "medal",
    "Rarity": "Rare",
    "BuyPrice": {
      "101": 1500,
      "102": 150
    },
    "SellPrice": {
      "101": 750,
      "102": 75
    },
    "Properties": {
      "value": "2",
      "collection": "None",
      "craftable": "false"
    },
    "Tradable": True,
    "Marketable": True
  }
]

# Преобразуем в JSON строку для отправки клиенту
FULL_ITEM_DEFINITIONS = json.dumps(ITEMS_DATA, ensure_ascii=False)

def get_item_by_id(item_id: int):
    """Получить предмет по ID"""
    for item in ITEMS_DATA:
        if item.get("Id") == item_id:
            return item
    return None

def get_items_by_type(item_type: str):
    """Получить все предметы определенного типа"""
    return [item for item in ITEMS_DATA if item.get("Type") == item_type]

def get_cases_and_boxes():
    """Получить все кейсы и коробки"""
    return [item for item in ITEMS_DATA if item.get("Type") in ["case", "box"]]

def get_weapon_skins():
    """Получить все скины оружия"""
    return [item for item in ITEMS_DATA if item.get("Type") == "weapon"]

if __name__ == "__main__":
    print(f"Загружено {len(ITEMS_DATA)} предметов")
    print(f"Предмет 301: {get_item_by_id(301)}")
