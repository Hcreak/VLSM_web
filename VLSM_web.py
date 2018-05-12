from flask import *
import VLSM.VLSM as VLSM
from shutil import *
from uuid import *
import os

app = Flask(__name__)
app.debug = True


def mvimg():
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    imguuid = str(uuid4())
    img_a = imguuid + '_a.jpg'
    img_b = imguuid + '_b.jpg'
    copyfile('VLSM/a.jpg', 'static/' + img_a)
    copyfile('VLSM/b.jpg', 'static/' + img_b)
    return (img_a, img_b)


@app.route('/', methods=['GET'])
def display():
    return render_template('index.html')


@app.route('/compute', methods=['POST'])
def compute():
    # print request.form['data']
    data = json.loads(request.form['data'])

    # print data
    i_source = data['address']
    i_alist = {}
    while len(data['subnet']) > 0:
        t = data['subnet'].popitem()
        i_alist[int(t[0])] = int(t[1])
    # print i_alist
    # print i_source

    # i_source='192.1.1.0'
    # i_alist={0:12,1:20,2:25}
    if VLSM.compute_web(i_source, i_alist)==True:
        img_a, img_b = mvimg()
        return jsonify({'a':url_for('static',filename=img_a),'b':url_for('static',filename=img_b)})

    else:
        return 'ERROR'


if __name__ == '__main__':
    app.run()
    # compute()
