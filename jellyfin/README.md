# Jellyfin Server

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/jellyfin
mkdir config cache media media2
cp sample.env .env
sed -i "s/jellyfin.tuservidor.es/fqdn_you_want/g" .env
```

If you want to work with Caddy reverse proxy,

```
docker-compose -f docker-compose.yml -f docker-compose.caddy.yml up -d
```
