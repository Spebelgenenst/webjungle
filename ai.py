from google import genai

class ai():
    def __init__(self, key):
        self.client = genai.Client(api_key=key)

    def prompt(self, prompt, model):
        try:
            response = self.client.models.generate_content(
                model=model, contents=prompt
            )
        except Exception as error:
            return None, error
        
        return response.text, None

    def extract_code(self, response):
        start = response.find("```html")
        if start == -1:
            return None
        
        code = response[start+7:]
        code = code[:code.find("```")]

        return code
