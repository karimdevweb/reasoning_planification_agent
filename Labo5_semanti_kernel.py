class SKPlanner:
    def create_plan(self, goal: str):
        if goal:
            steps = [
                "Rechercher des informations sur la cybersécurité",
                "Synthétiser les points clés",
                "Vérifier l’exactitude des informations",
                "Rédiger le rapport final",
            ]
            # ajouter la numérotation
            return [f"{i+1}- {step}" for i, step in enumerate(steps)]

# Utilisation
planner = SKPlanner()
plan = planner.create_plan("Créer un rapport sur la cybersécurité")

for step in plan:
    print(step)