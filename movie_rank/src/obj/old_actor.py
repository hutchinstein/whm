class Person:
    def __init__(self, person_id: int, person_name: str):
        self.person_id = person_id
        self.person_name = person_name
        self.person_scores = [[]]
        self.person_score = 0
        print("New person")

    def get_person_id(self) -> int:
        return self.person_id

    def get_person_name(self) -> str:
        return self.person_name

    def get_person_scores(self) -> list:
        return self.person_scores

    def get_person_score(self) -> int:
        return self.person_score

    def add_point_to_person_scores(self, score) -> None:
        self.person_scores[-1].append(score)

    def start_new_round(self) -> None:
        self.person_scores.append([])

    def calculate_person_score(self) -> int:
        self.person_score = sum(self.get_person_scores()[-1])
