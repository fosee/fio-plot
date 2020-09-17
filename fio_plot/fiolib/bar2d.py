#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import pprint
import fiolib.supporting as supporting
from datetime import datetime
import fiolib.shared_chart as shared


def chart_2dbarchart_jsonlogdata(settings, dataset):
    """This function is responsible for drawing iops/latency bars for a
    particular iodepth."""
    dataset_types = shared.get_dataset_types(dataset)
    data = shared.get_record_set(settings, dataset, dataset_types)
    pprint.pprint(data)
    fig, (ax1, ax2) = plt.subplots(
        nrows=2, gridspec_kw={'height_ratios': [7, 1]})
    ax3 = ax1.twinx()
    fig.set_size_inches(10, 6)

    #
    # Puts in the credit source (often a name or url)
    if settings['source']:
        plt.text(1, -0.08, str(settings['source']), ha='right', va='top',
                 transform=ax1.transAxes, fontsize=9)

    ax2.axis('off')
    iops = data['y1_axis']['data']
    latency = np.array(data['y2_axis']['data'], dtype=float)

    #
    # Creating the bars and chart
    x_pos1 = np.arange(1, len(iops) + 1, 1)
    x_pos2 = np.arange(len(iops) + 1, len(iops) + len(latency) + 1, 1)
    # x_pos = np.arange(0, len(data['x_axis']))
    width = 0.9

    rects1 = ax1.bar(x_pos1, iops, width, color='#a8ed63')
    rects2 = ax3.bar(x_pos2, latency, width, color='#34bafa')

    #
    # Configure axis labels and ticks
    ax1.set_ylabel(data['y1_axis']['format'])
    # ax1.set_xlabel(data['x_axis_format'])
    ax3.set_ylabel(data['y2_axis']['format'])

    x_axis = data['x_axis'] * 2
    ltest = np.arange(1, len(x_axis)+1, 1)
    ax1.set_xticks(ltest)
    ax1.set_xticklabels(x_axis)

    #
    # Set title
    settings['type'] = ""
    settings['iodepth'] = dataset_types['iodepth']
    if settings['rw'] == 'randrw':
        supporting.create_title_and_sub(settings, plt, skip_keys=['iodepth'])
    else:
        supporting.create_title_and_sub(
            settings, plt, skip_keys=['iodepth', 'filter'])
    #
    # Labeling the top of the bars with their value
    shared.autolabel(rects1, ax1)
    shared.autolabel(rects2, ax3)
    #
    #
    data['x_axis'] = data['x_axis']
    shared.create_stddev_table(data, ax2)
    #
    # Create legend
    ax2.legend((rects1[0], rects2[0]),
               (data['y1_axis']['format'],
                data['y2_axis']['format']), loc='center left', frameon=False)
    #
    # Save graph to file
    #
    now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    title = settings['title'].replace(" ", '-')
    title = title.replace("/", '-')
    plt.tight_layout(rect=[0, 0, 1, 1])
    fig.savefig(f"{title}_{now}.png", dpi=settings['dpi'])


def compchart_2dbarchart_jsonlogdata(settings, dataset):
    """This function is responsible for creating bar charts that compare data."""

    dataset_types = shared.get_dataset_types(dataset)
    # pprint.pprint(dataset_types)

    data = shared.get_record_set_improved(settings, dataset, dataset_types)

    pprint.pprint(data)

    fig, (ax1, ax2) = plt.subplots(
        nrows=2, gridspec_kw={'height_ratios': [7, 1]})
    ax3 = ax1.twinx()
    fig.set_size_inches(10, 6)

    #
    # Puts in the credit source (often a name or url)
    if settings['source']:
        plt.text(1, -0.08, str(settings['source']), ha='right', va='top',
                 transform=ax1.transAxes, fontsize=9)

    ax2.axis('off')

    iops = data['y1_axis']['data']
    latency = np.array(data['y2_axis']['data'], dtype=float)

    #
    # Creating the bars and chart
    x_pos1 = np.arange(1, len(iops) + 1, 1)
    x_pos2 = np.arange(len(iops) + 1, len(iops) + len(latency) + 1, 1)
    # x_pos = np.arange(0, len(data['x_axis']))
    width = 0.9

    rects1 = ax1.bar(x_pos1, iops, width, color='#a8ed63')
    rects2 = ax3.bar(x_pos2, latency, width, color='#34bafa')

    #
    # Configure axis labels and ticks
    ax1.set_ylabel(data['y1_axis']['format'])
    # ax1.set_xlabel(data['x_axis_format'])
    ax3.set_ylabel(data['y2_axis']['format'])

    # We need the X-axis values twice, for both IOPs and latency
    x_axis = data['x_axis'] * 2

    ltest = np.arange(1, len(x_axis)+1, 1)
    ax1.set_xticks(ltest)
    ax1.set_xticklabels(x_axis)
    #
    # Set title
    settings['type'] = ""
    settings['iodepth'] = dataset_types['iodepth']
    if settings['rw'] == 'randrw':
        supporting.create_title_and_sub(settings, plt, skip_keys=['iodepth'])
    else:
        supporting.create_title_and_sub(
            settings, plt, skip_keys=[])
    #
    # Labeling the top of the bars with their value
    shared.autolabel(rects1, ax1)
    shared.autolabel(rects2, ax3)

    #
    # Create legend
    ax2.legend((rects1[0], rects2[0]),
               (data['y1_axis']['format'],
                data['y2_axis']['format']), loc='center left', frameon=False)
    #
    # Save graph to file
    #
    now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    title = settings['title'].replace(" ", '-')
    title = title.replace("/", '-')
    plt.tight_layout(rect=[0, 0, 1, 1])
    fig.savefig(f"{title}_{now}.png", dpi=settings['dpi'])
