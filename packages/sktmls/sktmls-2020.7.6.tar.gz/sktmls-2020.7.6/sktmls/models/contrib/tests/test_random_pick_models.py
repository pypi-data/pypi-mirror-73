from sktmls.models.contrib import RandomPickModel


class TestRandomPickModel:
    def test_000_random_pick(self):
        rpm = RandomPickModel(
            model_name="test_model",
            model_version="test_version",
            candidates=[
                {"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}},
                {"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}},
            ],
        )

        assert rpm.predict(None) in [
            {"items": [{"id": "test_id1", "name": "test_name1", "type": "test_type", "props": {}}]},
            {"items": [{"id": "test_id2", "name": "test_name2", "type": "test_type", "props": {}}]},
        ]
