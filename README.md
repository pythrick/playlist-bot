<h1 align="center">Welcome to Playlist Bot 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000" />
  <a href="https://twitter.com/pythrick">
    <img alt="Twitter: pythrick" src="https://img.shields.io/twitter/follow/pythrick.svg?style=social" target="_blank" />
  </a>
</p>

> Bot to create a YouTube playlist based on comments written by people in 
<a href="https://www.instagram.com/p/B0W4E7LAzlQ">this Instagram post</a> containing 
the name of several songs that always hit people right in the feels 

## Goals
- [x] Use Instagram Official Website API to get all the post comments
- [ ] Normalize at least 80% from the comments in actual songs names
- [ ] Create a playlist on YouTube with the top 500 songs

### Extra Goals:
- [ ] Create the same playlist on Spotify 
- [ ] Create the same playlist on Deezer 

## Install

```sh
pipenv install
```

## Usage

```sh
pipenv run main.py
```

## Run tests

```sh
pipenv run pytest --cov-report term --cov=.
```

## Author

👤 **Patrick Rodrigues**

* Twitter: [@pythrick](https://twitter.com/pythrick)
* Github: [@pythrick](https://github.com/pythrick)

## Show your support

Give a ⭐️ if this project helped you!
