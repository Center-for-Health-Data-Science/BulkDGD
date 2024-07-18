#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    dgd_get_recount3_data.py
#
#    Get RNA-seq data associated with specific human samples for
#    projects hosted on the Recount3 platform.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public
#    License along with this program. 
#    If not, see <http://www.gnu.org/licenses/>.


#######################################################################


# Set the module's description.
__doc__ = \
    "Get RNA-seq data associated with specific human samples for " \
    "projects hosted on the Recount3 platform."


#######################################################################


# Import from the standard library.
import argparse
import logging as log
import logging.handlers as loghandlers
import os
import sys
# Import from third-party packages.
import dask
import pandas as pd
# Import from 'bulkDGD'.
from bulkDGD import defaults, util, recount3


#######################################################################


def main():


    # Create the argument parser.
    parser = argparse.ArgumentParser(description = __doc__)

    #-----------------------------------------------------------------#

    # Add the arguments.
    ib_help = \
        "A CSV or a YAML file used to download samples' data in bulk."
    parser.add_argument("-i", "--input-samples-batches",
                        type = str,
                        default = None,
                        help = ib_help)

    #-----------------------------------------------------------------#

    d_help = \
        "The working directory. The default is the current " \
        "working directory."
    parser.add_argument("-d", "--work-dir",
                        type = str,
                        default = os.getcwd(),
                        help = d_help)

    #-----------------------------------------------------------------#

    n_default = 1
    n_help = \
        "The number of processes to start. The default " \
        f"number of processes started is {n_default}."
    parser.add_argument("-n", "--n-proc",
                        type = int,
                        default = n_default,
                        help = n_help)

    #-----------------------------------------------------------------#

    sg_help = \
        "Save the original GZ file containing the RNA-seq " \
        "data for the samples. For each batch of samples, "\
        "the corresponding file will be saved in the " \
        "working directory and named '{recount3_project_name}_" \
        "{recount3_samples_category}_gene_sums.gz'. This file " \
        "will be written only once if more than one batch " \
        "refers to the same 'recount3_project_name' " \
        "and 'recount3_samples_category'."
    parser.add_argument("-sg", "--save-gene-sums",
                        action = "store_true",
                        help = sg_help)

    #-----------------------------------------------------------------#

    sm_help = \
        "Save the original GZ file containing the metadata " \
        "for the samples. For each batch of samples, "\
        "the corresponding file will be saved in the " \
        "working directory and named '{recount3_project_name}_" \
        "{recount3_samples_category}_metadata.gz'. This file will " \
        "be written only once if more than one batch refers " \
        "to the same 'recount3_project_name' and " \
        "'recount3_samples_category'."
    parser.add_argument("-sm", "--save-metadata",
                        action = "store_true",
                        help = sm_help)

    #-----------------------------------------------------------------#

    lf_default = "dgd_get_recount3_data.log"
    lf_help = \
        "The name of the log file. The file will be written " \
        "in the working directory. The default file name is " \
        f"'{lf_default}'."
    parser.add_argument("-lf", "--log-file",
                        type = str,
                        default = lf_default,
                        help = lf_help)

    #-----------------------------------------------------------------#

    lc_help = "Show log messages also on the console."
    parser.add_argument("-lc", "--log-console",
                        action = "store_true",
                        help = lc_help)

    #-----------------------------------------------------------------#

    v_help = "Enable verbose logging (INFO level)."
    parser.add_argument("-v", "--log-verbose",
                        action = "store_true",
                        help = v_help)

    #-----------------------------------------------------------------#

    vv_help = \
        "Enable maximally verbose logging for debugging " \
        "purposes (DEBUG level)."
    parser.add_argument("-vv", "--log-debug",
                        action = "store_true",
                        help = vv_help)

    #-----------------------------------------------------------------#

    # Parse the arguments.
    args = parser.parse_args()
    input_samples_batches = args.input_samples_batches
    wd = os.path.abspath(args.work_dir)
    n_proc = args.n_proc
    save_gene_sums = args.save_gene_sums
    save_metadata = args.save_metadata
    log_file = os.path.join(wd, args.log_file)
    log_console = args.log_console
    v = args.log_verbose
    vv = args.log_debug

    #-----------------------------------------------------------------#

    # Set WARNING logging level by default.
    log_level = log.WARNING

    # If the user requested verbose logging
    if v:

        # The minimal logging level will be INFO.
        log_level = log.INFO

    # If the user requested logging for debug purposes
    # (-vv overrides -v if both are provided)
    if vv:

        # The minimal logging level will be DEBUG.
        log_level = log.DEBUG

    # Get the logging configuration for Dask.
    dask_logging_config = \
        util.get_dask_logging_config(log_console = log_console,
                                     log_file = log_file)
    
    # Set the configuration for Dask-specific logging.
    dask.config.set({"distributed.logging" : dask_logging_config})
    
    # Configure the logging (for non-Dask operations).
    handlers = \
        util.get_handlers(\
            log_console = log_console,
            log_console_level = log_level,
            log_file_class = loghandlers.RotatingFileHandler,
            log_file_options = {"filename" : log_file,
                                "mode" : "w"},
            log_file_level = log_level)

    # Set the logging configuration.
    log.basicConfig(level = log_level,
                    format = defaults.LOG_FMT,
                    datefmt = defaults.LOG_DATEFMT,
                    style = defaults.LOG_STYLE,
                    handlers = handlers)

    #-----------------------------------------------------------------#
    
    # Import 'distributed' only here because, otherwise, the logging
    # configuration is not properly set    .
    from distributed import LocalCluster, Client, as_completed

    # Create the local cluster.
    cluster = LocalCluster(# Number of workers
                           n_workers = n_proc,
                           # Below which level log messages will
                           # be silenced
                           silence_logs = "ERROR",
                           # Whether to use processes, single-core
                           # or threads
                           processes = True,
                           # How many threads for each worker should
                           # be used
                           threads_per_worker = 1)

    # Open the client from the cluster.
    client = Client(cluster)

    #-----------------------------------------------------------------#

    # Try to load the samples' batches.
    try:

        df = recount3.load_samples_batches(\
            samples_file = input_samples_batches)
    
    # If something went wrong
    except Exception as e:
        
        # Warn the user and exit.
        errstr = \
            "It was not possible to load the samples' batches " \
            f"from '{input_samples_batches}'. Error: {e}"
        log.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the batches were successfully loaded.
    infostr = \
        "The samples' batches were successfully loaded from " \
        f"'{input_samples_batches}'."
    log.info(infostr)

    #-----------------------------------------------------------------#

    # Create a list to store the futures.
    futures = []

    # For each row of the data frame containing the samples' batches
    for num_batch, row in enumerate(df.itertuples(index = False), 1):

        # Get the name of the project.
        project_name = row.recount3_project_name

        # Get the samples' category.
        samples_category = row.recount3_samples_category

        # Get the query string, if provided.
        query_string = \
            row.query_string \
            if hasattr(row, "query_string") else None

        # Get the columns to keep, if provided.
        metadata_to_keep = \
            row.metadata_to_keep \
            if hasattr(row, "metadata_to_keep") else None

        # Get the columns to drop, if provided.
        metadata_to_drop = \
            row.metadata_to_drop \
            if hasattr(row, "metadata_to_drop") else None

        #-------------------------------------------------------------#

        # Get the name of the output file.
        output_csv_name = \
            f"{project_name}_{samples_category}_{num_batch}.csv"

        # Get the path to the output file.
        output_csv_path = os.path.join(wd, output_csv_name)

        # Inform the user that the results will be written to the
        # specified output file.
        infostr = \
            f"The results for batch # {num_batch} ('{project_name}' " \
            f"project, '{samples_category}' samples) will be " \
            f"written in '{output_csv_path}'."
        log.info(infostr)

        #-------------------------------------------------------------#

        # Get the path to the log file and the file's extension.
        log_file_name = \
            f"{project_name}_{samples_category}_{num_batch}.log"

        # Get the path to the log file.
        log_file_path = os.path.join(wd, log_file_name)

        # Inform the user about the log file for the current batch
        # of samples.
        infostr = \
            f"The log messages for batch # {num_batch} " \
            f"('{project_name}' project, '{samples_category}' " \
            f"samples) will be written in '{log_file_path}'."
        log.info(infostr)

        #-------------------------------------------------------------#

        # Build the list of arguments needed to send one calculation.
        args = \
            ["-ip", str(project_name),
             "-is", str(samples_category),
             "-o", output_csv_path,
             "-d", wd,
             "-lf", log_file_path]

        # If the user passed a query string for the current batch
        if query_string is not None and query_string != "":

            # Add the query string option to the list of arguments.
            args.extend(["-qs", str(query_string)])

        # If the user passed the metadata columns to keep
        if metadata_to_keep is not None and metadata_to_keep != "":

            # Add the option to keep only selected metadata columns to
            # the list of arguments.
            args.extend(["-mk", str(metadata_to_keep)])

        # If the user passed the metadata columns to drop
        if metadata_to_drop is not None and metadata_to_drop != "":

            # Add the option to drop selected metadata columns to the
            # list of arguments.
            args.extend(["-md", str(metadata_to_drop)])

        # If the user wants to save the original 'gene_sums' files
        if save_gene_sums:

            # Add the option for it to the list of arguments.
            args.append("-sg")

        # If the user wants to save the original 'metadata' files
        if save_metadata:

            # Add the option for it to the list of arguments.
            args.append("-sm")

        # If the user requested logging to the console
        if log_console:

            # Add the option for it to the list of arguments.
            args.append("-lc")

        # If the user requested verbose logging
        if v:

            # Add the option for it to the list of arguments.
            args.append("-v")

        # If the user requested debug-level logging
        if vv:

            # Add the option for it to the list of arguments.
            args.append("-vv")

        #-------------------------------------------------------------#

        # Submit the calculation.
        futures.append(\
            client.submit(\
                util.run_executable,
                executable = "_dgd_get_recount3_data_single_batch",
                arguments = args,
                extra_return_values = [num_batch]))

    #-----------------------------------------------------------------#

    # Get the futures as they are completed.
    for future, result in as_completed(futures,
                                       with_results = True):

        # Get the process and the batch number from the current
        # future.
        process, num_batch = result

        # Check the process' return code.
        try:

            process.check_returncode()

        # If something went wrong
        except Exception as e:

            # Log the error.
            errstr = \
                f"The run for batch # {num_batch} failed. Please " \
                f"check the log file '{process.args[10]}' for " \
                "more details."
            log.error(errstr)

            # Go to the next future.
            continue

        # Inform the user that the run completed successfully.
        infostr = \
            f"The run for batch # {num_batch} completed successfully."
        log.info(infostr)


#######################################################################


if __name__ == "__main__":
    main()
