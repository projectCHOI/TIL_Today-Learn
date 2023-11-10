from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import urllib.parse
import time
import requests

options=Options()
options.add_experimental_option('detach', True) #브라우저 바로꺼짐 방지

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://twitter.com/i/flow/login')
driver.implicitly_wait(10)

driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys("dante@fins.ai")
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3")[8].click()
time.sleep(1)

#분기!
driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys("01063108802")
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, "span.css-901oao")[6].click()
time.sleep(1)


driver.find_elements(By.CSS_SELECTOR, "input.r-30o5oe")[1].send_keys("abcd!@#$5678")
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3")[13].click()
time.sleep(1)


#헤더완성
cookie_text = ''
csrf = ''

for cookie in driver.get_cookies():
    cookie_text += f"{cookie['name']}={cookie['value']}; "
    if cookie['name'] == 'ct0':
        csrf = cookie['value']

headers = {
    'Accept':'*/*',
    #'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Authorization':'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'Content-Type':'application/json',
    'Cookie':cookie_text,
    'Referer':'https://twitter.com/search?q=%EC%A7%80%EB%93%9C%EB%9E%98%EA%B3%A4&src=typed_query&f=live',
    'Sec-Ch-Ua':'"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'X-Client-Transaction-Id':'WOx+yiL6yMr5hJJzf5KTxCPSB2bjXmpxEWTLF7mM1XINEyezX7LeMSKMbGuaG1Jkvho6oljnx2b7Vx1ZkyBOxQy4nyqyWQ',
    'X-Client-Uuid':'f68552d8-6ca1-47d6-9972-1c49492d2f14',
    'X-Csrf-Token':csrf,
    'X-Twitter-Active-User':'yes',
    'X-Twitter-Auth-Type':'OAuth2Session',
    'X-Twitter-Client-Language':'en'
}

query = "BTS"

variables = '{"rawQuery":"' + query + '","count":20,"querySource":"typed_query","product":"Latest"}'
features = '%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'

url = f'https://twitter.com/i/api/graphql/lZ0GCEojmtQfiUQa5oJSEw/SearchTimeline?variables={urllib.parse.quote(variables)}&features={features}'

response = requests.get(url, headers=headers)

for tweet in response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']:
    try:
        print(tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace('\n',''))
    except:
        pass

cursor = response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries'][-1]['content']['value']

while True:

    variables = '{"rawQuery":"' + query + '","cursor":"' + cursor + '","count":20,"querySource":"typed_query","product":"Latest"}'
    features = '%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'

    url = f'https://twitter.com/i/api/graphql/lZ0GCEojmtQfiUQa5oJSEw/SearchTimeline?variables={urllib.parse.quote(variables)}&features={features}'
    response = requests.get(url, headers=headers)

    for tweet in response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']:
        try:
            print(tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace('\n',''))
        except:
            pass

    cursor = response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][-1]['entry']['content']['value']
    print(cursor)

