# Alphabet Discord Bot

## Requirements
- [docker-ce 19.03.0+](https://docs.docker.com/get-docker/)
- [docker-compose 1.18+](https://docs.docker.com/compose/install/)

 **You must install these first before you can use the bot as intended**

## Steps to get the bot up and running on your local machine

1. Clone this repo:
    - `git clone https://github.com/AAADevs/alpha-bot.git`

2. Navigate into the project directory:
    - `cd alpha-bot`

3. Copy the config.json.sample to config.json:
    - `cp config.json.sample config.json`

4. Edit the config file and add your own bot token, admin roles etc.

5. To run the bot use either of the following:
    - Foreground:
      - `docker-compose up`
    - Background (daemon):
      - `docker-compose up -d`
