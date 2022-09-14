# Webdav server using alpine image

## Installation

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/webdav
cp sample.env .env
sed -i "s/webdav.tuservidor.es/fqdn_you_want/g" .env
```

Install htpasswd with `sudo apt-get install apache2-utils` and then create your credentials:
```
htpasswd -bc htpasswd your-user your-password
```

Remember to change `your-user` and `your-password` for your own credentials

If you want to work with Caddy,

```
docker-compose -f docker-compose.yml -f docker-compose.caddy.yml up -d
```
