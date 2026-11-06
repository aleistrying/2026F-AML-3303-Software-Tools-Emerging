import boto3
import pandas as pd
import io
import joblib

from botocore import UNSIGNED
from botocore.config import Config
from botocore.exceptions import NoCredentialsError
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

bucket = 'mlops-lambton-bucket-aml-3303'
key = 'iris.csv'

# Read public S3 object anonymously
public_s3 = boto3.client(
    's3',
    config=Config(signature_version=UNSIGNED)
)

obj = public_s3.get_object(Bucket=bucket, Key=key)
df = pd.read_csv(io.BytesIO(obj['Body'].read()))

X, y = df.iloc[:, :-1], df.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42
)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, 'rf_model.pkl')
print("Model trained and saved locally")

# Upload using authenticated credentials
try:
    private_s3 = boto3.client('s3')
    private_s3.upload_file(
        'rf_model.pkl', bucket, 'rf_model.pkl'
    )
    print("Model uploaded to S3")
except NoCredentialsError:
    print("Upload skipped: no AWS credentials available")
