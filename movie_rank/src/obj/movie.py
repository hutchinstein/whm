class Movie:
    def __init__(self, movie_id: int, cast: list[int], movie_name: str):
        self.movie_id = movie_id
        self.cast = cast
        self.movie_name = movie_name
        self.z_score = 1
        self.historical_z_scores = []
        self.movie_score = 0
        self.points_from_people = [[]]

    def get_movie_id(self) -> int:
        return self.movie_id

    def get_cast(self) -> list:
        return self.cast

    def get_movie_name(self) -> str:
        return self.movie_name

    def get_z_score(self) -> int:
        return self.z_score

    def get_movie_score(self) -> int:
        return self.movie_score

    def receive_points_from_person(self, points: int) -> None:
        self.points_from_people[-1].append(points)

    def update_movie_score(self) -> None:
        self.movie_score = sum(self.points_from_people[-1])

    def update_z_score(self, mean_movie_score: float,
                       std_movie_score: float) -> float:
        self.historical_z_scores.append(self.z_score)
        self.z_score = (self.movie_score - mean_movie_score)\
            / std_movie_score

    def start_new_round(self) -> None:
        self.historical_z_scores.append(self.get_z_score())

    def get_historical_z_scores(self) -> list:
        return self.historical_z_scores

    def needs_further_analysis(self) -> bool:
        if len(self.get_historical_z_scores()) < 2:
            return True
        if abs((self.get_historical_z_scores()[-1] -
                self.get_historical_z_scores()[-2])
                / self.get_historical_z_scores()[-2]) < 0.5:
            return False
        return True
