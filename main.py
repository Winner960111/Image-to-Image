import http.client
import os, json, time
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("PiAPI_KEY")

conn = http.client.HTTPSConnection("api.piapi.ai")

def get_target_ID(source_image, swap_image):

  payload_dict = {
      "target_image": swap_image,  # The image you want to swap faces with
      "swap_image": source_image,
      "result_type": "url"
  }

  payload = json.dumps(payload_dict)
  
  print("payload:", payload)
  headers = {
      'X-API-Key': api_key,                  #Insert your API Key here
      'Content-Type': "application/json",
      'Accept': "application/json"
  }

  conn.request("POST", "/api/face_swap/v1/async", payload, headers)

  res = conn.getresponse()
  data = res.read()

  return data.decode("utf-8")

def get_result(target_id, max_retries=5, retry_delay=3):

  for _ in range(max_retries):
    payload_dict = {
        "task_id": target_id
    }
    payload = json.dumps(payload_dict)

    headers = {
        'X-API-Key': api_key,                           #Insert your API Key here
        'Content-Type': "application/json",
        'Accept': "application/json"
    }

    conn.request("POST", "/api/face_swap/v1/fetch", payload, headers)

    res = conn.getresponse()
    data = res.read()

    result = data.decode("utf-8")
    status = json.loads(result)['data']['status']

    if status == "success":
      return json.loads(result)['data']['image']
    else:
      time.sleep(retry_delay)
      print(f"Waiting for result... Status: {status}")

source = "https://ucarecdn.com/1addacc7-dd5b-4cf6-9845-f44e69fc82bc/Test.png"
swap = "https://ucarecdn.com/e881a531-4920-42aa-a0fa-c11c552a6a76/purpose.jpg"

# source = "https://ucarecdn.com/a3e40c38-8a45-4f73-98b2-cced33ac73d2/male_06.jpg"
# swap = "https://ucarecdn.com/87ebb291-5d0f-4713-a16d-7be1eed0276f/avatar.jpg"

target = get_target_ID(source, swap)
print("target:", target)
id = json.loads(target)['data']['task_id']

result = get_result(id)
print(result)
