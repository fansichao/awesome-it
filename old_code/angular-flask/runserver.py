import os
from angular_flask import app


def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='192.168.172.70', port=port)

if __name__ == '__main__':
    runserver()
