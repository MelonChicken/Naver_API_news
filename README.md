# Naver News API Discord Bot

## Project Purpose

This project aims to utilize ***Naver's*** ***News API***  (https://developers.naver.com/) to fetch news articles on specific topics in **Korean** and deliver them to users via a ***Discord bot***. 

The goal is to allow users to stay informed about their topics of interest seamlessly through Discord.

## How to Use the Project

### Prerequisites

1. **Python**:  Make sure you have Python installed on your system.
2. **Discord Bot Token**:  Obtain a token for your Discord bot.
3. **Naver API Credentials**:  Sign up for Naver's Developer API and get the required credentials.

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/MelonChicken/Naver_API_news.git
    cd Naver_API_news
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

#### 1. `config.toml` File

The `config.toml` file is crucial for the bot's configuration. 
It should be located in the root directory of the project **(./res/static)**.

Below is an example structure of the `config.toml` file:

```toml
[CLIENT]
ID = "Your Client ID of Naver API"
SECRET = "Your Client Secret Code of Naver API"
URL = "https://openapi.naver.com/v1/search/"
KEYWORD = "Put the Keyword in Korean that you want to search"
NODE = "news"  #  This is for specify that we want to use Naver News API.
RESPONSE_TYPE = "json"  #  XML file can be used, but still developing so far.
DISPLAY_COUNT = 100 #  Put the number that you want to see in one view (1 ~ 100)
SORT_CRITERIA = "date" #  Put date if you want to sort by newest to oldest, or Put sim to sort by accuracy.

[DISCORD]
TOKEN = 0  #  Put your token from discord bot
GUILD_ID = 0  #  Put your guild id where you want to send message
CHANNEL_ID = 0  #  Put your channel id where you want to send message
COMMAND_PREFIX = "!" #  Customize your command prefix
NEWEST_NEWS = "240604-203100"  #  This autosaves the newest post that you are looking for.
```

#### 2. `criteria` File
The `criteria.json` is for recording the distribution of target keywords which will be initialized by functions which are named as `update_target_groups` and `get_target_possibility`.
To initialize, you can just run the code and add the function.

### Run the code
Once you have configured the config.toml and criteria.json files, you can start the bot by running:
```shell
    python bot.py
```

## Encouragement for Users
Thank you for using our `Naver News API Discord Bot`! We hope it helps you stay informed about your favorite topics with ease. If you encounter any issues or have suggestions for improvement, feel free to contribute or raise an issue. ***Happy coding!***