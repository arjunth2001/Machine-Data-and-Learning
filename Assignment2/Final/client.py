import json
import requests
import numpy as np

API_ENDPOINT = 'http://10.4.21.156'
MAX_DEG = 11


def urljoin(root, path=''):
    if path:
        root = '/'.join([root.rstrip('/'), path.rstrip('/')])
    return root


def send_request(id, vector, path):
    api = urljoin(API_ENDPOINT, path)
    vector = json.dumps(vector)
    response = requests.post(api, data={'id': id, 'vector': vector}).text
    if "reported" in response:
        print(response)
        exit()

    return response


def get_errors(id, vector):
    for i in vector:
        assert 0 <= abs(i) <= 10
    assert len(vector) == MAX_DEG

    return json.loads(send_request(id, vector, 'geterrors'))


def get_overfit_vector(id):
    return json.loads(send_request(id, [0], 'getoverfit'))


def submit(id, vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    """
    for i in vector:
        assert 0 <= abs(i) <= 10
    assert len(vector) == MAX_DEG
    return send_request(id, vector, 'submit')


# Replace 'SECRET_KEY' with your team's secret key (Will be sent over email)
if __name__ == "__main__":
    # topper = [-3.43443138e-02, - 2.38063335e-12, - 2.69250840e-13, - 4.68896595e-04,
    # - 3.90426623e-03, - 1.97864585e-15, - 2.77056954e-05,  2.35379033e-05,
    # - 1.95462508e-06, - 1.55062288e-08,  9.32455255e-10]
    topper = [1.44492243e-02, - 3.63335347e-02, - 1.35492094e-01, - 5.75856595e-01,
              - 2.89682141e-10, - 1.73843685e-15, - 4.87113653e-02,  2.58025239e-05,
              - 1.89688247e-06, - 1.62582575e-08, 8.92756185e-10]
    # print(get_errors('z60uCu1jsJeEi4n96iH7qwpMMnvIO1BEdnbC38CokXIn9y9lSR', topper))
  # print(get_overfit_vector('SECRET_KEY'))
    print(submit('z60uCu1jsJeEi4n96iH7qwpMMnvIO1BEdnbC38CokXIn9y9lSR', topper))
