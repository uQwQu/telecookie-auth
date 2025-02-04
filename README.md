
# telecookie-auth

Django website template with Telegram and cookie-based authentication

<img src="https://imgbb.io/ib/H2hZkU9BN9rK4G1_1737801501.jpg" width="250" style="border-radius: 25px;"/>

## Technologies used:

Django, Django REST framework | Docker | Redis | Celery | Nginx

## How to run: 

1. Clone the repo  
  
```bash
  git clone https://github.com/uQwQu/telecookie-auth.git  
```  
  
2. Start ngrok (or smth like that) to tunnel your local server  
  
```bash  
  ngrok http 8080  
```  
  
3. Create .env file based on .env.example  
  
```bash  
  cp .env.example .env  
```  
  
4. Set webhook  
  
```bash  
  ./webhook.sh  
```  
  
5. Run containers  
  
```bash
  make build  
``` 
<img src="https://imgbb.io/ib/Dyk69MWmUnxzzix_1737801501.jpg" width="650"/>
<img src="https://imgbb.io/ib/bdCRCoEwQW1JL1a_1737801503.jpg" width="650"/>