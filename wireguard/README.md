# Wireguard

## Clone the repository

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/wireguard
cp sample.env .env
sed -i "s/tuservidor.es/fqdn_you_want/g" .env
sed -i "s/your_password/pass_you_want/g" .env
```