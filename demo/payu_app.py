from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/create-token', methods=['POST', 'GET'])
def create_token():
    if request.method == 'POST':
        print request
        return render_template('created_token.html')

    return render_template('create_token.html')

if __name__ == '__main__':
    app.run(debug=True)
