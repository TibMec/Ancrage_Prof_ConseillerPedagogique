from pydantic import BaseModel, Field, field_validator
import re
from datetime import datetime
from typing import List

class Prof(BaseModel):
    nom: str = Field(...)
    prenom: str = Field(...)
    courriel: str = Field(...)
    ecoles: List[str] = Field(...)
    codesMatieres: List[str] = Field(...)
    password: str = Field(...)
    dateCreation: datetime = Field(default_factory=datetime.now)

    @field_validator("*", mode="before")
    def validate_not_empty(cls, v, info):
        field_name = info.field_name
        if isinstance(v, str):
            if not v or v.strip() == "":
                raise ValueError(f"{field_name} ne peut pas être vide")
        elif isinstance(v, list):
            if not v:
                raise ValueError(f"{field_name} ne peut pas être vide")
        return v

    @field_validator("courriel")
    def validate_email(cls, v):
        if not re.match(r".+\@.+\..+", v):
            raise ValueError("Email invalide")
        return v

    @field_validator("codesMatieres", mode="before")
    def validate_code_matiere(cls, v, info):
        field_name = info.field_name
        if isinstance(v, list):
            for item in v:
                if not re.match(r"^\d{3}-\d{3}$", item):
                    raise ValueError(f"{field_name} doit être au format XXX-XXX")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,}$", v):
            raise ValueError("Mot de passe doit contenir majuscule, minuscule, chiffre, caractère spécial et faire au moins 8 caractères")
        return v

    def __str__(self):
        return f'''{self.prenom} {self.nom.upper()},
                {self.courriel}
                {self.ecoles}
                {self.codesMatieres}
                '''

class CP(BaseModel):
    nom: str = Field(...)
    prenom: str = Field(...)
    courriel: str = Field(...)
    tel: str = Field(...)
    codesMatieres: List[str] = Field(...)
    password: str = Field(...)
    dateCreation: datetime = Field(default_factory=datetime.now)

    @field_validator("*", mode="before")
    def validate_not_empty(cls, v, info):
        field_name = info.field_name
        if isinstance(v, str):
            if not v or v.strip() == "":
                raise ValueError(f"{field_name} ne peut pas être vide")
        elif isinstance(v, list):
            if not v:
                raise ValueError(f"{field_name} ne peut pas être vide")
        return v

    @field_validator("courriel")
    def validate_email(cls, v):
        if not re.match(r".+\@.+\..+", v):
            raise ValueError("Email invalide")
        return v

    @field_validator("codesMatieres", mode="before")
    def validate_code_matiere(cls, v, info):
        field_name = info.field_name
        if isinstance(v, list):
            for item in v:
                if not re.match(r"^\d{3}-\d{3}$", item):
                    raise ValueError(f"{field_name} doit être au format XXX-XXX")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,}$", v):
            raise ValueError(
                "Mot de passe doit contenir majuscule, minuscule, chiffre, caractère spécial et faire au moins 8 caractères")
        return v

    def __str__(self):
        return f'''{self.prenom} {self.nom.upper()},
                {self.courriel}
                {self.tel}
                {self.codesMatieres}
                '''