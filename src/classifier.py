# imports
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_article(headline, similar_headlines):
    developer_prompt = """
        You are a classifier. Your job is to take in the headline of a news article, and classify 
        it depending on the headline itself and other similar headlines reported in the past.

        The categories that you can classify our target headline into are:

        1) Breaking news, has not been reported before. Evaluate whether it has been reported before
        based on the past similar headlines.

        2) A contiuation of a previous headline, but with significant updates to deem it breaking news.

        3) A duplicate article. Meaning, it is reporting the same thing as one of the previous similar
        headlines. This can be breaking news or non-breaking news.

        4) Not breaking news. It has been not been reported before, but is not significant enough to
        deem is as breaking news.

        5) A contiuation of a previous headline, but with only minor updates, not significant enough
        to make the update breaking news.'

        Breaking News is a significant development or event that has a large impact on the world or
        the sentiment of people. Limit it to the most important developments and events of the day,
        there should only be a few breaking news a day unless something really significant happens
        that day. Tilt some bias towards the US, as I am US based.

        Output one number (integer), 1-5, that reflects the headline based on the 5 above categories.
    """

    similar_list = "\n".join([f"{i}. {h}" for i, h in enumerate(similar_headlines, 1)])

    user_prompt = f"""
        Target/Main Headline: 
        - {headline}

        Similar Headlines:
        {similar_list}
    """

    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "medium"},
        input=[
            {"role": "developer", "content": developer_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    classification = int(response.output_text.strip())
    return classification