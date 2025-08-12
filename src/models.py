from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_planets_table = Table(
    "favorite_planets_table",
    db.Model.metadata,
    Column("left_id", ForeignKey("user.id")),
    Column("right_id", ForeignKey("planet.id")),
)

favorite_vehicles_table = Table(
    "favorite_vehicles_table",
    db.Model.metadata,
    Column("left_id", ForeignKey("user.id")),
    Column("right_id", ForeignKey("vehicle.id")),
)

favorite_characters_table = Table(
    "favorite_characters_table",
    db.Model.metadata,
    Column("left_id", ForeignKey("user.id")),
    Column("right_id", ForeignKey("character.id")),
)

favorite_weapons_table = Table(
    "favorite_weapons_table",
    db.Model.metadata,
    Column("left_id", ForeignKey("user.id")),
    Column("right_id", ForeignKey("weapon.id")),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorites_planets: Mapped[list["Planet"]] = relationship(
        "Planet",
        secondary=favorite_planets_table,
        back_populates="planet_favorite_by"
    )

    favorites_vehicles: Mapped[list["Vehicle"]] = relationship(
        "Vehicle",
        secondary=favorite_vehicles_table,
        back_populates="vehicle_favorite_by"
    )

    favorites_characters: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=favorite_characters_table,
        back_populates="character_favorite_by"
    )

    favorites_weapons: Mapped[list["Weapon"]] = relationship(
        "Weapon",
        secondary=favorite_weapons_table,
        back_populates="weapon_favorite_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "favorites_planets": [
                    favorite_planet.serialize() for 
                    favorite_planet in 
                    self.favorites_planets
                ],
            "favorites_vehicles": [
                    favorite_vehicle.serialize() for 
                    favorite_vehicle in 
                    self.favorites_vehicles
                ],
            "favorites_characters": [
                    favorite_character.serialize() for 
                    favorite_character in 
                    self.favorites_characters
                ],
            "favorites_weapons": [
                    favorite_weapon.serialize() for 
                    favorite_weapon in 
                    self.favorites_weapons
                ],
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))

    planet_favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_planets_table,
        back_populates="favorites_planets"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
        }
    
class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))

    vehicle_favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_vehicles_table,
        back_populates="favorites_vehicles"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
        }
    
class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))
    quote: Mapped[str] = mapped_column(String(255))

    character_favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_characters_table,
        back_populates="favorites_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
            "quote": self.quote,
        }
    
class Weapon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    image_url: Mapped[str] = mapped_column(String(255))
    weapon_type: Mapped[str] = mapped_column(String(60))

    weapon_favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_weapons_table,
        back_populates="favorites_weapons"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url,
            "weapon_type": self.weapon_type,
        }