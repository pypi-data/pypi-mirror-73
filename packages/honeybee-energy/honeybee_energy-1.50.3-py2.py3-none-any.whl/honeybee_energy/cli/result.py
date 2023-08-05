"""honeybee energy result parsing commands."""

try:
    import click
except ImportError:
    raise ImportError(
        'click is not installed. Try `pip install . [cli]` command.'
    )

from honeybee_energy.result.sql import SQLiteResult

import sys
import logging
import json

_logger = logging.getLogger(__name__)


@click.group(help='Commands for parsing EnergyPlus results.')
def result():
    pass


@result.command('available-results')
@click.argument('result-sql')
@click.option('--output-file', help='Optional file to output the list of available '
              'outputs. By default, it will be printed to stdout',
              type=click.File('w'), default='-', show_default=True)
def available_results(result_sql, output_file):
    """Get an array of all timeseries outputs that can be requested from the simulation.
    \n
    Args:
        result_sql: Full path to an SQLite file that was generated by EnergyPlus.
    """
    try:
        sql_obj = SQLiteResult(result_sql)
        output_file.write(json.dumps(sql_obj.available_outputs))
    except Exception as e:
        _logger.exception('Failed to parse sql file.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@result.command('data-by-output')
@click.argument('result-sql')
@click.argument('output-name', type=str)
@click.option('--output-file', help='Optional file to output the JSON strings of '
              'the data collections. By default, it will be printed to stdout',
              type=click.File('w'), default='-', show_default=True)
def data_by_output(result_sql, output_name, output_file):
    """Get an array of DataCollection JSONs for a specific EnergyPlus output.
    \n
    Args:
        result_sql: Full path to an SQLite file that was generated by EnergyPlus.\n
        output_name: The name of an EnergyPlus output to be retrieved from
            the SQLite result file. This can also be an array of names if the
            string is formatted as a JSON array with [] brackets. Note that only
            a single array of data collection JSONs will be returned from this
            method and, if data collections must be grouped, the data_by_outputs
            method should be used.
    """
    try:
        sql_obj = SQLiteResult(result_sql)
        output_name = str(output_name)
        if output_name.startswith('['):
            output_name = tuple(outp.replace('"', '').strip()
                                for outp in output_name.strip('[]').split(','))
        data_colls = sql_obj.data_collections_by_output_name(output_name)
        output_file.write(json.dumps([data.to_dict() for data in data_colls]))
    except Exception as e:
        _logger.exception('Failed to retrieve outputs from sql file.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@result.command('data-by-outputs')
@click.argument('result-sql')
@click.argument('output-names', type=str, nargs=-1)
@click.option('--output-file', help='Optional file to output the JSON strings of '
              'the data collections. By default, it will be printed to stdout',
              type=click.File('w'), default='-', show_default=True)
def data_by_outputs(result_sql, output_names, output_file):
    """Get an array of DataCollection JSONs for a several EnergyPlus outputs.
    \n
    Args:
        result_sql: Full path to an SQLite file that was generated by EnergyPlus.\n
        output_names: An array of EnergyPlus output names to be retrieved from
            the SQLite result file. This can also be a nested array (an array of
            output name arrays) if each string is formatted as a JSON array
            with [] brackets.
    """
    try:
        sql_obj = SQLiteResult(result_sql)
        data_colls = []
        for output_name in output_names:
            output_name = str(output_name)
            if output_name.startswith('['):
                output_name = tuple(outp.replace('"', '').strip()
                                    for outp in output_name.strip('[]').split(','))
            data_cs = sql_obj.data_collections_by_output_name(output_name)
            data_colls.append([data.to_dict() for data in data_cs])
        output_file.write(json.dumps(data_colls))
    except Exception as e:
        _logger.exception('Failed to retrieve outputs from sql file.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@result.command('output-csv')
@click.argument('result-sql')
@click.argument('output-names', type=str, nargs=-1)
@click.option('--output-file', help='Optional file to output the CSV data of '
              'the results. By default, it will be printed to stdout',
              type=click.File('w'), default='-', show_default=True)
def output_csv(result_sql, output_names, output_file):
    """Get CSV for specific EnergyPlus outputs.
    \n
    Args:
        result_sql: Full path to an SQLite file that was generated by EnergyPlus.\n
        output_names: The name of an EnergyPlus output to be retrieved from
            the SQLite result file. This can also be several output names
            for which all data collections should be retrieved.
    """
    try:
        # get the data collections
        sql_obj = SQLiteResult(result_sql)
        data_colls = []
        for output_name in output_names:
            output_name = str(output_name)
            if output_name.startswith('['):
                output_name = tuple(outp.replace('"', '').strip()
                                    for outp in output_name.strip('[]').split(','))
            data_colls.extend(sql_obj.data_collections_by_output_name(output_name))

        # create the header rows
        type_row = ['DateTime'] + [data.header.metadata['type'] for data in data_colls]
        units_row = [''] + [data.header.unit for data in data_colls]
        obj_row = ['']
        for data in data_colls:
            try:
                obj_row.append(data.header.metadata['Zone'])
            except KeyError:
                try:
                    obj_row.append(data.header.metadata['Surface'])
                except KeyError:
                    try:
                        obj_row.append(data.header.metadata['System'])
                    except KeyError:
                        obj_row.append('')

        # create the data rows
        try:
            datetimes = [data_colls[0].datetimes]
        except IndexError:  # no data for the requested type
            datetimes = []
        val_columns = datetimes + [data.values for data in data_colls]

        # write everything into the output file
        def write_row(row):
            output_file.write(','.join([str(item) for item in row]) + '\n')
        write_row(type_row)
        write_row(units_row)
        write_row(obj_row)
        for row in zip(*val_columns):
            write_row(row)
    except Exception as e:
        _logger.exception('Failed to retrieve outputs from sql file.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@result.command('zone-sizes')
@click.argument('result-sql')
@click.option('--output-file', help='Optional file to output the JSON strings of '
              'the ZoneSize objects. By default, it will be printed to stdout',
              type=click.File('w'), default='-', show_default=True)
def zone_sizes(result_sql, output_file):
    """Get a dictionary with two arrays of ZoneSize JSONs under 'cooling' and 'heating'.
    \n
    Args:
        result_sql: Full path to an SQLite file that was generated by EnergyPlus.\n
    """
    try:
        sql_obj = SQLiteResult(result_sql)
        base = {}
        base['cooling'] = [zs.to_dict() for zs in sql_obj.zone_cooling_sizes]
        base['heating'] = [zs.to_dict() for zs in sql_obj.zone_heating_sizes]
        output_file.write(json.dumps(base))
    except Exception as e:
        _logger.exception('Failed to retrieve zone sizes from sql file.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)


@result.command('component-sizes')
@click.argument('result-sql')
@click.option('--component-type', help='A name of a HVAC component type, which will '
              'be used to filter the output HVAC components. If None, all HVAC component'
              ' sizes will be output.', type=str, default=None, show_default=True)
@click.option('--output-file', help='Optional file to output the JSON strings of '
              'the ComponentSize objects. By default, it will be printed to stdout',
              type=click.File('w'), default='-', show_default=True)
def component_sizes(result_sql, component_type, output_file):
    """Get a list of ComponentSize JSONs.
    \n
    Args:
        result_sql: Full path to an SQLite file that was generated by EnergyPlus.\n
    """
    try:
        sql_obj = SQLiteResult(result_sql)
        comp_sizes = []
        if component_type is None:
            for comp_size in sql_obj.component_sizes:
                comp_sizes.append(comp_size.to_dict())
        else:
            for comp_size in sql_obj.component_sizes_by_type(component_type):
                comp_sizes.append(comp_size.to_dict())
        output_file.write(json.dumps(comp_sizes))
    except Exception as e:
        _logger.exception('Failed to retrieve component sizes from sql.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)
