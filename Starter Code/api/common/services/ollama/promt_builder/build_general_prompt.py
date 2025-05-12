
def general_prompt(prompt,conversations):
    conversation_history = "\n".join([f"{'User' if 'user' in msg else 'AI'}: {msg.get('user', msg.get('ai'))}" for msg in conversations])

    return f""" 
    
            You are a professional plant expert AI assistant, if the user ask irrelevant questions 
            not pertaining to Plants please repond a respectfull message that you are only limited to Plants. Examine the
            previous conversation if not empty for you to have a meaningful and related response 
            Answer the user prompt: "{prompt}"
            
            Previous Conversation:

            {conversations}

        """


def general_prompt_json(prompt, conversations):

    conversation_history = "\n".join(
        [f"{'User' if 'user' in msg else 'AI'}: {msg.get('user', msg.get('ai'))}" for msg in conversations])

    return f"""
      Previous Conversation:
      {conversations}
      You are a professional plant expert AI assistant. A user asked: "{prompt}"

      Follow this respones format:

      INTRODUCTION: (give the user brief introduction about the the user prompt )

      SUMMARY: (provide the brief summary about the context (Note don't give the context jus a overall summary))

      """