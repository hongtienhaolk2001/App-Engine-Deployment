import math
from flask import request, render_template
from app import utils, app
from app.analysis import Analysis


@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories()
    }


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/news/<int:category_id>/', methods=['GET', 'POST'])
def news_list(category_id=0):
    category_name = {0: " ", 1: "Lúa Gạo", 2: "Cà Phê", 3: "Cao Su"}
    page = request.args.get('page', 1)
    kw = request.args.get('keyword')
    news = utils.load_news(category_id=category_id, page=int(page), keyword=kw)
    counter = utils.count_news(category_id)
    return render_template('news.html',
                           category_name=category_name[category_id],
                           cate_id=category_id,
                           news=news,
                           pages=math.ceil(counter / app.config['PAGE_SIZE']))


@app.route('/read/')
def read():
    return render_template('read.html')


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method.__eq__('POST'):
        news_sentence = f"{request.form['headline']} {request.form['brief']}"  # Get review from input
        model = Analysis(api_key="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")
        final_output = model.get_response(news_sentence)
        return render_template("analysis.html",
                               predict=final_output)
    else:
        return render_template("analysis.html")


if __name__ == '__main__':
    app.run(debug=True)
