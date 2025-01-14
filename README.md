# tg-auth-bot

## How to run:

1. Clone the repo, create a virtualenv, install dependencies

```bash
  git clone https://github.com/uQwQu/tg-auth-bot.git
  cd tg-auth-bot
  python3 -m venv venv
  source venv/bin/activate 
  pip install -r requirements.txt
```
2. Start ngrok (or smth like that) to tunnel your local server

```bash
  ngrok http 8000
```

2. Create .env file based on .env.example

```bash
  cp .env.example .env
```

3. Start local server

```bash
  python3 -m http.server
```
5. Set webhook

```bash
  ./webhook.sh
```

![Image](https://i.ibb.co/LkL172v/1.png)
![Image](https://i.ibb.co/dQysrG4/2.png)
![Image](https://i.ibb.co/BN5DGmT/3.png)
![Image](https://i.ibb.co/pQ7r0tV/4.png)


