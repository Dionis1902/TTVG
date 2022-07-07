from TTVG.voice.voices import voices as voices_list
import random
import requests


class Voice:
    def __init__(self, token):
        self._url = 'https://dnecdiq809.execute-api.us-east-1.amazonaws.com/prod201102/{}/speak?display_name={}&speed={}'
        self._s = requests.Session()
        self._s.headers.update({
            'accept': 'audio/mpeg',
            'authorization': token,
            'Content-Type': 'application/json',
            'origin': 'https://www.naturalreaders.com',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        })

    def generate_voice(self, text, file, speed=0):
        voice = random.choice(voices_list)
        r = self._s.post(self._url.format(voice[0], voice[1].replace(" ", "%20"), speed), data='{"text": "%s"}' % text.encode("ascii", "ignore").decode())
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
