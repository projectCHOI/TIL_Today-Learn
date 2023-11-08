# 트위터를 크롤링을 위해서는 '백그라운드'에 트윗터가 로그인 되어 있어야 된다.

import requests
import urllib.parse

headers = {
    'Accept' : '*/*',
    # 'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Authorization' : 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'Content-Type' : 'application/json',
    'Cookie' : 'external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; guest_id=v1%3A169933301507225892; _ga=GA1.2.2052717593.1699333015; _gid=GA1.2.1168370804.1699333015; g_state={"i_l":0}; kdt=VSWaFMSdl7fiY8g4AInFkcDhSNF1Njh7FX7aggFM; auth_token=f1236ee32272332f725bd29eb8532404822e3215; ct0=a143c9bb785daae52d66be760e107fd7a7e99aecf9900f1c3971900424673cf3a6b0056ffde6bc15273505cd3728a6b81b01ec2b364d210cb417fcbd4e302bb9d3050864bd61c999f001ea3aaa219441; att=1-txOU0Tn9P3a2ym29VpBWNkClQpXDEKrdnvpp20Bp; guest_id_ads=v1%3A169933301507225892; guest_id_marketing=v1%3A169933301507225892; lang=en; twid=u%3D1714237922566955008; personalization_id="v1_2Aq99JbmbeY1wH88OB29vg=="',
    'Referer' : 'https://twitter.com/search?q=%EB%A9%94%EC%9D%B4%ED%94%8C%EC%8A%A4%ED%86%A0%EB%A6%AC&src=typed_query&f=live',
    'Sec-Ch-Ua' : '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'Sec-Ch-Ua-Mobile' :'?0',
    'Sec-Ch-Ua-Platform' :'"Windows"',
    'Sec-Fetch-Dest' : 'empty',
    'Sec-Fetch-Mode' : 'cors',
    'Sec-Fetch-Site' : 'same-origin',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'X-Client-Transaction-Id' : 'y4XYb3jgV7CYpwAVPnotVZ+LBKvauv6Y4wAzb7pO9VRoy3UjH9IMrE2e9wIqcNAAhqCpMcubbI9mnzzgWPHgdX9QgXb1yg',
    'X-Client-Uuid' : '00cae34c-4bc7-4c39-aa6e-f7b06dcb2f69',
    'X-Csrf-Token' : 'a143c9bb785daae52d66be760e107fd7a7e99aecf9900f1c3971900424673cf3a6b0056ffde6bc15273505cd3728a6b81b01ec2b364d210cb417fcbd4e302bb9d3050864bd61c999f001ea3aaa219441',
    'X-Twitter-Active-User' : 'yes',
    'X-Twitter-Auth-Type' : 'OAuth2Session',
    'X-Twitter-Client-Language' : 'en'
    }


print(urllib.parse.quote("지드레곤"))

url = 'https://twitter.com/i/api/graphql/lZ0GCEojmtQfiUQa5oJSEw/SearchTimeline?variables=%7B%22rawQuery%22%3A%22%EB%A9%94%EC%9D%B4%ED%94%8C%EC%8A%A4%ED%86%A0%EB%A6%AC%22%2C%22count%22%3A40%2C%22cursor%22%3A%22DAADDAABCgABF-TiSMUaIJUKAAIX4_KRLFvQHAAIAAIAAAABCAADAAAAAAgABAAAAAEKAAUX5OesqAAnEAoABhfk56yn_7HgAAA%22%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'

response = requests.get(url, headers=headers)

for i in range(10):# 10회 반복 내가 추가 함.
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