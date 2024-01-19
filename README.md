# Malicious URL detector

Tool to detect malicious URLs using Cisco Umbrella.

Example :
```
curl -X POST -H "Content-Type: application/json" -H "x-monitor-authority: vowel-unified-plugins.int.dev.eticloud.io" -d "{\"body\": {\"raw_prompt\": \"Don't know if these URLs are valid - http://example.com I am thinking maybe not http://113.27.8.90:31926/.i\"}}" http://localhost:8000/request
```