#!/usr/bin/env python
from comet_ml import Experiment
from xml.etree import ElementTree
import os
import click
import git
import sys

__version__ = '0.1.1'

@click.command()
@click.option('--project-name', help='Name of Comet ML project')
def main(project_name):
    stdin_report = '<report>' + ''.join(sys.stdin.readlines()) + '</report>'
    xml_report = ElementTree.fromstring(stdin_report)

    benchmarks = [{
        'name': xml_result.attrib['name'],
        'time': float(xml_result.find('mean').attrib['value'])}
        for xml_result in xml_report.iter('BenchmarkResults')
    ]

    repo = git.Repo(search_parent_directories=True)

    commit = repo.head.object
    report = {
        'hexsha': commit.hexsha,
        'message': commit.message,
        'author': commit.author.name,
        'benchmarks': benchmarks
    }

    api_key = os.getenv('COMMET_ML_API_KEY')

    experiment = Experiment(api_key=api_key, project_name=project_name, )
    common_time = 0.0
    for b in benchmarks:
        experiment.log_metric(name=b['name'], value=float(b['time']))
        common_time += b['time']

    experiment.log_metric(name='Common time', value=common_time)
    experiment.log_text(report['hexsha'])
    experiment.log_parameters(report)


if __name__ == '__main__':
    main()
