import asyncio
from playwright.async_api import async_playwright;
import pandas as pd
from langdetect import detect, LangDetectException
import time
import matplotlib.pyplot as plt


async def scrape_youtube_comments(video_url, max_comments = 500) :
  async with async_playwright() as p: 
    browser = await p.chromium.launch(headless=False)
    page = await browser.new_page()
    
    # 유튜브 비디오 URL로 이동 
    await page.goto(video_url) 
    # 댓글 섹션이 로드 될 때까지 기다림
    await page.wait_for_selector('ytd-comments') 
    
    comments = []
    
    while len(comments) < max_comments: 
      await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
      time.sleep(2)
      
      await page.evaluate("window.scrollBy(0, -1000)")
      time.sleep(2)
      
      await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
      time.sleep(2)
      
      comment_elements = await page.query_selector_all('#content-text')
      
      for comment in comment_elements : 
        comment_text = await comment.inner_text()
        comments.append(comment_text)
        comments =  list(set(comments)) 
        
        if len(comments) >= max_comments : 
          break
        
        print(f'comments length = {len(comments)}')
        
    await browser.close()
    
    comments_data = []
    for comment in comments :  
      try : 
        lang = detect(comment)
      except LangDetectException :
        lang = 'unknown'      
      comments_data.append({
        'Comment' : comment,
        'Lang' : lang
      })
      
    df = pd.DataFrame(comments_data)
    
    grouped = df.groupby('Lang')
    for lang, group in grouped : 
      group.to_csv(f"youtube_comments_{lang}.csv", index=False)
      
    print("댓글 수집 및 업어별 분류 완료")
      
    
  lang_counts = df['Lang'].value_counts()
  plt.figure(figsize=(10, 6))
  lang_counts.plot(kind='bar')
  plt.title("Number of Comments by Language")
  plt.xlabel("Language")
  plt.ylabel
  plt.xticks(rotation=45)
  plt.show()
  
video_url = input("Enter the Youtube video URL: ") 
max_comments = int(input("Enter the number of comments to scrape: "))
asyncio.run(scrape_youtube_comments(video_url, int(max_comments)))