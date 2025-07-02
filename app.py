import http.client
  
conn = http.client.HTTPSConnection("api.piapi.ai")

payload = "{\n  \"task_id\": \"e9a8f498-70e4-4504-b205-c34f9c2f5df4\"\n}"   #Replace the task ID with your task ID

headers = {
    'X-API-Key': "",                          #Insert your API Key here
    'Content-Type': "application/json",
    'Accept': "application/json"
}

conn.request("POST", "/api/face_swap/v1/fetch", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))