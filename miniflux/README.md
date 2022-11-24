# Installation

```
git clone https://github.com/atareao/self-hosted.git
cd self-hosted/miniflux
mv sample.env .env
sed -i "s/miniflux.tuservidor.es/el_fqdn_que_quieras/g" .env
```

Para levantar el servicio ejecutar:

```
docker-compose -f docker-compose.yml -f docker-compose.caddy.yml up -d
docker-compose logs -f
```