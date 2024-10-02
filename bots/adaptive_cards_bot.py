import aiohttp  # To make async API calls
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from botbuilder.schema import Attachment
from botbuilder.core import MessageFactory
class AdaptiveCardsBot(ActivityHandler):
    """
    This bot will respond to the user's input, pass it to an external API via POST request,
    and return the API response in a table format using an Adaptive Card.
    """

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Welcome to the bot! Type anything to start.")

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text.strip()

        # Fetch response from external API based on the user's input question
        api_response = await self._ask_question_api(user_message)

        # Create an adaptive card to display the response as a table
        adaptive_card = self.create_table_card(api_response)

        # Send the adaptive card back to the user
        await turn_context.send_activity(
            MessageFactory.attachment(Attachment(content_type="application/vnd.microsoft.card.adaptive", content=adaptive_card))
        )

    async def _ask_question_api(self, question: str) -> dict:
        """
        Send the user's question to the external API via POST request and return the response.
        :param question: The user's question from the bot conversation.
        :return: The response from the external API in JSON format.
        """
        api_url = "https://19cc-202-166-170-107.ngrok-free.app/ask_question"
        payload = {"question": question}  # JSON payload to be sent to the API

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()  # Assuming the API returns JSON
                        return data  # Return the JSON response as a dictionary
                    else:
                        return {"error": f"API call failed with status: {response.status}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    def create_table_card(self, api_response: dict) -> dict:
        """
        Create an Adaptive Card that displays the API response (movie titles and revenue) in a table format.
        :param api_response: The response from the API (JSON data).
        :return: The Adaptive Card as a dictionary.
        """
        # Check if there's an error in the API response
        if "error" in api_response:
            return {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": api_response["error"],
                        "weight": "Bolder",
                        "color": "Attention"
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.2"
            }

        # Assuming the API response contains a list of movie titles and revenues
        movies = api_response.get("output", [])
        # Dynamically determine the keys available in the movies array (for dynamic columns)
        keys = set()
        for movie in movies:
            keys.update(movie.keys())  # Collect all unique keys

        # Create a dynamic table header based on the available keys
        header = {
            "type": "ColumnSet",
            "columns": [
                {"type": "Column", "items": [
                    {"type": "TextBlock",
                      "text": "No.", 
                      "weight": "Normal"
                      }
                    ], "width": "auto"
                },  # Number column
                *[
                    {"type": "Column",
                      "items": [
                        {
                            "type": "TextBlock", 
                            "text": key.capitalize(), 
                            "weight": "Normal",
                            "wrap": True
                            }
                        ], "width": "1"}
                    for key in keys
                ]
            ],
            "width": "auto",
            "spacing": "0",  # Add spacing
            "separator": True  # Add a separator line
        }

        # Create table rows dynamically by mapping over the movie list

        rows = [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column", 
                        "items": [
                            {"type": "TextBlock", "text": str(index + 1)}
                        ], 
                        "width": "auto"
                    },  # Row number
                    *[
                        {
                            "type": "Column", 
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": str(movie.get(key, ""))
                                }
                            ], 
                            # Conditional styling based on even/odd row count
                            "style": "light" if (index + 1) % 2 == 0 else "light",
                            "width": "1"
                        }
                        for key in keys  # Create columns for each key dynamically
                    ]
                ],
                "spacing": "0",  # Add spacing
                "separator": True,  # Add a separator line
                "showGridLines": True
            }
            for index, movie in enumerate(movies)
        ]


        # Combine the header and rows into the Adaptive Card body
        card_body = [header] + rows

        return {
            "type": "AdaptiveCard",
            "body": card_body,
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.2"
        }

    
    def __init__(self):
        pass
