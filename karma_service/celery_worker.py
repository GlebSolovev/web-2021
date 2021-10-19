from time import sleep
from typing import List, Dict

import numpy as np

from karma_service.celery_app import celery_app


@celery_app.task(acks_late=True)
def calculate_stat(candidates: List[int], probabilities: np.array, user_id: int) -> Dict[str, float]:
    probabilities = probabilities.tolist()
    user_index = None
    for candidate_id in candidates:
        if candidate_id == user_id:
            user_index = candidate_id
            break
    user_probability = probabilities[user_index]
    sleep(5)

    sorted_results = sorted(zip(candidates, probabilities), key=lambda elem: elem[1], reverse=True)
    place = None
    for i in range(len(sorted_results)):
        if sorted_results[i][0] == user_id:
            place = i
            break
    place_percentage = place / len(candidates) * 100

    return {"probability_to_win": user_probability, "percentage_among_users": place_percentage}
