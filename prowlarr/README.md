# Prowlarr

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/prowlarr
mkdir data 
mkdir data/config
cp sample.env .env
sed -i "s/prowlarr.tuservidor.es/fqdn_you_want/g" .env
```

If you want to work with Caddy reverse proxy,

```
docker-compose -f docker-compose.yml -f docker-compose.caddy.yml up -d
```