#!/bin/bash

# Base URL of the Django application
BASE_URL="http://127.0.0.1:8000/video_comments/"

# Test video ID (replace with a valid one)
VIDEO_ID="iY9KQwEMgMc"

# Number of requests to make
REQUESTS=7

echo "Testing RateLimitMiddleware..."

# Make multiple POST requests
for ((i=1; i<=REQUESTS; i++))
do
    echo "Request #$i:"
    
    # Make the request and capture the response code
    RESPONSE_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL" -d "video_id=$VIDEO_ID")
    
    # Print the response code
    echo "Response Code: $RESPONSE_CODE"
    
    # Check if the response indicates rate limiting
    if [[ "$RESPONSE_CODE" -eq 429 ]]; then
        echo "Rate limit exceeded on request #$i."
        break
    else
        echo "Request #$i was successful."
    fi
    
    sleep 1  # Wait 1 second before the next request (adjust as necessary)
done

echo "Finished testing RateLimitMiddleware."