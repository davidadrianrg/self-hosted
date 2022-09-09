# Filebrowser $ Webdav Server

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/filebrowser-webdav
mkdir data
touch data/filebrowser.db
mv filebrowser.json data/
cp sample.env .env
sed -i "s/filebrowser.tuservidor.es/fqdn_you_want/g" .env
sed -i "s/webdav.tuservidor.es/fqdn_you_want/g" .env
sed -i "s/YOUR_USERNAME/user_you_want/g" .env
sed -i "s/YOUR_PASSWORD/password_you_want/g" .env
```

If you want to work with Caddy reverse proxy,

```
docker-compose -f docker-compose.yml -f docker-compose.caddy.yml up -d
```