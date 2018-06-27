import sys
import os
from urllib import request
from PIL import Image

def download(url, decode=False):
    response = request.urlopen(url)
    if response.geturl() == "https://s.yimg.com/pw/images/en-us/photo_unavailable.png":
        # Flickr :This photo is no longer available iamge.
        raise RuntimeError("This photo is no longer available iamge.")

    body = response.read()
    if decode == True:
        body = body.decode()
    return body

def save(dir, filename, img):
    path = os.path.join(dir, filename)
    with open("{}".format(path), 'wb') as f:
        f.write(img)

if __name__ == '__main__':
# see http://image-net.org/archive/words.txt
    classes = {"apple":"n07739125", "banana":"n07753592", "orange":"n07747607"}

    offset = 0
    max = 10
    os.makedirs('images', exist_ok=True)
    incremental_id = 0
    for dir, id in classes.items():
        print(dir)
        urls = download("http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={}".format(id), decode=True).split()
        print(len(urls))
        i = 0
        for url in urls:
            if i < offset:
                continue
            if i > max:
                break

            incremental_id = incremental_id + 1
            try:
                filename = "{}_{}.{}".format(incremental_id, dir, 'jpg')
                save('images/', filename, download(url))
                print("done: ({}){}".format(str(i), url))
            except RuntimeError:
                print("RuntimeError:", sys.exc_info()[0])
                print("error: ({}){}".format(str(i), url))
            i = i + 1
