import pandas as pd

def composite(hbfile):
    '''
    Cleans up the holobatch composite file which contains information about 
    sampling.

    Parameters
    ----------
    hbfile : string 
        path to the firsthologram_lasthologram_All.csv file produced by HoloBatch
    
    Returns 
    -------
    Pandas dataframe with correct headers
    '''

    # taken from the holobatch manual
    headers = [
                'year',
                'month',
                'day',
                'hour',
                'minute',
                'second',
                '1/100th_sec',
                'depth',
                'temperature',
                'input_voltage',
                'exposure',
                'laser_power',
                'laser_photo_diode',
                'brightness',
                'shutter',
                'gain',
                'deployment_id',
                'image_number',
                'number_of_particles',
                'reserved_0',
                'reserved_1',
                'reserved_2',
                'reserved_3',
                'reserved_4',
                'total_volume',
            ]
    for i in range(50):headers.append('size_distribution' +str(i))
    
    # Load holobatch composite file and add headers
    return pd.read_csv(hbfile,names=headers)
    
