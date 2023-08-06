import pandas as pd, os
import zipfile

names1 = ['commod', 'region', 'balitem', 'date', 'value']
names2 = ['region', 'commod', 'date', 'value']
names3 = ['balitem', 'region', 'commod', 'date', 'value']
names4 = ['region', 'date', 'value']
names5 = ['balitem', 'type', 'date', 'value']

# ['CRUDEDAT.TXT', 'NOECDDE.TXT', 'OECDDE.TXT', 'PRODDAT.TXT', 'STOCKDAT.TXT', 'SUMMARY.TXT', 'SUPPLY.TXT']


def allmods(sdbstxt_zip_loc, raw=False):
    z = zipfile.ZipFile(sdbstxt_zip_loc)
    res = {}
    res['PRODDAT'] = proddat(z, raw)
    res['CRUDEDAT'] = crudedat(z, raw)
    res['SUPPLY'] = supply(z, raw)
    res['STOCKSDAT'] = stockdat(z, raw)
    res['OECDDE'] = oecdde(z, raw)
    res['NOECDDE'] = noecdde(z, raw)
    res['SUMMARY'] = summary(z, raw)

    return res


def to_excel(allmods, outp):
    for dataset in allmods:
        outpf = os.path.join(outp, '{}.xlsx'.format(dataset))
        allmods[dataset].to_excel(outpf)


def proddat(z, raw=False):
    df = pd.read_csv(z.open('PRODDAT.TXT'), sep='\s+', header=None, names=names1, parse_dates=['date'])
    if raw:
        return df

    df['series'] = df.apply(lambda x: 'IEA.PROD.{}.{}.{}'.format(x.commod, x.region, x.balitem), 1)
    df = df.groupby(['date', 'series']).mean().unstack()['value']
    return df


def crudedat(z, raw=False):
    df = pd.read_csv(z.open('CRUDEDAT.TXT'), sep='\s+', header=None, names=names1, parse_dates=['date'])
    if raw:
        return df

    df['series'] = df.apply(lambda x: 'IEA.CRUDE.{}.{}.{}'.format(x.commod, x.region, x.balitem), 1)
    df = df.groupby(['date', 'series']).mean().unstack()['value']
    return df


def oecdde(z, raw=False):
    df = pd.read_csv(z.open('OECDDE.TXT'), sep='\s+', header=None, names=names2, parse_dates=['date'])
    if raw:
        return df

    df['series'] = df.apply(lambda x: 'IEA.OECDDE.{}.{}'.format(x.commod, x.region), 1)
    df = df.groupby(['date', 'series']).mean().unstack()['value']
    return df


def noecdde(z, raw=False):
    df = pd.read_csv(z.open('NOECDDE.TXT'), sep='\s+', header=None, names=names4)
    if raw:
        return df

    df['series'] = df.apply(lambda x: 'IEA.NOECDDE.{}'.format(x.region), 1)
    df = df.groupby(['date', 'series']).mean().unstack()['value']
    return df


def summary(z, raw=False):
    df = pd.read_csv(z.open('SUMMARY.TXT'), sep='\s+', header=None, names=names5)
    if raw:
        return df

    df['series'] = df.apply(lambda x: 'IEA.SUMMARY.{}.{}'.format(x.balitem, x.type), 1)
    # remove non numbers
    df = df[df['value'] != 'x']
    df['value'] = df['value'].astype('float') # turn back to number
    df = df.groupby(['date', 'series']).mean().unstack()['value']
    return df


def stockdat(z, raw=False):
    df = pd.read_csv(z.open('STOCKDAT.TXT'), sep='\s+', header=None, names=names3, parse_dates=['date'])
    if raw:
        return df

    df['series'] = df.apply(lambda x: 'IEA.STOCKS.{}.{}.{}'.format(x.balitem, x.commod, x.region,  ),1)
    df = df.groupby(['date', 'series']).mean().unstack()['value']
    return df


def supply(z, raw=False):
    df = pd.read_csv(z.open('SUPPLY.TXT'), sep='\s+', header=None, names=names2, parse_dates=['date'])
    if raw:
        return df

    df['series'] = df.apply(lambda x: 'IEA.SUPPLY.{}.{}'.format(x.commod, x.region), 1)
    df = df.groupby(['date', 'series']).mean().unstack()['value']
    return df

