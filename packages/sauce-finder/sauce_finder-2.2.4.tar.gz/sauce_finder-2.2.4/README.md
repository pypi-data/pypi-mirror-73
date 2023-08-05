# Sauce finder

Production [![build status](https://gitlab.com/miicat/sauce-finder/badges/production/pipeline.svg)](https://gitlab.com/miicat/sauce-finder/commits/production)

Master [![build status](https://gitlab.com/miicat/sauce-finder/badges/master/pipeline.svg)](https://gitlab.com/miicat/sauce-finder/commits/master)



**sauce_finder** is a Python script to find sauce for anime images (and to download them).
It will try to find the sauce using [danbooru.iqdb.org](http://danbooru.iqdb.org/) with URL of the image you want to search. You can also download the found image automatically to current folder.


## Usage

See [wiki](https://gitlab.com/miicat/img-renamer/-/wikis/home) for full usage


### Find only sauce

This will try to find sauce for the image and show similarity percentage.
When no relevant match is found, it will list all possible matches.

```
sauce_finder https://url/to/img


example output:

Match found, with 94% similarity
http://danbooru.donmai.us/posts/xxxxxxx
```

### Find and download the found image

This will try to find sauce for the image, show similarity percentage and save the image to current folder.
If no relevant match is found, it will list all and download only the first possible match.

```
sauce_finder -d https://url/to/img


example output:

Match found, with 94% similarity
http://danbooru.donmai.us/posts/xxxxxxx
Downloading image
Image saved as image_name.png
```

## Author
[Miika Launiainen](https://gitlab.com/miicat)


## Donating

If you want to support me, feel free to use paypal
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/miicat)

## License

This library is licensed under GPLv3
