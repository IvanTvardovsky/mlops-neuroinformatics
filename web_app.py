import pandas as pd
from flask import Flask, render_template, request
import plotly.graph_objs as go

app = Flask(__name__, template_folder="template")

def load_data():
    assets_data = pd.read_csv("data/assets.csv", index_col=0)
    train_predictions = pd.read_csv("data/train_pred.csv", index_col=0)
    test_predictions = pd.read_csv("data/test_pred.csv", index_col=0)

    predictions = pd.concat([train_predictions, test_predictions])
    predictions['Signal'] = 'None'
    predictions.loc[predictions['Prediction'] > 0, 'Signal'] = 'Buy'
    predictions.loc[predictions['Prediction'] < 0, 'Signal'] = 'Sell'

    return assets_data, predictions

assets_data, predictions = load_data()

def calculate_investment(starting_value, assets_data, predictions):
    investment_value = []
    current_value = starting_value
    buy_dates, sell_dates = [], []
    prev_signal = None

    for date in assets_data.index:
        if date in predictions.index:
            signal = predictions.loc[date, 'Signal']
            if signal == 'Buy':
                price_change = assets_data.loc[date, 'target'] / 100
                current_value *= (1 + price_change)
                if signal != prev_signal:
                    buy_dates.append(date)
            elif signal == 'Sell' and signal != prev_signal:
                sell_dates.append(date)

            prev_signal = signal

        investment_value.append(current_value)

    return pd.DataFrame(data=investment_value, index=assets_data.index, columns=['Investment Value']), buy_dates, sell_dates

def create_figure(assets_data, investment_data, buy_dates, sell_dates):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=assets_data.index,
        y=assets_data['close'],
        mode='lines',
        name='BTC Price'
    ))

    fig.add_trace(go.Scatter(
        x=investment_data.index,
        y=investment_data['Investment Value'],
        mode='lines',
        name='Investment Value'
    ))

    fig.add_trace(go.Scatter(
        x=buy_dates,
        y=assets_data.loc[buy_dates, 'close'],
        mode='markers',
        name='Buy',
        marker_symbol='triangle-up',
        marker=dict(size=10, color='green')
    ))

    fig.add_trace(go.Scatter(
        x=sell_dates,
        y=assets_data.loc[sell_dates, 'close'],
        mode='markers',
        name='Sell',
        marker_symbol='triangle-down',
        marker=dict(size=10, color='red')
    ))

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Value',
        title='BTC Price vs. Investment Value with Buy/Sell Signals',
    )

    return fig.to_html(full_html=False)

@app.route('/', methods=['GET', 'POST'])
def plot():
    starting_value = 400
    if request.method == 'POST':
        starting_value = float(request.form.get('starting_value', starting_value))

    investment_data, buy_dates, sell_dates = calculate_investment(starting_value, assets_data, predictions)

    table_data = pd.DataFrame({
        'Date': assets_data.index,
        'BTC Price': assets_data['close'],
        'Prediction': predictions['Prediction'],
        'Investment Value': investment_data['Investment Value']
    })

    plot_url = create_figure(assets_data, investment_data, buy_dates, sell_dates)

    return render_template('plot.html', plot_url=plot_url, starting_value=starting_value, data=table_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1488)
