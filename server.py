from flask import Flask, render_template, request, redirect
import requests
import urllib

app = Flask(__name__)
app.config.from_pyfile('keys.cfg')
app.config['SITE'] = 'https://connect.stripe.com'
app.config['AUTHORIZE_URI'] = '/oauth/authorize'
app.config['TOKEN_URI'] = '/oauth/token'

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/authorize')
def authorize():
  site   = app.config['SITE'] + app.config['AUTHORIZE_URI']
  params = {'response_type': 'code',
            'scope': 'read_write',
            'client_id': app.config['CLIENT_ID']
           }

  # Redirect to Stripe /oauth/authorize endpoint
  url = site + '?' + urllib.urlencode(params)
  return redirect(url)

@app.route('/oauth/callback')
def callback():
  code   = request.args.get('code')
  header = {'Authorization': 'Bearer %s' % app.config['API_KEY']}
  data   = {'grant_type': 'authorization_code',
            'client_id': app.config['CLIENT_ID'],
            'code': code
           }

  # Make /oauth/token endpoint POST request
  url = app.config['SITE'] + app.config['TOKEN_URI']
  resp = requests.post(url, params=data, headers=header)

  # Grab access_token (use this as your user's API key)
  token = resp.json.get('access_token')
  return render_template('callback.html', token=token)

if __name__ == '__main__':
  app.run()
