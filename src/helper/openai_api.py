from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Conversation:
    
    def __init__(self, api_key=None,
 conversation_id="default" ):
        self.conversation_id = conversation_id
        self.history = [
            {"role": "system", "content":
                "Reply fast and short. Remember previous message."}
        ]
        
    def  prompt_response( self, prompt ):
        self.history.append({"role": "user","content": prompt})
        
        if len(self.history) > 10:
            self.history = self.history[-10:]
        
        response = client.chat.completions.create(
              model="gpt-4o-mini",
              messages=self.history,
              max_tokens=150
          )
        reply = response.choices[0].message.content
        self.history.append({"role": "assistant","content" : reply})
        return reply
                
                    
 