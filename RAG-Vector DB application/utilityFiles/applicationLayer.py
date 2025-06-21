class ChatBot:
    def __init__(self,model,vector_store,prompt,memory_limit=10):
        self.conversation_history = [
            {"role": "system", "content": prompt}
        ]
        self.memory_limit = memory_limit
        self.vector_store = vector_store 
        self.openai=model
        self.prompt=prompt
    
    def format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def generate_response(self, text, context=None):
        # Manage memory by removing old messages if limit exceeded
        if len(self.conversation_history) > self.memory_limit * 2:  # *2 because each exchange has 2 messages
            # Keep only relevant recent messages and system message
            self.conversation_history = [
                self.conversation_history[0],  # Keep the base system message
                *self.conversation_history[-(self.memory_limit * 2 - 2):]  # Recent user-assistant messages
            ]

        docs=self.vector_store.similarity_search(text)
        context=self.format_docs(docs)

        # Create a dynamic system message with the provided context
        system_message = f"""{self.prompt}'{context if context else ''}"""

        # Update the system message in conversation history
        self.conversation_history[0]["content"] = system_message

        # Add user's new message
        self.conversation_history.append({"role": "user", "content": text})

        response = self.openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=self.conversation_history,
        )

        # Store assistant's response
        assistant_message = response.choices[0].message
        self.conversation_history.append({"role": "assistant", "content": assistant_message.content})

        return assistant_message.content

    def clear_history(self):
        self.conversation_history = [self.conversation_history[0]]  # Keep only the system message
    
    def get_history(self):
        return self.conversation_history[1:]  # Return history excluding system message
