# Infrastructure as Code (Terraform)

This Infrastructure as Code (IaC) implementation satisfies the following requirements:

- Create an **Amazon S3 bucket** for model artifacts
- Upload a model artifact (`model.tar.gz`) using Terraform
- Configure an **IAM execution role** for SageMaker
- Deploy an **AWS SageMaker model**
- Create a **SageMaker endpoint configuration**
- Launch a **SageMaker endpoint**
- Allow full teardown of all resources with minimal manual effort

---

## Architecture
The Terraform configuration provisions the following AWS resources:

- **Amazon S3 Bucket**
  - Stores model artifacts
  - Automatically deleted during teardown
- **IAM Role**
  - Assumed by SageMaker at runtime
  - Grants access to S3 and CloudWatch Logs
- **SageMaker Model**
  - Uses an AWS-provided PyTorch inference container
  - Loads model artifacts from S3
- **SageMaker Endpoint Configuration**
  - Defines instance type and deployment settings
- **SageMaker Endpoint**
  - Provides real-time inference

All resources are defined in a **single `main.tf` file**.

---

## Prerequisites
- Terraform **v1.3+**
- AWS CLI configured with valid credentials
- AWS account permissions to create:
  - S3 buckets
  - IAM roles and policies
  - SageMaker resources

---

## Project Structure
```text
.
├── main.tf - Terraform configuration
└── model.tar.gz - Model artifact (dummy model for now)
```
---
## Creating the Model Artifact

If no trained model is available, create a dummy artifact:
```
mkdir model
echo "placeholder" > model/dummy.txt
tar -czf model.tar.gz model
```
---
##  Deployment
- Initialize Terraform
```
terraform init
```

- Apply Infrastructure
``` terraform apply \
  -var="bucket_name=genmab-task-artifacts-2c4cbbb1"
  ```

Terraform performs the following actions:

- Creates the S3 bucket

- Uploads the model artifact

- Creates the IAM execution role

- Creates the SageMaker model

- Creates the endpoint configuration

- Deploys the SageMaker endpoint

- Endpoint creation may take several minutes.

---
### Teardown / Destroy

To remove all resources created by this project:
```
terraform destroy
```
---