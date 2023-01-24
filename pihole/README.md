# Pihole

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/pihole
cp sample.env .env
sed -i "s/pihole.tuservidor.es/fqdn_you_want/g" .env
sed -i "s/your_password/pass_you_want/g" .env
```

If you want to work with Caddy reverse proxy,

```
docker-compose -f docker-compose.yml -f docker-compose.caddy.yml up -d