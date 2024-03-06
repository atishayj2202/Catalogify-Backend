import os

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


class ComputerVisionCli:
    env_var_api_key = "COMPUTER_VISION_API_KEY1"
    env_var_endpoint = "COMPUTER_VISION_ENDPOINT"

    def __init__(self):
        subscription_key = os.environ[self.env_var_api_key]
        endpoint = os.environ[self.env_var_endpoint]
        credentials = CognitiveServicesCredentials(subscription_key)
        self._client = ComputerVisionClient(endpoint, credentials)

    def analyze_image(self, ImageURL):
        description = self._client.describe_image(ImageURL)
        captions = description.captions
        for caption in captions:
            print(caption.text)


if __name__ == "__main__":
    tempfile = ComputerVisionCli()
    tempfile.analyze_image(
        "https://www.shutterstock.com/image-photo/tropical-paradise-beach-white-sand-260nw-1201599862.jpg"
    )
