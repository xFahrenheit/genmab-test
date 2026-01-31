# Task 1: Customer Segmentation with AWS Sagemaker

### 1. Dataset Selection
I used the provided `customer_segmentation_data.csv` for this stage.

Available features:
* **Age**, **Gender**: Customer demographic information.
* **Income**: Annual earnings.
* **Purchases**: Historical purchase frequency.

Choices:
- I converted the `Income` and `Purchases` and created a `Spending_Power` variable (Spending Power = Income / Purchases). This ratio provided a strong signal for the clustering.
- I dropped the Gender column as I believe it does not provide any insight in segmentation.

### 2. Model Selection: K-Means Clustering
I chose *K-Means Clustering* as the primary algorithm.
* **Reasoning**: It is highly efficient for discovering patterns in unlabeled data and provides clear, interpretable "centroids" for business personas.
* **Alternatives Considered & Rejected**:
    * *DBSCAN*: Rejected because it identifies "outliers" as noise, whereas this project required every customer to be assigned to a segment.

### 3. Environment & Feature Engineering
The project was developed using an **AWS SageMaker Notebook Instance**. 

#### **Feature Engineering**
* I engineered a "power user" feature: `Spending_Power = Income / Purchases`.
* I used `StandardScaler` to ensure that high `Income` values did not bias the distance-based calculations.

### 4. Deployment & Optimization
The model was deployed to a persistent **SageMaker Endpoint** (`ml.m5.xlarge`).
* **Optimization**: The deployment was optimized for low-latency by using a Scikit-Learn Inference Container.
* **Inference Logic**: A custom `script.py` was developed with a dedicated `input_fn` to handle **JSON payloads**, allowing for high-speed batch predictions.

#### **Model Versioning & Management**
* **Versioning**: Managed via SageMaker's S3 integration. Every training run generates a unique timestamped `.tar.gz` model artifact.
* **Management**: The use of a Scikit-Learn `Pipeline` ensures that the preprocessing logic (scaling) is versioned and bundled exactly with the model weights.

---

## Usage & Inference
* The endpoint is configured to accept JSON lists representing `[Age, Spending_Power]`.

**Example JSON Payload:**
```json
[
  [25, 1250.0], 
  [45, 3000.5]
]
```

## Stopping Endpoint
* To prevent billing as I am using the free tier, the endpoint is stopped by using `predictor.delete_endpoint()`
