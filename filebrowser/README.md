# Filebrowser

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/filebrowser
mkdir data
touch data/filebrowser.db
cp sample.env .env
sed -i "s/filebrowser.tuservidor.es/fqdn_you_want/g" .env
sed -i "s/YOUR_FB_USERNAME/user_you_want/g" .env
sed -i "s/YOUR_FB_HASHED_BCRYPT_PASSWORD/password_you_want_hashed/g" .env
```

If you want to work with Caddy reverse proxy,

```
docker-compose -f docker-compose.yml -f docker-compose.caddy.yml up -d
```