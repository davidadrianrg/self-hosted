# Installation

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/gameserver_discord_bot
cp sample.env .env
sed -i "s/YOUR_DISCORD_TOKEN/the_token_you_want/g" .env

docker-compose up -d
```