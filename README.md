# kira-cli
My personalised useful cli 

* weather command  
  Usage:
  ```
  Usage: weather [OPTIONS] CITY

    Kira-cli | display weather information that retrieve from darksky API

  Options:
    --language TEXT  Language Ex: ja, en.
    --interval TEXT  Interval (daily or hourly). Default is daily.
    --help           Show this message and exit.
  ```
  
  Demo:
  ![](https://github.com/chienkira/kira-cli/blob/master/kira-cli-weather-demo.gif)

# Installation

*Now, it requires a python3 enviroment*

```bash
git clone https://github.com/chienkira/kira-cli.git && cd kira-cli
python setup.py install
weather tokyo
```
