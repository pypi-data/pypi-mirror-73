import random
from typing import Any, Dict, List

from sktmls.models import MLSRuleModel


class RandomPickModel(MLSRuleModel):
    def __init__(self, model_name: str, model_version: str, candidates: List[Dict[str, Any]]):
        super().__init__(model_name, model_version, ["user_id"])
        self.candidates = candidates

    def predict(self, x: List[Any]) -> Dict[str, Any]:
        return {"items": [random.choice(self.candidates)]}
