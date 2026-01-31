import argparse
import requests
import json

LAMBDA_URL = "https://fmcitbvvlmnu7qhwfgeg22w3ue0mppsa.lambda-url.us-east-2.on.aws/"

def test_document_processor(args):
    # Define the payload
    payload = {
        "text": args.text,
        "query": args.query,
        "auth_key": args.auth_key
    }

    print("--- Sending request to Lambda ---")
    
    try:
        # Send the POST request
        response = requests.post(
            LAMBDA_URL, 
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        # Check for success
        if response.status_code == 200:
            result = response.json()
            print("Response from Claude Haiku:")
            raw_response = result.get("model_response", "No response field found.")
            print(json.dumps(json.loads(raw_response), indent=2))
        else:
            print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--auth_key", 
        required=True,
        default=None,
        help="Preset auth_key."
    )
    parser.add_argument(
        "--text",
        type=str,
        default="Barack Hussein Obama II[a] (born August 4, 1961) is an American politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African American president. Obama previously served as a U.S. senator representing Illinois from 2005 to 2008 and as an Illinois state senator from 1997 to 2004.\nBorn in Honolulu, Hawaii, Obama graduated from Columbia University in 1983 with a Bachelor of Arts degree in political science and later worked as a community organizer in Chicago. In 1988, Obama enrolled in Harvard Law School, where he was the first black president of the Harvard Law Review. He became a civil rights attorney and an academic, teaching constitutional law at the University of Chicago Law School from 1992 to 2004. In 1996, Obama was elected to represent the 13th district in the Illinois Senate, a position he held until 2004, when he successfully ran for the U.S. Senate. In the 2008 presidential election, after a close primary campaign against Hillary Clinton, he was nominated by the Democratic Party for president. Obama selected Joe Biden as his running mate and defeated Republican nominee John McCain and his running mate Sarah Palin.",
        help="Document text as a string"
    )
    parser.add_argument(
        "--query",
        type=str, 
        default="", 
        help="Specific user query to focus on specific aspects of the document."
    )

    args = parser.parse_args()
    test_document_processor(args)
