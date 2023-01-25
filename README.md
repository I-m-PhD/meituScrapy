# Intro.
This is a starter-friendly crawler/spider based on Scrapy, targeting at **[meitu131.com](https://www.meitu131.com/)**.
Fundamental thought is to download all pictures under a certain category, e.g. 
**[Rank](https://www.meitu131.com/rank/nvshen/)** in this demo, and keep them in a 3-level structure 
`<girls>/<albums>/images.jpg` stored in a root folder `./rank`.

This demo is built on 
> - macOS 13.1  
> - Python: 3.9.6  
> - scrapy  
> - pillow  

# Usage
Just type in the following commands in the `Terminal`:
```python
cd meitu_rank
```
```python
pip install -r requirements.txt
```
```python
python run.py
```
There you go!
