from examples.sample_project import billing
from examples.sample_project import storage

def checkout():
    record = storage.save_order({'total': 12})
    return billing.charge(record)
