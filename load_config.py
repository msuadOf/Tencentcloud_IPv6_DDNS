# import pyyaml module
import yaml
from yaml.loader import SafeLoader


def getKey(filename):
    with open(filename) as f:
        data = yaml.load(f, Loader=SafeLoader)
        print(data)
    return data["SecretId"],data["SecretKey"]


if __name__ == '__main__':
    print(__file__+" "+str(getKey('key.yaml')))

'''
{'SecretId': '123', 'SecretKey': '123', 'APPID': 123}
'''