# S3 SSE-S3 Encryption Automation Script

This Python script automates the process of ensuring all objects in a specified Amazon S3 bucket and prefix are encrypted using SSE-S3 (Server-Side Encryption with Amazon S3-Managed Keys). If an object is found without SSE-S3 encryption, the script will update the encryption setting of that object.

## Requirements

- Python 3.x
- Boto3 library
- AWS CLI configured with appropriate permissions to access and modify S3 bucket objects

### Setup

1. **Python 3.x**: Ensure Python 3.x is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

2. **Boto3**: Install the Boto3 library, which allows Python scripts to interact with Amazon Web Services (AWS). Install it using pip:

    ```bash
    pip install boto3
    ```

3. **AWS CLI**: Configure the AWS CLI with credentials that allow reading and writing to the specified S3 bucket. For more information on configuring the AWS CLI, visit [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

## Script Usage

The script is run from the command line, where you must specify the bucket name and the prefix for the objects you want to check and update. Use the following format:

```bash
python3 main.py <bucket name> <prefix>
