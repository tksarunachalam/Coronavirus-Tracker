from requests import request
from flask import Flask, render_template
from wtforms import SelectField, SubmitField, TextField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aa99d1144cc3270de4c2e59277c22655'


class SelectState(FlaskForm):
    state = SelectField('Choose State',validators=[DataRequired()],choices=['Tamil Nadu','Delhi'])


@app.route("/", methods=['GET','POST'])
def home():

    url = "https://api.covid19india.org/data.json"
    payload = {}
    headers = {}

    response = request("GET", url, headers=headers, data=payload)
    response = response.json()
   
    daily_cases_timeline = [ response["cases_time_series"][i]['totalconfirmed'] for i in range(len(response["cases_time_series"])) ]
    daily_cases_timeline_date  = [ response["cases_time_series"][i]['date'] for i in range(len(response["cases_time_series"])) ]

    count = {
        'confirmed': response.get('statewise')[0]["confirmed"],
        'active' : response.get('statewise')[0]["active"],
        'deaths' : response.get('statewise')[0]["deaths"],
        'updated_date':response.get('statewise')[0]["lastupdatedtime"]
    }
    state_list = []
    for i in range(len(response.get('statewise'))):
            state_list.append(response.get('statewise')[i]["state"])
    
    stateform = SelectState()
    stateform.state.choices = state_list
    state = stateform.state.data
    # print(f'check2{state}')

    for j in state_list:
        if state == j:
            i = state_list.index(j)
            # response has keys: dict_keys(['cases_time_series', 'statewise', 'tested'])
            # response.get('statewise') List of Dictionary
            # response.get('statewise')[1] {'active': '91065', 'confirmed': '223724', 'deaths': '9448', 'deltaconfirmed': '6603', 'deltadeaths': '198', 'deltarecovered': '4634', 'lastupdatedtime': '08/07/2020 20:28:27', 'migratedother': '19', 'recovered': '123192', 'state': 'Maharashtra', 'statecode': 'MH', 'statenotes':}
    if response.get('statewise')[i]["state"] == state:

        count['confirmed'] = response.get('statewise')[i]["confirmed"]
        count['active'] = response.get('statewise')[i]["active"]
        count['deaths'] = response.get('statewise')[i]["deaths"]
        count['updated_date'] = response.get('statewise')[i]["lastupdatedtime"]
        
    return render_template('corona_state.html',form = stateform, count = count, updated_date = count['updated_date'],cases_timeline = daily_cases_timeline, date_timeline = daily_cases_timeline_date )


if __name__ == '__main__':
    app.run(debug=True )


