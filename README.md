# Placeholder


#### Preparation: 
Create a file inside "lambda_code/AWS_Inventory" with the name "cross_account_roles.json" and content like the following:

```json
[
    {
        "RoleArn": "arn:aws:iam::123456789012:role/AWS-Inventory",
        "RoleSessionName": "123456789012-Inventory",
        "Description": "Some-Description"
    }
]
```