from os import write

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired,URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe URL', validators=[DataRequired(),URL(require_tld=True, message="Invalid URL")])
    open_time = StringField("Opening Time", validators=[DataRequired()])
    close_time = StringField("Closing Time", validators=[DataRequired()])
    cafe_rating = SelectField(
        'Cafe Rating',
        choices=[('☕','☕'), ('☕☕','☕☕'), ('☕☕☕','☕☕☕'), ('☕☕☕☕','☕☕☕☕')], validators=[DataRequired()])
    wifi_rating = SelectField(
        'Wifi Rating',
        choices=[('✘','✘'), ('💪','💪'), ('💪💪','💪💪'), ('💪💪💪','💪💪💪'), ('💪💪💪💪','💪💪💪💪')], validators=[DataRequired()])
    power_rating = SelectField(
        'Power Socket Availability',
        choices=[('✘','✘'), ('🔌 ','🔌 '), ('🔌🔌 ','🔌 🔌 '), ('🔌🔌🔌','🔌🔌🔌'), ('🔌🔌🔌🔌','🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_data = form.cafe.data
        location_data = form.location.data
        open_data = form.open_time.data
        close_data = form.close_time.data
        cafe_rating_data = form.cafe_rating.data
        wifi_rating_data = form.wifi_rating.data
        power_rating = form.power_rating.data

        with open('cafe-data.csv','a+', encoding="utf-8") as file:
            file.write(f"\n{cafe_data},{location_data},{open_data},{close_data},{cafe_rating_data},{wifi_rating_data},{power_rating}")

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
