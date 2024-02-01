from typing import Text

import pandas as pd
from django.db import models
from . import finview_app


# Create your models here.

def model_payment_provider_pie_chart(username: Text):
    cols_name_chronology = ['date_of_purchase', 'business_name', 'charge_amount', 'payment_type',
                            'total_amount', 'sha1_identifier', 'username', 'payment_provider']

    query = finview_app.ask['which_records_of_payment_provider'](payment_provider='', username=username)
    return pd.DataFrame(query, columns=cols_name_chronology).groupby('payment_provider')['total_amount'].sum()

