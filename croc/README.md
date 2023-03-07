# Jellyfin Server

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/croc
cp sample.env .env
sed -i "s/your_croc_password/pass_you_want/g" .env
docker-compose up -d
```
