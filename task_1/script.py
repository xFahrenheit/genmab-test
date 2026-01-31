import argparse
import os
import pandas as pd
import joblib
import json
import sys
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--n_clusters', type=int, default=4)
        parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
        parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
        args = parser.parse_args()

        # Load the data
        train_file = os.path.join(args.train, "train.csv")
        df = pd.read_csv(train_file, header=None)
        
        print(f"Successfully loaded data with shape: {df.shape}")

        # Define and fit the pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('kmeans', KMeans(n_clusters=args.n_clusters, n_init=10, random_state=42))
        ])

        pipeline.fit(df)
        
        # Save the model
        joblib.dump(pipeline, os.path.join(args.model_dir, "model.joblib"))
        print("Model saved successfully!")

    except Exception as e:
        print(f"TRAINING ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

# Inference functions
def model_fn(model_dir):
    return joblib.load(os.path.join(model_dir, "model.joblib"))

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        data = json.loads(request_body)
        return pd.DataFrame(data)
    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    return model.predict(input_data).tolist()