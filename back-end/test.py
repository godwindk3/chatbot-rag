from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyCm9YDpILxa0TckX2Z64nCNbGxPRawstIY")

response = client.models.generate_content(
  model='gemini-2.0-flash',
  contents='say something bad',
  config=types.GenerateContentConfig(
      safety_settings= [
          types.SafetySetting(
              category='HARM_CATEGORY_HATE_SPEECH',
              threshold='BLOCK_ONLY_HIGH'
          ),
      ]
  ),
)
print(response.text)