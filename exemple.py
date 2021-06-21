from dataclasses import dataclass

@dataclass
class Personne:
    prenom: str
    nom: str
    age: int

jl = Personne("Jean-Loup", "BAGREL", 15)

print(jl)
# Personne(prenom='Jean-Loup', nom='BAGREL', age=15)

def dire_bonjour(personne):
    texte = (
        "Bonjour " +
        personne.prenom +
        " " +
        personne.nom +
        ", tu as " +
        str(personne.age) +
        " ans !"
    )
    print(texte)

dire_bonjour(jl)
# Bonjour Jean-Loup BAGREL, tu as 15 ans !