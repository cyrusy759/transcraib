from groq import Groq

def make_flash_card(text, number, purpose):
    client = Groq(api_key="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")

    text = "testing testing testing testing testing"
    purpose = "english revision"
    number = "2"

    response = client.chat.completions.create(
    model="llama3-70b-8192", 
    messages=[
        {
            "role": "user",
            "content": f"create {number} flashcards for {purpose} based on {text} and return them as json with the topic as the title and the summary as the content"
            }
            ],
    temperature=0.5,
    )
    return response