# python class
from os import rename

# django class
from django.shortcuts import render
from rivers2.settings import FILES

# control and models class
from pms_app.classes import OpenDir, OpenPosCSV
import pms_app.models as pm


# Create your views here.
def index(request):
    """
    View for select positions csv files for import action with ajax completion
    :param request: dict
    :rtype : render
    """
    parameters = {
        'files': OpenDir().to_json(),
    }

    return render(request, 'index.html', parameters)


def complete(request, date=None):
    """
    Ajax view for info complete insert positions into db
    :param date: str
    :param request: dict
    :rtype : render
    """
    try:
        path = OpenDir().get_path(date)
        fname = OpenDir().get_fname_from_path(path)

        positions, overall = OpenPosCSV(path).read()

        for position in positions:
            # save positions
            pos = pm.Position(
                symbol=position['Symbol'],
                company=position['Company'],
                date=date
            )
            pos.save()

            # save instrument
            instrument = pm.PositionInstrument()
            instrument.set_dict(position['Instrument'])
            instrument.position = pos
            instrument.save()

            # save stock
            stock = pm.PositionStock()
            stock.set_dict(position['Stock'])
            stock.position = pos
            stock.save()

            # save options
            for pos_option in position['Options']:
                option = pm.PositionOption()
                option.set_dict(pos_option)
                option.position = pos
                option.save()

        pos_overall = pm.Overall(**overall)
        pos_overall.date = date
        pos_overall.save()

        # move files into completed folder
        rename(path, FILES['tos_positions_completed'] + fname)

        # set parameters into template
        parameters = {
            'date': date,
            'fname': fname
        }
    except IOError:
        # set parameters into template
        parameters = {
            'date': False,
            'fname': False
        }

    return render(request, 'complete.html', parameters)

