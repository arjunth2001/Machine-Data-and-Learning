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
    topper = [-3.36404584e-02, - 2.26266364e-12, - 2.57536883e-13, - 3.67148164e-04,
              - 1.37489968e-03, - 1.89009699e-15, - 2.74050451e-05, 2.36454934e-05,
              - 2.00527075e-06, - 1.61030030e-08,  9.67071397e-10]
    # topper = [0.00000000e+00, - 5.86218128e-02, - 8.47236055e-02,  4.81725507e-11,
    #           4.50053831e-01, - 1.86199213e-15, - 6.61977601e-02,  2.08152272e-05,
    #           - 2.09480744e-06, - 1.59792834e-08,  9.95205344e-10]
    # print(get_errors('z60uCu1jsJeEi4n96iH7qwpMMnvIO1BEdnbC38CokXIn9y9lSR', topper))
  # print(get_overfit_vector('SECRET_KEY'))
    print(submit('z60uCu1jsJeEi4n96iH7qwpMMnvIO1BEdnbC38CokXIn9y9lSR', topper))
