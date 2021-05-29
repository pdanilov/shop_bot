Bot allowing you to add users via referral links and sell them items.
Admins can add items to the shop via admin panel.

First, you need to create .env file from given .env.dist template <br/>
<b>ADMINS</b> is a one or many telegram ids of admins who are allowed to use admin panel.
If there are more than one admin, ids should be separated by comma,
like <b>id1,id2</b> <br/>
<b>BOT_TOKEN</b> is a token for your bot, it can be obtained from
[@BotFather](https://t.me/BotFather) <br/>
<b>PROVIDER_TOKEN</b> is a token for a payment system to use in bot.
It can also be obtained from [@BotFather](https://t.me/BotFather) <br/> –
we recommend you to choose test mode for chosen payment system to use not real money of users
but local bot currency

<b>Note</b>: your bot should be enabled for inline mode.
This option also turns on in [@BotFather](https://t.me/BotFather) settings

You also need to install [Docker](https://docs.docker.com/get-docker/)
and [Docker Compose](https://docs.docker.com/compose/install/).
Then simply run:
```
docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up
```
You'll probably have to run this command with sudo privileges.
