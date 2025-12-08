# from math import cos
# import litellm
# from litellm.integrations.custom_logger import CustomLogger
# from litellm import completion, acompletion

# class MyCustomHandler(CustomLogger):
#     # def log_pre_api_call(self, model, messages, kwargs): 
#     #     for key, Value in kwargs.items():
#     #         print(f"{key}: {Value}")

#     #     print(f"Pre-API Call")
    
#     # def log_post_api_call(self, kwargs, response_obj, start_time, end_time): 

#     #     print(f"Post-API Call\n\n")
#     #     for key, Value in kwargs.items():
#     #         print(f"{key}: {Value}")
    

#     def log_success_event(self, kwargs, response_obj, start_time, end_time): 
#         print(f"On Success")

#     def log_failure_event(self, kwargs, response_obj, start_time, end_time): 
#         print(f"On Failure")

#     def track_cost(kwargs, completion_response, start_time, end_time):
#         cost = kwargs["response_cost"]
#         print(cost)

    
#     #### ASYNC #### - for acompletion/aembeddings

#     async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
#         print(f"On Async Success")

#     async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
#         print(f"On Async Failure")

# customHandler = MyCustomHandler()

# litellm.callbacks = [customHandler]

# ## sync 
# # response = completion(model="gpt-3.5-turbo", messages=[{ "role": "user", "content": "Hi 👋 - i'm openai"}],
# #                               stream=True)
# # for chunk in response: 
# #     continue


# ## async
# import asyncio 

# async def completion():
#     response = await acompletion(model="gpt-3.5-turbo", messages=[{ "role": "user", "content": "Hi 👋 - i'm openai"}],
#                               stream=True)
#     async for chunk in response: 
#         print(chunk.ModelResponseStream.id)
#         continue
# asyncio.run(completion())


import litellm
from litellm import completion, acompletion
import asyncio
import time
from litellm.integrations.custom_logger import CustomLogger



class MyLogger(CustomLogger):
    """Use this when you need more control"""
    
    def log_pre_api_call(self, model, messages, kwargs):
        """Called BEFORE API request"""
        print(f"About to call: {model}")
        print(messages)
    
    def log_post_api_call(self, kwargs, response_obj, start_time, end_time):
        """Called AFTER API request (always)"""
        print(f"API call completed")
    
    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        """Called ONLY on success"""
        cost = kwargs.get("response_cost", 0)
        if kwargs["response_cost"]:
            print(kwargs["response_cost"])
        print(f"Success! Cost: ${cost}")

        if hasattr(response_obj, 'usage') and response_obj.usage:
            usage = response_obj.usage
            print(response_obj)
            print(f"Tokens: {usage.total_tokens} (Prompt: {usage.prompt_tokens})")

    
    def log_failure_event(self, kwargs, response_obj, start_time, end_time):
        """Called ONLY on failure"""
        error = kwargs.get("exception")
        print(f"Failed! Error: {error}")
    
    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        """Called on async success"""
        print("Async success!")
    
    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        """Called on async failure"""
        print("Async failure!")

# Register the class instance
my_logger = MyLogger()
litellm.callbacks = [my_logger]  # ← Register class instance

response = completion(model="gpt-3.5-turbo", messages=[{ "role": "user", "content": "Hi 👋 - Can you write a AI poem"}],
                          stream=False)

print("\n--- Response ---")
print(response.choices[0].message.content)