# Task 3: Generative AI Integration

# Setup

## Step 1: Setting up AWS permissions in IAM console

1. In the **AWS Management Console**, create a new **Role** for the use case *Lambda*
2. Add policies
    - AWSLambdaBasicExecutionRole: Allows for logging controls
    - Custom policy to enable the use of `bedrock:InvokeModel` in the Lambda function

## Step 2: Set up (Python) Lambda function

1. Configure the Lambda function to assume the newly created role
2. Modify the function logic to read user input and invoke an AWS Bedrock model on it
    - Currently, I've set it up to use `us.anthropic.claude-3-haiku-20240307-v1:0`
    - Expects a `text` field and an optional user `query`
3. Configure a higher wait time for the Lambda function
    - Default wait time is too short for testing LLM inference

# Implemented Functionality

The API endpoint ingests a request containing:
- `auth_key`: for simple authentication
- `text`: unstructured text document
- `query`: (Optional) query

The endpoint returns a dictionary containing:
- `statusCode`: Anything besides 200 is an error
- `message_response`: A JSON string containing the structured response

# Sample Tests

## Test 1

```json
{
  "text": "Barack Hussein Obama II[a] (born August 4, 1961) is an American politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African American president. Obama previously served as a U.S. senator representing Illinois from 2005 to 2008 and as an Illinois state senator from 1997 to 2004.\nBorn in Honolulu, Hawaii, Obama graduated from Columbia University in 1983 with a Bachelor of Arts degree in political science and later worked as a community organizer in Chicago. In 1988, Obama enrolled in Harvard Law School, where he was the first black president of the Harvard Law Review. He became a civil rights attorney and an academic, teaching constitutional law at the University of Chicago Law School from 1992 to 2004. In 1996, Obama was elected to represent the 13th district in the Illinois Senate, a position he held until 2004, when he successfully ran for the U.S. Senate. In the 2008 presidential election, after a close primary campaign against Hillary Clinton, he was nominated by the Democratic Party for president. Obama selected Joe Biden as his running mate and defeated Republican nominee John McCain and his running mate Sarah Palin.",
  "query": "",
  "auth_key": "<ADD-AUTH-KEY-HERE>"
}
```

## Test 2

```json
{
  "text": "Barack Hussein Obama II[a] (born August 4, 1961) is an American politician who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, he was the first African American president. Obama previously served as a U.S. senator representing Illinois from 2005 to 2008 and as an Illinois state senator from 1997 to 2004.\nBorn in Honolulu, Hawaii, Obama graduated from Columbia University in 1983 with a Bachelor of Arts degree in political science and later worked as a community organizer in Chicago. In 1988, Obama enrolled in Harvard Law School, where he was the first black president of the Harvard Law Review. He became a civil rights attorney and an academic, teaching constitutional law at the University of Chicago Law School from 1992 to 2004. In 1996, Obama was elected to represent the 13th district in the Illinois Senate, a position he held until 2004, when he successfully ran for the U.S. Senate. In the 2008 presidential election, after a close primary campaign against Hillary Clinton, he was nominated by the Democratic Party for president. Obama selected Joe Biden as his running mate and defeated Republican nominee John McCain and his running mate Sarah Palin.",
  "query": "Extract education details.",
  "auth_key": "<ADD-AUTH-KEY-HERE>"
}
```
