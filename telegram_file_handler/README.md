# Installation

```
git clone https://github.com/davidadrianrg/self-hosted.git
cd self-hosted/telegram_file_handler
cp sample.env .env
sed -i "s/YOUR_TELEGRAM_TOKEN/the_token_you_want/g" .env
sed -i "s/YOUR_USER_ID/the_id_you_have_in_telegram/g" .env
sed -i "s/YOUR_IMDB_TOKEN/the_token_you_have_in_imdb_api/g" .env

docker-compose up -d
```