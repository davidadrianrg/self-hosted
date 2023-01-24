# Pihole

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/pihole
cp sample.env .env
sed -i "s/pihole.tuservidor.es/fqdn_you_want/g" .env
sed -i "s/your_password/pass_you_want/g" .env
sed -i "s/your_server_ip/server_ip_you_have/g" .env
```

Launch with:

```
docker-compose up -d