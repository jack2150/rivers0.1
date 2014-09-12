from django.shortcuts import render, HttpResponse

from pms_app import models
from pms_app.classes.identify import Identify


def index(request):
    params = {
        'date': '2014-09-05'
    }

    return render(request, 'spread_view_app/index.html', params)


def webix_js(request):
    """
    A webix components for views
    :param request: dict
    :return: render
    """
    return render(request, 'spread_view_app/webix.js',
                  content_type='application/javascript')


def logic_js(request):
    """
    A webix actions for views
    :param request: dict
    :return: render
    """
    return render(request, 'spread_view_app/logic.js',
                  content_type='application/javascript')


def symbol_state(status, pl_open):
    """
    Set state for trade using status and pl_open
    :param status: str
    :param pl_open: float
    :return: str ['danger', 'normal', 'safe']
    """
    if 'profit' in status or pl_open > 0:
        state = 'safe'
    elif 'loss' in status or pl_open < 0:
        state = 'danger'
    else:
        state = 'normal'

    return state


def symbols_json(request, date):
    """
    Return a list of symbols with fields
    [state, status, symbol, pl_open]
    :param request: dict
    :param date: str
    :return: render json
    """
    symbols = []

    if date:
        positions = models.Position.objects.filter(date=date)

        if positions.exists():
            for position in positions:
                spread = Identify(position).spread
                """ :type: Spread """

                symbols.append({
                    'symbol': position.symbol,
                    'spread': spread.__name,
                    #'status': spread.current_status(),
                    #'pl_open': pl_open,
                    #'state': symbol_state(status, instrument.pl_open)
                })

            # todo: later

    return HttpResponse(
        symbols,
        content_type='application/json'
    )






def spreads_json(request, date, context=None):
    """
    Get positions for that date then
    make each position into spreads
    return it using json data format
    :param request: dict
    :param date: str
    :param context: str
    :return: render
    """
    spreads = None

    if date and context:
        # get all date position
        positions = models.Position.objects.filter(date=date)

        spreads = list()
        for position in positions:
            spread = Identify(position=position).spread
            """ :type: Spread """

            if spread and spread.context == context:
                spreads.append('%s' % spread.json())


    # todo: until here, convert into json format
    # todo: go into each spread, do json output

    return HttpResponse(
        '[' + ','.join(spreads) + ']',
        content_type='application/json'
    )

