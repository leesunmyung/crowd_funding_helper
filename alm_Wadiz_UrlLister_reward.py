from crawlLibWadiz import *

pagename ='wadiz'
#page_url = 'https://www.wadiz.kr/web/wreward/category?keyword=&endYn=Y&order=recent'   #종료된, 최신순.
#page_url = 'https://www.wadiz.kr/web/wreward/main?keyword=&endYn=N&order=recent' #진행중, 최신순. 50개 더 가져오려고.
page_url = 'https://www.wadiz.kr/web/wreward/comingsoon'   #오픈예정.
nUrl = 37
wc = WadizCrawler()
#wc.getUrlLister(pagename, page_url, nUrl)
#wc.getBrand(page_url, nUrl)
#wc.getBrandOnly(pagename, page_url)

wc.getReadyWadiz(page_url, nUrl)
