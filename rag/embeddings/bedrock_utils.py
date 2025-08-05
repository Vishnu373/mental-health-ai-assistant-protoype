import boto3
import json

def generated_embeddings(chunks, region):
    bedrock = boto3.client("bedrock-runtime", region_name = region)

    embeddings = []

    for text in chunks:
        response = bedrock.invoke_model(
            modelId = "amazon.titan-embed-text-v2:0",
            body = json.dumps({"inputText": text})
        )

        result = json.loads(response['body'].read())
        embeddings.append(result['embedding'])

    return embeddings    