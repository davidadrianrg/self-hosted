# Watch Your Lan

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/watchyourlan
cp sample.env .env
sed -i "s/gotify.tuservidor.es/fqdn_you_want/g" .env
docker-compose up -d
```