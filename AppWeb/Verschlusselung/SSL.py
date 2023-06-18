from flask import Flask
import ssl
 

###### SSL-Files ######
ssl_cert = "C:\\Users\\Raul\Desktop\\VC_Workspace\\SSL Dateien\\self-signed-ca-cert.crt"
ssl_key  = "C:\\Users\\Raul\\Desktop\\VC_Workspace\\SSL Dateien\\private-ca.key"

###### Config  TLS_1.3 Encryption ######
cryp = ssl.SSLContext(ssl.PROTOCOL_TLS)
cryp.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
cryp.load_cert_chain(ssl_cert, ssl_key)


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True, ssl_context=cryp)