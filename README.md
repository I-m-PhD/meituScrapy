# Introduction  

Aims at [MEITU131](https://www.meitu131.net).  

# Specification  

> Built on `macOS 13.1`  
> with os built-in `Python: 3.9.6`  
> utilising `scrapy` `pillow` `pandas`  
> some project also utilises `selenium` for JS-loaded elements  

# Contents

Contains three scrapy projects:  
- `meitu_model` starting with the page [女神大全](https://www.meitu131.net/nvshen/)  
- `meitu_rank` starting with the page [排行榜DIGG/总榜](https://www.meitu131.net/rank/nvshen/)  
- `meitu_rank_diy` is similar to `meitu_model` while it collects the entire models including those invisible in the index page, sorts them according to the "score" (JS-loaded element in each model's page), and parses the top listed ones.
