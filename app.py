from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    from datetime import datetime
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime(2016, 1, 2)
    end = datetime(2016, 3, 10)
    df = data.DataReader(name="GOOG", data_source="yahoo", start=start, end=end)

    def status(c, o):
        if c > o:
            return "Increase"
        elif c < o:
            return "Decrease"
        else:
            return "Equal"

    df["Status"] = [status(c, o) for c, o in zip(df.Close, df.Open)]

    df["Middle"] = (df.Close + df.Open) / 2
    df["Height"] = abs(df.Close - df.Open)

    p = figure(x_axis_type='datetime', width=1000, height=500, sizing_mode='scale_width')
    p.title.text = "Candlestick Chart"

    hours_12 = 12 * 60 * 60 * 1000
    p.grid.grid_line_alpha = 0.3
    p.segment(df.index, df.High, df.index, df.Low, color='Black')
    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
           hours_12, df.Height[df.Status == "Increase"], color='green')
    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], hours_12,
           df.Height[df.Status == "Decrease"], color='red')
    script, div = components(p)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    return render_template("plot.html", script=script, div=div,
                           cdn_css=cdn_css[0], cdn_js=cdn_js[0])


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
