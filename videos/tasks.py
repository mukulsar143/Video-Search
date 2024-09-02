from celery import shared_task
from .models import Video
import boto3
import subprocess
import os
import uuid

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    # Create a unique identifier for the subtitle file
    subtitle_file = f"{uuid.uuid4()}.srt"
    video_path = video.video_file.path

    # Extract subtitles using ccextractor
    subprocess.run(['ccextractor', video_path, '-o', subtitle_file])

    # Upload video to S3
    s3_client = boto3.client('s3')
    s3_client.upload_file(video_path, 'your-bucket-name', os.path.basename(video_path))

    # Read subtitles and store in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('your-dynamodb-table')
    with open(subtitle_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # Assuming each line in the SRT file is a subtitle text
            table.put_item(
                Item={
                    'video_id': video_id,
                    'subtitle_text': line.strip(),
                    'timestamp': str(uuid.uuid4())  # Use an appropriate timestamp
                }
            )

    # Clean up
    os.remove(subtitle_file)
