import subprocess
import validators


class BackgroundActions:
    def execute(self, command):
        cmd = command.strip()
        output, error = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate()
        output = output.decode('utf-8').strip()
        error = error.decode('utf-8').strip()
        return (output, error)


class ValidateURLs:
    def validate_url(self, urls):
        if urls:
            urls = [url.strip() for url in urls]
            for index, url in enumerate(urls):
                if not validators.url(url):
                    print("Excluding \'%s\' - Invalid url" % url)
                    urls.remove(url)
                    break
                if '&list' in url:
                    urls[index] = url.split('&')[0]
            if urls:
                return urls
            else:
                exit(1)
        if not url:
            return 'Empty URL'
