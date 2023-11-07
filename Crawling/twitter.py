import requests
import urllib.parse

headers = {
    'Accept':'*/*',
    #'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Authorization':'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'Content-Type':'application/json',
    'Cookie':'guest_id=v1%3A169933269060333944; _ga=GA1.2.914031610.1699332691; _gid=GA1.2.1691818659.1699332691; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCMgfH6iLAToMY3NyZl9p%250AZCIlMTg4NjMyZmI5NjI5ZGY4ZDQ1YTQ1MjE4MWU2YWFkZWQ6B2lkIiVmNTIz%250AMGUwNThjY2IzMDk2NDNlMjYxODY5MDhiMDA1ZQ%253D%253D--ead42b441cc59124dba4fae50e5e62f1cf2cafdd; g_state={"i_l":0}; kdt=88wLUXJGTNPej8TLYU03CM12ICTQYqhetN0URFa4; auth_token=50872c6448d76501f914bf28addbe814e923f826; ct0=5d1ba31a26a78adf206d90e4b58efa9885e4c73cf4d8ce0e9a0ae3c8fd3046a6dae032293670fd5cfef361f5cd75fa9a3917234038b3009cb6d31225b7aa6f3a47d94d270c8d5892da1a4526a3c57aac; att=1-MiJXlKUUKUI1SHCbsToQDRqEK2hlozY1glonRaCn; guest_id_ads=v1%3A169933269060333944; guest_id_marketing=v1%3A169933269060333944; lang=en; twid=u%3D1427265694303866887; personalization_id="v1_bQXk7oVgHyRmLpFq9MfMqw=="',
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
    'X-Csrf-Token':'5d1ba31a26a78adf206d90e4b58efa9885e4c73cf4d8ce0e9a0ae3c8fd3046a6dae032293670fd5cfef361f5cd75fa9a3917234038b3009cb6d31225b7aa6f3a47d94d270c8d5892da1a4526a3c57aac',
    'X-Twitter-Active-User':'yes',
    'X-Twitter-Auth-Type':'OAuth2Session',
    'X-Twitter-Client-Language':'en'
}

print(urllib.parse.quote("지드래곤"))

url = 'https://twitter.com/i/api/graphql/lZ0GCEojmtQfiUQa5oJSEw/SearchTimeline?variables=%7B%22rawQuery%22%3A%22%EC%A7%80%EB%93%9C%EB%9E%98%EA%B3%A4%22%2C%22count%22%3A20%2C%22cursor%22%3A%22DAADDAABCgABF-TnwSFaQR8KAAIX5OaFl9uA0wAIAAIAAAACCAADAAAAAAgABAAAAAAKAAUX5OfSIEAnEAoABhfk59IgP9jwAAA%22%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
response = requests.get(url, headers=headers)

for tweet in response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']:
    try:
        print(tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace('\n',''))
    except:
        pass

cursor = response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][-1]['entry']['content']['value']

while True:

    url = 'https://twitter.com/i/api/graphql/lZ0GCEojmtQfiUQa5oJSEw/SearchTimeline?variables=%7B%22rawQuery%22%3A%22%EC%A7%80%EB%93%9C%EB%9E%98%EA%B3%A4%22%2C%22count%22%3A20%2C%22cursor%22%3A%22' + cursor + '%22%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'

    response = requests.get(url, headers=headers)

    for tweet in response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']:
        try:
            print(tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace('\n',''))
        except:
            pass

    cursor = response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][-1]['entry']['content']['value']
