# Watchtower

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/watchtower
cp sample.env .env
sed -i "s/gotify.tuservidor.es/fqdn_you_want/g" .env
sed -i "s/your_gotify_token/fill_with_your_token/g" .env
docker-compose up -d
```