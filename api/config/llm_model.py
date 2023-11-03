from secret import Secret
import google.generativeai as palm


class LLMModel:
    model = None

    @staticmethod
    def init(model_name: str = "palm"):
        LLMModel.model = LLMModel.get_palm_model()

    @staticmethod
    def get_palm_model():
        palm.configure(api_key=Secret.API_KEY)

        models = [
            m
            for m in palm.list_models()
            if "generateText" in m.supported_generation_methods
        ]
        print(f"${models=}")
        model = models[0].name

        return model
