import requests,json

class Av:
    def __init__(self):
        pass
    
    @staticmethod
    def get(keyword):
        url = "https://api.avgle.com/v1/search/{}/0".format(keyword)
        res = json.loads(requests.get(url).content.decode())
        if res["success"]:
            total = res["response"]["total_videos"]
            if total == 0:
                return {'error':'no result.'}
            best = res["response"]["videos"][0]
            return {'total':total,'title':best["title"],'thumb':best["preview_url"],'link':best["video_url"]}
        else:
            return {'error':'request fail'}

if __name__ == "__main__":
    pass