import os
from groq import Groq
import base64

from dotenv import load_dotenv

load_dotenv()


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

list_invoice = [ 'invoice_1.jpg', 'invoice_2.png', 'invoice_3.jpg']

for invoice in list_invoice:
# Path to your image
    image_path = invoice

    print( 'Invoice analysis: ', invoice )

    # Getting the base64 string
    base64_image = encode_image(image_path)

    client = Groq()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": " Que combustível foi consumido e quantos litros?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )

    print(chat_completion.choices[0].message.content)

    print( "===================================")
    print()

    
